"""Altair chart builders for the observatory. Data-driven and interactive:
bound dropdowns filter client-side (slice-and-dice) with no hand-written JS.
Each builder takes the tidy policy_facts DataFrame and returns a themed chart.
"""
import base64

import altair as alt
import pandas as pd

import theme

# Hide the Vega action menu (the "···" export dropdown) on every chart.
# renderer="svg" is load-bearing, not a preference: the SVG renderer paints
# fill/stroke as attributes, which CSS can re-point for dark mode (see
# theme.scss). The canvas default would bake the light palette into pixels.
alt.renderers.set_embed_options(actions=False, renderer="svg")

# Reader-facing sector names (the data carries database slugs).
SECTOR_LABELS = {
    "news": "News",
    "media_lifestyle": "Media & lifestyle",
    "ecommerce": "E-commerce",
    "health": "Health",
    "real_estate": "Real estate",
    "pa": "Public administration",
    "publishing_education": "Publishing & education",
    "banking_insurance": "Banking & insurance",
    "travel_tourism": "Travel & tourism",
    "telco_utilities": "Telecoms & utilities",
    "betting_gaming": "Betting & gaming",
}


def _observed(df):
    """Policy rows for the sites whose robots.txt we could read. A site that
    blocked us, or answered from another site, has no verdict and stays out of
    every share — counting it as 'allowed' would invent a policy."""
    return df[df["source"] != "unobservable"]


def _crawler_order(df):
    """Fixed x-axis order: crawlers by specific-block volume, descending.
    Computed on the full data so the axis stays stable while filtering."""
    blk = df[(df.verdict == "blocked") & (df.source == "specific")]
    return (blk.groupby("crawler")["n_domains"].sum()
            .sort_values(ascending=False).index.tolist())


def verdict_by_crawler(df, default_source="All"):
    """Verdict mix per crawler, sliceable by sector and source.

    Every domain has exactly one verdict per crawler, so each bar is a whole:
    the segments are shares of the sites in the current slice. The share is
    printed inside each segment (segments under 7% stay bare — no room), so
    the x-axis goes away entirely and nothing reads as a raw count. Counts
    live in the tooltip. Two dropdowns filter the rows before aggregation —
    the bars re-normalize live."""
    df = _observed(df)
    sectors = sorted(df["sector"].unique())
    sector_p = alt.param(
        name="sector", value="All",
        bind=alt.binding_select(
            options=["All"] + sectors,
            labels=["All sectors"] + [SECTOR_LABELS.get(s, s) for s in sectors],
            name="Sector  "))
    source_p = alt.param(
        name="source", value=default_source,
        bind=alt.binding_select(
            options=["All", "specific", "wildcard", "no_robots"],
            labels=["Any rule", "Names the crawler", "Catch-all (*)", "No robots.txt"],
            name="Rule  "))

    # Aggregate inside the spec (after the dropdowns filter) so the printed
    # share re-computes on every slice, exactly like the bar widths.
    base = (
        alt.Chart(df)
        .transform_filter("sector == 'All' || datum.sector == sector")
        .transform_filter("source == 'All' || datum.source == source")
        .transform_aggregate(n="sum(n_domains)",
                             groupby=["crawler", "operator", "verdict"])
        .transform_joinaggregate(tot="sum(n)", groupby=["crawler"])
        .transform_calculate(
            pct="datum.n / datum.tot",
            ord=f"indexof({theme.VERDICT_DOMAIN}, datum.verdict)",
            label="datum.n / datum.tot >= 0.07"
                  " ? format(datum.n / datum.tot, '.0%') : ''")
    )

    y = alt.Y("crawler:N", sort=_crawler_order(df), title=None,
              axis=alt.Axis(domain=False, ticks=False))
    x_kw = dict(stack="zero", axis=None, title=None,
                scale=alt.Scale(domain=[0, 1]))
    x = alt.X("pct:Q", **x_kw)
    x_mid = alt.X("pct:Q", bandPosition=0.5, **x_kw)   # centre text in segment
    order = alt.Order("ord:Q")

    bars = base.mark_bar().encode(
        y=y, x=x, order=order,
        color=alt.Color(
            "verdict:N",
            scale=alt.Scale(domain=theme.VERDICT_DOMAIN,
                            range=theme.VERDICT_RANGE),
            legend=alt.Legend(title=None)),
        tooltip=[alt.Tooltip("crawler:N"), alt.Tooltip("operator:N"),
                 alt.Tooltip("verdict:N"),
                 alt.Tooltip("n:Q", title="domains"),
                 alt.Tooltip("pct:Q", title="share", format=".1%")])
    # Labels sit inside their segment; on the ink-dark "blocked" block they
    # have to invert to stay legible.
    labels = base.mark_text(fontSize=12, baseline="middle").encode(
        y=y, x=x_mid, order=order,
        text=alt.Text("label:N"),
        color=alt.condition("datum.verdict === 'blocked'",
                            alt.value(theme.PAPER), alt.value(theme.ACCENT)))

    chart = ((bars + labels)
             .add_params(sector_p, source_p)
             .properties(width="container", height=520))
    return theme.themed(chart)


