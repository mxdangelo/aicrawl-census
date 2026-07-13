"""Stage 6 — Generate the visual study (report.html) from census.db.

Usage: python run_report.py  (requires the dw_* tables: run run_dw.py first)
Self-contained HTML: no external assets, light/dark via prefers-color-scheme,
hover tooltips on every mark, a table view per figure (accessibility twin).
Palette: validated reference instance (see design notes in the report).
"""
import html
import json
import math
import sqlite3
from datetime import date

import config

# ---------------------------------------------------------------- palette
# Categorical slots 1-2 (validated: light CVD dE 73.6, dark 69.8).
# Aqua is sub-3:1 on the light surface -> relief: direct labels + table views.
LIGHT = {"s1": "#2a78d6", "s2": "#1baf7a", "gray": "#b5b3ab"}
DARK = {"s1": "#3987e5", "s2": "#199e70", "gray": "#5a5952"}
SEQ_LIGHT = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
SEQ_DARK = list(reversed(SEQ_LIGHT))  # dark mode: near-zero anchors to the dark surface
ORD_LIGHT = ["#86b6ef", "#2a78d6", "#104281"]  # validated --ordinal
ORD_DARK = ["#184f95", "#3987e5", "#9ec5f4"]

KEY_CRAWLERS = ["GPTBot", "ClaudeBot", "CCBot", "Google-Extended",
                "PerplexityBot", "Bytespider", "Applebot-Extended",
                "meta-externalagent"]

E = html.escape


# ---------------------------------------------------------------- svg helpers
def rbar(x, y, w, h, r=4):
    """Horizontal bar path: 4px rounded data-end, square at the baseline."""
    r = min(r, max(0.5, w / 2), h / 2)
    return (f"M{x:.1f},{y:.1f} h{w - r:.1f} a{r},{r} 0 0 1 {r},{r} "
            f"v{h - 2 * r:.1f} a{r},{r} 0 0 1 -{r},{r} h-{w - r:.1f} z")


def svg_open(w, h):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" '
            f'style="width:100%;height:auto;display:block">')


def figure(fid, title, caption, svg, table_html, legend_html=""):
    return f"""
<figure class="card" id="{fid}">
  <h3>{E(title)}</h3>
  {legend_html}
  {svg}
  <figcaption>{caption}</figcaption>
  <details class="tv"><summary>Table view</summary>{table_html}</details>
</figure>"""


def table(headers, rows):
    th = "".join(f"<th>{E(h)}</th>" for h in headers)
    trs = "".join(
        "<tr>" + "".join(f"<td>{E(str(c))}</td>" for c in r) + "</tr>"
        for r in rows)
    return f'<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


def legend(items):
    """items: [(kind 'rect'|'line'|'dot', css color var/hex, label)]"""
    spans = []
    for kind, color, label in items:
        shape = {"rect": "leg-rect", "line": "leg-line", "dot": "leg-dot"}[kind]
        spans.append(f'<span class="leg"><span class="{shape}" '
                     f'style="background:{color}"></span>{E(label)}</span>')
    return '<div class="legend">' + "".join(spans) + "</div>"


def hbar_chart(rows, vmax, w=760, bar_h=18, gap=10, label_w=170,
               color_of=None, val_fmt=str):
    """rows: [(label, value, series)] -> horizontal bars, value at the tip."""
    x0, top = label_w, 6
    plot_w = w - x0 - 64
    h = top + len(rows) * (bar_h + gap) + 8
    out = [svg_open(w, h)]
    out.append(f'<line x1="{x0}" y1="{top - 4}" x2="{x0}" y2="{h - 6}" '
               f'class="axis"/>')
    for i, (label, value, series) in enumerate(rows):
        y = top + i * (bar_h + gap)
        bw = plot_w * value / vmax if vmax else 0
        color = color_of(series) if color_of else "var(--s1)"
        tt = f"{label}\n{val_fmt(value)}"
        out.append(f'<text x="{x0 - 8}" y="{y + bar_h / 2 + 4}" '
                   f'class="lab" text-anchor="end">{E(label)}</text>')
        out.append(f'<path d="{rbar(x0, y, max(bw, 1), bar_h)}" fill="{color}" '
                   f'class="mark" tabindex="0" data-tt="{E(tt)}"/>')
        out.append(f'<text x="{x0 + max(bw, 1) + 8}" y="{y + bar_h / 2 + 4}" '
                   f'class="val">{E(val_fmt(value))}</text>')
    out.append("</svg>")
    return "".join(out)


def stacked_bar(segments, total, w=760, bar_h=26, label_w=170, y_label=""):
    """One horizontal 100%-stacked bar. segments: [(label, count, color)].
    2px surface gap between fills; interior labels only when they fit."""
    x0 = label_w
    plot_w = w - x0 - 16
    h = bar_h + 12
    out = [svg_open(w, h)]
    out.append(f'<text x="{x0 - 8}" y="{bar_h / 2 + 8}" class="lab" '
               f'text-anchor="end">{E(y_label)}</text>')
    x = x0
    for i, (label, count, color) in enumerate(segments):
        seg_w = plot_w * count / total if total else 0
        gap_w = 2 if i < len(segments) - 1 else 0
        draw_w = max(seg_w - gap_w, 0.5)
        pct = 100 * count / total if total else 0
        tt = f"{label}\n{count} domains ({pct:.1f}%)"
        rx = 4 if i == len(segments) - 1 else 0
        if rx:
            out.append(f'<path d="{rbar(x, 4, draw_w, bar_h)}" fill="{color}" '
                       f'class="mark" tabindex="0" data-tt="{E(tt)}"/>')
        else:
            out.append(f'<rect x="{x:.1f}" y="4" width="{draw_w:.1f}" '
                       f'height="{bar_h}" fill="{color}" class="mark" '
                       f'tabindex="0" data-tt="{E(tt)}"/>')
        est_text_w = (len(label) + 6) * 7
        if draw_w > est_text_w + 16:  # interior label only when it fits
            ink = "#ffffff" if color in (LIGHT["s1"], ORD_LIGHT[1], ORD_LIGHT[2]) \
                else "var(--ink1)"
            out.append(f'<text x="{x + draw_w / 2:.1f}" y="{bar_h / 2 + 8}" '
                       f'class="segl" fill="{ink}" text-anchor="middle">'
                       f'{E(label)} · {count}</text>')
        x += seg_w
    out.append("</svg>")
    return "".join(out)


