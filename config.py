"""Configuration for the AI-crawler policy census on Italian websites."""

DB_PATH = "census.db"
DOMAINS_CSV = "domains.csv"  # columns: domain,sector

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
