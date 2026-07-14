"""Regenerate census-lite.db, the shippable snapshot of census.db.

Same tables, except fetches drops the raw bodies (body -> body_bytes): the
blobs are what push census.db past GitHub's 100 MB limit. Run after each
pipeline pass, before dashboard/build_data.py.

Usage: python build_lite.py
"""
import os
import sqlite3

import config

LITE_PATH = "census-lite.db"

FETCHES_LITE = """
CREATE TABLE fetches AS
SELECT domain, resource, final_url, status, content_type, redirects,
       LENGTH(body) AS body_bytes, headers_json, error, ts, client
FROM src.fetches
"""


def main():
    if os.path.exists(LITE_PATH):
        os.remove(LITE_PATH)
    con = sqlite3.connect(LITE_PATH)
    con.execute(f"ATTACH '{config.DB_PATH}' AS src")
    tables = [r[0] for r in con.execute(
        "SELECT name FROM src.sqlite_master WHERE type='table'")]
    for t in tables:
        con.execute(FETCHES_LITE if t == "fetches"
                    else f"CREATE TABLE {t} AS SELECT * FROM src.{t}")
    con.commit()
    con.execute("VACUUM")
    print(f"{LITE_PATH}: {len(tables)} tables, "
          f"{os.path.getsize(LITE_PATH) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
