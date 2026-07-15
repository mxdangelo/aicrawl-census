---
name: snapshot
description: Use when taking a new census snapshot for the AI Crawler Observatory (re-crawl, new snapshot, run the pipeline, update the dashboard data). The full runbook with the ordering constraints and gotchas that are not obvious from the README.
---

# Taking a new snapshot

One crawl = one snapshot. The parquet layer (`dashboard/data/`) accumulates
snapshots; the SQLite layer does NOT — `fetches` is keyed `(domain, resource)`
with INSERT OR REPLACE, so a re-run **overwrites the previous crawl's raw
layer**. Back it up first.

## Runbook (repo root; `py`, never bare `python`)

```
cp census.db census.YYYY-MM-DD.backup.db   # previous snapshot date; *.backup.* is gitignored
py run_fetch.py            # full re-run — NO --only-missing (it would skip everything)
py run_refetch.py          # shielded domains, browser TLS impersonation
py run_parse.py
py run_cluster.py
py run_dw.py
py test_parsers.py
py build_lite.py           # regenerate census-lite.db (the tracked artifact)
py dashboard/build_data.py # snapshot date auto-derived from fetch ts; upserts parquet
quarto render dashboard/index.qmd   # see the user-level quarto skill (QUARTO_PYTHON!)
```

Fetch takes several minutes (2.7k requests) — run in background.

## Gotchas

- **Prose figures in `index.qmd` are hardcoded** and must be refreshed against
  the new snapshot: the lead (GPTBot % for news / media / overall), the Offer
  counts ("N of 543 sites, X%", the banking fraction), the Reserve counts
  ("8 of 543", sector split). Charts and the dateline update themselves; the
  prose does not.
- `build_data.py` is idempotent per `(snapshot_date, country)`. To rebuild a
  *past* snapshot's parquet rows (e.g. after adding a new tidy table), run it
  against that snapshot's backup DB:
  `py dashboard/build_data.py --db census.YYYY-MM-DD.backup.db --snapshot-date YYYY-MM-DD`.
- Verify after render: `dashboard/data/meta.json` lists all snapshots; the page
  shows 543 domains (not a multiple — that means the latest-snapshot filter
  broke) and the dateline shows the new date.

## Delta for the PR description

Week-over-week changes are the interesting output. Attach the backup and diff:

```sql
ATTACH 'census.YYYY-MM-DD.backup.db' AS old;
-- changed verdicts (who moved)
SELECT v.domain, v.crawler, o.verdict, v.verdict FROM verdicts v
JOIN old.verdicts o ON o.domain=v.domain AND o.crawler=v.crawler
WHERE v.verdict != o.verdict;
-- file presence: SUM(present) per resource in files vs old.files
-- tdmrep any-channel: valid=1 OR via_header=1 OR via_meta=1 in tdmrep_meta
```

Robots.txt that appear/disappear on PA sites are often infrastructure noise —
note them, don't headline them.

## Ship

Branch `snapshot-YYYY-MM-DD`, two commits (code changes if any, then data
injection), PR with the delta table. After merge: `quarto publish gh-pages`
from `dashboard/` — production deploy, needs the user's explicit go-ahead.
