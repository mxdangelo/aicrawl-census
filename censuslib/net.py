"""Network helpers shared by the fetch stages."""


def candidate_hosts(domain: str) -> list[str]:
    """The host and its www. variant, for the DNS-fallback fetch. Bare hosts
    that don't resolve (common for PA sites) are retried once with www.;
    hosts already prefixed with www. are used as-is."""
    if domain.startswith("www."):
        return [domain]
    return [domain, f"www.{domain}"]
