# IT sample revision — 2026-10-02

Probe: curl_cffi `impersonate="chrome"`, https bare then www, plus `socket.getaddrinfo`.
Sector counts unchanged (595 rows, unique, CRLF).

## Removed (moved to international list) — 19

ecommerce: benetton.com, intimissimi.com, tezenis.com, calzedonia.com, yoox.com,
luisaviaroma.com, kikocosmetics.com, terranovastyle.com, callmewine.com, vino.com.
travel_tourism: lastminute.com, ita-airways.com, aeroitalia.com.
telco_utilities: eni.com, netsons.com. banking_insurance: satispay.com, scalapay.com,
moneyfarm.com. real_estate: casavo.com.

## Tested: luxuryestate.com and docsity.com — both international, removed

- **luxuryestate.com** (real_estate): 200 on www.luxuryestate.com, title in English.
  Language paths `/it/ /de/ /fr/ /ru/ /es/ /pt/ /pl/ /tr/`, and the homepage links
  country market paths: `/argentina /australia /germany /united-kingdom /japan
  /united-arab-emirates /thailand ...` (23 countries). One host serving many countries'
  markets → international. Suggested: real_estate, home IT, reach global.
- **docsity.com** (publishing_education): 200 to the Chrome probe (the plain-probe 403 is
  bot blocking). 35 hreflang entries with country-coded editions on one host:
  `en-us=/en/usa/, en-gb=/en/gbr/, en-in=/en/ind/, en-ph=/en/phl/, es-es=/es/esp/ ...`.
  → international. Suggested: publishing_education, home IT, reach global.

## Dead / alias rows

- **gaslini.org** (health): no DNS. gaslini.it resolves but is a parked register.it
  placeholder (title "Home page", registrar banners; https gives SSL error).
  ospedalegaslini.ge.it and gaslini.ge.it: no DNS. ospedalegaslini.it, istitutogaslini.it,
  istitutogaslini.org: resolve but time out. fondazionegaslini.org is the Fondazione Gerolamo
  Gaslini (endowment body), not the hospital, and links no hospital domain.
  No live hospital host found → **removed**, slot refilled (santagostino.it).
- **dovevivo.com** (real_estate): redirects to coliving.joivy.com. Joivy (the DoveVivo
  rebrand) serves Italy, Spain, Portugal and France from one host: hreflang en/it/fr/es,
  homepage names Milan, Rome, Turin, Bologna, Madrid, Lisbon, Porto, Paris → multi-country,
  **removed**. International candidate: joivy.com, real_estate, home IT, reach europe.
- **redooc.com** (publishing_education): redirects to sapere.virgilio.it; virgilio.it
  already present → **removed** (alias), slot refilled.
- **finecobank.com** (banking_insurance): redirects to it.finecobank.com (200, Italian
  title) → **replaced in place** with it.finecobank.com.

## Replacements — 24 (appended at end)

Tranco = rank in today's .it-filtered Tranco list; "-" = not listed.

| domain | sector | Tranco | probe |
|---|---|---|---|
| qvc.it | ecommerce | 19983 | 418 (bot block), www.qvc.it |
| deghi.it | ecommerce | 22366 | 200 |
| libreriauniversitaria.it | ecommerce | 33173 | 200 |
| backmarket.it | ecommerce | 59609 | 200; other countries on own ccTLDs |
| cisalfasport.it | ecommerce | 66471 | 200 |
| expert.it | ecommerce | 66611 | 200; hreflang it-it only |
| toyscenter.it | ecommerce | 68583 | 200 |
| eurospin.it | ecommerce | 69762 | 200 |
| mondoconv.it | ecommerce | 73471 | 200 |
| bricocenter.it | ecommerce | 75298 | 200 |
| findomestic.it | banking_insurance | 139298 | 200 |
| cdp.it | banking_insurance | 139404 | 200; it/en language editions |
| compass.it | banking_insurance | 149999 | 200 |
| autostrade.it | travel_tourism | 33017 | 200 |
| costacrociere.it | travel_tourism | 42440 | 200; Italian host of Costa |
| alpitour.it | travel_tourism | 66748 | 200 |
| trovacasa.it | real_estate | 48870 | 200 |
| astegiudiziarie.it | real_estate | 176847 | 200 |
| soloaffitti.it | real_estate | 603077 | 200 |
| ehiweb.it | telco_utilities | 27449 | 200 (ISP/VoIP/hosting, replaces netsons) |
| servizioelettriconazionale.it | telco_utilities | 182799 | 200 (energy, replaces eni) |
| unipv.it | publishing_education | 25411 | 200 → portale.unipv.it |
| erickson.it | publishing_education | 65469 | 200 |
| santagostino.it | health | 70489 | 200 |