def heatmap(row_labels, col_labels, values, denom, w=760):
    """values[r][c] = blocked count; denom[r] = sector size. Sequential ramp."""
    label_w, top = 170, 30
    cw = (w - label_w - 10) / len(col_labels)
    ch = 32
    h = top + len(row_labels) * (ch + 2) + 6
    vmax = max((values[r][c] / denom[r] for r in range(len(row_labels))
                for c in range(len(col_labels))), default=1) or 1
    out = [svg_open(w, h)]
    for c, cl in enumerate(col_labels):
        out.append(f'<text x="{label_w + c * cw + cw / 2:.0f}" y="18" '
                   f'class="lab" text-anchor="middle">{E(cl)}</text>')
    peak = (0, 0)
    for r, rl in enumerate(row_labels):
        y = top + r * (ch + 2)
        out.append(f'<text x="{label_w - 8}" y="{y + ch / 2 + 4}" class="lab" '
                   f'text-anchor="end">{E(rl)}</text>')
        for c in range(len(col_labels)):
            share = values[r][c] / denom[r]
            step = 0 if vmax == 0 else min(6, int(share / vmax * 6.999))
            if share > values[peak[0]][peak[1]] / denom[peak[0]]:
                peak = (r, c)
            tt = (f"{rl} × {col_labels[c]}\n{share:.0%} blocked "
                  f"({values[r][c]}/{denom[r]})")
            out.append(f'<rect x="{label_w + c * cw:.1f}" y="{y}" '
                       f'width="{cw - 2:.1f}" height="{ch}" rx="2" '
                       f'class="cell c{step} mark" tabindex="0" '
                       f'data-tt="{E(tt)}"/>')
    # in-cell label on the extreme only (selective direct labeling)
    r, c = peak
    share = values[r][c] / denom[r]
    out.append(f'<text x="{label_w + c * cw + (cw - 2) / 2:.1f}" '
               f'y="{top + r * (ch + 2) + ch / 2 + 4}" class="segl" '
               f'fill="#ffffff" text-anchor="middle">{share:.0%}</text>')
    out.append("</svg>")
    # scale legend
    sw = "".join(f'<span class="sq c{i}"></span>' for i in range(7))
    scale = (f'<div class="scale"><span class="lab-t">0%</span>{sw}'
             f'<span class="lab-t">{vmax:.0%} of sector blocked</span></div>')
    return out, scale, h


# ---------------------------------------------------------------- data
def collect(con):
    q = lambda s, *p: con.execute(s, p).fetchall()
    d = {}
    d["n"] = q("SELECT COUNT(*) FROM site_meta")[0][0]
    d["llms"] = q("SELECT COUNT(*) FROM files WHERE resource='llms' AND present=1")[0][0]
    d["llms_full"] = q("SELECT COUNT(*) FROM files WHERE resource='llms_full' AND present=1")[0][0]
    d["tdmrep"] = q("SELECT COUNT(*) FROM tdmrep_meta "
                    "WHERE valid=1 OR via_header=1 OR via_meta=1")[0][0]
    d["blockers"] = q("SELECT COUNT(DISTINCT domain) FROM verdicts "
                      "WHERE verdict='blocked' AND source='specific'")[0][0]
    d["unobservable"] = q(
        "SELECT COUNT(*) FROM fetches WHERE resource='robots' "
        "AND status IN (0,202,403,429,503)")[0][0]
    d["instructions"] = q("SELECT COUNT(*) FROM llms_meta WHERE has_instructions=1")[0][0]

    # heatmap: sector x crawler specific-block counts
    sectors = [r[0] for r in q(
        """SELECT s.sector FROM site_meta s
           LEFT JOIN verdicts v ON v.domain=s.domain
             AND v.verdict='blocked' AND v.source='specific'
           GROUP BY s.sector
           ORDER BY CAST(COUNT(DISTINCT v.domain) AS REAL)/COUNT(DISTINCT s.domain) DESC""")]
    denom = dict(q("SELECT sector, COUNT(*) FROM site_meta GROUP BY sector"))
    grid = {(r[0], r[1]): r[2] for r in q(
        """SELECT s.sector, v.crawler, COUNT(*) FROM verdicts v
           JOIN site_meta s ON s.domain=v.domain
           WHERE v.verdict='blocked' AND v.source='specific'
           GROUP BY s.sector, v.crawler""")}
    d["sectors"] = sectors
    d["denom"] = [denom[s] for s in sectors]
    d["grid"] = [[grid.get((s, c), 0) for c in KEY_CRAWLERS] for s in sectors]

    # crawler bars (all with >0 blocks), purpose attached
    d["crawler_rows"] = q(
        """SELECT crawler, purpose, SUM(verdict='blocked' AND source='specific')
           FROM verdicts GROUP BY crawler HAVING 3 > 0
           ORDER BY 3 DESC""")
    d["crawler_rows"] = [(c, p, b) for c, p, b in d["crawler_rows"] if b > 0]

    # posture (ordered by restrictiveness)
    d["posture"] = q(
        """WITH b AS (SELECT domain,
             MAX(verdict='blocked' AND source='specific' AND purpose='training') bt,
             MAX(verdict='blocked' AND source='specific' AND purpose='search') bs
           FROM verdicts GROUP BY domain)
           SELECT SUM(bt=0 AND bs=0), SUM(bt=1 AND bs=0), SUM(bt=1 AND bs=1),
                  SUM(bt=0 AND bs=1) FROM b""")[0]

    # decided vs inherited
    d["robots_template"] = q(
        "SELECT COUNT(*) FROM clusters WHERE cluster_size >= 5")[0][0]
    d["llms_generated"] = q(
        """SELECT COUNT(*) FROM llms_meta WHERE valid=1 AND
           (signatures != '' OR COALESCE(full_similarity, 0) >= 0.9)""")[0][0]

    # top clusters with example domains + member signatures
    d["clusters"] = q(
        """SELECT c.cluster_id, c.cluster_size,
                  GROUP_CONCAT(c.domain, ', '),
                  COALESCE((SELECT GROUP_CONCAT(DISTINCT NULLIF(m.signatures,''))
                            FROM robots_meta m JOIN clusters c2 ON c2.domain=m.domain
                            WHERE c2.cluster_id=c.cluster_id), '')
           FROM clusters c GROUP BY c.cluster_id
           ORDER BY c.cluster_size DESC LIMIT 8""")

    # deliberate deciders by sector: bespoke blockers vs hand-written llms
    d["deciders"] = q(
        """SELECT d.sector, COUNT(*) n,
             SUM(CASE WHEN b.blocked=1 AND COALESCE(d.ai_cluster_size,1) < 5
                 THEN 1 ELSE 0 END),
             SUM(d.llms_origin='hand')
           FROM dw_dim_domain d
           LEFT JOIN (SELECT domain_key,
                        MAX(verdict='blocked' AND verdict_source='specific') blocked
                      FROM dw_fact_policy GROUP BY domain_key) b
             USING (domain_key)
           GROUP BY d.sector ORDER BY 3 + 4 DESC""")

    # llms anatomy scatter
    d["scatter"] = q(
        """SELECT m.domain, s.sector, m.n_links, m.n_chars,
                  (m.signatures != '' OR COALESCE(m.full_similarity,0) >= 0.9),
                  m.has_instructions
           FROM llms_meta m JOIN site_meta s ON s.domain=m.domain
           WHERE m.valid=1""")

    # similarity strip
    d["pairs"] = q(
        """SELECT domain, full_similarity FROM llms_meta
           WHERE valid=1 AND has_llms_full=1 ORDER BY full_similarity""")

    # coherence table
    d["coherence"] = q(
        """SELECT v.domain, s.sector,
                  SUM(v.verdict='blocked' AND v.purpose='training'),
                  SUM(v.verdict='blocked' AND v.purpose='search'),
                  m.has_instructions, COALESCE(NULLIF(m.signatures,''),'—')
           FROM verdicts v
           JOIN files f ON f.domain=v.domain AND f.resource='llms' AND f.present=1
           JOIN site_meta s ON s.domain=v.domain
           LEFT JOIN llms_meta m ON m.domain=v.domain
           WHERE v.source='specific'
           GROUP BY v.domain HAVING SUM(v.verdict='blocked') > 0""")
    return d


