"""Soft-404 validation and parsers for llms.txt and tdmrep.json."""
import hashlib
import json
import re


def looks_like_html(body: str) -> bool:
    head = body[:500].lower()
    return "<html" in head or "<!doctype" in head or "<head" in head


def validate_robots(status: int, content_type: str, body: str):
    if status != 200:
        return False, f"status_{status}"
    if looks_like_html(body):
        return False, "soft404_html"
    if not body.strip():
        return False, "empty"
    if not re.search(r"^\s*(user-agent|sitemap|disallow|allow)\s*:", body,
                     re.I | re.M):
        return False, "no_directives"
    return True, "ok"


def validate_llms(status: int, content_type: str, body: str):
    if status != 200:
        return False, f"status_{status}"
    if looks_like_html(body):
        return False, "soft404_html"
    if not body.strip():
        return False, "empty"
    # The spec requires markdown with a leading H1; we tolerate non-conforming
    # files (including the missing space after #, seen in the wild) but demand
    # at least minimal markdown structure.
    if not re.search(r"^#{1,3}\s*\S", body, re.M):
        return False, "not_markdown"
    return True, "ok"


def parse_llms(body: str) -> dict:
    h1 = re.search(r"^#(?!#)\s*(.+)$", body, re.M)
    return {
        "h1": h1.group(1).strip() if h1 else "",
        "has_blockquote": int(bool(re.search(r"^>\s*\S", body, re.M))),
        "n_sections": len(re.findall(r"^##(?!#)\s*\S", body, re.M)),
        "n_links": len(re.findall(r"\[[^\]]*\]\([^)]+\)", body)),
        "n_chars": len(body),
    }


def parse_llms_sections(body: str) -> list:
    """Sections with their links, for the JSON column. Links before the
    first H2 go under title ''."""
    sections = []
    current = {"title": "", "links": []}
    for line in body.splitlines():
        m = re.match(r"^##(?!#)\s*(.+)$", line)
        if m:
            if current["title"] or current["links"]:
                sections.append(current)
            current = {"title": m.group(1).strip(), "links": []}
            continue
        for text, url in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", line):
            current["links"].append({"text": text, "url": url})
    if current["title"] or current["links"]:
        sections.append(current)
    return sections


def norm_hash(text: str) -> str:
    """SHA-1 of whitespace-normalized text; for template comparison."""
    return hashlib.sha1(" ".join(text.split()).encode()).hexdigest()[:12]


INSTRUCTION_PATTERNS = [
    # instruction-like language aimed at LLMs, English + Italian
    (r"\byou (are|should|must|can|may)\b", "you_directive"),
    (r"\b(do not|don.t|never|always)\b", "imperative"),
    (r"\b(when (answering|citing|responding)|if (asked|users ask))\b",
     "conditional"),
    (r"\b(please )?(cite|quote|link|attribute|reference)\b", "citation"),
    (r"\b(ai (agents?|assistants?|models?)|llms?|language models?|chatbots?)\b",
     "addresses_ai"),
    (r"\b(non (citare|copiare|riprodurre)|quando (rispondi|citi)|si prega)\b",
     "italian_directive"),
    (r"\b(instructions?|guidelines|usage policy|terms)\b", "policy_words"),
]
# these two alone are weak: prose mentions, not directives
WEAK_SIGNALS = {"addresses_ai", "policy_words"}


def instruction_signals(text: str) -> list[str]:
    """Labels of instruction-like patterns found in the file."""
    low = text.lower()
    return sorted({label for rx, label in INSTRUCTION_PATTERNS
                   if re.search(rx, low)})


def text_similarity(a: str, b: str) -> float:
    """Jaccard on word 5-shingles, whitespace-normalized and lowercased.
    Measures content overlap, not formatting: catches pairs where llms.txt
    and llms-full.txt are the same text with different markdown spacing
    (facile.it writes '#Title' in one file and '# Title' in the other)."""
    def shingles(t):
        # strip markdown line prefixes (#, >, list bullets) before tokenizing
        lines = (re.sub(r"^[#>*\-\s]+", "", ln) for ln in t.lower().splitlines())
        w = " ".join(lines).split()
        if len(w) <= 5:
            return {tuple(w)} if w else set()
        return {tuple(w[i:i + 5]) for i in range(len(w) - 4)}
    sa, sb = shingles(a), shingles(b)
    return len(sa & sb) / len(sa | sb) if sa | sb else 1.0


def validate_tdmrep(status: int, content_type: str, body: str):
    if status != 200:
        return False, f"status_{status}"
    if looks_like_html(body):
        return False, "soft404_html"
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return False, "invalid_json"
    if not isinstance(data, list):
        return False, "not_array"
    if not all(isinstance(r, dict) and "location" in r for r in data):
        return False, "malformed_rules"
    return True, "ok"


def parse_tdmrep(body: str) -> dict:
    data = json.loads(body)
    root_res = None
    # most generic location = shortest pattern
    for rule in sorted(data, key=lambda r: len(str(r.get("location", "")))):
        if "tdm-reservation" in rule:
            root_res = int(rule["tdm-reservation"])
            break
    return {
        "n_rules": len(data),
        "reservation_root": root_res,
        "has_policy": int(any("tdm-policy" in r for r in data)),
    }


def tdm_headers(headers: dict) -> bool:
    return any(k.lower().startswith("tdm-") for k in headers)


TDM_META_RX = re.compile(
    r'<meta[^>]+name\s*=\s*["\']tdm-(?:reservation|policy)["\']', re.I)


def tdm_meta(html_body: str) -> bool:
    """TDMRep's third channel: <meta name="tdm-reservation"> in the HTML."""
    return bool(TDM_META_RX.search(html_body))