Probed spares, not used: gardaland.it (51662), vivaticket.it (33473), msccrociere.it (71820,
401), viaggiatreno.it (46347, Trenitalia network), unipr.it (28576), accademiadellacrusca.it
(147046), deascuola.it, doctolib.it (46521), fideuram.it, agos.it, sara.it, cattolica.it,
openfiber.it, twt.it, intred.it, alperia.eu (it/de, one region: national), unilibro.it,
doveconviene.it, tigota.it, acquaesapone.it, bricoio.it. Skipped: redcare.it (online pharmacy;
pharmacies sit in health, already 7), trovit.it (Lifull clone network), gruppotim.it (TIM
corporate, near tim.it), homepal.it (redirects to rexer.it), estra.it (redirects to
aliaestra.it), agsmaim.it (redirects to gruppomagis.it), mecshopping.it (language editions
it/en/de/fr/es on one host; borderline).

## Multi-country hosts found among candidates (for the international list)

| host | sector | home | reach | evidence |
|---|---|---|---|---|
| luxuryestate.com | real_estate | IT | global | 23 country paths + 8 language paths |
| docsity.com | publishing_education | IT | global | country-coded editions /en/usa/, /es/esp/ ... |
| joivy.com (coliving.joivy.com) | real_estate | IT | europe | IT/ES/PT/FR cities on one host |
| carpisa.it | ecommerce | IT | europe | /de-at /de-de /fr-fr /es-es /en-cz /en-nl on one host |
| pittarello.com | ecommerce | IT | europe | /de-eu, /it-eu for AT and DE; SI on its own .si |

Not international by the rule: spusu.it (AT/DE/UK/CH on their own ccTLDs) and
prenatal.it redirects to prenatal.com, which is the Italian edition (GR/PT/ES on their own
domains): national, not international.

## Revision 2 (after the US vantage run)
Rule: national vs international is a judgement on the host's primary market; probe signals (root
routing from a third country, hreflang country editions) are evidence, not the test. The root test
is vantage-dependent (elpais.com and theguardian.com route US visitors to /us/).
Back to Italy (primary market Italy): satispay, scalapay, vino.com, callmewine, pittarello.com (new),
casavo, netsons, aeroitalia. Stay international: benetton, intimissimi, tezenis, calzedonia, yoox,
kiko, luisaviaroma, terranova, carpisa, ita-airways, lastminute, eni.com, moneyfarm, luxuryestate,
docsity, joivy. Blocked from Azure (403), fine from Italy: luisaviaroma, ita-airways, netsons,
aeroitalia, docsity.

## Revision 3 (robots.txt served by another site)
In the 2026-10-02 crawl, 12 Italian domains had their robots.txt answered by a different site.
- Replaced by the target host: istruzione.it -> mim.gov.it, giornaledisicilia.it -> gds.it, telethon.it -> fondazionetelethon.it, madisoft.it -> nuvolascuola.it, homobile.it -> ho-mobile.it, 3bmeteo.it -> 3bmeteo.com, deagostini.it -> deagostini.com (no other country editions declared).
- Dropped: unipolsai.it (lands on unipol.it, already in the sample), feltrinelli.it (lands on lafeltrinelli.it, already in), helvetia.it and nh-hotels.it (land on multi-country hosts). dovevivo.com was already out.
- Refills: sara.it and cattolica.it (banking_insurance), gardaland.it (travel_tourism), accademiadellacrusca.it (publishing_education).
- cdp.it moved to pa, like caissedesdepots.fr and kfw.de; comune.prato.it out to keep pa at 85.
- pa tiers: comune.* local; regione.*, provincia.tn.it and provincia.bz.it regional; the rest central.
