# AI Crawler Census — AI-crawler policies on Italian websites

ETL pipeline: census of robots.txt, llms.txt and tdmrep.json across a sample
of Italian domains. Three signals, three semantics: technical convention
(robots), offer to LLMs (llms.txt), legal reservation under Art. 4 CDSM
(TDMRep).

## Usage

```bash
pip install httpx curl_cffi
# set your email in config.py (USER_AGENT) before fetching
python build_sample.py           # stage 0: stratified domains.csv
                                 #          (sector lists + DNS validation)
python run_fetch.py              # stage 1: fetch (idempotent with --only-missing)
python run_refetch.py            # stage 1b: retry shielded domains (curl_cffi,
                                 #           browser TLS impersonation)
python run_parse.py              # stage 2+3: validation, parsing, verdicts
python run_cluster.py            # stage 4: template clustering
python run_dw.py                 # stage 5: star-schema DW layer (dw_* tables)
python run_report.py             # stage 6: visual study (report.html) —
                                 #          needs the DW tables, run 5 first
python test_parsers.py           # parser tests
```

Windows note: if `python` resolves to the Microsoft Store alias
(`WindowsApps\python`, hangs or "Permission denied"), use `py` or the full
interpreter path instead.

Output: `census.db` (SQLite). Main tables:

- `verdicts` — domain × crawler: verdict ∈ {blocked, partial, allowed},
  source ∈ {specific, wildcard, no_robots}. "blocked" = root path denied
  under RFC 9309 semantics (longest-match, allow wins on ties).
- `files` — validated presence of the three files (soft-404 excluded,
  with the reason).
- `robots_meta` — hash of the AI block (for clustering) + generator signatures.
- `llms_meta` / `tdmrep_meta` — file structure. In `llms_meta`,
  `valid` = llms.txt valid, `has_llms_full` = llms-full.txt valid: they vary
  independently (some sites publish only the -full). `llms_hash` /
  `llms_full_hash` are SHA-1 of the whitespace-normalized text;
  `full_same_as_llms` = 1 when both are valid and identical;
  `full_similarity` is the Jaccard on word 5-shingles between the two,
  robust to formatting differences (plugin-generated pairs sit at ~0.96
  without being byte-identical). `has_instructions` /
  `instruction_signals` flag directive language aimed at LLMs ("you should",
  "when answering", citation requests) — boilerplate plugin preambles count
  too, so cross them with `signatures` to separate decided from inherited.
- `site_meta` — sector, CMS, SEO plugin, CDN.
- `clusters` — template clusters (exact hash + Jaccard ≥ 0.8).
- `fetches` — the raw source layer: bodies, headers, final URL, timestamp,
  and `client` (httpx | chrome_impersonate) recording how each row was
  obtained. Everything downstream is re-derivable from here.
- JSON columns (queryable with SQLite JSON1): `robots_meta.parsed_json`
  (full groups/rules structure), `llms_meta.sections_json` (sections with
  links), `tdmrep_meta.rules_json` (validated rule array) — no parsed
  information is flattened away.
- `dw_dim_domain` / `dw_dim_crawler` / `dw_fact_policy` — star schema for
  BI queries (grain: domain × crawler), rebuilt idempotently by run_dw.py.

Artifacts: `report.html` (self-contained visual study, stage 6) and
`slides.md` (20-slide presentation draft mapped to the homework spec).

## Design decisions

- **Soft-404**: presence = status 200 + structurally valid content.
  A 200 on llms.txt proves nothing: many servers answer 200 with HTML
  on any path.
- **not_mentioned ≠ allowed**: the `source` column separates explicit
  permission (specific) from absence of mention (wildcard/no_robots).
  Keep them apart in the analysis: the latter is the default, not a choice.
- **Normalized AI block**: agents sorted alphabetically before hashing,
  so token order doesn't split clusters.
- **`purpose` (training/search)**: enables the coherence analysis
  (e.g. blocks training but not search, or vice versa).
- **www. fallback**: bare domains that fail DNS (common for PA sites,
  e.g. gov.it) are retried once with the `www.` prefix; `final_url`
  records what was actually fetched.

## Limits to declare in the study

- robots.txt measures declared intent, not crawler behavior.
- The CMS fingerprint is heuristic (false negatives on sites that mask it).
- TDMRep is read through all three spec channels (well-known file,
  HTTP headers, HTML meta tags in the homepage).

## TODO

- [x] definitive domains.csv (stratified sample by sector;
      backbone: tranco_it.csv — Tranco top-1M filtered to .it, 10k domains —
      foreign domain hacks excluded)
- [x] llms-full.txt check (fetch + parse; hashes, shingle similarity,
      instruction detection)
- [x] recovery pass for bot-walled domains (curl_cffi TLS impersonation)
- [x] star-schema DW layer (source → staging → dw_*)
- [x] visual study (report.html) + presentation draft (slides.md)
- [x] tdm:* meta tags in the homepage (third TDMRep channel; found
      corriere.it and gazzetta.it — RCS — raising adoption to 8/543)
- [ ] `unknown` verdict for unobservable domains (now counted as
      allowed/no_robots with a caveat — cleaner as its own class)
- [ ] historical dimension via Wayback Machine (optional stage)
- [ ] recurring observatory: monthly snapshots, trend charts
      (SQLite → DuckDB/Postgres when it happens)