# ---------------------------------------------------------------- figures
def fig_heatmap(d):
    cols = [c.replace("Applebot-Extended", "Applebot-Ext")
            .replace("meta-externalagent", "meta-external")
            .replace("Google-Extended", "Google-Ext") for c in KEY_CRAWLERS]
    parts, scale, _ = heatmap(d["sectors"], cols, d["grid"], d["denom"])
    tbl = table(["sector", "n"] + KEY_CRAWLERS,
                [[s, d["denom"][i]] + d["grid"][i]
                 for i, s in enumerate(d["sectors"])])
    unob = 100 * d["unobservable"] / d["n"]
    cap = (f"Share of each sector's sampled domains whose robots.txt names and "
           f"blocks the crawler (root path, RFC 9309 semantics). Domains that "
           f"could not be observed ({unob:.0f}%, bot-walled or unreachable) "
           f"count as not blocking, so true shares are lower bounds.")
    return figure("f-heatmap", "Who blocks whom — sector × crawler",
                  cap, "".join(parts), tbl, scale)


def fig_crawlers(d):
    rows = [(c, b, p) for c, p, b in d["crawler_rows"]]
    vmax = max(b for _, b, _ in rows)
    color_of = lambda p: {"training": "var(--s1)", "search": "var(--s2)"}.get(p, "var(--gray)")
    svg = hbar_chart(rows, vmax, color_of=color_of,
                     val_fmt=lambda v: f"{v}")
    leg = legend([("rect", "var(--s1)", "training crawler"),
                  ("rect", "var(--s2)", "search crawler"),
                  ("rect", "var(--gray)", "both/ambiguous")])
    tbl = table(["crawler", "purpose", "domains blocking (specific)"],
                [(c, p, b) for c, p, b in d["crawler_rows"]])
    cap = ("Domains with a specific robots.txt group blocking the crawler at "
           "root. The cliff between training bots (top) and search bots "
           "(bottom) shows sites distinguish the two functions.")
    return figure("f-crawlers", "The training/search cliff", cap, svg, tbl, leg)


def fig_posture(d):
    none, t_only, both, s_only = d["posture"]
    segs = [("no specific AI block", none, "var(--o0)"),
            ("blocks training", t_only, "var(--o1)"),
            ("blocks training + search", both, "var(--o2)")]
    svg = stacked_bar(segs, none + t_only + both, y_label="543 domains")
    leg = legend([("rect", "var(--o0)", "no specific AI block"),
                  ("rect", "var(--o1)", "blocks training only"),
                  ("rect", "var(--o2)", "blocks training + search")])
    tbl = table(["posture", "domains"],
                [("no specific AI block", none),
                 ("blocks training only", t_only),
                 ("blocks training + search", both),
                 ("blocks search only", s_only)])
    cap = (f"Restrictiveness is ordered, so the ramp is ordinal (one hue, "
           f"light → dark). One further domain blocks search bots only "
           f"(excluded from the bar for legibility; it is in the table).")
    return figure("f-posture", "Postures — how far does blocking go",
                  cap, svg, tbl, leg)


def fig_inherited(d):
    r_tpl, r_all = d["robots_template"], d["blockers"]
    l_gen, l_all = d["llms_generated"], d["llms"]
    svg1 = stacked_bar([("shared template", r_tpl, "var(--gray)"),
                        ("bespoke", r_all - r_tpl, "var(--s1)")],
                       r_all, y_label=f"robots.txt AI blocks ({r_all})")
    svg2 = stacked_bar([("plugin-generated", l_gen, "var(--gray)"),
                        ("hand-written", l_all - l_gen, "var(--s1)")],
                       l_all, y_label=f"llms.txt files ({l_all})")
    leg = legend([("rect", "var(--gray)", "inherited (template / plugin)"),
                  ("rect", "var(--s1)", "decided (bespoke / hand-written)")])
    tbl = table(["signal", "inherited", "decided", "total"],
                [("robots.txt AI block", r_tpl, r_all - r_tpl, r_all),
                 ("llms.txt", l_gen, l_all - l_gen, l_all)])
    cap = ("Inherited = robots AI-block shared by a template cluster of ≥5 "
           "domains; llms.txt with a generator signature (Shopify, Yoast, "
           "AIOSEO) or ≥0.9 content similarity between llms.txt and "
           "llms-full.txt (the plugin twin-file pattern). The entire robots "
           "inherited share is one template — Cloudflare's managed robots.txt "
           "(8 of its 25 members still carry the “Managed by Cloudflare” "
           "comment; its members are cross-sector competitors, which rules "
           "out an editorial-group decision). The ≥5 threshold is "
           "conservative: 4-domain single-publisher clusters (e.g. the "
           "Caltagirone dailies) count as decided.")
    return figure("f-inherited", "Decided vs inherited",
                  cap, svg1 + svg2, tbl, leg)


