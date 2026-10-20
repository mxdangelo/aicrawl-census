"""Observatory data layer — aggregate the census into the tables the dashboard serves.

Reads the SQLite star schema (census-lite.db) with DuckDB, tags it with a snapshot
date, a country and a sample version, aggregates to small tidy Parquet tables, and
accumulates them across snapshots. Idempotent: re-run on each data injection (one
crawl = one snapshot); rows for an existing (snapshot_date, country, sample) are
replaced, others kept.

Usage (database and country default to CENSUS_COUNTRY, IT if unset; the sample
defaults to config.SAMPLES for the country):
    python dashboard/build_data.py                       # snapshot date from the data
    CENSUS_COUNTRY=FR python dashboard/build_data.py     # census-lite.fr.db, country FR
    python dashboard/build_data.py --snapshot-date 2026-08-01 --country IT
    python dashboard/build_data.py --db path/to/other.db --country IT --sample 2026-07

The sample is part of the key, so a re-crawl on a new domain list under the same
date adds a snapshot instead of erasing the old one. Replacing a stored snapshot
with a different number of domains under the same sample is refused unless
--replace is given: it usually means the list changed and SAMPLES was not bumped.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import sys

import duckdb

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import config  # noqa: E402  (repo root, made importable just above)

OUT = HERE / "data"
DEFAULT_DB = HERE.parent / f"census-lite{config.SUFFIX}.db"
KEY = "? AS snapshot_date, ? AS country, ? AS sample"

# Tidy fact for slice-and-dice: verdict counts at the finest grain the dashboard
# filters on. Everything the flagship charts show (blocked share by crawler /
# operator / sector, specific vs inherited) derives from here client-side.
POLICY_FACTS = f"""
SELECT
    {KEY},
    d.sector, d.tier, c.crawler, c.operator, c.purpose,
    f.verdict, f.verdict_source AS source,
    COUNT(*) AS n_domains
FROM src.dw_fact_policy f
JOIN src.dw_dim_domain  d ON d.domain_key  = f.domain_key
JOIN src.dw_dim_crawler c ON c.crawler_key = f.crawler_key
GROUP BY ALL
"""

# Per-sector signal presence: robots / llms / tdmrep adoption and the
# decided-vs-inherited split (llms_origin). The observable_* columns count the
# same signals on observable sites only, the denominator every share uses.
SECTOR_SIGNALS = f"""
SELECT
    {KEY}, sector,
    COUNT(*)                                          AS n_domains,
    SUM(observable)                                   AS observable,
    SUM(robots_present)                               AS robots_present,
    SUM(llms_present)                                 AS llms_present,
    SUM(llms_full_present)                            AS llms_full_present,
    SUM(tdmrep_present)                               AS tdmrep_present,
    SUM(CASE WHEN llms_origin = 'hand'      THEN 1 ELSE 0 END) AS llms_hand,
    SUM(CASE WHEN llms_origin = 'generated' THEN 1 ELSE 0 END) AS llms_generated,
    SUM(CASE WHEN observable = 1 AND llms_origin = 'hand'
             THEN 1 ELSE 0 END)                       AS observable_llms_hand,
    SUM(CASE WHEN observable = 1 AND llms_origin = 'generated'
             THEN 1 ELSE 0 END)                       AS observable_llms_generated,
    SUM(CASE WHEN observable = 1 THEN tdmrep_present ELSE 0 END)
                                                      AS observable_tdmrep
FROM src.dw_dim_domain
GROUP BY ALL
"""

# The sites asserting the TDMRep reservation, by name — the Reserve section
# names them (table view). Tiny by construction (9 in IT).
RESERVED_DOMAINS = f"""
SELECT
    {KEY}, d.domain, d.sector, d.observable,
    concat_ws(', ',
        CASE WHEN t.valid = 1 THEN '.well-known file' END,
        CASE WHEN t.via_header = 1 THEN 'HTTP header' END,
        CASE WHEN t.via_meta = 1 THEN 'meta tag' END) AS channels
FROM src.dw_dim_domain d
JOIN src.tdmrep_meta t USING (domain)
WHERE d.tdmrep_present = 1
"""

# One row per domain and snapshot: the panel that trends are computed on. The
# aggregates above cannot follow the same sites across a sample change; this
# can (join snapshots on domain). Headline measures only, to stay small.
DOMAIN_PANEL = f"""
SELECT
    {KEY}, d.domain, d.sector, d.tier, d.observable, d.unobservable_reason,
    d.robots_present, d.llms_present, d.llms_origin, d.tdmrep_present,
    g.verdict AS gptbot_verdict, g.verdict_source AS gptbot_source,
    COALESCE(n.named_blocks, 0) AS n_crawlers_blocked_by_name
FROM src.dw_dim_domain d
LEFT JOIN (SELECT f.domain_key, f.verdict, f.verdict_source
           FROM src.dw_fact_policy f JOIN src.dw_dim_crawler c USING (crawler_key)
           WHERE c.crawler = 'GPTBot') g USING (domain_key)
