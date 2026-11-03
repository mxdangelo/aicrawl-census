"""Custom robots.txt parser.

Preserves comments and ordering (needed for fingerprinting) and implements
RFC 9309 semantics: group selection by most specific user-agent match,
longest-match between Allow/Disallow, Allow wins on ties.
"""
import hashlib
import re
from dataclasses import dataclass, field


@dataclass
class Group:
    agents: list = field(default_factory=list)   # user-agent tokens, lowercase
    rules: list = field(default_factory=list)    # (type, pattern), type in {allow,disallow}
    start_line: int = 0


@dataclass
class Robots:
    groups: list = field(default_factory=list)
    comments: list = field(default_factory=list)  # (line_no, text)
    n_lines: int = 0
    other_directives: list = field(default_factory=list)  # sitemap, crawl-delay, ...


def parse(text: str) -> Robots:
    r = Robots()
    current = None
    last_was_agent = False
    lines = text.splitlines()
    r.n_lines = len(lines)
    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            r.comments.append((i, line))
            continue
        if "#" in line:  # inline comment
            line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip().lower(), val.strip()
        if key == "user-agent":
            if not last_was_agent:
                current = Group(start_line=i)
                r.groups.append(current)
            current.agents.append(val.lower())
            last_was_agent = True
        elif key in ("allow", "disallow"):
            last_was_agent = False
            if current is not None:
                current.rules.append((key, val))
        else:
            last_was_agent = False
            r.other_directives.append((key, val))
    return r


def _pattern_to_regex(pattern: str):
    parts = []
    for ch in pattern:
        if ch == "*":
            parts.append(".*")
        elif ch == "$":
            parts.append("$")
        else:
            parts.append(re.escape(ch))
    return re.compile("^" + "".join(parts))


def _select_group(robots: Robots, ua_token: str):
    """Group with the most specific user-agent match; none -> wildcard.

    Returns (effective_rules, source) with source in {specific, wildcard, none}.
    Groups naming the same agent are merged (Google behavior).
    """
    ua = ua_token.lower()
    specific, wildcard = [], []
    for g in robots.groups:
        for a in g.agents:
            if a == "*":
                wildcard.extend(g.rules)
            elif a == ua or ua.startswith(a) or a.startswith(ua):
                specific.extend(g.rules)
    if specific:
        return specific, "specific"
    if wildcard:
        return wildcard, "wildcard"
    return [], "none"


def verdict_for(robots: Robots, ua_token: str, path: str = "/"):
    """Returns (verdict, source, mentioned).

    verdict: blocked  -> root path denied
             partial  -> root allowed but non-empty Disallow rules exist
             allowed  -> no applicable restriction
    """
    rules, source = _select_group(robots, ua_token)
    return _evaluate(rules, path), source, source == "specific"


def _evaluate(rules, path):
    """blocked | partial | allowed for `path` under longest-match, Allow
    winning ties."""
    best_len, best_type = -1, "allow"
    for rtype, pattern in rules:
        if pattern == "":
            continue  # empty "Disallow:" = allow everything
        if _pattern_to_regex(pattern).search(path):
            plen = len(pattern)
            if plen > best_len or (plen == best_len and rtype == "allow"):
                best_len, best_type = plen, rtype

    if best_type == "disallow":
        return "blocked"
    has_disallow = any(t == "disallow" and p for t, p in rules)
    return "partial" if has_disallow else "allowed"


def usage_pref(robots: Robots, token: str, path: str = "/"):
    """Usage preference bound to a policy token
    (draft-kelley-aipref-training-preference-signal-00).

    Returns (pref, exceptions, mixed):
      pref        against  -> path disallowed for the token
                  partial  -> path allowed, other paths disallowed
                  in_favor -> no path disallowed
                  none     -> no group names the token: no preference
      exceptions  1 when `pref` is against and some path is allowed
                  (Figure 1 of the draft: Disallow: / + Allow: /press-kit/)
      mixed       1 when a group binds the token together with other agents

    Unlike verdict_for, the token is matched exactly (case aside, §4.1) and
    the * group never applies (§4.2). The result is independent of the
    crawler verdicts (§4.3): it says how content may be used, not fetched.
    """
    tok = token.lower()
    groups = [g for g in robots.groups if tok in g.agents]
    if not groups:
        return "none", 0, 0
    rules = [r for g in groups for r in g.rules]
    verdict = _evaluate(rules, path)
    pref = {"blocked": "against", "partial": "partial",
            "allowed": "in_favor"}[verdict]
    exceptions = int(pref == "against"
                     and any(t == "allow" and p for t, p in rules))
    mixed = int(any(len(set(g.agents)) > 1 for g in groups))
    return pref, exceptions, mixed


def as_dict(robots: Robots) -> dict:
    """Full parsed structure, for the JSON column (no information loss)."""
    return {
        "groups": [{"agents": g.agents, "rules": [[t, p] for t, p in g.rules]}
                   for g in robots.groups],
        "other_directives": [[k, v] for k, v in robots.other_directives],
    }


def ai_block(robots: Robots, ai_tokens) -> tuple[str, str]:
    """Extracts the groups mentioning AI crawlers, normalized, for template
    clustering. Returns (text, hash)."""
    tokens = {t.lower() for t in ai_tokens}
    chunks = []
    for g in robots.groups:
        if any(a in tokens for a in g.agents):
            head = "\n".join(f"user-agent: {a}" for a in sorted(g.agents))
            body = "\n".join(f"{t}: {p}" for t, p in g.rules)
            chunks.append(head + "\n" + body)
    text = "\n---\n".join(chunks)
    h = hashlib.sha1(text.encode()).hexdigest()[:12] if text else ""
    return text, h


GENERATOR_SIGNATURES = {
    "yoast":       re.compile(r"yoast", re.I),
    "rank_math":   re.compile(r"rank\s*math", re.I),
    "aioseo":      re.compile(r"all in one seo", re.I),
    "cloudflare":  re.compile(r"cloudflare", re.I),
    "wix":         re.compile(r"wix\.com", re.I),
    "squarespace": re.compile(r"squarespace", re.I),
    "shopify":     re.compile(r"shopify", re.I),
    "darkvisitors": re.compile(r"dark\s*visitors", re.I),
}


def signatures(text: str) -> list[str]:
    return [name for name, rx in GENERATOR_SIGNATURES.items() if rx.search(text)]