def fig_clusters(d):
    rows, tbl_rows = [], []
    for cid, size, members, sigs in d["clusters"]:
        label = (sigs.split(",")[0] if sigs else f"template {cid[:6]}")
        rows.append((label, size, members))
        tbl_rows.append((label, size, members[:120]))
    vmax = max(s for _, s, _ in rows)
    out = [svg_open(760, len(rows) * 28 + 14)]
    out.append('<line x1="170" y1="2" x2="170" y2="%d" class="axis"/>'
               % (len(rows) * 28 + 8))
    for i, (label, size, members) in enumerate(rows):
        y = 6 + i * 28
        bw = (760 - 170 - 64) * size / vmax
        ex = ", ".join(members.split(", ")[:4])
        tt = f"{label}\n{size} domains\ne.g. {ex}"
        out.append(f'<text x="162" y="{y + 13}" class="lab" '
                   f'text-anchor="end">{E(label)}</text>')
        out.append(f'<path d="{rbar(170, y, max(bw, 1), 18)}" fill="var(--s1)" '
                   f'class="mark" tabindex="0" data-tt="{E(tt)}"/>')
        out.append(f'<text x="{170 + max(bw, 1) + 8}" y="{y + 13}" '
                   f'class="val">{size}</text>')
    out.append("</svg>")
    tbl = table(["attributed template", "domains", "examples"], tbl_rows)
    cap = ("Largest robots.txt AI-block templates (exact hash + near-duplicate "
           "clustering, Jaccard ≥ 0.8). Attribution from generator signatures "
           "in comments where present; hover a bar for example domains.")
    return figure("f-clusters", "Template clusters — the shared robots.txt",
                  cap, "".join(out), tbl)


def fig_deciders(d):
    rows = d["deciders"]
    bar_h, gap, group_gap, label_w, w = 14, 4, 14, 170, 760
    vmax = max(max(bl / n, hl / n) for _, n, bl, hl in rows) * 1.05
    plot_w = w - label_w - 64
    h = 6 + len(rows) * (2 * bar_h + gap + group_gap)
    out = [svg_open(w, h)]
    out.append(f'<line x1="{label_w}" y1="2" x2="{label_w}" y2="{h - 4}" '
               f'class="axis"/>')
    for i, (sector, n, blockers, hand) in enumerate(rows):
        y = 6 + i * (2 * bar_h + gap + group_gap)
        out.append(f'<text x="{label_w - 8}" y="{y + bar_h + 2}" class="lab" '
                   f'text-anchor="end">{E(sector)}</text>')
        for j, (val, color, kind) in enumerate(
                [(blockers, "var(--s1)", "blocks with bespoke rules"),
                 (hand, "var(--s2)", "publishes hand-written llms.txt")]):
            by = y + j * (bar_h + gap)
            share = val / n
            bw = plot_w * share / vmax if vmax else 0
            tt = f"{sector}\n{kind}\n{share:.0%} ({val}/{n})"
            out.append(f'<path d="{rbar(label_w, by, max(bw, 1), bar_h)}" '
                       f'fill="{color}" class="mark" tabindex="0" '
                       f'data-tt="{E(tt)}"/>')
            out.append(f'<text x="{label_w + max(bw, 1) + 6}" '
                       f'y="{by + bar_h - 3}" class="val">{share:.0%}</text>')
    out.append("</svg>")
    leg = legend([("rect", "var(--s1)", "blocks with bespoke robots.txt rules"),
                  ("rect", "var(--s2)", "publishes hand-written llms.txt")])
    tbl = table(["sector", "domains", "bespoke blockers", "hand-written llms.txt"],
                [(s, n, b, hl) for s, n, b, hl in rows])
    cap = ("Share of each sector's domains showing a deliberate decision: an "
           "AI block outside any shared template (bespoke), or an llms.txt "
           "with no generator fingerprint. The two instruments are nearly "
           "disjoint: news decides by blocking, finance decides by offering — "
           "public administration and health barely decide at all.")
    return figure("f-deciders", "Who decides — and with which instrument",
                  cap, "".join(out), tbl, leg)


