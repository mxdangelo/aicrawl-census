"""Stage 1b — Re-fetch shielded domains with browser TLS impersonation.

Usage: python run_refetch.py
Some sites (403, tarpit timeouts) block non-browser TLS fingerprints, not
just user-agents: httpx never gets an answer while any real browser does.
This pass retries the suspect rows with curl_cffi impersonating Chrome and
replaces them only when it gets an actual response; the `client` column
records which rows came from this pass. Re-run run_parse.py afterwards.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json

from curl_cffi import requests as creq

import config
from censuslib import db

SUSPECT_STATUS = (0, 202, 403, 429, 503)
WORKERS = 8


def refetch(job):
    domain, resource, path = job
    hosts = [domain] if domain.startswith("www.") else [domain, f"www.{domain}"]
    for host in hosts:
        try:
            r = creq.get(f"https://{host}{path}", impersonate="chrome",
                         timeout=config.TIMEOUT, allow_redirects=True)
            return {
                "domain": domain, "resource": resource,
                "final_url": str(r.url), "status": r.status_code,
                "content_type": r.headers.get("content-type", ""),
                "redirects": len(r.history), "body": r.content[:512_000],
                "headers_json": json.dumps(dict(r.headers)), "error": "",
                "ts": datetime.now(timezone.utc).isoformat(),
                "client": "chrome_impersonate",
            }
        except Exception:
            continue
    return None  # still unreachable: keep the original row


def main():
    con = db.connect(config.DB_PATH)
    ph = ",".join("?" * len(SUSPECT_STATUS))
    jobs = [(d, res, config.RESOURCES[res]) for d, res in con.execute(
        f"SELECT domain, resource FROM fetches WHERE status IN ({ph})",
        SUSPECT_STATUS)]
    print(f"{len(jobs)} suspect rows, retrying with Chrome impersonation...")

    recovered = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for res in ex.map(refetch, jobs):
            if res is None:
                continue
            recovered += 1
            con.execute(
                "INSERT OR REPLACE INTO fetches VALUES "
                "(:domain,:resource,:final_url,:status,:content_type,"
                ":redirects,:body,:headers_json,:error,:ts,:client)", res)
    con.commit()
    print(f"Recovered {recovered}/{len(jobs)} rows "
          f"(any response counts, including 404).")
    for row in con.execute(
        "SELECT status, COUNT(*) FROM fetches "
        "WHERE client='chrome_impersonate' GROUP BY status ORDER BY 2 DESC"):
        print(f"  status {row[0]}: {row[1]}")


if __name__ == "__main__":
    main()
