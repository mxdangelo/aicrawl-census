import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS fetches (
    domain TEXT, resource TEXT, final_url TEXT,
    status INTEGER, content_type TEXT, redirects INTEGER,
    body BLOB, headers_json TEXT, error TEXT, ts TEXT,
    client TEXT DEFAULT 'httpx',             -- httpx | chrome_impersonate
    PRIMARY KEY (domain, resource)
);
CREATE TABLE IF NOT EXISTS files (          -- validation outcome per resource
    domain TEXT, resource TEXT,
    present INTEGER,                         -- 1 = valid file, 0 = absent/soft-404
    reason TEXT,                             -- why present/absent
    PRIMARY KEY (domain, resource)
);
CREATE TABLE IF NOT EXISTS verdicts (        -- domain x crawler
    domain TEXT, crawler TEXT, operator TEXT, purpose TEXT,
    mentioned INTEGER,                       -- specific group in robots.txt
    verdict TEXT,                            -- blocked | allowed | partial
    source TEXT,                             -- specific | wildcard | no_robots
    PRIMARY KEY (domain, crawler)
);
CREATE TABLE IF NOT EXISTS robots_meta (
    domain TEXT PRIMARY KEY,
    n_groups INTEGER, n_lines INTEGER, n_comments INTEGER,
    ai_block_hash TEXT,                      -- hash of the AI directives block
    ai_block_text TEXT,
    signatures TEXT,                         -- generator signatures in comments (csv)
    parsed_json TEXT                         -- full groups/rules structure (JSON1-queryable)
);
CREATE TABLE IF NOT EXISTS llms_meta (
    domain TEXT PRIMARY KEY,
    valid INTEGER, h1 TEXT, has_blockquote INTEGER,
    n_sections INTEGER, n_links INTEGER, n_chars INTEGER,
    has_llms_full INTEGER,
    llms_hash TEXT, llms_full_hash TEXT,     -- SHA-1 of whitespace-normalized text
    full_same_as_llms INTEGER,               -- 1 = both valid and identical
    full_similarity REAL,                    -- line-Jaccard llms vs -full (NULL if not both valid)
    has_instructions INTEGER,                -- directive language beyond AI mentions
    instruction_signals TEXT,                -- matched pattern labels (csv)
    signatures TEXT,
    sections_json TEXT                       -- sections with their links (JSON)
);
CREATE TABLE IF NOT EXISTS tdmrep_meta (
    domain TEXT PRIMARY KEY,
    valid INTEGER, n_rules INTEGER,
    reservation_root INTEGER,                -- tdm-reservation for the widest location
    has_policy INTEGER, via_header INTEGER,  -- tdm-* headers on the homepage
    via_meta INTEGER,                        -- tdm-* meta tags in the homepage HTML
    rules_json TEXT                          -- validated rule array (JSON)
);
CREATE TABLE IF NOT EXISTS site_meta (
    domain TEXT PRIMARY KEY,
    sector TEXT, cms TEXT, seo_plugin TEXT, cdn TEXT
);
"""


def connect(path):
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    return con