def _block_agg(df, crawler):
    """Per-sector share of sites that *specifically* block the given crawler.
    Shared by the hero chart and its table view."""
    g = _observed(df)
    g = g[g["crawler"] == crawler].copy()
    g["blk"] = (((g["verdict"] == "blocked") & (g["source"] == "specific"))
                * g["n_domains"])
    agg = g.groupby("sector", as_index=False).agg(
        blk=("blk", "sum"), tot=("n_domains", "sum"))
    agg["pct"] = 100 * agg["blk"] / agg["tot"]
    agg["sector_label"] = agg["sector"].map(SECTOR_LABELS).fillna(agg["sector"])
    return agg


def block_by_sector(df, crawler="GPTBot", emphasize="news"):
    """Hero finding: share of each sector that *specifically* blocks the given
    crawler. Emphasis form — the story sector in the accent ink, the rest gray;
    no gridlines, no x-axis (every bar is directly labeled with its %). The
    tooltip carries the counts behind the percentage."""
    agg = _block_agg(df, crawler)
    agg["pct_label"] = agg["pct"].round().astype(int).astype(str) + "%"

    base = alt.Chart(agg).encode(
        y=alt.Y("sector_label:N", sort="-x", title=None,
                axis=alt.Axis(domain=False, ticks=False)),
        x=alt.X("pct:Q", axis=None,
                scale=alt.Scale(domain=[0, agg["pct"].max() * 1.12])))
    bars = base.mark_bar(cornerRadiusEnd=4, height=20).encode(
        color=alt.condition(f"datum.sector === '{emphasize}'",
                            alt.value(theme.ACCENT), alt.value(theme.BAR_GRAY)),
        tooltip=[alt.Tooltip("sector_label:N", title="sector"),
                 alt.Tooltip("blk:Q", title=f"blocks {crawler} by name"),
                 alt.Tooltip("tot:Q", title="sites observed"),
                 alt.Tooltip("pct:Q", title="share (%)", format=".1f")])
    labels = base.mark_text(align="left", dx=6, color=theme.INK,
                            fontSize=13).encode(text=alt.Text("pct_label:N"))
    return theme.themed((bars + labels).properties(width="container", height=360))


