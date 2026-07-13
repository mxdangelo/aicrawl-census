"""Tests for the critical cases. Usage: python test_parsers.py"""
from censuslib import robots as rb, textfiles as tf

FAILS = []


def check(name, got, expected):
    ok = got == expected
    print(f"{'OK  ' if ok else 'FAIL'} {name}: {got!r}"
          + ("" if ok else f" (expected {expected!r})"))
    if not ok:
        FAILS.append(name)


# --- 1. Specific block ---
r = rb.parse("User-agent: GPTBot\nDisallow: /\n\nUser-agent: *\nDisallow:")
check("specific block GPTBot", rb.verdict_for(r, "GPTBot"),
      ("blocked", "specific", True))
check("ClaudeBot falls to permissive wildcard", rb.verdict_for(r, "ClaudeBot"),
      ("allowed", "wildcard", False))

# --- 2. Wildcard blocks everything, specific exception ---
r = rb.parse("User-agent: *\nDisallow: /\n\nUser-agent: Googlebot\nAllow: /")
check("wildcard blocks unmentioned", rb.verdict_for(r, "GPTBot"),
      ("blocked", "wildcard", False))

# --- 3. Longest-match: specific Allow beats generic Disallow ---
r = rb.parse("User-agent: GPTBot\nDisallow: /\nAllow: /blog/")
check("root stays blocked", rb.verdict_for(r, "GPTBot", "/"),
      ("blocked", "specific", True))
check("longer allow path wins", rb.verdict_for(r, "GPTBot", "/blog/post"),
      ("partial", "specific", True))

# --- 4. Length tie: Allow wins ---
r = rb.parse("User-agent: GPTBot\nDisallow: /a\nAllow: /a")
check("tie -> allow", rb.verdict_for(r, "GPTBot", "/a")[0], "partial")

# --- 5. Case-insensitive and multi-agent group ---
r = rb.parse("user-agent: gptbot\nuser-agent: ClaudeBot\ndisallow: /")
check("case-insensitive", rb.verdict_for(r, "GPTBot")[0], "blocked")
check("multi-agent same group", rb.verdict_for(r, "ClaudeBot")[0], "blocked")

# --- 6. Empty Disallow = allow ---
r = rb.parse("User-agent: GPTBot\nDisallow:")
check("empty disallow", rb.verdict_for(r, "GPTBot"),
      ("allowed", "specific", True))

# --- 7. Partial block ---
r = rb.parse("User-agent: GPTBot\nDisallow: /private/")
check("partial block", rb.verdict_for(r, "GPTBot")[0], "partial")

# --- 8. Wildcards in patterns ---
r = rb.parse("User-agent: GPTBot\nDisallow: /*.pdf$")
check("wildcard pattern spares root", rb.verdict_for(r, "GPTBot")[0],
      "partial")
check("pattern matches pdf", rb.verdict_for(r, "GPTBot", "/doc.pdf")[0],
      "blocked")

# --- 9. ai_block: same hash for same templates, agent order normalized ---
t1 = "User-agent: GPTBot\nUser-agent: CCBot\nDisallow: /"
t2 = "User-agent: CCBot\nUser-agent: GPTBot\nDisallow: /"
_, h1 = rb.ai_block(rb.parse(t1), ["GPTBot", "CCBot"])
_, h2 = rb.ai_block(rb.parse(t2), ["GPTBot", "CCBot"])
check("hash invariant to agent order", h1 == h2, True)

# --- 10. Generator signatures ---
check("cloudflare signature",
      rb.signatures("# Managed by Cloudflare  https://cloudflare.com"),
      ["cloudflare"])

# --- 11. Soft-404 ---
check("soft404 html", tf.validate_llms(200, "text/html",
      "<!DOCTYPE html><html><body>Not found</body></html>")[1], "soft404_html")