def fig_scatter(d):
    w, h, pad_l, pad_b, pad_t = 760, 380, 64, 40, 12
    pts = [(dom, sec, l, c, gen, instr) for dom, sec, l, c, gen, instr
           in d["scatter"] if c > 0]
    # both axes log: link counts are as skewed as file sizes
    lx = lambda v: math.log10(max(v, 1))
    xmin_l = lx(1) - 0.05
    xmax_l = max(lx(p[2]) for p in pts) + 0.1
    ys = [math.log10(max(p[3], 50)) for p in pts]
    ymin, ymax = min(ys) - 0.1, max(ys) + 0.15
    sx = lambda v: pad_l + (w - pad_l - 16) * (lx(v) - xmin_l) / (xmax_l - xmin_l)
    sy = lambda v: pad_t + (h - pad_t - pad_b) * (1 - (math.log10(max(v, 50)) - ymin) / (ymax - ymin))
    out = [svg_open(w, h)]
    for yv in (100, 1000, 10000, 100000):
        if ymin <= math.log10(yv) <= ymax:
            out.append(f'<line x1="{pad_l}" y1="{sy(yv):.1f}" x2="{w - 16}" '
                       f'y2="{sy(yv):.1f}" class="grid"/>')
            out.append(f'<text x="{pad_l - 6}" y="{sy(yv) + 4:.1f}" class="lab" '
                       f'text-anchor="end">{yv:,}</text>')
    for xv in (1, 3, 10, 30, 100, 300, 1000):
        if xmin_l <= lx(xv) <= xmax_l:
            out.append(f'<text x="{sx(xv):.1f}" y="{h - 16}" class="lab" '
                       f'text-anchor="middle">{xv}</text>')
    out.append(f'<text x="{(pad_l + w) / 2:.0f}" y="{h - 2}" class="lab" '
               f'text-anchor="middle">links in the file (log)</text>')
    out.append(f'<text x="12" y="{h / 2:.0f}" class="lab" text-anchor="middle" '
               f'transform="rotate(-90 12 {h / 2:.0f})">characters (log)</text>')
    for dom, sec, links, chars, gen, instr in pts:
        color = "var(--gray)" if gen else "var(--s1)"
        kind = "plugin-generated" if gen else "hand-written"
        note = " · has LLM instructions" if instr else ""
        tt = f"{dom} ({sec})\n{links} links · {chars:,} chars\n{kind}{note}"
        cx, cy = sx(links), sy(chars)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{color}" '
                   f'class="dot"/>')
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13" fill="transparent" '
                   f'class="mark" tabindex="0" data-tt="{E(tt)}"/>')
    out.append("</svg>")
    leg = legend([("dot", "var(--s1)", "hand-written"),
                  ("dot", "var(--gray)", "plugin-generated")])
    tbl = table(["domain", "sector", "links", "chars", "origin", "instructions"],
                [(p[0], p[1], p[2], f"{p[3]:,}",
                  "plugin" if p[4] else "hand", "yes" if p[5] else "no")
                 for p in sorted(pts, key=lambda p: -p[3])])
    cap = ("Each dot is a valid llms.txt. Plugin-generated files (gray) cluster "
           "in shape; hand-written ones (blue) spread. Hover for the domain; "
           "the emphasis is on the decided files, so generated ones recede.")
    return figure("f-scatter", "Anatomy of the 42 llms.txt files",
                  cap, "".join(out), tbl, leg)


