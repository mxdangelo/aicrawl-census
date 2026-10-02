# How the samples are built

Five country samples and one international list, drawn in October 2026 with the
same rules. The per-country notes in this folder record every borderline call;
this file states the rules they apply.

| File | Country | Domains |
|---|---|---|
| `domains.csv` | Italy | 595 |
| `domains.de.csv` | Germany | 808 |
| `domains.uk.csv` | United Kingdom | 804 |
| `domains.fr.csv` | France | 494 |
| `domains.es.csv` | Spain | 361 |
| `domains.intl.csv` | international hosts | 133 |

`CENSUS_COUNTRY` (IT by default) picks which list and database a pipeline run
uses: `CENSUS_COUNTRY=FR py run_fetch.py` reads `domains.fr.csv` and writes
`census.fr.db`.

## Sample size

Each country's size follows its number of domains in the Tranco top-1M list
under its own TLD, dampened so the largest countries do not dominate:

    n = 595 × (country's Tranco domains ÷ Italy's) ^ 0.5

Italy's 595 is the anchor. Tranco counts on 2026-10-02: Germany 27,352, UK
27,062, Italy 14,836, France 10,245, Spain 5,474. Within a country, sectors take
Italy's proportions. The count is a rough proxy for web size: it undercounts
countries where national sites often use `.com` (likely the UK and Spain).

## Sectors

Eleven: `pa`, `news`, `publishing_education`, `ecommerce`, `travel_tourism`,
`banking_insurance`, `media_lifestyle`, `telco_utilities`, `health`,
`betting_gaming`, `real_estate`. `betting_gaming` is new in this round; it was
the largest group of high-ranked Italian sites the earlier taxonomy left out.
Conventions that recur across countries: sport and tech outlets are `news`;
public research bodies and state lenders are `pa`; postal and parcel services and
price comparators are `telco_utilities`; gambling regulators are `pa`.

`pa` rows carry a `tier`: `central`, `regional` or `local`. City-states (Berlin,
Hamburg, Bremen) and the devolved UK administrations are `regional`. Central
government is large enough to compare across countries (38 to 92 sites per
country). The regional tier is close to a full population where it exists (all
16 Länder) and is reported as counts. The local tier is too small outside Italy
(3 to 10 sites) for cross-country shares.

## Inclusion rules

1. **Audience.** A site belongs to a country if it is aimed mainly at that
   country's audience, whatever its TLD. National sites on `.com`, `.cat`,
   `.eus` or `.gal` qualify.
2. **One host, one country.** robots.txt belongs to a host, so each host is
   counted in exactly one place. A host dedicated to one country belongs to that
   country, whoever owns it: `amazon.fr` is French, `fr.shopping.rakuten.com`
   is French. A redirect to a path on a global host (`ikea.com/fr/`) gives no
   French robots.txt and is out.
3. **Primary market.** A host that serves several countries goes to the
   international list when it competes across those markets more or less on a
   par (`benetton.com`, `lufthansa.com`, `theguardian.com`). It stays national
   when its home market is clearly its main one, even with foreign editions
   (`elpais.com`, `satispay.com`). This is a judgement. The evidence for each
   call — root routing seen from a third country, country-coded `hreflang`
   editions — is in the notes. Neither signal decides alone: the root test
   depends on the vantage (`elpais.com` sends US visitors to `/us/`), and
   `hreflang` lists sister sites on other domains.
4. **Visitors are not markets.** Language editions for foreign visitors on a
   host about the country (tourism boards, museums, hotels, ferries) are national.
5. **Drop rule.** A domain is dropped only if it fails DNS (bare and `www.`), is
   parked, is infrastructure (CDN, DNS, ad-tech, shorteners), or is an alias that
   redirects to another site; the target is kept instead. A site that blocks the
   probe (403, challenge page, timeout, no robots.txt) stays in and is reported
   as not observable. Dropping it would remove the sites that block hardest.
6. **Clusters are capped.** Near-identical sites from one template are kept but
   limited: city halls, regional-press titles of one publisher, Sparkassen,
   German state lotteries, NHS trusts, universities, betting skins of one
   platform. Each country's notes list the caps and what was kept.

## The international list

`domains.intl.csv` holds the hosts excluded by rules 2 and 3, with the company's
`home` country and its `reach` (`europe` or `global`). It is a by-product of the
country drafts, not a designed sample: the largest global platforms are absent
because no country draft surfaced them. Crawling it needs its own selection pass.
The `home` and `reach` values come from general knowledge and are unverified.

## Changes to the Italian sample

The four Italian snapshots up to 2026-10-02 used 543 domains. The current list
keeps 513 of them, removes 30 and adds 82, so trends must be computed on the
domains present in every snapshot.

- **Added (82):** 52 new sites, including the 38 of `betting_gaming`; 22 refills
  for removed rows; 8 target hosts replacing aliases.
- **Moved to the international list (17):** 14 multi-country hosts (fashion
  brands, ITA Airways, lastminute.com, Eni's group site, Moneyfarm, Luxury Estate,
  Docsity), `dovevivo.com` (now Joivy, four countries on one host),
  `helvetia.it` and `nh-hotels.it` (both land on a global host).
- **Replaced by their target host (8):** for example `istruzione.it` by
  `mim.gov.it`, `finecobank.com` by `it.finecobank.com`.
- **Removed (5):** `gaslini.org` (no DNS), `redooc.com` (alias of `virgilio.it`),
  `feltrinelli.it` and `unipolsai.it` (aliases of sites already in the sample),
  `comune.prato.it` (to keep the `pa` count when `cdp.it` moved there).

## Observability and vantage

All fetches run from one Italian address on GARR, the national research network.
Two consequences, both measured:

- **Geo-blocks and geo-redirects.** 23 sites refuse Italian visitors (HTTP 451)
  or send them to their Italian edition. They are almost all betting operators:
  11 of 51 in the UK, 7 of 23 in Spain, 3 of 52 in Germany. The pipeline records
  them as not observable (`blocked` for 451, `offsite` for a redirect), so they
  are never counted as allowing a crawler. UK and Spanish betting figures cover
  only the sites we could observe.
- **Bot protection.** Some sites block any non-browser client. From a US data
  centre, five sites that answer from Italy returned 403, so a commercial vantage
  would not reduce this.

A vantage inside each country (a VPN, cloud functions per region, or colleagues
running the fetch) would recover the geo cases. Tor exits were considered and
not used: the Tor Project is blocked on this network, and betting sites commonly
block Tor exits (not tested).

## Notes files

`notes_it.md`, `notes_fr.md`, `notes_de.md`, `notes_uk.md` and `notes_es.md` are
the working notes of each draft, kept as written: borderline sector calls, alias
resolutions, dropped domains with reasons, clusters kept, sites not observable
from here. Later revisions are appended under REVISION headings, so the last
heading in a file holds the decisions in force.
