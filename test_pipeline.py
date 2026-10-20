"""End-to-end test of parse -> cluster -> DW on a synthetic database.

Usage: python test_pipeline.py
Runs the real stage scripts in a temporary directory (CENSUS_COUNTRY=XX, so
census.xx.db) and checks the cases the unit tests cannot see: rows that must
disappear between passes, and the observability rules of the DW layer.
"""
import json
import os
import pathlib
import sqlite3
import subprocess
import sys
import tempfile

from censuslib import db

ROOT = pathlib.Path(__file__).resolve().parent
FAILS = []


def check(name, got, expected):
    ok = got == expected
    print(f"{'OK  ' if ok else 'FAIL'} {name}: {got!r}"
          + ("" if ok else f" (expected {expected!r})"))
    if not ok:
        FAILS.append(name)


def fetch(con, domain, resource, status, body, headers=None):
    db.upsert_fetch(con, {
        "domain": domain, "resource": resource,
        "final_url": f"https://{domain}/{resource}", "status": status,
        "content_type": "", "redirects": 0, "body": body,
        "headers_json": json.dumps(headers or {}), "error": "",
        "ts": "2026-10-20T10:00:00+00:00", "client": "httpx"})


def run(stage, cwd):
    env = {**os.environ, "CENSUS_COUNTRY": "XX", "PYTHONPATH": str(ROOT)}
    subprocess.run([sys.executable, str(ROOT / stage)], cwd=cwd, env=env,
                   check=True, capture_output=True)


with tempfile.TemporaryDirectory() as tmp:
    path = pathlib.Path(tmp) / "census.xx.db"
    con = db.connect(path)
    for d in ("bom.it", "err.it", "wall.it", "gone.it", "tdm.it", "gems.it"):
        con.execute("INSERT INTO site_meta (domain, sector) VALUES (?, 'news')", (d,))
    fetch(con, "bom.it", "robots", 200, "﻿User-agent: *\nDisallow: /\n".encode())
    fetch(con, "err.it", "robots", 500, b"Internal Server Error")
    fetch(con, "wall.it", "robots", 200,
          b"<!DOCTYPE html><html><head><title>Just a moment...</title></head></html>")
    fetch(con, "gone.it", "robots", 200, b"User-agent: GPTBot\nDisallow: /\n")
    fetch(con, "gone.it", "llms", 200, b"# Gone\n- [x](https://gone.it)")
    fetch(con, "tdm.it", "robots", 404, b"")
    fetch(con, "tdm.it", "tdmrep", 200, b'[{"location": "/", "tdm-reservation": 1}]')
    fetch(con, "gems.it", "robots", 404, b"")
    fetch(con, "gems.it", "tdmrep", 404, b"")
    fetch(con, "gems.it", "home", 200, b"<html></html>", {"tdm-a": "1"})
    con.commit()

    run("run_parse.py", tmp)
    # gone.it's llms.txt disappears behind a 403 before the second pass
    fetch(con, "gone.it", "llms", 403, b"")
    con.commit()
    for stage in ("run_parse.py", "run_cluster.py", "run_dw.py"):
        run(stage, tmp)

    q = sqlite3.connect(path)
    dim = {r[0]: r[1:] for r in q.execute(
        "SELECT domain, observable, unobservable_reason, llms_origin, tdmrep_present "
        "FROM dw_dim_domain")}
    gpt = dict(q.execute(
        "SELECT d.domain, f.verdict || '/' || f.verdict_source FROM dw_fact_policy f "
        "JOIN dw_dim_domain d USING (domain_key) JOIN dw_dim_crawler c USING (crawler_key) "
        "WHERE c.crawler = 'GPTBot'"))

    check("BOM keeps the wildcard group", gpt["bom.it"], "blocked/wildcard")
    check("5xx is unobservable", dim["err.it"][:2], (0, "server_error"))
    check("5xx has no verdict", gpt["err.it"], None)
    check("challenge page is a block", dim["wall.it"][:2], (0, "blocked"))
    check("vanished llms.txt leaves no origin", dim["gone.it"][2], "none")
    check("vanished llms.txt leaves no meta row",
          q.execute("SELECT COUNT(*) FROM llms_meta WHERE domain='gone.it'").fetchone()[0], 0)
    check("tdmrep file with reservation 1 reserves", dim["tdm.it"][3], 1)
    check("tdm-a header does not reserve", dim["gems.it"][3], 0)

print(f"\n{'ALL OK' if not FAILS else f'FAILED: {FAILS}'}")
sys.exit(1 if FAILS else 0)
