"""Observatory data layer — aggregate the census into the tables the dashboard serves.

Reads the SQLite star schema (census-lite.db) with DuckDB, tags it with a snapshot
date and a country, aggregates to small tidy Parquet tables, and accumulates them
across snapshots. Idempotent: re-run on each data injection (one crawl = one
snapshot); rows for an existing (snapshot_date, country) are replaced, others kept.

Usage:
    python dashboard/build_data.py                       # snapshot date from the data, country IT
    python dashboard/build_data.py --snapshot-date 2026-08-01 --country IT
    python dashboard/build_data.py --db path/to/other.db --country FR
"""
import argparse
import datetime as dt
import json
import pathlib
import re

import duckdb

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "data"
DEFAULT_DB = HERE.parent / "census-lite.db"

# Tidy fact for slice-and-dice: verdict counts at the finest grain the dashboard
# filters on. Everything the flagship charts show (blocked share by crawler /
# operator / sector, specific vs inherited) derives from here client-side.
POLICY_FACTS = """
SELECT
    ? AS snapshot_date, ? AS country,
    d.sector, c.crawler, c.operator, c.purpose,
    f.verdict, f.verdict_source AS source,
    COUNT(*) AS n_domains
FROM src.dw_fact_policy f
JOIN src.dw_dim_domain  d ON d.domain_key  = f.domain_key
JOIN src.dw_dim_crawler c ON c.crawler_key = f.crawler_key
GROUP BY ALL
"""

# Per-sector signal presence: robots / llms / tdmrep adoption and the
# decided-vs-inherited split (llms_origin).
SECTOR_SIGNALS = """
SELECT
    ? AS snapshot_date, ? AS country, sector,
    COUNT(*)                                          AS n_domains,
    SUM(observable)                                   AS observable,
    SUM(robots_present)                               AS robots_present,
    SUM(llms_present)                                 AS llms_present,
    SUM(llms_full_present)                            AS llms_full_present,
    SUM(tdmrep_present)                               AS tdmrep_present,
    SUM(CASE WHEN llms_origin = 'hand'      THEN 1 ELSE 0 END) AS llms_hand,
    SUM(CASE WHEN llms_origin = 'generated' THEN 1 ELSE 0 END) AS llms_generated
FROM src.dw_dim_domain
GROUP BY ALL
"""

# The sites asserting the TDMRep reservation, by name — the Reserve section
# names them (dotgrid tooltip + table view). Tiny by construction (8 in IT).
RESERVED_DOMAINS = """
SELECT
    ? AS snapshot_date, ? AS country, d.domain, d.sector,
    concat_ws(', ',
        CASE WHEN t.valid = 1 THEN '.well-known file' END,
        CASE WHEN t.via_header = 1 THEN 'HTTP header' END,
        CASE WHEN t.via_meta = 1 THEN 'meta tag' END) AS channels
FROM src.dw_dim_domain d
JOIN src.tdmrep_meta t USING (domain)
WHERE d.tdmrep_present = 1
"""

TABLES = {"policy_facts": POLICY_FACTS, "sector_signals": SECTOR_SIGNALS,
          "reserved_domains": RESERVED_DOMAINS}


def _upsert(con, name, sql, snapshot_date, country):
    """Run the aggregation and merge it into data/<name>.parquet, replacing any
    rows for this (snapshot_date, country) and preserving other snapshots."""
    con.execute(f"CREATE OR REPLACE TEMP TABLE fresh AS {sql}",
                [snapshot_date, country])
    path = OUT / f"{name}.parquet"
    if path.exists():
        con.execute(
            "CREATE OR REPLACE TEMP TABLE merged AS "
            "SELECT * FROM read_parquet(?) "
            "WHERE NOT (snapshot_date = ? AND country = ?) "
            "UNION ALL BY NAME SELECT * FROM fresh",
            [str(path), snapshot_date, country])
        src_tbl = "merged"
    else:
        src_tbl = "fresh"
    con.execute(f"COPY (SELECT * FROM {src_tbl} ORDER BY snapshot_date, country) "
                f"TO '{path}' (FORMAT parquet)")
    return con.execute(f"SELECT COUNT(*), COUNT(DISTINCT snapshot_date) "
                       f"FROM {src_tbl}").fetchone()


def build(db_path, snapshot_date, country):
    OUT.mkdir(exist_ok=True)
    con = duckdb.connect()
    con.execute("INSTALL sqlite; LOAD sqlite;")
    con.execute(f"ATTACH '{db_path}' AS src (TYPE sqlite, READ_ONLY);")

    if snapshot_date is None:
        snapshot_date = con.execute(
            "SELECT max(substr(ts, 1, 10)) FROM src.fetches").fetchone()[0]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", snapshot_date or ""):
        raise SystemExit(f"snapshot date must be YYYY-MM-DD, got {snapshot_date!r}")

    print(f"snapshot {snapshot_date} / country {country} from {db_path.name}")
    for name, sql in TABLES.items():
        rows, snaps = _upsert(con, name, sql, snapshot_date, country)
        print(f"  {name}.parquet: {rows} rows across {snaps} snapshot(s)")

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
    ap.add_argument("--country", default="IT")
    a = ap.parse_args()
    build(a.db.resolve(), a.snapshot_date, a.country)