def fig_similarity(d):
    w, h = 760, 148
    axis_y, pad_l, pad_r = 78, 60, 40
    sx = lambda v: pad_l + (w - pad_l - pad_r) * v
    out = [svg_open(w, h)]
    out.append(f'<line x1="{pad_l}" y1="{axis_y}" x2="{w - pad_r}" '
               f'y2="{axis_y}" class="axis"/>')
    for tick in (0, .25, .5, .75, 1):
        out.append(f'<line x1="{sx(tick):.1f}" y1="{axis_y - 4}" '
                   f'x2="{sx(tick):.1f}" y2="{axis_y + 4}" class="axis"/>')
        out.append(f'<text x="{sx(tick):.1f}" y="{axis_y + 22}" class="lab" '
                   f'text-anchor="middle">{tick:.2f}</text>')
    out.append(f'<text x="{sx(0):.1f}" y="{axis_y + 40}" class="lab">'
               f'← completely different content</text>')
    out.append(f'<text x="{sx(1):.1f}" y="{axis_y + 40}" class="lab" '
               f'text-anchor="end">identical content →</text>')
    hi = [p for p in d["pairs"] if p[1] >= 0.9]
    for dom, sim in d["pairs"]:
        tt = f"{dom}\nllms vs llms-full similarity {sim:.2f}"
        out.append(f'<circle cx="{sx(sim):.1f}" cy="{axis_y}" r="6" '
                   f'fill="var(--s1)" class="dot"/>')
        out.append(f'<circle cx="{sx(sim):.1f}" cy="{axis_y}" r="14" '
                   f'fill="transparent" class="mark" tabindex="0" '
                   f'data-tt="{E(tt)}"/>')
    # selective labels: the two poles of the story
    if hi:
        out.append(f'<text x="{sx(0.98):.1f}" y="{axis_y - 34}" class="lab" '
                   f'text-anchor="end">same file twice ({len(hi)}, plugin)</text>')
        out.append(f'<line x1="{sx(0.98):.1f}" y1="{axis_y - 28}" '
                   f'x2="{sx(0.98):.1f}" y2="{axis_y - 12}" class="grid"/>')
    lo = [p for p in d["pairs"] if p[1] < 0.9]
    if lo:
        mid = lo[len(lo) // 2]
        out.append(f'<text x="{sx(mid[1]):.1f}" y="{axis_y - 34}" class="lab">'
                   f'genuine index + full pair ({len(lo)})</text>')
        out.append(f'<line x1="{sx(mid[1]):.1f}" y1="{axis_y - 28}" '
                   f'x2="{sx(mid[1]):.1f}" y2="{axis_y - 12}" class="grid"/>')
    out.append("</svg>")
    tbl = table(["domain", "similarity (word 5-shingle Jaccard)"],
                [(dom, f"{s:.3f}") for dom, s in d["pairs"]])
    cap = ("Content similarity between a site's llms.txt and llms-full.txt "
           "(Jaccard on word 5-shingles, markdown stripped). Two populations: "
           "plugins that publish the same file under both names, and sites "
           "where -full genuinely expands the index.")
    return figure("f-similarity", "llms.txt vs llms-full.txt — one file or two?",
                  cap, "".join(out), tbl)


def fig_coherence(d):
    def reading(bs, instr, sig):
        if sig != "—":
            return ("⚠ contradiction: robots blocks everything, the platform "
                    "auto-publishes an invitation")
        if instr:
            return "✓ layered: blocks training, instructs on citation"
        return ("✓ layered: blocks training, offers a hand-written index"
                if bs == 0 else
                "✓ layered: blocks crawling, still offers an index")
    rows = [(dom, sec, f"{bt} training / {bs} search",
             "yes" if instr else "no", sig, reading(bs, instr, sig))
            for dom, sec, bt, bs, instr, sig in d["coherence"]]
    tbl = table(["domain", "sector", "bots blocked", "LLM instructions",
                 "generator signature", "reading"], rows)
    cap = ("All domains that both block AI crawlers in robots.txt and publish "
           "llms.txt. The pair is only a contradiction when the two signals "
           "have different authors: a human blocking everything while the "
           "e-commerce platform auto-publishes a catalog invitation (yeppon.it)."
           " When one hand writes both, it is layered strategy: deny model "
           "training, but guide the AI search agents that arrive anyway "
           "(llms.txt speaks at inference time, a layer robots.txt does not "
           "govern).")
    return f"""
<figure class="card" id="f-coherence">
  <h3>The four both-ways domains</h3>
  {tbl}
  <figcaption>{cap}</figcaption>
</figure>"""


# ---------------------------------------------------------------- page
def kpi_row(d):
    n = d["n"]
    tiles = [
        ("llms.txt adoption", f"{100 * d['llms'] / n:.1f}%",
         f"{d['llms']} of {n} domains"),
        ("block ≥1 AI crawler", f"{100 * d['blockers'] / n:.1f}%",
         f"{d['blockers']} domains, specific rules"),
        ("TDMRep adoption", f"{100 * d['tdmrep'] / n:.1f}%",
         f"{d['tdmrep']} domains (file or header)"),
        ("not observable", f"{100 * d['unobservable'] / n:.1f}%",
         f"{d['unobservable']} domains bot-walled/unreachable"),
    ]
    cells = "".join(
        f'<div class="tile"><div class="t-label">{E(l)}</div>'
        f'<div class="t-value">{E(v)}</div>'
        f'<div class="t-sub">{E(s)}</div></div>'
        for l, v, s in tiles)
    return f'<div class="kpis">{cells}</div>'


def hero(d):
    it = 100 * d["tdmrep"] / d["n"]
    fr = 100 * 143 / 250
    w, bh = 560, 22
    sx = lambda v: 220 + (w - 220 - 70) * v / 60
    svg = [svg_open(w, 76)]
    for i, (label, v, color) in enumerate(
            [("France (top 250, 2025)", fr, "var(--gray)"),
             ("Italy (this census)", it, "var(--s1)")]):
        y = 8 + i * (bh + 12)
        svg.append(f'<text x="212" y="{y + bh / 2 + 4}" class="lab" '
                   f'text-anchor="end">{E(label)}</text>')
        bw = max(sx(v) - 220, 2)
        svg.append(f'<path d="{rbar(220, y, bw, bh)}" fill="{color}" '
                   f'class="mark" tabindex="0" '
                   f'data-tt="{E(label)}&#10;{v:.1f}% of domains"/>')
        svg.append(f'<text x="{220 + bw + 8}" y="{y + bh / 2 + 4}" class="val">'
                   f'{v:.1f}%</text>')
    svg.append("</svg>")
    return f"""
<div class="card hero-card">
  <div class="hero-num">{it:.1f}%</div>
  <p class="hero-sub">of Italian domains carry a TDMRep reservation — the EU's
  legal opt-out from text &amp; data mining (Art. 4 CDSM). France's
  publisher-led push reached 57% of its top sites.</p>
  {''.join(svg)}
</div>"""


CSS = """
:root { color-scheme: light dark; }
body { margin:0; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
/* background and ink live on .viz, where the variables are defined —
   on body the var() lookups fail and the OS theme wins over the toggle */
.viz { background: var(--plane); color: var(--ink1); min-height: 100vh; }
.viz {
  --plane:#f9f9f7; --surface:#fcfcfb; --ink1:#0b0b0b; --ink2:#52514e;
  --muted:#898781; --grid:#e1e0d9; --axis:#c3c2b7;
  --border:rgba(11,11,11,.10);
  --s1:#2a78d6; --s2:#1baf7a; --gray:#b5b3ab;
  --o0:#86b6ef; --o1:#2a78d6; --o2:#104281;
  --q0:#cde2fb; --q1:#9ec5f4; --q2:#6da7ec; --q3:#3987e5; --q4:#256abf;
  --q5:#184f95; --q6:#0d366b;
}
@media (prefers-color-scheme: dark) { .viz {
  --plane:#0d0d0d; --surface:#1a1a19; --ink1:#ffffff; --ink2:#c3c2b7;
  --muted:#898781; --grid:#2c2c2a; --axis:#383835;
  --border:rgba(255,255,255,.10);
  --s1:#3987e5; --s2:#199e70; --gray:#8f8d84;
  --o0:#184f95; --o1:#3987e5; --o2:#9ec5f4;
  --q0:#0d366b; --q1:#184f95; --q2:#256abf; --q3:#3987e5; --q4:#6da7ec;
  --q5:#9ec5f4; --q6:#cde2fb;
}}
/* explicit toggle beats the media query (higher specificity) */
.viz[data-theme="light"] { color-scheme: light; }
.viz[data-theme="dark"] { color-scheme: dark; }
.viz[data-theme="light"] {
  --plane:#f9f9f7; --surface:#fcfcfb; --ink1:#0b0b0b; --ink2:#52514e;
  --muted:#898781; --grid:#e1e0d9; --axis:#c3c2b7;
  --border:rgba(11,11,11,.10);
  --s1:#2a78d6; --s2:#1baf7a; --gray:#b5b3ab;
  --o0:#86b6ef; --o1:#2a78d6; --o2:#104281;
  --q0:#cde2fb; --q1:#9ec5f4; --q2:#6da7ec; --q3:#3987e5; --q4:#256abf;
  --q5:#184f95; --q6:#0d366b;
}
.viz[data-theme="dark"] {
  --plane:#0d0d0d; --surface:#1a1a19; --ink1:#ffffff; --ink2:#c3c2b7;
  --muted:#898781; --grid:#2c2c2a; --axis:#383835;
  --border:rgba(255,255,255,.10);
  --s1:#3987e5; --s2:#199e70; --gray:#8f8d84;
  --o0:#184f95; --o1:#3987e5; --o2:#9ec5f4;
  --q0:#0d366b; --q1:#184f95; --q2:#256abf; --q3:#3987e5; --q4:#6da7ec;
  --q5:#9ec5f4; --q6:#cde2fb;
}
.theme-btn { position: absolute; top: 44px; right: 0; font: 12px system-ui;
  color: var(--ink2); background: var(--surface); border: 1px solid
  var(--border); border-radius: 6px; padding: 5px 10px; cursor: pointer; }
header.study { position: relative; }
.wrap { max-width: 860px; margin: 0 auto; padding: 24px 20px 64px; }
header.study { padding: 40px 0 8px; }
h1 { font-size: 28px; line-height:1.25; margin: 0 0 6px; }
.meta { color: var(--ink2); font-size: 14px; margin-bottom: 4px; }
h2 { font-size: 20px; margin: 40px 0 4px; }
h3 { font-size: 15px; margin: 0 0 10px; font-weight: 600; }
p  { line-height: 1.55; color: var(--ink1); }
p.lede { color: var(--ink2); }
.card { background: var(--surface); border: 1px solid var(--border);
  border-radius: 10px; padding: 18px 18px 12px; margin: 16px 0; }
figcaption { color: var(--ink2); font-size: 13px; line-height: 1.5;
  margin-top: 10px; }
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px,1fr));
  gap: 12px; margin: 16px 0; }
.tile { background: var(--surface); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 16px; }
.t-label { font-size: 13px; color: var(--ink2); }
.t-value { font-size: 32px; font-weight: 600; margin: 2px 0; }
.t-sub { font-size: 12px; color: var(--muted); }
.hero-card { padding: 22px; }
.hero-num { font-size: 52px; font-weight: 650; line-height: 1; }
.hero-sub { color: var(--ink2); font-size: 14px; max-width: 560px; }
text.lab { font-size: 12px; fill: var(--muted); }
text.val { font-size: 12px; fill: var(--ink2); font-variant-numeric: tabular-nums; }
text.segl { font-size: 12px; font-weight: 600; }
.lab-t { font-size: 12px; color: var(--muted); }
line.grid { stroke: var(--grid); stroke-width: 1; }
line.axis { stroke: var(--axis); stroke-width: 1; }
.cell { }
.c0{fill:var(--q0)} .c1{fill:var(--q1)} .c2{fill:var(--q2)} .c3{fill:var(--q3)}
.c4{fill:var(--q4)} .c5{fill:var(--q5)} .c6{fill:var(--q6)}
.sq { width: 22px; height: 12px; display: inline-block; border-radius: 2px; }
.sq.c0{background:var(--q0)} .sq.c1{background:var(--q1)}
.sq.c2{background:var(--q2)} .sq.c3{background:var(--q3)}
.sq.c4{background:var(--q4)} .sq.c5{background:var(--q5)}
.sq.c6{background:var(--q6)}
.scale { display: flex; align-items: center; gap: 3px; margin: 2px 0 10px; }
.scale .lab-t { margin: 0 6px; }
.dot { stroke: var(--surface); stroke-width: 2; pointer-events: none; }
.mark { transition: filter .1s; outline: none; }
.mark:hover, .mark:focus { filter: brightness(1.12); }
.legend { display: flex; gap: 16px; flex-wrap: wrap; margin: 0 0 10px; }
.leg { display: inline-flex; align-items: center; gap: 6px; font-size: 12px;
  color: var(--ink2); }
.leg-rect { width: 12px; height: 12px; border-radius: 3px; display:inline-block; }
.leg-dot { width: 10px; height: 10px; border-radius: 50%; display:inline-block; }
.leg-line { width: 14px; height: 2px; display:inline-block; }
details.tv { margin-top: 10px; }
details.tv summary { font-size: 12px; color: var(--muted); cursor: pointer; }
table { border-collapse: collapse; width: 100%; font-size: 13px; margin-top: 8px; }
th { text-align: left; color: var(--ink2); font-weight: 600; }
th, td { padding: 5px 10px 5px 0; border-bottom: 1px solid var(--grid); }
td { font-variant-numeric: tabular-nums; }
.tt { position: fixed; pointer-events: none; background: var(--ink1);
  color: var(--surface); font-size: 12px; line-height: 1.45;
  padding: 7px 10px; border-radius: 6px; white-space: pre-line;
  max-width: 320px; opacity: 0; transition: opacity .08s; z-index: 10; }
.tt strong { font-size: 13px; }
.methods p, .design p { font-size: 14px; color: var(--ink2); }
.methods li, .design li { font-size: 14px; color: var(--ink2);
  line-height: 1.55; }
footer { color: var(--muted); font-size: 12px; margin-top: 48px; }
@media print { .tt { display:none } }
"""

JS = """
(function () {
  var tt = document.createElement('div');
  tt.className = 'tt';
  document.querySelector('.viz').appendChild(tt);
  function show(el, x, y) {
    tt.textContent = el.getAttribute('data-tt') || '';
    tt.style.opacity = '1';
    var pad = 14, r = tt.getBoundingClientRect();
    var left = x + pad, top = y + pad;
    if (left + r.width > window.innerWidth - 8) left = x - r.width - pad;
    if (top + r.height > window.innerHeight - 8) top = y - r.height - pad;
    tt.style.left = left + 'px'; tt.style.top = top + 'px';
  }
  function hide() { tt.style.opacity = '0'; }
  document.querySelectorAll('[data-tt]').forEach(function (el) {
    el.addEventListener('pointermove', function (e) { show(el, e.clientX, e.clientY); });
    el.addEventListener('pointerleave', hide);
    el.addEventListener('focus', function () {
      var r = el.getBoundingClientRect();
      show(el, r.left + r.width / 2, r.top);
    });
    el.addEventListener('blur', hide);
  });
  var root = document.querySelector('.viz');
  var btn = document.getElementById('theme-toggle');
  var modes = ['auto', 'light', 'dark'];
  var cur = 'auto';
  try { cur = localStorage.getItem('census-theme') || 'auto'; } catch (e) {}
  function apply(m) {
    if (m === 'auto') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', m);
    btn.textContent = 'theme: ' + m;
  }
  apply(cur);
  btn.addEventListener('click', function () {
    cur = modes[(modes.indexOf(cur) + 1) % 3];
    apply(cur);
    try { localStorage.setItem('census-theme', cur); } catch (e) {}
  });
})();
"""

METHODS = """
<!-- UNOBSERVABLE is substituted at render time -->
<section class="methods">
<h2>Method</h2>
<p><strong>Sample.</strong> 543 domains in 10 hand-curated sector strata
(news, e-commerce, public administration, banking/insurance, health,
travel/tourism, real estate, publishing/education, telco/utilities,
media/lifestyle), popularity backbone from the Tranco top-1M filtered to .it.
Foreign domain hacks (redd.it, kahoot.it) excluded by construction; every
domain DNS-validated. Sector lists are versioned in
<code>build_sample.py</code>.</p>
<p><strong>Collection.</strong> Five resources per domain (robots.txt,
llms.txt, llms-full.txt, /.well-known/tdmrep.json, homepage), async httpx
with a declared research user-agent, retries with backoff, raw bodies and
headers stored in SQLite for full reproducibility. Domains that answered
with bot-wall responses (403) or TLS-fingerprint tarpits were re-fetched
with a browser-impersonating client (curl_cffi); the <code>client</code>
column records the provenance of every row. UNOBSERVABLE domains remained
unobservable and are reported as such, never as "allows".</p>
<p><strong>Validation.</strong> Presence means status 200 <em>and</em>
structurally valid content: HTML soft-404s, empty bodies and non-markdown
responses are rejected (real-world tolerance: heading markers without the
space, as published by facile.it, are accepted). robots.txt verdicts follow
RFC 9309: most-specific user-agent group, longest-match Allow/Disallow,
Allow wins ties. <em>blocked</em> means the root path is denied;
<em>source</em> separates an explicit specific rule from wildcard inheritance
— "not mentioned" is never counted as a decision.</p>
<p><strong>Limits.</strong> robots.txt measures declared intent, not crawler
behavior. CMS/plugin fingerprints are heuristic (false negatives when
masked). TDMRep is read through all three spec channels (well-known file,
HTTP headers, HTML meta tags). Single snapshot (2026-07-07): no historical
dimension yet.</p>
</section>"""

DESIGN_NOTES = """
<section class="design">
<h2>Design notes</h2>
<p>Every encoding decision below is a rule applied, not a taste:</p>
<ul>
<li><strong>Form before color.</strong> Headline ratios are stat tiles, not
one-bar charts; the France comparison is an emphasis pair (context in gray);
sector × crawler is a magnitude grid → heatmap with one sequential hue;
part-to-whole postures are a single stacked bar — ordered by restrictiveness,
so it wears an ordinal ramp of one hue rather than categorical hues.</li>
<li><strong>Palette validated, not eyeballed.</strong> The categorical pair
(blue = training, aqua = search) passes CVD separation at ΔE 73.6 light /
69.8 dark (target ≥ 12); the ordinal ramps pass monotone-lightness checks in
both modes. Aqua sits below 3:1 contrast on the light surface, which
obligates relief: every bar carries a visible value label and every figure
ships a table view.</li>
<li><strong>Marks.</strong> Bars ≤ 24px with 4px rounded data-ends and square
baselines; 2px surface gaps separate stacked segments (never strokes); dots
carry 2px surface rings; grid and axes are solid hairlines one step off the
surface.</li>
<li><strong>Selective labeling.</strong> Only extremes and story-carriers are
direct-labeled (the heatmap peak, the similarity poles); the axis, tooltip
and table carry the rest. Text never wears a series color.</li>
<li><strong>Interaction that never gates.</strong> Every mark has a hover and
keyboard-focus tooltip with a hit target larger than the mark (13–14px radius
on 5–6px dots); every value shown on hover is also in the figure's table
view. Dark mode is a selected palette — the sequential ramp re-anchors so
near-zero recedes into the dark surface — not an automatic inversion.</li>
</ul>
</section>"""


def main():
    con = sqlite3.connect(config.DB_PATH)
    d = collect(con)
    today = date.today().isoformat()
    n = d["n"]

    body = f"""<div class="viz"><div class="wrap">
<header class="study">
<button id="theme-toggle" class="theme-btn" type="button">theme: auto</button>
<h1>Who's at the door? AI-crawler policies on Italian websites</h1>
<div class="meta">A census of robots.txt, llms.txt and TDMRep across
{n} Italian domains in 10 sectors · snapshot {today}</div>
<p class="lede">Three signals govern how a website meets AI: a technical
convention (robots.txt), an offer of content to language models (llms.txt),
and a legal reservation of text-and-data-mining rights (TDMRep, Art. 4 CDSM).
This study measures all three on a stratified sample of the Italian web —
and asks whether the policies it finds were <em>decided</em> or
<em>inherited from platform defaults</em>.</p>
</header>

{kpi_row(d)}
{hero(d)}

<h2>Who blocks whom</h2>
<p class="lede">News blocks hardest; public administration barely engages.
And across every sector, sites treat model training and AI search as
different questions.</p>
{fig_heatmap(d)}
{fig_crawlers(d)}
{fig_posture(d)}

<h2>Decided or inherited?</h2>
<p class="lede">A policy only means something if someone chose it. Template
clusters and plugin fingerprints separate deliberate choices from platform
defaults.</p>
{fig_inherited(d)}
{fig_clusters(d)}
{fig_deciders(d)}

<h2>Inside llms.txt</h2>
<p class="lede">{d['llms']} domains ({100 * d['llms'] / n:.1f}%) publish a
valid llms.txt — and {d['instructions']} of them go beyond a link catalog,
addressing the model directly with instructions on citation and use.</p>
{fig_scatter(d)}
{fig_similarity(d)}

<h2>When the signals disagree</h2>
{fig_coherence(d)}

{METHODS.replace("UNOBSERVABLE",
    f"{d['unobservable']} ({100 * d['unobservable'] / n:.1f}%)")}
{DESIGN_NOTES}

<footer>Data: census.db (SQLite), pipeline stages 0–6 in this repository.
Every figure is reproducible with <code>python run_report.py</code>.
Benchmarks: TDMRep adoption in France (W3C TDMRep community group
reporting, 2025); global robots.txt measurements — Data Provenance
Initiative, “Consent in Crisis” (2024); HTTP Archive Web Almanac; top-1M
trackers (GPTBot fully blocked on ~10.6% of sites, Aug 2025, vs 9.2% in
this sample). No Italian sector-stratified census predates this one.</footer>
</div></div>
<script>{JS}</script>"""

    page = (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>AI-crawler policies on Italian websites — census '
            f'{today}</title><style>{CSS}</style></head>'
            f'<body>{body}</body></html>')
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(page)
    print(f"report.html written ({len(page):,} bytes).")


if __name__ == "__main__":
    main()
