"""Stage 1 — Fetch of robots.txt, llms.txt, llms-full.txt, tdmrep.json, homepage.

Usage: python run_fetch.py [--limit N] [--only-missing]
Input: domains.csv (columns: domain,sector). Output: fetches table in SQLite.
Idempotent: --only-missing resumes from where it stopped.
"""
import argparse
import asyncio
import csv
import json
from datetime import datetime, timezone

import httpx

import config
from censuslib import db


async def _get(client, url):
    """One GET with retries. Returns a response, or the last exception."""
    err = None
    for attempt in range(config.RETRIES + 1):
        try:
            return await client.get(url)
        except httpx.HTTPError as e:
            err = e
            if attempt < config.RETRIES:
                await asyncio.sleep(1.5 * (attempt + 1))
    return err


async def fetch_one(client, sem, domain, resource, path):
    # bare domains that don't resolve (common for PA sites) fall back to www.
    hosts = [domain]
    if not domain.startswith("www."):
        hosts.append(f"www.{domain}")
    async with sem:
        for host in hosts:
            url = f"https://{host}{path}"
            r = await _get(client, url)
            if not isinstance(r, Exception):
                return {
                    "domain": domain, "resource": resource,
                    "final_url": str(r.url), "status": r.status_code,
                    "content_type": r.headers.get("content-type", ""),
                    "redirects": len(r.history),
                    "body": r.content[:512_000],  # cap 500KB (homepage)
                    "headers_json": json.dumps(dict(r.headers)),
                    "error": "",
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "client": "httpx",
                }
            if not isinstance(r, httpx.ConnectError):
                break  # only connection/DNS failures justify the www. retry
        return {
            "domain": domain, "resource": resource, "final_url": url,
            "status": 0, "content_type": "", "redirects": 0, "body": b"",
            "headers_json": "{}", "error": f"{type(r).__name__}: {r}",
            "ts": datetime.now(timezone.utc).isoformat(),
            "client": "httpx",
        }


async def main(limit, only_missing):
    con = db.connect(config.DB_PATH)
    with open(config.DOMAINS_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if limit:
        rows = rows[:limit]

    for row in rows:
        con.execute(
            "INSERT OR IGNORE INTO site_meta (domain, sector) VALUES (?,?)",
            (row["domain"].strip().lower(), row.get("sector", "").strip()))
    con.commit()

    done = set()
    if only_missing:
        done = set(con.execute(
            "SELECT domain, resource FROM fetches WHERE status != 0"))

    tasks = []
    sem = asyncio.Semaphore(config.CONCURRENCY)
    async with httpx.AsyncClient(
        follow_redirects=True, timeout=config.TIMEOUT,
        headers={"User-Agent": config.USER_AGENT},
        limits=httpx.Limits(max_connections=config.CONCURRENCY),
    ) as client:
        for row in rows:
            dom = row["domain"].strip().lower()
            for resource, path in config.RESOURCES.items():
                if (dom, resource) in done:
                    continue
                tasks.append(fetch_one(client, sem, dom, resource, path))

        print(f"{len(tasks)} fetches to run...")
        n = 0
        for coro in asyncio.as_completed(tasks):
            res = await coro
            con.execute(
                "INSERT OR REPLACE INTO fetches VALUES "
                "(:domain,:resource,:final_url,:status,:content_type,"
                ":redirects,:body,:headers_json,:error,:ts,:client)", res)
            n += 1
            if n % 100 == 0:
                con.commit()
                print(f"  {n}/{len(tasks)}")
        con.commit()

    errs = con.execute(
        "SELECT COUNT(*) FROM fetches WHERE status = 0").fetchone()[0]
    print(f"Done. Failed fetches (after retries): {errs}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only-missing", action="store_true")
    a = ap.parse_args()
    asyncio.run(main(a.limit, a.only_missing))
