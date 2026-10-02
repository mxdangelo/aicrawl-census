# draft notes international sample (2026-10-02)

## What it is
Hosts that belong to no single country: one host serving several countries' markets with no single primary market, or an inherently international audience (international organisations). 300 rows, `domain,sector,home,reach,note`. `home` = ISO country of the company's or body's headquarters (seat for international organisations: CH for WHO, US for the UN, BE for most EU institutions). `reach` = `europe` or `global`. Replaces the earlier 133-row list that the country drafts produced as a by-product.

## Method
Candidates: Tranco global top 5,000 (2026-10-02), minus .it .fr .de .uk .es hosts and anything already in a country list; plus the 133 earlier rows; plus well-known international hosts. About 560 hand-listed, 541 probed (curl_cffi chrome impersonation, https:// then https://www.; DNS on bare and www.; homepage status, final host, html lang, hreflang editions on the same host, robots.txt with a user-agent line). Ranked by Tranco within each sector; unranked hosts last.

Primary-market test: the host is in if Europeans use that host for their own market (country paths or country-coded hreflang editions on one host, an x-default global edition, a country selector) or if the audience is international by nature. It is out if another host carries the country editions and this one is the home edition. Probe signals are evidence, not the test: root routing depends on the vantage.

## Quotas
All 11 sectors at quota: pa 43, news 41, publishing_education 36, ecommerce 30, travel_tourism 27, banking_insurance 25, media_lifestyle 24, telco_utilities 22, health 20, betting_gaming 19, real_estate 13. No shortfall. real_estate had the thinnest pool (19 eligible for 13 slots).

Split: reach global 256, europe 44. Home: US 57, GB 47, DE 31, CH 30, FR 20, NL 14, BE 9, SE 8, ES 6, IT 5, rest 1-4 each across 34 countries.

## Sector calls
- Search engines and portals (google.com, bing.com, msn.com) in media_lifestyle, as the country lists put yahoo and pagesjaunes there.
- pa: UN system, EU institutions and agencies, OECD, Council of Europe, NATO, OSCE-type bodies, ESA, IEA. Development banks and central-bank bodies are pa: worldbank.org, imf.org, eib.org, bis.org, ecb.europa.eu. eib.org and bis.org are in by convention, above rank, in place of reliefweb.int (an OCHA service rather than a body) and unctad.org.
- WHO, ECDC and EMA in pa (international health bodies). msf.org in health (NGO, not intergovernmental). Gavi stays pa-candidate, cut by rank.
- Sport bodies and championships (fifa.com, uefa.com, olympics.com, formula1.com, motogp.com, atptour.com) and score sites (flashscore, sofascore, livescore, fotmob, 365scores) in news. hltv.org (esports) in news.
- Translation and dictionaries (deepl.com, reverso.net, dictionary.cambridge.org) in publishing_education. thomsonreuters.com in publishing_education (legal and professional publishing).
- Pharma groups and health apps/devices (ouraring.com, withings.com, flo.health, helloclue.com) in health. Pharma group sites are corporate, one host for all markets.
- speedtest.net, 17track.net, nordvpn.com and proton.me in telco_utilities (connectivity tools, parcel tracking). The fit is loose; there is no better sector.
- Energy and telecom group sites (shell, bp, totalenergies, eni, iberdrola, telefonica, telekom, orange, vodafone) in telco_utilities: one corporate host for many countries.
- Car and electronics brands with country paths (apple, samsung, dell, hp, lenovo, mi.com, tesla, porsche, volvocars) in ecommerce as multi-country brands.
- Betting prediction and odds sites (forebet.com, oddsportal.com) in betting_gaming, as the countries count trade/affiliate media there.
- Corporate real-estate advisers (cbre, jll, cushmanwakefield, colliers, savills, knightfrank) in real_estate next to listing and rental platforms. Hypothesis: their pages are mostly market reports and listings, close enough to the sector.

## US-headquartered global platforms
US home is not a reason to exclude. Excluded are US-first hosts: the host whose primary market is the US, typically because the other countries have their own hosts. Kept as global (home US): google.com, youtube.com, facebook.com, instagram.com, whatsapp.com, linkedin.com, x.com, netflix.com, apple.com, paypal.com, stripe.com, wikipedia.org, archive.org, arxiv.org, coursera.org and similar. Out as US-first: amazon.com, ebay.com, nytimes-type news, businessinsider.com, wired.com, theweek.com, bloomberg.com, apnews.com, goodhousekeeping.com, yahoo.com, tripadvisor.com, expedia.com, marriott.com, hilton.com, ups.com, accuweather.com, sothebysrealty.com.
Borderline and kept: etsy.com (US its largest market, but one host serves all countries), nike.com, tesla.com, dell.com, hp.com, uber.com, viator.com, westernunion.com, mastercard.com, fandom.com, quora.com, cbre.com, jll.com, cushmanwakefield.com.
Borderline and out: reddit.com (about half its audience in the US, hypothesis), airbnb.com, pinterest.com, flixbus.com, hometogo.com, vinted.com, shein.com (the .com is the US or English edition; the country editions sit on other hosts: hreflang on airbnb.com points to 95 other domains), khanacademy.org (country editions on subdomains).

## UK-first hosts returned
The UK draft moved these here by the host rule. On primary market they are UK: boden.com, riverisland.com, whitestuff.com, newlook.com, mandmdirect.com, tkmaxx.com, lookfantastic.com, selfridges.com, clearpay.com, group.mandg.com, personalinvesting.jpmorgan.com, womanandhome.com, premierinn.com, spectator.com, oddschecker.com, skyscanner.net (the .net is the UK edition), megabus.com (UK and US). They are not in the UK list either, so they are candidates for its next revision.

## Earlier list (133 rows)
41 kept. 23 out on primary market (the 17 UK hosts above, plus businessinsider.com, wired.com, theweek.com, goodhousekeeping.com, yahoo.com) or as an alias (helvetia.com, which now lands on helvetia-baloise.com, unranked). 69 still eligible but below the quota cut by rank, among them most Italian fashion hosts (calzedonia cluster, benetton, yoox, kiko, luisaviaroma, terranova, carpisa), the Spanish airlines and publishers (iberia, vueling, volotea, aireuropa, penguinlibros, tirant, grupo-sm, smartick, cervantes.org), deezer.com, crunchyroll.com, zattoo.com, lastminute.com, ita-airways.com, eurostar.com, joivy.com, docsity.com, moneyfarm.com.

## Aliases (kept the target once)
ec.europa.eu -> commission.europa.eu; springer.com -> link.springer.com; xiaomi.com -> mi.com; degruyter.com -> degruyterbrill.com; worldrugby.org -> world.rugby; helvetia.com -> helvetia-baloise.com; a1.group -> a1.com. None of the targets made the quota cut except commission.europa.eu, link.springer.com and mi.com.

## Other exclusions
- Already in a country list: france24.com, rfi.fr, openedition.org, asos.com, infomaniak.com.
- euractiv.com: redirects to rapporteur.com. Not checked further; out.
- tipico.com: lands on tipico-sportwetten.com, German-first. green-acres.com: lands on green-acres.fr.
- Infrastructure skipped at the Tranco skim: CDNs, DNS, cloud APIs and consoles, ad-tech and tracking, shorteners, registrars, app-store and telemetry hosts. Adult and piracy hosts skipped.
- No candidate failed DNS.
- Not used for relevance: hosts of Asian or Latin American markets with little European use, RT and other EU-sanctioned outlets.

## Clusters kept
- EU institutions on europa.eu: 10 (europa.eu, commission, europarl, consilium, curia, eur-lex, ecb, ema, ecdc, efsa). Cut by the cap: eea, europol, euipo.
- Google 2 (google.com, youtube.com); Meta 3 (facebook, instagram, whatsapp); Microsoft 3 (linkedin, bing, msn); Amazon 1 (twitch.tv; primevideo.com cut by rank).
- Wikimedia 3 (wikipedia, wikimedia, wiktionary); RELX 3 (sciencedirect, elsevier, thelancet); Springer Nature 2 (link.springer.com, nature.com); OUP 2 (global.oup.com, academic.oup.com); Cambridge 2 (cambridge.org, dictionary.cambridge.org).
- Booking Holdings 3 (booking.com, agoda.com, rentalcars.com); IAG 1 (britishairways.com; iberia, vueling cut by rank, aerlingus by the cap); Lufthansa Group 1 (lufthansa.com; swiss, eurowings cut by rank, austrian by the cap).
- Future plc: techradar.com, cyclingnews.com, itpro.com (t3.com and loudersound.com cut by the cap).
- Flutter 2 (betfair.com, pokerstars.com); Entain 2 (bwin.com, partypoker.com); Evoke 1 (888casino.com).

## Not observable from here (kept)
- Geo-redirect from the Italian address to the Italian site (13): eurosport.com -> eurosport.it, philips.com -> philips.it, and 11 of the 19 betting hosts: betfair, betway, partypoker (-> giocodigitale.it), bwin, pokerstars, betsson, 888casino, leovegas, pinnacle, stake, oddsportal (-> centroquote.it). The international betting figures will rest on 8 hosts unless the fetch runs from another vantage.
- 403/401/451/timeout on the homepage (37): news.un.org unesco.org oecd.org imf.org unhcr.org unece.org iaea.org reuters.com economist.com atptour.com researchgate.net academic.oup.com tandfonline.com cambridge.org thelancet.com pubs.rsc.org reverso.net hp.com etsy.com hm.com tesla.com lego.com adidas.com uniqlo.com britishairways.com easyjet.com lufthansa.com emirates.com radissonhotels.com linkedin.com nordvpn.com orange.com forebet.com superbet.com boylesports.com jamesedition.com properstar.com
- Answered but no robots.txt user-agent line seen (24, overlaps the above): europarl.europa.eu eur-lex.europa.eu unesco.org unhcr.org unece.org wikimedia.org link.springer.com nature.com global.oup.com reverso.net hp.com getyourguide.com britishairways.com epicgames.com telegram.org nordvpn.com orange.com novonordisk.com orpha.net betano.com superbet.com betway.com boylesports.com pinnacle.com. Several (europarl, eur-lex, global.oup.com) answered 202, likely a bot challenge (hypothesis).

## Home values to verify
From general knowledge, not checked: binance.com AE (no formal headquarters), temu.com IE (PDD Holdings' seat), investing.com CY, forebet.com CY, oddsportal.com CZ, 1xbet.com CY, stake.com CW, nordvpn.com LT, lenovo.com HK, tiktok.com SG, telegram.org AE, reuters.com GB (Thomson Reuters is CA).

## Revision 2
- The 17 UK-first hosts listed above moved to the UK sample.
- 1xbet.com and stake.com out: unlicensed in most European markets, while the country samples use licensed operators. In: tipico.com (licensed in Germany and Austria) and 888sport.com (888 Holdings), the next licensed multi-country operators by Tranco rank.
