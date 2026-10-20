"""The headline of each country page: the finding that sets that country apart.

Every story is a rule over the latest rows of all countries. A rule returns a
dict (headline, dek, hero kind, hero sector) or None when the data no longer
supports it; the page then falls back to the block lead. Numbers and ranks come
from the data. Which angle a country gets is an editorial call, recorded in
RULES below; a rule whose claim stops holding in a later snapshot drops out on
its own instead of printing a stale sentence.
"""
import charts

MIN = charts.MIN_SECTOR_SITES


def _label(sector):
    return charts.SECTOR_LABELS.get(sector, sector).lower()


def _block_by_country(facts, sector):
    """{country: (pct, blk, tot)} for one sector, GPTBot named-and-denied."""
    out = {}
    for code, rows in facts.groupby("country"):
        a = charts._block_agg(rows, "GPTBot")
        a = a[(a["sector"] == sector) & (a["tot"] >= MIN)]
        if len(a):
            r = a.iloc[0]
            out[code] = (r["pct"], int(r["blk"]), int(r["tot"]))
    return out


def _offer_by_country(sig):
    out = {}
    for code, rows in sig.groupby("country"):
        out[code] = (rows["llms_hand"].sum() + rows["llms_generated"].sum()) \
            / rows["n_domains"].sum()
    return out


def _reserve_by_country(res):
    return res.groupby("country").size().to_dict()


def block_press(country, facts, sig, res):
    """Germany: news and media block more than in any other country."""
    news = _block_by_country(facts, "news")
    media = _block_by_country(facts, "media_lifestyle")
    if not all(country in d and d[country][0] == max(v[0] for v in d.values())
               for d in (news, media)):
        return None
    low = min(news, key=lambda c: news[c][0])
    return {
        "headline": (f"{news[country][0]:.0f}% of {charts.COUNTRY_ADJ[country]} "
                     f"news sites block GPTBot by name, and "
                     f"{media[country][0]:.0f}% of media sites."),
        "dek": (f"The highest of the five countries for both. At the other end, "
                f"{charts.COUNTRY_NAMES[low]}'s news sites: {news[low][0]:.0f}%."),
        "hero": "block", "sector": "news"}


def block_public(country, facts, sig, res):
    """Spain: public bodies block, where elsewhere almost none do."""
    pa = _block_by_country(facts, "pa")
    if country not in pa or pa[country][1] < 3:
        return None
    mine = pa[country]
    others = [v[0] for c, v in pa.items() if c != country]
    if mine[0] <= max(others):
        return None
    news = _block_by_country(facts, "news").get(country)
    tail = f" The press still leads, at {news[0]:.0f}%." if news else ""
    return {
        "headline": (f"{charts.COUNTRY_ADJ[country]} public bodies block GPTBot: "
                     f"{mine[1]} of {mine[2]} sites."),
        "dek": (f"In the other countries the share runs from {min(others):.0f}% to "
                f"{max(others):.0f}%.{tail} Small numbers: read it as an "
                f"indication."),
        "hero": "block", "sector": "pa"}


def offer_lead(country, facts, sig, res):
    """Italy: the country where llms.txt is most common, led by one sector."""
    shares = _offer_by_country(sig)
    if shares[country] < max(shares.values()):
        return None
    mine = sig[(sig["country"] == country) & (sig["n_domains"] >= MIN)].copy()
    mine["pub"] = mine["llms_hand"] + mine["llms_generated"]
    mine["share"] = mine["pub"] / mine["n_domains"]
    row = mine.sort_values(["share", "llms_hand"], ascending=False).iloc[0]
    hand = ("all written by hand" if row["llms_generated"] == 0
            else f"{int(row['llms_hand'])} written by hand")
    n_llms = int(mine["pub"].sum())
    return {
        "headline": (f"{charts.SECTOR_LABELS[row['sector']]} leads llms.txt in "
                     f"{charts.COUNTRY_NAMES[country]}: {int(row['pub'])} of "
                     f"{int(row['n_domains'])} sites, {hand}."),
        "dek": (f"Across the whole sample {100 * shares[country]:.1f}% of sites "
                f"publish one, the highest of the five countries."),
        "hero": "offer", "sector": row["sector"]}


