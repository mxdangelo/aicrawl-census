"""Network helpers shared by the fetch stages."""
from urllib.parse import urlparse


def same_site(domain: str, url: str) -> bool:
    """True if `url` stays on `domain`'s own host family (itself, www., or a
    subdomain, or `domain` being a subdomain of it). A fetch that ends anywhere
    else - a rebrand, or a geo-redirect to another country's site - did not
    observe this domain's own file."""
    host = (urlparse(url).hostname or "").lower().removeprefix("www.")
    domain = domain.lower().removeprefix("www.")
    return host == domain or host.endswith(f".{domain}") or domain.endswith(f".{host}")


def candidate_hosts(domain: str) -> list[str]:
    """The host and its www. variant, for the DNS-fallback fetch. Bare hosts
    that don't resolve (common for PA sites) are retried once with www.;
    hosts already prefixed with www. are used as-is."""
    if domain.startswith("www."):
        return [domain]
    return [domain, f"www.{domain}"]
