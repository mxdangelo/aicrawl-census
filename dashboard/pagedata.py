"""What one country page reads: its current snapshot, and the figures its prose
quotes. Every number on a page comes from here or from charts.py, never from
the page text, so a new snapshot cannot leave a stale sentence behind.

Snapshots are keyed by (snapshot_date, country, sample). A page shows its
country's current sample (the latest version) at its latest date. Trends run on
the per-domain panel instead, restricted to the domains present at every date,
so a change of sample cannot pass for a change of behaviour.
"""
import pathlib

import pandas as pd

DATA = pathlib.Path(__file__).resolve().parent / "data"

# Page order, file name and reader-facing names of each country.
COUNTRIES = {
    "IT": {"page": "index.html", "name": "Italy", "adj": "Italian"},
    "FR": {"page": "fr.html", "name": "France", "adj": "French"},
    "DE": {"page": "de.html", "name": "Germany", "adj": "German"},
    "UK": {"page": "uk.html", "name": "United Kingdom", "adj": "British"},
    "ES": {"page": "es.html", "name": "Spain", "adj": "Spanish"},
}


def _read(name):
    return pd.read_parquet(DATA / f"{name}.parquet")


def current(df, country):
    """Rows of the country's current snapshot: latest sample, latest date."""
    df = df[df["country"] == country]
    sample = df["sample"].max()
    df = df[df["sample"] == sample]
    return df[df["snapshot_date"] == df["snapshot_date"].max()]


class Page:
    """Everything a country page needs, loaded once."""

    def __init__(self, country):
        self.country = country
        self.names = COUNTRIES[country]
        self.facts = current(_read("policy_facts"), country)
        self.sig = current(_read("sector_signals"), country)
        self.reserved = current(_read("reserved_domains"), country)
        self.panel = _read("domain_panel")
        self.snapshot = self.facts["snapshot_date"].iloc[0]
        self.sample = self.facts["sample"].iloc[0]

        self.n_domains = int(self.sig["n_domains"].sum())
        self.n_observed = int(self.sig["observable"].sum())
        self.n_unobserved = self.n_domains - self.n_observed
        self.n_sectors = self.sig["sector"].nunique()
        self.n_crawlers = self.facts["crawler"].nunique()
        self.n_llms = int(self.sig["observable_llms_hand"].sum()
                          + self.sig["observable_llms_generated"].sum())
        self.n_llms_plain = int(self.sig["observable_llms_hand"].sum())
        self.n_reserve = int(self.sig["observable_tdmrep"].sum())

    def pct(self, n, base=None):
        return f"{100 * n / (base or self.n_observed):.1f}%"


def country_nav(active):
    """Links between the country pages and the comparison; the current page is
    plain text, not a link."""
    items = [(c["page"], c["name"], code == active) for code, c in COUNTRIES.items()]
    items.append(("compare.html", "Compare", active == "compare"))
    links = " · ".join(
        f'<span aria-current="page">{name}</span>' if here
        else f'<a href="{page}">{name}</a>' for page, name, here in items)
    return f'<nav class="country-nav" aria-label="Countries">{links}</nav>'


def trend(panel, country):
    """Headline measures over time on a fixed set of sites: the domains present
    at every snapshot date of the country, whatever the sample. Where two
    samples share a date, the later sample's crawl stands for that date.
    Shares are of the panel sites observable at each date. None when the
    country has a single date."""
    p = panel[panel["country"] == country]
    latest = p.groupby("snapshot_date")["sample"].transform("max")
    p = p[p["sample"] == latest]
    dates = sorted(p["snapshot_date"].unique())
    if len(dates) < 2:
        return None
    every = p.groupby("domain")["snapshot_date"].nunique()
    p = p[p["domain"].isin(every[every == len(dates)].index)]
    obs = p[p["observable"] == 1].copy()
    obs["gptbot_named_block"] = ((obs["gptbot_verdict"] == "blocked")
                                 & (obs["gptbot_source"] == "specific"))
    obs["llms"] = obs["llms_origin"] != "none"
    measures = {"gptbot_named_block": "Block GPTBot by name",
                "llms": "Publish an llms.txt",
                "tdmrep_present": "Reserve rights (TDMRep)"}
    g = obs.groupby("snapshot_date")
    rows = []
    for col, label in measures.items():
        n = g[col].sum()
        base = g.size()
        for date in dates:
            rows.append({"snapshot_date": date, "measure": label,
                         "n": int(n[date]), "base": int(base[date]),
                         "share": n[date] / base[date]})
    out = pd.DataFrame(rows)
    out.attrs["n_panel"] = int(p["domain"].nunique())
    return out


def compare(facts, sig):
    """One row per country: the headline shares of its current snapshot, all on
    observable sites, overall and in the two strata the samples were built to
    compare (news, central government)."""
    rows = []
    for code, c in COUNTRIES.items():
        f = current(facts, code)
        f = f[(f["crawler"] == "GPTBot") & (f["source"] != "unobservable")]
        s = current(sig, code)

        def named(sub):
            blk = sub.loc[(sub["verdict"] == "blocked") & (sub["source"] == "specific"),
                          "n_domains"].sum()
            return blk / sub["n_domains"].sum()

        obs = int(s["observable"].sum())
        top = (f[(f["verdict"] == "blocked") & (f["source"] == "specific")]
               .groupby("sector")["n_domains"].sum()
               / f.groupby("sector")["n_domains"].sum()).idxmax()
        rows.append({
            "country": c["name"],
            "top sector": top,
            "central sites": int(f.loc[f["tier"] == "central", "n_domains"].sum()),
            "sites observed": obs,
            "Block GPTBot by name": named(f),
            "… news sites": named(f[f["sector"] == "news"]),
            "… central government": named(f[f["tier"] == "central"]),
            "Publish an llms.txt": (s["observable_llms_hand"].sum()
                                    + s["observable_llms_generated"].sum()) / obs,
            "Reserve rights (TDMRep)": s["observable_tdmrep"].sum() / obs,
            "snapshot": f["snapshot_date"].iloc[0],
        })
    return pd.DataFrame(rows)