def offer_by_sector(sig):
    """Offer finding: among the sites that publish an llms.txt at all, how many
    wrote it by hand (a decision) versus inherited it from a plugin.

    Grouped, not stacked: this section asks how much adoption was a decision, so
    the two quantities are the finding and the sector total is the confusing
    third number. Grouping shows the two and drops the total. Each bar carries
    its count just past its end, so every value stays legible down to 1.

    Positions are computed, not left to a band+offset scale: an offset scale
    always reserves a slot for the missing origin, so a sector with one bar
    lands off-center in its lane. Here each lane is one unit tall; a lone bar
    sits on the lane center, a pair straddles it by ±OFF. Dividers are explicit
    rules between lanes only — none above the first lane or below the last."""
    OFF = 0.2                       # half-gap between the two bars of a sector
    d = sig.melt(id_vars=["sector"], value_vars=["llms_hand", "llms_generated"],
                 var_name="origin", value_name="n")
    d["origin"] = d["origin"].map(
        {"llms_hand": "hand-written", "llms_generated": "plugin default"})
    d["sector_label"] = d["sector"].map(SECTOR_LABELS).fillna(d["sector"])

    tot = d.groupby("sector_label", as_index=False)["n"].sum()
    order = tot.sort_values("n", ascending=False)["sector_label"].tolist()
    lane = {name: i for i, name in enumerate(order)}     # 0 = top lane
    n_lanes = len(order)

    THICK = 0.14                    # bar thickness, in lane units
    bar = d[d["n"] > 0].copy()
    bar["lane"] = bar["sector_label"].map(lane)
    # How many bars this sector actually has — one bar centers, two straddle.
    pair = bar.groupby("lane")["origin"].transform("size").eq(2)
    sign = bar["origin"].map({"hand-written": -1, "plugin default": 1})
    bar["yc"] = bar["lane"] + sign * OFF * pair          # lone bar: +0 → centered
    # Thickness is an explicit vertical span (y..y2) so the bar is horizontal —
    # x alone is the length. A continuous y with no span makes a vertical bar.
    bar["y0"] = bar["yc"] - THICK / 2
    bar["y1"] = bar["yc"] + THICK / 2
    bar["x0"] = 0                   # y2 ranges the bar, so x needs a span too

    origin_domain = ["hand-written", "plugin default"]
    y_scale = alt.Scale(domain=[n_lanes - 0.5, -0.5])   # lane 0 at top
    x_scale = alt.Scale(domain=[0, d["n"].max() * 1.12])   # headroom for labels
    x = alt.X("x0:Q", axis=None, title=None, scale=x_scale)
    color = alt.Color(
        "origin:N",
        scale=alt.Scale(domain=origin_domain, range=[theme.ACCENT, theme.BAR_GRAY]),
        legend=alt.Legend(title=None))

    # Divider rules sit between lanes: at 0.5, 1.5, … n-1.5 — never at an edge.
    rules = pd.DataFrame({"y": [i + 0.5 for i in range(n_lanes - 1)]})
    dividers = alt.Chart(rules).mark_rule(
        color=theme.GRID, strokeWidth=1).encode(
        y=alt.Y("y:Q", scale=y_scale, axis=None))

    bars = alt.Chart(bar).mark_bar(cornerRadiusEnd=2).encode(
        y=alt.Y("y0:Q", scale=y_scale, axis=None),
        y2="y1:Q", x=x, x2="n:Q", color=color,
        tooltip=["sector_label:N", "origin:N", alt.Tooltip("n:Q", title="files")])
    counts = alt.Chart(bar).mark_text(
        align="left", dx=4, fontSize=11, color=theme.INK, baseline="middle").encode(
        y=alt.Y("yc:Q", scale=y_scale, axis=None),
        x=alt.X("n:Q", scale=x_scale, axis=None), text=alt.Text("n:Q"))
    # Fixed width: "container" is not honoured inside an hconcat, and the page
    # already carries a fixed-width chart (reserve). Names + plot fit the column.
    plot = (dividers + bars + counts).properties(width=520, height=430)

    # Sector names as their own left column, sharing the lane scale so rows line
    # up. A dedicated text panel sidesteps the layered-axis label-space problems
    # of the manual y layout — the panel reserves its own width cleanly.
    names = pd.DataFrame({"i": range(n_lanes), "name": order})
    name_col = alt.Chart(names).mark_text(
        align="right", baseline="middle", fontSize=13, color=theme.INK).encode(
        y=alt.Y("i:Q", scale=y_scale, axis=None),
        x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[0, 1])),
        text="name:N").transform_calculate(x="1").properties(width=150, height=430)

    return theme.themed(
        alt.hconcat(name_col, plot, spacing=10)
        .configure_concat(spacing=10))


