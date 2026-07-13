"""Altair chart builders for the observatory. Data-driven and interactive:
bound dropdowns filter client-side (slice-and-dice) with no hand-written JS.
Each builder takes the tidy policy_facts DataFrame and returns a themed chart.
"""
import altair as alt

import theme


def _crawler_order(df):
    """Fixed x-axis order: crawlers by specific-block volume, descending.
    Computed on the full data so the axis stays stable while filtering."""
    blk = df[(df.verdict == "blocked") & (df.source == "specific")]
    return (blk.groupby("crawler")["n_domains"].sum()
            .sort_values(ascending=False).index.tolist())


def verdict_by_crawler(df):
    """Normalized verdict mix per crawler, sliceable by sector and source.

    Every domain has exactly one verdict per crawler, so the 100%-stacked bars
    read as 'share of domains' directly. Two dropdowns filter the underlying
    rows before aggregation — the bars re-normalize live."""
    sectors = sorted(df["sector"].unique())
    sector_p = alt.param(
        name="sector", value="All",
        bind=alt.binding_select(options=["All"] + sectors, name="Sector  "))
    source_p = alt.param(
        name="source", value="All",
        bind=alt.binding_select(
            options=["All", "specific", "wildcard", "no_robots"],
            name="Source  "))

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("crawler:N", sort=_crawler_order(df), title=None,
                    axis=alt.Axis(labelAngle=-40)),
            y=alt.Y("sum(n_domains):Q", stack="normalize",
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
        .properties(width=680, height=360,
                    title="AI-crawler verdict mix by crawler")
    )
    return theme.themed(chart)
