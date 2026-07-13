"""Stage 5 — Data warehouse layer (star schema) on top of staging.

Usage: python run_dw.py
Three-layer architecture, per BI convention:
  source   — domains.csv + fetches (raw bodies/headers, provenance in `client`)
  staging  — files, verdicts, robots_meta, llms_meta, tdmrep_meta, site_meta
             (validated, typed, one grain each)
  DW       — dw_dim_domain, dw_dim_crawler, dw_fact_policy (this script)
The fact grain is domain × crawler; everything analytical joins on surrogate
keys. Rebuilt idempotently from staging on every run.
"""
import sqlite3

import config

DDL = """
DROP TABLE IF EXISTS dw_fact_policy;
DROP TABLE IF EXISTS dw_dim_domain;
DROP TABLE IF EXISTS dw_dim_crawler;

CREATE TABLE dw_dim_crawler (
    crawler_key INTEGER PRIMARY KEY,
    crawler TEXT UNIQUE, operator TEXT, purpose TEXT
);
CREATE TABLE dw_dim_domain (
    domain_key INTEGER PRIMARY KEY,
    domain TEXT UNIQUE, sector TEXT,
    cms TEXT, seo_plugin TEXT, cdn TEXT,
    observable INTEGER,           -- robots.txt reachable (any HTTP answer)
    robots_present INTEGER, llms_present INTEGER,
    llms_full_present INTEGER, tdmrep_present INTEGER,
    llms_origin TEXT,             -- hand | generated | none
    llms_has_instructions INTEGER,
    ai_template_cluster TEXT, ai_cluster_size INTEGER
);
CREATE TABLE dw_fact_policy (
    domain_key INTEGER REFERENCES dw_dim_domain(domain_key),
    crawler_key INTEGER REFERENCES dw_dim_crawler(crawler_key),
    mentioned INTEGER, verdict TEXT, verdict_source TEXT,
    PRIMARY KEY (domain_key, crawler_key)
);
"""


def main():
    con = sqlite3.connect(config.DB_PATH)
    con.executescript(DDL)

    for crawler, (operator, purpose) in config.AI_CRAWLERS.items():
        con.execute(
            "INSERT INTO dw_dim_crawler (crawler, operator, purpose) "
            "VALUES (?,?,?)", (crawler, operator, purpose))

    shielded_in = ",".join(str(s) for s in config.SHIELDED_STATUS)
    con.execute(f"""
        INSERT INTO dw_dim_domain (domain, sector, cms, seo_plugin, cdn,
            observable, robots_present, llms_present, llms_full_present,
            tdmrep_present, llms_origin, llms_has_instructions,
            ai_template_cluster, ai_cluster_size)
        SELECT s.domain, s.sector, s.cms, s.seo_plugin, s.cdn,
            (SELECT status NOT IN ({shielded_in}) FROM fetches
              WHERE domain=s.domain AND resource='robots'),
            COALESCE((SELECT present FROM files
                      WHERE domain=s.domain AND resource='robots'), 0),
            COALESCE((SELECT present FROM files
                      WHERE domain=s.domain AND resource='llms'), 0),
            COALESCE((SELECT present FROM files
                      WHERE domain=s.domain AND resource='llms_full'), 0),
            COALESCE((SELECT valid=1 OR via_header=1 OR via_meta=1
                      FROM tdmrep_meta WHERE domain=s.domain), 0),
            CASE
              WHEN (SELECT valid FROM llms_meta WHERE domain=s.domain) IS NULL
                   OR (SELECT valid FROM llms_meta WHERE domain=s.domain)=0
                THEN 'none'
              WHEN (SELECT signatures != ''
                        OR COALESCE(full_similarity,0) >= 0.9
                    FROM llms_meta WHERE domain=s.domain)
                THEN 'generated' ELSE 'hand' END,
            COALESCE((SELECT has_instructions FROM llms_meta
                      WHERE domain=s.domain), 0),
            (SELECT cluster_id FROM clusters WHERE domain=s.domain),
            (SELECT cluster_size FROM clusters WHERE domain=s.domain)
        FROM site_meta s""")

    con.execute("""
        INSERT INTO dw_fact_policy
        SELECT d.domain_key, c.crawler_key, v.mentioned, v.verdict, v.source
        FROM verdicts v
        JOIN dw_dim_domain d ON d.domain = v.domain
        JOIN dw_dim_crawler c ON c.crawler = v.crawler""")

    con.commit()
    for t in ("dw_dim_crawler", "dw_dim_domain", "dw_fact_policy"):
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {n} rows")
    # smoke: a BI-style query through the star only
    print("\nBI smoke query — blocked share by sector x purpose (top 5):")
    for r in con.execute("""
        SELECT d.sector, c.purpose,
               ROUND(100.0 * SUM(f.verdict='blocked' AND f.verdict_source='specific')
                     / COUNT(*), 1) pct
        FROM dw_fact_policy f
        JOIN dw_dim_domain d USING (domain_key)
        JOIN dw_dim_crawler c USING (crawler_key)
        WHERE c.purpose IN ('training','search')
        GROUP BY d.sector, c.purpose ORDER BY pct DESC LIMIT 5"""):
        print(f"  {r[0]} / {r[1]}: {r[2]}%")


if __name__ == "__main__":
    main()
