"""Altair chart builders for the observatory. Data-driven and interactive:
bound dropdowns filter client-side (slice-and-dice) with no hand-written JS.
Each builder takes the tidy policy_facts DataFrame and returns a themed chart.
"""
import altair as alt
import pandas as pd

import theme

# Hide the Vega action menu (the "···" export dropdown) on every chart.
alt.renderers.set_embed_options(actions=False)

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
}


def _crawler_order(df):
    """Fixed x-axis order: crawlers by specific-block volume, descending.
    Computed on the full data so the axis stays stable while filtering."""
    blk = df[(df.verdict == "blocked") & (df.source == "specific")]
    return (blk.groupby("crawler")["n_domains"].sum()
            .sort_values(ascending=False).index.tolist())


def verdict_by_crawler(df, default_source="All"):
    """Normalized verdict mix per crawler, sliceable by sector and source.

    Every domain has exactly one verdict per crawler, so the 100%-stacked bars
    read as 'share of domains' directly. Two dropdowns filter the underlying
    rows before aggregation — the bars re-normalize live."""
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

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            y=alt.Y("crawler:N", sort=_crawler_order(df), title=None,
                    axis=alt.Axis(domain=False, ticks=False)),
            x=alt.X("sum(n_domains):Q", stack="normalize",
                    title="share of domains", axis=alt.Axis(format="%")),
            color=alt.Color(
                "verdict:N",
                scale=alt.Scale(domain=theme.VERDICT_DOMAIN,
                                range=theme.VERDICT_RANGE),
                legend=alt.Legend(title="verdict")),
            tooltip=[alt.Tooltip("crawler:N"), alt.Tooltip("operator:N"),
                     alt.Tooltip("verdict:N"),
                     alt.Tooltip("sum(n_domains):Q", title="domains")],
        )
        .add_params(sector_p, source_p)
        .transform_filter("sector == 'All' || datum.sector == sector")
        .transform_filter("source == 'All' || datum.source == source")
        .properties(width="container", height=520)
    )
    return theme.themed(chart)


def block_by_sector(df, crawler="GPTBot", emphasize="news"):
    """Hero finding: share of each sector that *specifically* blocks the given
    crawler. Emphasis form — the story sector in the accent ink, the rest gray;
    no gridlines, no x-axis (every bar is directly labeled with its %)."""
    g = df[df["crawler"] == crawler].copy()
    g["blk"] = (((g["verdict"] == "blocked") & (g["source"] == "specific"))
                * g["n_domains"])
    agg = g.groupby("sector", as_index=False).agg(
        blk=("blk", "sum"), tot=("n_domains", "sum"))
    agg["pct"] = 100 * agg["blk"] / agg["tot"]
    agg["sector_label"] = agg["sector"].map(SECTOR_LABELS).fillna(agg["sector"])
    agg["pct_label"] = agg["pct"].round().astype(int).astype(str) + "%"

    base = alt.Chart(agg).encode(
        y=alt.Y("sector_label:N", sort="-x", title=None,
                axis=alt.Axis(domain=False, ticks=False)),
        x=alt.X("pct:Q", axis=None,
                scale=alt.Scale(domain=[0, agg["pct"].max() * 1.12])))
    bars = base.mark_bar(cornerRadiusEnd=4, height=20).encode(
        color=alt.condition(f"datum.sector === '{emphasize}'",
                            alt.value(theme.ACCENT), alt.value(theme.BAR_GRAY)))
    labels = base.mark_text(align="left", dx=6, color=theme.INK,
                            fontSize=13).encode(text=alt.Text("pct_label:N"))
    return theme.themed((bars + labels).properties(width="container", height=360))


def offer_by_sector(sig):
    """Offer finding: how many sites in each sector publish an llms.txt, split
    by whether it was hand-written (a decision) or plugin-generated (inherited).
    Absolute counts — the scarcity is the point. Horizontal, sorted by total."""
    d = sig.melt(id_vars=["sector"], value_vars=["llms_hand", "llms_generated"],
                 var_name="origin", value_name="n")
    d["origin"] = d["origin"].map(
        {"llms_hand": "hand-written", "llms_generated": "plugin default"})
    d["ord"] = d["origin"].map({"hand-written": 0, "plugin default": 1})
    d["sector_label"] = d["sector"].map(SECTOR_LABELS).fillna(d["sector"])

    tot = d.groupby("sector_label", as_index=False)["n"].sum()
    order = tot.sort_values("n", ascending=False)["sector_label"].tolist()
    xmax = tot["n"].max() * 1.14
    y = alt.Y("sector_label:N", sort=order, title=None,
              axis=alt.Axis(domain=False, ticks=False))

    bars = alt.Chart(d).mark_bar(cornerRadiusEnd=4, height=20).encode(
        y=y,
        x=alt.X("sum(n):Q", stack=True, axis=None,
                scale=alt.Scale(domain=[0, xmax])),
        color=alt.Color(
            "origin:N",
            scale=alt.Scale(domain=["hand-written", "plugin default"],
                            range=[theme.ACCENT, theme.BAR_GRAY]),
            legend=alt.Legend(title=None)),
        order=alt.Order("ord:Q"),
        tooltip=["sector_label:N", "origin:N",
                 alt.Tooltip("sum(n):Q", title="files")])
    labels = alt.Chart(tot).mark_text(align="left", dx=6, color=theme.INK,
                                      fontSize=13).encode(
        y=alt.Y("sector_label:N", sort=order),
        x=alt.X("n:Q", scale=alt.Scale(domain=[0, xmax])),
        text=alt.Text("n:Q"))
    return theme.themed((bars + labels).properties(width="container", height=340))


def reserve_dotgrid(sig):
    """Reserve finding as a unit chart: one square per site (543), the handful
    that assert the TDMRep legal reservation lit — book publishers/universities
    in ink, news in a mid tone. The rarity reads as an image, not a near-empty
    bar chart."""
    counts = dict(zip(sig["sector"], sig["tdmrep_present"].astype(int)))
    n_pub = counts.get("publishing_education", 0)
    n_news = counts.get("news", 0)
    total = int(sig["n_domains"].sum())
    reserved = n_pub + n_news

    cols = 31
    d = pd.DataFrame({"i": range(total)})
    d["x"] = d["i"] % cols
    d["y"] = d["i"] // cols
    # spread the lit squares across the field (deterministic, not a corner block)
    step = total // reserved
    positions = [k * step + step // 2 for k in range(reserved)]
    cat = {p: ("Publishers & universities" if k < n_pub else "News")
           for k, p in enumerate(positions)}
    d["category"] = d["i"].map(cat).fillna("—")

    return theme.themed(
        alt.Chart(d).mark_square(size=100, cornerRadius=2).encode(
            x=alt.X("x:O", axis=None),
            y=alt.Y("y:O", axis=None, scale=alt.Scale(reverse=True)),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["Publishers & universities", "News", "—"],
                    range=[theme.ACCENT, "#7a776f", "#efeee8"]),
                legend=alt.Legend(
                    title=None, labelLimit=320,
                    values=["Publishers & universities", "News"])),
            tooltip=alt.value(None),
        ).properties(width=620, height=360))
