"""CMS, SEO plugin and CDN fingerprinting from the homepage."""
import re

CMS_PATTERNS = [
    ("wordpress",   re.compile(r"wp-content|wp-includes|wp-json", re.I)),
    ("shopify",     re.compile(r"cdn\.shopify\.com|Shopify\.theme", re.I)),
    ("prestashop",  re.compile(r"prestashop", re.I)),
    ("magento",     re.compile(r"magento|mage/cookies", re.I)),
    ("joomla",      re.compile(r"joomla", re.I)),
    ("drupal",      re.compile(r"drupal", re.I)),
    ("wix",         re.compile(r"wix\.com|wixstatic", re.I)),
    ("squarespace", re.compile(r"squarespace", re.I)),
    ("webflow",     re.compile(r"webflow", re.I)),
    ("typo3",       re.compile(r"typo3", re.I)),
]

SEO_PLUGIN_PATTERNS = [
    ("yoast",     re.compile(r"yoast seo|yoast\.com", re.I)),
    ("rank_math", re.compile(r"rank math", re.I)),
    ("aioseo",    re.compile(r"all in one seo", re.I)),
    ("seopress",  re.compile(r"seopress", re.I)),
]


def fingerprint(html: str, headers: dict) -> dict:
    gen = re.search(
        r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)', html, re.I)
    generator = gen.group(1).lower() if gen else ""
    cms = ""
    for name, rx in CMS_PATTERNS:
        if name in generator or rx.search(html):
            cms = name
            break
    plugin = ""
    for name, rx in SEO_PLUGIN_PATTERNS:
        if rx.search(html):
            plugin = name
            break
    hdrs = {k.lower(): v for k, v in headers.items()}
    cdn = ""
    if "cf-ray" in hdrs or "cloudflare" in hdrs.get("server", "").lower():
        cdn = "cloudflare"
    elif "x-akamai-transformed" in hdrs:
        cdn = "akamai"
    elif "x-served-by" in hdrs and "fastly" in hdrs.get("x-served-by", "").lower():
        cdn = "fastly"
    elif "x-vercel-id" in hdrs:
        cdn = "vercel"
    return {"cms": cms, "seo_plugin": plugin, "cdn": cdn}