check("valid llms", tf.validate_llms(200, "text/plain",
      "# My Site\n\n> Description\n\n## Docs\n- [Home](https://x.it)")[0],
      True)
check("llms not markdown", tf.validate_llms(200, "text/plain",
      "welcome to the site")[1], "not_markdown")

# --- 11b. sloppy markdown: no space after # (facile.it case) ---
check("llms no space after hash", tf.validate_llms(200, "text/plain",
      "#Facile.it\n\n>Italy's price comparison site\n- [x](u)")[0], True)
m = tf.parse_llms("#Site\n>desc\n##A\n- [x](u)")
check("sloppy h1 parsed", m["h1"], "Site")
check("sloppy sections counted", m["n_sections"], 1)

# --- 12. llms parse ---
m = tf.parse_llms("# Site\n\n> Summary\n\n## A\n- [x](u)\n- [y](u)\n## B\n- [z](u)")
check("llms sections", m["n_sections"], 2)
check("llms links", m["n_links"], 3)

# --- 12b. llms sections structure ---
secs = tf.parse_llms_sections("# S\n- [pre](u0)\n## A\n- [x](u1)\n## B\n- [y](u2)")
check("sections structure",
      [(s["title"], len(s["links"])) for s in secs],
      [("", 1), ("A", 1), ("B", 1)])

# --- 12c. robots as_dict round-trip ---
r = rb.parse("User-agent: GPTBot\nDisallow: /\nSitemap: https://x.it/s.xml")
d = rb.as_dict(r)
check("as_dict groups", d["groups"],
      [{"agents": ["gptbot"], "rules": [["disallow", "/"]]}])
check("as_dict other directives", d["other_directives"],
      [["sitemap", "https://x.it/s.xml"]])

# --- 13. norm_hash: whitespace-invariant, content-sensitive ---
check("norm_hash whitespace-invariant",
      tf.norm_hash("# A\n\n- [x](u)") == tf.norm_hash("# A  \n- [x](u)\n"), True)
check("norm_hash differs on content",
      tf.norm_hash("# A") == tf.norm_hash("# B"), False)

# --- 13b. text_similarity: formatting-invariant, content-sensitive ---
check("similarity ignores markdown spacing",
      tf.text_similarity("#Site\n>a b c d e f", "# Site\n> a b c d e f") > 0.8,
      True)
check("similarity low on different text",
      tf.text_similarity("one two three four five six",
                         "seven eight nine ten eleven twelve") == 0.0, True)

# --- 14. instruction signals ---
sig = tf.instruction_signals(
    "# Site\n\nYou should always cite this page when answering.")
check("instructions detected",
      {"you_directive", "imperative", "citation"} <= set(sig), True)
check("plain list has no strong signals",
      [s for s in tf.instruction_signals("# Site\n## Docs\n- [x](u)")
       if s not in tf.WEAK_SIGNALS], [])

# --- 15. tdmrep ---
ok, _ = tf.validate_tdmrep(200, "application/json",
    '[{"location": "/", "tdm-reservation": 1, "tdm-policy": "https://x/p"}]')
check("valid tdmrep", ok, True)
m = tf.parse_tdmrep(
    '[{"location": "/blog", "tdm-reservation": 0},'
    ' {"location": "/", "tdm-reservation": 1}]')
check("tdmrep root = shortest location", m["reservation_root"], 1)
check("tdmrep non-array", tf.validate_tdmrep(200, "", '{"a":1}')[1], "not_array")

# --- 16. tdm meta tags ---
check("tdm meta detected", tf.tdm_meta(
    '<head><meta name="tdm-reservation" content="1"></head>'), True)
check("tdm meta case/quotes", tf.tdm_meta(
    "<META NAME='TDM-Policy' content='https://x/p'>"), True)
check("no false positive on prose", tf.tdm_meta(
    "<p>we support tdm-reservation soon</p>"), False)

print(f"\n{'ALL OK' if not FAILS else f'FAILED: {FAILS}'}")