# Reserve views group the reserving sectors into two reader-facing categories.
RESERVE_CATEGORY = {
    "publishing_education": "Publishers & universities",
    "news": "News",
}


def signal_cards(df, sig, reserved, crawler="GPTBot"):
    """The three signals as the page's routing layer: one card each, carrying
    the headline figure and linking to its section. This is the 'overview'
    step — the whole observatory in three numbers, before any chart.

    Reserve reads as a count, not a share, on purpose: eight sites is a
    countable handful and rounding it to 1.5% buries the finding.

    All figures come from the data — the page's prose does not."""
    total = int(sig["n_domains"].sum())
    agg = _block_agg(df, crawler)
    blocked = 100 * agg["blk"].sum() / agg["tot"].sum()
    offer = 100 * (sig["llms_hand"].sum() + sig["llms_generated"].sum()) / total

    cards = [
        ("block", f"{blocked:.1f}%", f"block {crawler} by name",
         "robots.txt rules that shut a named AI crawler out."),
        ("offer", f"{offer:.1f}%", "publish an llms.txt",
         "A file that offers models a curated view of the site."),
        ("reserve", f"{len(reserved)}", f"of {total} reserve rights",
         "TDMRep — the only signal with legal weight in the EU."),
    ]
    items = "".join(
        f'<a class="signal-card" href="#{anchor}">'
        f'<span class="signal-figure">{figure}</span>'
        f'<span class="signal-what">{what}</span>'
        f'<span class="signal-note">{note}</span></a>'
        for anchor, figure, what, note in cards)
    return f'<nav class="signal-cards" aria-label="The three signals">{items}</nav>'


def reserve_stat(sig, reserved):
    """Reserve finding as a single number, not a chart: eight sites out of the
    sample is too little to plot — any chart of it is a near-empty field the
    reader has to decode. The figure states it, the table below names the
    sites. Computed from the data so it can't go stale."""
    total = int(sig["n_domains"].sum())
    n = len(reserved)
    by_cat = (reserved["sector"].map(RESERVE_CATEGORY).fillna("Other")
              .value_counts())
    breakdown = " · ".join(f"{cat} {int(c)}" for cat, c in by_cat.items())
    if "Other" not in by_cat:
        breakdown += " · every other sector 0"
    return (
        '<div class="statblock">'
        f'<p class="stat-figure"><span class="stat-number">{n}</span>'
        f'<span class="stat-unit">of {total} sites</span></p>'
        f'<p class="stat-note">{breakdown}</p>'
        '</div>'
    )


# --- Table views -----------------------------------------------------------
# One table per chart, same data, reachable without hovering (accessibility).


def table_html(t, filename):
    """A table view plus its own download. The CSV is embedded as a data URI —
    the page stays a single self-contained file, so the download works from
    `file://`, from GitHub Pages, and offline, with no endpoint to maintain.

    The numbers come from the same builders the charts use, so what is
    downloaded is exactly what is on screen."""
    csv = t.to_csv(index=False)
    href = ("data:text/csv;charset=utf-8;base64,"
            + base64.b64encode(csv.encode("utf-8")).decode("ascii"))
    return (
        f'<div class="table-actions">'
        f'<a class="download-csv" href="{href}" download="{filename}">'
        f'Download CSV</a></div>'
        + t.to_html(index=False, classes="table table-sm", border=0)
    )


