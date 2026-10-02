"""Root-edition check: what a site serves at its root to a visitor from here.

Tells national hosts from multi-country ones. Run it from outside the sites'
home country (the GitHub Actions runner is the usual vantage): a national host
still serves its home edition at the root; a multi-country host routes the
visitor to a country edition or a global selector.

Usage: python vantage_check.py elpais.com yoox.com ... > vantage.json
"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor

from curl_cffi import requests as creq

LANG = re.compile(r"<html[^>]*\blang=[\"']?([A-Za-z-]+)", re.I)
HREFLANG = re.compile(r"hreflang=[\"']?([A-Za-z-]+)", re.I)


def get(url):
    return creq.get(url, impersonate="chrome", timeout=20, allow_redirects=True)


def check(domain):
    error = None
    for host in (domain, f"www.{domain}"):
        try:
            r = get(f"https://{host}/")
        except Exception as e:  # any failure: try the www host, then report it
            error = f"{type(e).__name__}: {e}"[:200]
            continue
        lang = LANG.search(r.text)
        return {
            "domain": domain,
            "status": r.status_code,
            "final_url": str(r.url),
            "lang": lang.group(1) if lang else None,
            "hreflang": sorted({h.lower() for h in HREFLANG.findall(r.text)}),
        }
    return {"domain": domain, "error": error}


def vantage():
    """Where the requests leave from, so every result says what it was seen from."""
    try:
        info = get("https://ipinfo.io/json").json()
        return {k: info.get(k) for k in ("country", "region", "org")}
    except Exception as e:
        return {"error": type(e).__name__}


def main(domains):
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(check, domains))
    json.dump({"vantage": vantage(), "results": results}, sys.stdout, indent=1)


if __name__ == "__main__":
    main([d.strip().lower() for d in sys.argv[1:] if d.strip()])
