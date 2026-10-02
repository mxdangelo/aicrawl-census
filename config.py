"""Configuration for the AI-crawler policy census (one country per database)."""
import os

# CENSUS_COUNTRY picks the country: IT keeps the original file names, any other
# code gets its own database and domain list (census.fr.db, domains.fr.csv).
COUNTRY = os.environ.get("CENSUS_COUNTRY", "IT").upper()
SUFFIX = "" if COUNTRY == "IT" else f".{COUNTRY.lower()}"

DB_PATH = f"census{SUFFIX}.db"
DOMAINS_CSV = f"domains{SUFFIX}.csv"  # columns: domain,sector

# User-agent token -> (operator, declared purpose)
# Purposes: training = model training; search = live retrieval/citation;
# both = ambiguous or both. The distinction matters for the coherence analysis.
AI_CRAWLERS = {
    "GPTBot":             ("OpenAI", "training"),
    "OAI-SearchBot":      ("OpenAI", "search"),
    "ChatGPT-User":       ("OpenAI", "search"),
    "ClaudeBot":          ("Anthropic", "training"),
    "Claude-User":        ("Anthropic", "search"),
    "Claude-SearchBot":   ("Anthropic", "search"),
    "anthropic-ai":       ("Anthropic", "training"),   # legacy token, still in templates
    "Google-Extended":    ("Google", "training"),
    "PerplexityBot":      ("Perplexity", "search"),
    "Perplexity-User":    ("Perplexity", "search"),
    "CCBot":              ("Common Crawl", "training"),
    "Bytespider":         ("ByteDance", "training"),
    "Amazonbot":          ("Amazon", "both"),
    "Applebot-Extended":  ("Apple", "training"),
    "meta-externalagent": ("Meta", "training"),
    "FacebookBot":        ("Meta", "both"),
    "cohere-ai":          ("Cohere", "training"),
    "Diffbot":            ("Diffbot", "both"),
    "AI2Bot":              ("Allen Institute", "training"),
    "MistralAI-User":     ("Mistral", "search"),
}

# Fetch
CONCURRENCY = 15
TIMEOUT = 15.0
RETRIES = 2

# HTTP outcomes that mean "no usable answer": DNS/connection failure (0),
# tarpit/queue (202), the blocks a WAF returns to non-browser TLS
# (403/429/503), and 451, a site refusing visitors from our country (UK
# betting sites do this to non-UK IPs). run_refetch.py retries these with
# browser impersonation; run_dw.py treats them as not observable. Single
# source to avoid drift.
SHIELDED_STATUS = (0, 202, 403, 429, 451, 503)
USER_AGENT = (
    "Mozilla/5.0 (compatible; AICrawlCensus/0.1; academic research; "
    "+mailto:mxdangelo.seo@gmail.com)"
)

RESOURCES = {
    "robots":    "/robots.txt",
    "llms":      "/llms.txt",
    "llms_full": "/llms-full.txt",  # some sites only publish this one
    "tdmrep":    "/.well-known/tdmrep.json",
    "home":      "/",
}