def block_table(df, crawler="GPTBot"):
    agg = _block_agg(df, crawler).sort_values("pct", ascending=False)
    return pd.DataFrame({
        "Sector": agg["sector_label"],
        f"Blocks {crawler} by name": agg["blk"].astype(int),
        "Sites observed": agg["tot"].astype(int),
        "Share": agg["pct"].map("{:.1f}%".format),
    })


def verdict_table(df, source="specific"):
    """Verdict counts per crawler on one rule slice — by default 'specific',
    the rules that name the crawler (the chart's opening view)."""
    df = _observed(df)
    g = df if source == "All" else df[df["source"] == source]
    t = (g.pivot_table(index=["crawler", "operator"], columns="verdict",
                       values="n_domains", aggfunc="sum", fill_value=0)
         .reindex(columns=["blocked", "partial", "allowed"], fill_value=0)
         .reset_index()
         .sort_values("blocked", ascending=False))
    t.columns = ["Crawler", "Operator", "Blocked", "Partial", "Allowed"]
    return t


def offer_table(sig):
    t = sig.copy()
    t["total"] = t["llms_hand"] + t["llms_generated"]
    t = t.sort_values(["total", "llms_hand"], ascending=False)
    return pd.DataFrame({
        "Sector": t["sector"].map(SECTOR_LABELS).fillna(t["sector"]),
        "Hand-written": t["llms_hand"].astype(int),
        "Plugin default": t["llms_generated"].astype(int),
        "Total": t["total"].astype(int),
        "Sites in sample": t["n_domains"].astype(int),
    })


def reserve_table(reserved):
    r = reserved.copy()
    r["category"] = r["sector"].map(RESERVE_CATEGORY).fillna("Other")
    r = r.sort_values(["category", "domain"], ascending=[False, True])
    return pd.DataFrame({
        "Site": r["domain"],
        "Who": r["category"],
        "Signals via": r["channels"],
    })


# --- Cross-country comparison ----------------------------------------------
# The parquet tables carry every country; these builders take the rows of one
# snapshot per country (the page picks each country's latest) and put them side
# by side. Shares use observed sites only, like every other chart.

COUNTRY_NAMES = {"IT": "Italy", "FR": "France", "DE": "Germany",
                 "UK": "United Kingdom", "ES": "Spain"}


def _per_country(facts, fn):
    """Concatenate fn(country_rows) over countries, tagging each with its code."""
    parts = []
    for code, rows in facts.groupby("country"):
        part = fn(rows).copy()
        part["country"] = code
        parts.append(part)
    return pd.concat(parts, ignore_index=True)


def country_summary(facts, sig, reserved, crawler="GPTBot"):
    """One row per country: sample size and the three headline shares.

    Block = sites that name `crawler` and deny it the root, over observed
    sites. Offer = llms.txt publishers over the whole sample (the page's own
    definition). Reserve = TDMRep sites over the whole sample; the count rides
    along because a handful of sites is not a rate to round."""
    rows = []
    for code in sorted(facts["country"].unique()):
        agg = _block_agg(facts[facts["country"] == code], crawler)
        s = sig[sig["country"] == code]
        n = int(s["n_domains"].sum())
        n_res = int((reserved["country"] == code).sum())
        n_llms = int(s["llms_hand"].sum() + s["llms_generated"].sum())
        rows.append({
            "country": code, "name": COUNTRY_NAMES.get(code, code),
            "sites": n, "observed": int(agg["tot"].sum()),
            "block_pct": 100 * agg["blk"].sum() / agg["tot"].sum(),
            "offer_n": n_llms, "offer_pct": 100 * n_llms / n,
            "reserve_n": n_res, "reserve_pct": 100 * n_res / n,
        })
    return pd.DataFrame(rows)