def reserve_lead(country, facts, sig, res):
    """France: far more sites reserve their rights than anywhere else."""
    counts = _reserve_by_country(res)
    mine = counts.get(country, 0)
    others = [v for c, v in counts.items() if c != country] or [0]
    if mine < 2 * max(others):
        return None
    mine_rows = res[res["country"] == country]
    by_cat = (mine_rows["sector"].map(charts.RESERVE_CATEGORY).fillna("Other")
              .value_counts())
    breakdown = " · ".join(f"{k} {int(v)}" for k, v in by_cat.items())
    top = mine_rows["sector"].value_counts().index[0]
    return {
        "headline": (f"{mine} {charts.COUNTRY_ADJ[country]} sites reserve their "
                     f"rights under TDMRep. No other country has more than "
                     f"{max(others)}."),
        "dek": f"{breakdown}.",
        "hero": "reserve", "sector": top}


def unreadable_sector(country, facts, sig, res):
    """UK: a whole sector our crawler could not read."""
    def cells(rows):
        a = charts._unobserved_agg(rows)
        return a[a["tot"] >= MIN]
    allc = {c: cells(rows) for c, rows in facts.groupby("country")}
    mine = allc[country]
    if mine.empty:
        return None
    row = mine.sort_values("pct", ascending=False).iloc[0]
    best_elsewhere = max((a["pct"].max() for c, a in allc.items()
                          if c != country and len(a)), default=0)
    if row["pct"] < 25 or row["pct"] <= best_elsewhere:
        return None
    return {
        "headline": (f"{int(row['un'])} of {int(row['tot'])} "
                     f"{charts.COUNTRY_ADJ[country]} {row['sector_label'].lower()} "
                     f"sites could not be read."),
        "dek": (f"Their robots.txt stayed out of reach: they refused or did not "
                f"answer our Italian address. Every figure for this sector "
                f"rests on the sites that did."),
        "hero": "unobserved", "sector": row["sector"]}


RULES = {"IT": offer_lead, "FR": reserve_lead, "DE": block_press,
         "ES": block_public, "UK": unreadable_sector}


def block_default(country, facts, sig, res):
    """Fallback, and the original lead: the sector that blocks GPTBot most."""
    df = facts[facts["country"] == country]
    top = charts.top_block_sector(df)
    name = "the press" if top["sector"] == "news" else top["sector_label"].lower()
    verb = "concentrated in" if top["sector"] == "news" else "highest in"
    return {"headline": f"Resistance to AI crawlers is {verb} {name}.",
            "dek": "", "hero": "block", "sector": top["sector"]}


def choose(country, facts, sig, res):
    rule = RULES.get(country)
    return (rule and rule(country, facts, sig, res)) \
        or block_default(country, facts, sig, res)


def hero(story, df, sig, res):
    """(chart, table, csv name, caption) for a story's hero."""
    kind, sector = story["hero"], story["sector"]
    if kind == "offer":
        return (charts.offer_share_by_sector(sig, sector),
                charts.offer_share_table(sig), "llmstxt-share-by-sector.csv",
                "Share of each sector's sites that publish an llms.txt.")
    if kind == "reserve":
        return (charts.reserve_by_sector(sig, res, sector),
                charts.reserve_share_table(sig, res), "tdmrep-by-sector.csv",
                "Share of each sector's sites that reserve rights through TDMRep.")
    if kind == "unobserved":
        return (charts.unobserved_by_sector(df, sector),
                charts.unobserved_table(df), "unreadable-by-sector.csv",
                "Share of each sector's sites whose robots.txt we could not read.")
    return (charts.block_by_sector(df, emphasize=sector), charts.block_table(df),
            "block-by-sector.csv",
            "Share of each sector's sites that block GPTBot *by name*.")