LEFT JOIN (SELECT domain_key, COUNT(*) AS named_blocks FROM src.dw_fact_policy
           WHERE verdict = 'blocked' AND verdict_source = 'specific'
           GROUP BY domain_key) n USING (domain_key)
"""

TABLES = {"policy_facts": POLICY_FACTS, "sector_signals": SECTOR_SIGNALS,
          "reserved_domains": RESERVED_DOMAINS, "domain_panel": DOMAIN_PANEL}


def _upsert(con, name, sql, key):
    """Run the aggregation and merge it into data/<name>.parquet, replacing any
    rows for this (snapshot_date, country, sample) and preserving the others."""
    con.execute(f"CREATE OR REPLACE TEMP TABLE fresh AS {sql}", key)
    path = OUT / f"{name}.parquet"
    if path.exists():
        con.execute(
            "CREATE OR REPLACE TEMP TABLE merged AS "
            "SELECT * FROM read_parquet(?) "
            "WHERE NOT (snapshot_date = ? AND country = ? AND sample = ?) "
            "UNION ALL BY NAME SELECT * FROM fresh",
            [str(path), *key])
        src_tbl = "merged"
    else:
        src_tbl = "fresh"
    con.execute(f"COPY (SELECT * FROM {src_tbl} ORDER BY snapshot_date, country, sample) "
                f"TO '{path}' (FORMAT parquet)")
    return con.execute(f"SELECT COUNT(*), COUNT(DISTINCT snapshot_date) "
                       f"FROM {src_tbl}").fetchone()


def _guard_sample(con, key, replace):
    """Stop before overwriting a stored snapshot that counts a different number
    of domains under the same sample: the list changed, so the sample should
    have a new version."""
    path = OUT / "sector_signals.parquet"
    if replace or not path.exists():
        return
    stored = con.execute(
        "SELECT SUM(n_domains) FROM read_parquet(?) "
        "WHERE snapshot_date = ? AND country = ? AND sample = ?",
        [str(path), *key]).fetchone()[0]
    fresh = con.execute("SELECT COUNT(*) FROM src.dw_dim_domain").fetchone()[0]
    if stored is not None and int(stored) != fresh:
        date, country, sample = key
        raise SystemExit(
            f"{country} {date} (sample {sample}) is stored with {int(stored)} domains, "
            f"the database has {fresh}. Bump config.SAMPLES, or pass --replace.")


def build(db_path, snapshot_date, country, sample, replace=False):
    if not sample:
        raise SystemExit(f"no sample version for {country}: add it to config.SAMPLES")
    OUT.mkdir(exist_ok=True)
    con = duckdb.connect()
    con.execute("INSTALL sqlite; LOAD sqlite;")
    con.execute(f"ATTACH '{db_path}' AS src (TYPE sqlite, READ_ONLY);")

    if snapshot_date is None:
        snapshot_date = con.execute(
            "SELECT max(substr(ts, 1, 10)) FROM src.fetches").fetchone()[0]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", snapshot_date or ""):
        raise SystemExit(f"snapshot date must be YYYY-MM-DD, got {snapshot_date!r}")

    key = [snapshot_date, country, sample]
    _guard_sample(con, key, replace)
    print(f"snapshot {snapshot_date} / country {country} / sample {sample} "
          f"from {db_path.name}")
    for name, sql in TABLES.items():
        rows, snaps = _upsert(con, name, sql, key)
        print(f"  {name}.parquet: {rows} rows across {snaps} snapshot date(s)")

    _write_meta(con)
    print(f"wrote {OUT.relative_to(HERE.parent)}/")


def _write_meta(con):
    """Small manifest for the dashboard: available filters and provenance."""
    facts = str(OUT / "policy_facts.parquet")

    def distinct(col):
        return [r[0] for r in con.execute(
            f"SELECT DISTINCT {col} FROM read_parquet('{facts}') "
            "ORDER BY 1").fetchall()]

    meta = {
        "generated_at": dt.datetime.now(dt.timezone.utc)
                          .isoformat(timespec="seconds"),
        "snapshots": distinct("snapshot_date"),
        "countries": distinct("country"),
        "samples": [{"country": c, "sample": s, "snapshots": n} for c, s, n in con.execute(
            f"SELECT country, sample, COUNT(DISTINCT snapshot_date) "
            f"FROM read_parquet('{facts}') GROUP BY ALL ORDER BY 1, 2").fetchall()],
        "sectors": distinct("sector"),
        "crawlers": distinct("crawler"),
        "operators": distinct("operator"),
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=pathlib.Path, default=DEFAULT_DB)
    ap.add_argument("--snapshot-date", default=None,
                    help="YYYY-MM-DD; defaults to the latest fetch date in the DB")
    ap.add_argument("--country", default=config.COUNTRY)
    ap.add_argument("--sample", default=None,
                    help="sample version; defaults to config.SAMPLES[country]")
    ap.add_argument("--replace", action="store_true",
                    help="overwrite a stored snapshot even if its domain count differs")
    a = ap.parse_args()
    build(a.db.resolve(), a.snapshot_date, a.country,
          a.sample or config.SAMPLES.get(a.country, ""), a.replace)