def compare_signals(summary, crawler="GPTBot"):
    """The three signals, one small panel each, countries on the same rows.

    Same axis within a panel, free across panels: the three shares differ by an
    order of magnitude. Each bar carries its value; reserve also names the
    count, since 1 site and 53 sites need different words."""
    long = pd.concat([
        summary.assign(signal=f"Block · name {crawler}", pct=summary["block_pct"],
                       label=summary["block_pct"].map("{:.0f}%".format)),
        summary.assign(signal="Offer · publish llms.txt", pct=summary["offer_pct"],
                       label=summary["offer_pct"].map("{:.1f}%".format)),
        summary.assign(signal="Reserve · TDMRep", pct=summary["reserve_pct"],
                       label=summary.apply(
                           lambda r: f"{r.reserve_pct:.1f}% ({r.reserve_n})", axis=1)),
    ], ignore_index=True)
    order = ["Block · name " + crawler, "Offer · publish llms.txt",
             "Reserve · TDMRep"]
    y = alt.Y("name:N", title=None, sort=summary.sort_values(
        "block_pct", ascending=False)["name"].tolist(),
        axis=alt.Axis(domain=False, ticks=False))
    base = alt.Chart(long).encode(
        y=y,
        x=alt.X("pct:Q", axis=None, scale=alt.Scale(domainMin=0, nice=False)))
    bars = base.mark_bar(cornerRadiusEnd=3, height=16, color=theme.BAR_GRAY).encode(
        tooltip=[alt.Tooltip("name:N", title="country"),
                 alt.Tooltip("sites:Q", title="sites in sample"),
                 alt.Tooltip("pct:Q", title="share (%)", format=".2f")])
    text = base.mark_text(align="left", dx=5, color=theme.INK, fontSize=12).encode(
        text="label:N")
    # Headroom for the value labels: an invisible mark 1.45x the panel's max
    # stretches that panel's own scale (the panels' x scales are independent).
    long["room"] = long.groupby("signal")["pct"].transform("max") * 1.45
    room = alt.Chart(long).mark_point(opacity=0).encode(
        y=y, x=alt.X("room:Q", axis=None))
    panels = (bars + text + room).properties(width=200, height=170).facet(
        column=alt.Column("signal:N", sort=order, title=None,
                          header=alt.Header(labelFontSize=13, labelColor=theme.INK,
                                            labelAnchor="start")))
    return theme.themed(panels.resolve_scale(x="independent"))


def compare_sector_heatmap(facts, crawler="GPTBot"):
    """Sector × country grid of the share of sites naming `crawler` and denying
    it the root. One mark per cell, value printed in it; empty cell = no
    observed site in that sector. Rows ordered by the all-country mean so the
    press sits on top wherever it leads."""
    cells = _per_country(facts, lambda rows: _block_agg(rows, crawler))
    cells["name"] = cells["country"].map(COUNTRY_NAMES).fillna(cells["country"])
    cells["label"] = cells["pct"].round().astype(int).astype(str) + "%"
    sector_order = (cells.groupby("sector_label")["pct"].mean()
                    .sort_values(ascending=False).index.tolist())
    country_order = (cells.groupby("name")["pct"].mean()
                     .sort_values(ascending=False).index.tolist())
    base = alt.Chart(cells).encode(
        x=alt.X("name:N", sort=country_order, title=None,
                axis=alt.Axis(orient="top", labelAngle=0, domain=False, ticks=False)),
        y=alt.Y("sector_label:N", sort=sector_order, title=None,
                axis=alt.Axis(domain=False, ticks=False)))
    rect = base.mark_rect(stroke="transparent", strokeWidth=2).encode(
        color=alt.Color("pct:Q", legend=None,
                        scale=alt.Scale(range=theme.SEQ, domain=[0, 70], clamp=True)),
        tooltip=[alt.Tooltip("name:N", title="country"),
                 alt.Tooltip("sector_label:N", title="sector"),
                 alt.Tooltip("blk:Q", title=f"block {crawler} by name"),
                 alt.Tooltip("tot:Q", title="sites observed"),
                 alt.Tooltip("pct:Q", title="share (%)", format=".1f")])
    text = base.mark_text(fontSize=13).encode(
        text="label:N",
        color=alt.condition("datum.pct > 38", alt.value(theme.PAPER),
                            alt.value(theme.ACCENT)))
    return theme.themed((rect + text).properties(width="container", height=400))


def compare_table(summary, crawler="GPTBot"):
    return pd.DataFrame({
        "Country": summary["name"],
        "Sites in sample": summary["sites"],
        "Sites observed": summary["observed"],
        f"Block {crawler} by name": summary["block_pct"].map("{:.1f}%".format),
        "Publish llms.txt": summary["offer_n"].astype(str) + " ("
                            + summary["offer_pct"].map("{:.1f}%".format) + ")",
        "Reserve (TDMRep)": summary["reserve_n"].astype(str) + " ("
                            + summary["reserve_pct"].map("{:.1f}%".format) + ")",
    })


def sector_compare_table(facts, crawler="GPTBot"):
    """Heatmap data as a countries-across table (accessibility twin)."""
    cells = _per_country(facts, lambda rows: _block_agg(rows, crawler))
    cells["name"] = cells["country"].map(COUNTRY_NAMES).fillna(cells["country"])
    t = cells.pivot(index="sector_label", columns="name", values="pct")
    t = t.loc[t.mean(axis=1).sort_values(ascending=False).index]
    t = t[t.mean().sort_values(ascending=False).index]
    t = t.map(lambda v: "" if pd.isna(v) else f"{v:.1f}%")
    t.insert(0, "Sector", t.index)
    t.columns.name = None
    return t.reset_index(drop=True)


# --- Country pages: computed prose and navigation --------------------------

COUNTRY_ADJ = {"IT": "Italian", "FR": "French", "DE": "German",
               "UK": "British", "ES": "Spanish"}
# Page file per country; Italy keeps index.html, the original address.
COUNTRY_PAGES = {"IT": "index.html", "FR": "fr.html", "DE": "de.html",
                 "UK": "uk.html", "ES": "es.html"}
MIN_SECTOR_SITES = 15   # a sector smaller than this can't carry a "lead" claim


def top_block_sector(df, crawler="GPTBot"):
    """The sector with the highest share of sites naming `crawler` and denying
    it the root, among sectors with enough observed sites to rank."""
    agg = _block_agg(df, crawler)
    agg = agg[agg["tot"] >= MIN_SECTOR_SITES]
    return agg.sort_values("pct", ascending=False).iloc[0]


def top_offer_sector(sig):
    """One sentence on the sector where llms.txt is most common, with how much
    of it was written by hand. Computed so it can't state another country's
    finding."""
    t = sig[sig["n_domains"] >= MIN_SECTOR_SITES].copy()
    t["pub"] = t["llms_hand"] + t["llms_generated"]
    t["share"] = t["pub"] / t["n_domains"]
    row = t.sort_values(["share", "llms_hand"], ascending=False).iloc[0]
    label = SECTOR_LABELS.get(row["sector"], row["sector"]).lower()
    hand = (f"all {int(row['llms_hand'])} hand-written"
            if row["llms_generated"] == 0
            else f"{int(row['llms_hand'])} of them hand-written")
    return (f"The lead is {label}: {int(row['pub'])} of {int(row['n_domains'])} "
            f"sites ({100 * row['share']:.0f}%), {hand}.")


def country_nav(current):
    """One link per country page plus the comparison. `current` is a country
    code, or "compare"."""
    items = [(c, COUNTRY_NAMES[c], COUNTRY_PAGES[c]) for c in COUNTRY_PAGES]
    items.append(("compare", "Compare", "compare.html"))
    links = "".join(
        f'<a href="{href}"' + (' aria-current="page"' if code == current else "")
        + f'>{label}</a>' for code, label, href in items)
    return f'<nav class="country-nav" aria-label="Countries">{links}</nav>'
