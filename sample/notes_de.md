# Germany sample — draft notes (2026-10-02)

808 domains, every sector at quota, no shortfall. Probed from Italy with curl_cffi (chrome).

## Per sector

- pa: 115/115
- news: 111/111
- publishing_education: 96/96
- ecommerce: 82/82
- travel_tourism: 73/73
- banking_insurance: 67/67
- media_lifestyle: 64/64
- telco_utilities: 60/60
- health: 53/53
- betting_gaming: 52/52
- real_estate: 35/35

## Borderline sector calls

- deutschlandfunk.de, deutschlandfunkkultur.de -> news (news radio); regional broadcasters br/ndr/wdr/swr/mdr/hr/sr -> media_lifestyle; their news portals tagesschau, zdfheute, hessenschau, rbb24 -> news.
- t-online.de -> news (portal, but news-led); web.de, gmx.net -> media_lifestyle (mass portals).
- finanzen.net, wallstreet-online, ariva, boerse.de -> news; onvista.de (now a bank), finanztip, finanzfluss, schufa, bonify -> banking_insurance.
- teltarif.de -> telco_utilities (tariff comparator); check24.de, verivox.de, heizoel24.de -> telco_utilities.
- kvb.de is the Kassenaerztliche Vereinigung Bayerns, not Cologne transit -> health. Krankenkassen (aok, tk, barmer, dak, ikk-classic, kkh, knappschaft) -> health.
- kit.edu -> publishing_education (university, although also a Helmholtz centre). Other Helmholtz/Max-Planck/Fraunhofer/Leibniz bodies, DFG, KfW, NRW.BANK candidate -> pa.
- ihk.de, verbraucherzentrale.de, giz.de, gtai (cut) -> pa (public-law or state-owned bodies).
- adac.de and clever-tanken.de -> travel_tourism (motoring/transport); komoot dropped (global .com).
- juris.de, dejure.org, haufe.de, beck.de -> publishing_education (legal publishing).
- aktion-mensch.de, postcode-lotterie.de, fernsehlotterie (cut) -> betting_gaming (social lotteries); deutscher-galopp.de, racebets.de -> betting (horse racing); wette.de, wettbasis.com, isa-guide.de (cut) -> trade/comparison media.
- my-hammer.de, aroundhome.de, houzz.de, baunetz -> real_estate (renovation); vonovia, degewo, howoge, gewobag, leg-wohnen, deutsche-wohnen -> real_estate (landlords).
- mydealz.de, idealo.de, geizhals.de, billiger.de -> ecommerce (deal/price comparison); lieferando.de -> ecommerce.

## Clusters kept

- Laender: all 16 (berlin.de, hamburg.de, bremen.de counted as Laender) in pa.
- Cities: 6 (muenchen.de, stadt-koeln.de, frankfurt.de, stuttgart.de, duesseldorf.de, leipzig.de); dresden, hannover, nuernberg, karlsruhe, essen not selected.
- bund.de hosts kept as separate hosts: bund.de, bmi.bund.de, bsi.bund.de, bmftr.bund.de, bmbfsfj.bund.de, bmwsb.bund.de, bfdi.bund.de, gesund.bund.de (health). bfr.bund.de cut by rank.
- Ippen: merkur, tz, fr, hna, ruhr24 (5). Funke: waz, derwesten, abendblatt, morgenpost, thueringer-allgemeine (5). Madsack: rnd, haz, lvz, maz-online (+kn-online cut) (4). NOZ/mh:n: noz, shz, nordkurier (svz redirects to nordkurier). SWMH: sueddeutsche, stuttgarter-zeitung, stuttgarter-nachrichten, swp (4). DuMont: ksta, express. Axel Springer national titles: bild, welt, businessinsider, computerbild, autobild.
- Sparkassen: sparkasse.de, berliner-sparkasse.de, haspa.de, ksk-koeln.de (4; sskm.de dropped for cap). Volksbanken: vr.de only (other Volksbanken cut by rank). Landesbanken: lbbw.de + bw-bank.de (same group).
- Universities: 20 (tum, rwth-aachen, uni-heidelberg, fu-berlin, hu-berlin, uni-hamburg, uni-bonn, uni-koeln, uni-frankfurt, uni-tuebingen, tu-dresden, uni-goettingen, uni-freiburg, lmu, fau, uni-muenster, fernuni-hagen, iu, kit.edu, tu.berlin).
- State lotteries: all 16 Laender lottery sites + lotto.de, eurojackpot.de, oddset.de (DLTB family, likely shared templates). Novomatic family: novoline.de, stargames.de. Gauselmann/Merkur: merkurbets.de (merkur-spielhalle cut). Online-slot brands jackpotpiraten/bingbong/slotmagie/drueckglueck/wunderino/lapalingo/loewen-play may share platforms (not verified).
- Public broadcasting: ARD family (ard, ardmediathek, tagesschau, sportschau, br, ndr, wdr, swr, mdr, sr, ardsounds) + ZDF (zdf, zdfheute, 3sat). RTL Group: rtl.de only. ProSiebenSat.1: joyn.de (prosieben/sat1/kabeleins all redirect there).

## Alias resolutions (redirect verified; alias dropped, target kept)

bmbf.de -> bmftr.bund.de, bmel.de -> bmleh.de, bmfsfj.de -> bmbfsfj.bund.de, bmwk.de -> bundeswirtschaftsministerium.de, bmwi.de -> bundeswirtschaftsministerium.de, bmuv.de -> bundesumweltministerium.de, bmj.de -> bmjv.de, bzga.de -> bioeg.de, antidiskriminierungsstelle.de -> antidiskriminierungsstelle.gov.de, gfz-potsdam.de -> gfz.de, ifw-kiel.de -> kielinstitut.de, ran.de -> joyn.de, svz.de -> nordkurier.de, general-anzeiger-bonn.de -> ga.de, sportbild.de -> bild.de, br24.de -> br.de, heute.de -> zdfheute.de, tagesschau24.de -> tagesschau.de, uni-muenchen.de -> lmu.de, tu-berlin.de -> tu.berlin, penguinrandomhouse.de -> penguin.de, randomhouse.de -> penguin.de, weltbild.de -> thalia.de, tuicruises.com -> meinschiff.com, bayern.by -> erlebe.bayern, frankfurt-tourismus.de -> visitfrankfurt.travel, santander.de -> openbank.de, barmenia.de -> barmeniagothaer.de, gothaer.de -> barmeniagothaer.de, barclays.de -> easybank.de, lidl-connect.de -> lidl.de, freenet-mobilfunk.de -> freenet.de, mobilcom-debitel.de -> freenet.de, o2.de -> o2online.de, neobet.de -> neo.bet, x-tip.de -> merkurbets.de, merkur-casino.de -> merkur-spielhalle.de, immonet.de -> immowelt.de, wohnungsboerse.net -> immobilienscout24.de, vermietet.de -> immobilienscout24.de, daserste.de -> ardmediathek.de, prosieben.de -> joyn.de, sat1.de -> joyn.de, kabeleins.de -> joyn.de, vox.de -> rtl.de, rbb-online.de -> rbb24.de, 4players.de -> 4p.de, ardaudiothek.de -> ardsounds.de, rtlplus.de -> plus.rtl.de, magentatv.de -> telekom.de, 1live.de -> wdr.de, wahl-o-mat.de -> bpb.de, ntv.de -> n-tv.de, handelsblatt.de -> handelsblatt.com, thieme.de -> thieme-connect.de, immobilien-zeitung.de -> iz.de, selbst.de -> bauer-plus.de, wunderweib.de -> bauer-plus.de, caschys-blog.de -> stadt-bremerhaven.de, swb-gruppe.de -> swb.de, gmx.de -> gmx.net

## Dropped

- No DNS on bare and www (4): skl-glueckslotterie.de, grand-city-property.de, bundesministerium-gesundheit.de, tipico-sportwetten.de
- Global or non-German host (34): nzz.de (nzz.ch), nomos-elibrary.de (inlibra.com), wolterskluwer-online.de (wolterskluwer.eu), komoot.de (komoot.com), boerse-frankfurt.de (deutsche-boerse.com), netcup.de (netcup.com), dpd.de (dpd.com), avm.de (fritz.com), samedi.de (samedi.com), 888slots.de (888casino (geo .it)), homegate.de (homegate.ch), springer.de (link.springer.com), dpa.de (dpa.com), dpa.com (global), fraport.de (fraport.com), lufthansa.de (lufthansa.com), lufthansa.com (global), eurowings.de (eurowings.com), eurowings.com (global), condor.de (condor.com), condor.com (global), motel-one.com (global), hetzner.com (global), tibber.com (global), n26.com (global), traderepublic.com (global), trade-republic.com (global), scalable.capital (global), engelvoelkers.com (global), euronews.com (global), germany.travel (foreign-visitor audience), zattoo.com (DE+CH host), lottoland.com (global), lottoland.de (no host)
- Not selected, unreachable and unverifiable/minor (16): 1und1-mobilfunk.de, abitur-und-studium.de, airberlin.de, bausparen.de, bmdv.de, bmvi.de, bundesagentur.de, bundeskanzleramt.de, bundesverkehrsministerium.de, ewetel.de, immobilienpreise.de, kabel-deutschland.de, kleinanzeigen-immobilien.de, lfa.de, stadtwerke-muenchen.de, wikipedia.de. bmdv.de/bmvi.de are old domains of the renamed transport ministry (bmv.de kept).
- Reachable but not selected: bundesverband.de (not a public body), bundesstiftung-aufarbeitung.de (minor foundation), ipp.mpg.de (institute subdomain of mpg.de), dresden.de (city cap), hannover.de (city cap), nuernberg.de (city cap), karlsruhe.de (city cap), essen.de (city cap), uni-stuttgart.de (university cap), uni-leipzig.de (university cap), tu-darmstadt.de (university cap), ruhr-uni-bochum.de (university cap), uni-mannheim.de (university cap), epubli.de (alias of epubli.com), deichmann.com (global host (served Italian)), interwetten.com (global host), check24.net (duplicate CHECK24 host), unitymedia.de (legacy Vodafone brand page), kalaydo.de (now a job board), immo.de (not a property portal), immoxxl.de (B2B website builder), immoprofessional.de (B2B software), sprengnetter.de (B2B valuation software), wohnen.de (furniture shop), sskm.de (Sparkasse cap), plus.rtl.de (second RTL host), redcare-pharmacy.de (same firm as shop-apotheke.com, timed out), mybet.de (inactive placeholder), interamt.de (swap), bgbl.de (swap), dihk.de (swap), itzbund.de (swap), bundesjustizamt.de (swap), medizinfuchs.de (swap), zentrum-der-gesundheit.de (swap), praktischarzt.de (swap (job board)), zalando-lounge.de (swap (second Zalando host)), guenstiger.de (swap)
- Cut by rank to fit quota: pa: geomar.de unternehmensregister.de bundeswahlleiterin.de gtai.de ble.de govdata.de thuenen.de hzdr.de zew.de thw.de bverwg.de julius-kuehn.de insolvenzbekanntmachungen.de dzne.de bundesfinanzhof.de kielinstitut.de lba.de hereon.de helmholtz-munich.de bundesarbeitsgericht.de bast.de nrwbank.de fli.de bundesfreiwilligendienst.de polizei.de bundesrechnungshof.de antidiskriminierungsstelle.gov.de bfr.bund.de; news: lr-online.de tichyseinblick.de deraktionaer.de butenunbinnen.de jungewelt.de kn-online.de cicero.de reviersport.de epochtimes.de dwdl.de inside-digital.de nius.de 90min.de boersen-zeitung.de mobiflip.de; publishing_education: studycheck.de reclam.de deutsches-schulportal.de volkshochschule.de scribbr.de epubli.com; ecommerce: roller.de hoeffner.de kik.de pearl.de rosebikes.de fielmann.de flaschenpost.de spreadshirt.de lampenwelt.de fahrrad-xxl.de bike24.de hood.de hellofresh.de segmueller.de euronics.de westwing.de babyone.de dehner.de wirkaufendeinauto.de sheego.de hellweg.de knuspr.de momox.de; travel_tourism: holidu.de momondo.de billiger-mietwagen.de hotel.de europcar.de visitduesseldorf.de zugspitze.de stuttgart-tourist.de heide-park.de dreamlines.de nicko-cruises.de harzinfo.de costakreuzfahrten.de bestfewo.de msccruises.de reiseland-brandenburg.de ltsh.de flixtrain.de schwarzwald-tourismus.info tuifly.com visitfrankfurt.travel; banking_insurance: consorsfinanz.de creditplus.de continentale.de provinzial.de verti.de berliner-volksbank.de frankfurter-volksbank.de sparda-bw.de ukv.de volksbank-stuttgart.de sparda.de; media_lifestyle: kochbar.de eurogamer.de cinestar.de nationalgeographic.de cinemaxx.de radio.de donnerwetter.de kinopolis.de uci-kinowelt.de bildderfrau.de rtl2.de 4p.de ffh.de eatsmarter.de radioeins.de adticket.de eltern.de glamour.de laut.de metal-hammer.de jolie.de radiobremen.de myself.de schoener-wohnen.de cosmopolitan.de hr.de musikexpress.de quotenmeter.de rockantenne.de bigfm.de gutekueche.de muenchenticket.de sunshine-live.de radiohamburg.de kachelmannwetter.com; telco_utilities: tarifcheck.de gasag.de entega.de lycamobile.de otelo.de n-ergie.de yello.de naturstrom.de badenova.de simyo.de stromauskunft.de ay-yildiz.de hermes-paketshop.de netzclub.de stadtwerke-duesseldorf.de; health: agaplesion.de mhh.de sana.de meineapotheke.de vivantes.de abda.de clickdoc.de krankenkassen.de schoen-klinik.de blutspende.de sanicare.de deutsche-alzheimer.de internisten-im-netz.de hkk.de pronovabkk.de teleclinic.com; betting_gaming: fernsehlotterie.de netbet.de interwetten.de pferdewetten.de bet3000.de isa-guide.de spielbanken-bayern.de spielbank-wiesbaden.de merkur-spielhalle.de spielbank-berlin.de sunmaker.de gluecksspirale.de happybet.de spielbank-hamburg.de vbet.de; real_estate: vivawest.de tag-wohnen.de mieterengel.de heizungsfinder.de immobilienmakler.de saga.hamburg wunderflats.com

## Geo-redirects from Italy (kept, flag)

tipico.de -> tipico-sportwetten.com/italia, pokerstars.de -> pokerstars.it, 888poker.de homepage -> 888 Italy (robots on www.888poker.de is served). These are German-licensed hosts redirecting by visitor country; from this vantage point their robots.txt is the Italian one. Also from here: vbet.de 'Country was blocked', racebets.de '403 Not Available'.

## Kept but blocked/challenged/unreachable from here (59)

aerztezeitung.de(200) allianz.de(403) apodiscounter.de(403) arbeitsagentur.de(Failed to perform, cur) auxmoney.com(503) badische-zeitung.de(403) betano.de(403) bundesnetzagentur.de(404) bwin.de(403) decathlon.de(403) dfki.de(403) douglas.de(403) ebay.de(403) expedia.de(429) fachportal-paedagogik.de(Failed to perform, cur) fewo-direkt.de(429) frankfurt.de(403) galeria.de(403) gamepro.de(403) gamestar.de(403) getyourguide.de(403) globetrotter.de(403) goethe.de(403) hausundgrund.de(Failed to perform, cur) haz.de(403) immobilienscout24.de(401) iz.de(403) kaufland.de(403) kicker.de(403) lapalingo.de(403) lastminute.de(403) lottohelden.de(403) lvz.de(403) manomano.de(403) maz-online.de(403) medpex.de(403) merkur.de(503) mobile.de(403) neo.bet(403) notebooksbilliger.de(404) novoline.de(403) nrw.de(Failed to perform, cur) pcgames.de(403) pcgameshardware.de(403) ptb.de(500) racebets.de(200) reisereporter.de(403) rnd.de(403) rossmann.de(200) saechsische.de(403) schufa.de(200) springermedizin.de(200) springerprofessional.de(200) superprof.de(403) thueringen.de(200) tripadvisor.de(403) utb.de(403) wunderino.de(403) xxxlutz.de(403)

(several of these still served robots.txt; only the homepage was challenged)

## Kept, homepage reachable but no robots.txt with user-agent (40)

3sat.de alditalk.de bafa.de bamf.de bbaw.de beck.de berlin.de betway.de bfarm.de bildungsserver.de brandenburg.de bundeswirtschaftsministerium.de c24.de clever-tanken.de deutschlandticket.de dguv.de elster.de fernsehserien.de frankfurt-airport.com handelsregister.de ifo.de kinderaerzte-im-netz.de klett.de leibniz-gemeinschaft.de lotto-thueringen.de marktstammdatenregister.de mdc-berlin.de myhermes.de neuschwanstein.de openthesaurus.de remax.de sachsenlotto.de simpleclub.com tipico.de tipwin.de tvspielfilm.de uberspace.de webgo.de weg.de wetterzentrale.de

## Shortfalls

None. All 11 sectors at quota.

# REVISION 2 — betting_gaming

## State-lottery cap (max 6)
Kept: lotto.de, westlotto.de, lotto-bw.de, lotto-hessen.de, lotto-bayern.de, lotto-niedersachsen.de (largest Länder companies by Tranco rank; oddset.de ranks below them, so it was removed).
Removed (13): eurojackpot.de, oddset.de, sachsenlotto.de, lotto-rlp.de, lotto-berlin.de, lottomv.de, lotto-sh.de, lotto-hh.de, lotto-brandenburg.de, lotto-thueringen.de, lotto-bremen.de, lottosachsenanhalt.de, saartoto.de.
Unchanged outside the cluster: lotto24.de, tipp24.de, lottohelden.de (brokers), aktion-mensch.de, postcode-lotterie.de (charity).

## Refill (13 licensed operators, by Tranco rank)
tiptorro.de, mrgreen.de, jokerstar.de, wildz.de (403 challenge), netbet.de, leovegas.de (geo-redirect to leovegas.it), interwetten.de (challenge), pferdewetten.de, bet3000.de (403), ggpoker.de, merkur-spielhalle.de, sportingbet.de, sunmaker.de (403).
Probed but not used: partypoker.de (redirects to help.partypoker.de/closed), unibet.de and betvictor.de (pages say closed), ladbrokes.de -> bwin.de, mobilebet.de -> sunmaker.de, cashpoint.de -> merkurbets.de (aliases), merkur24.de -> merkur24.com and crazybuzzer.de -> crazybuzzer.com (global social casino), betfair.de -> betfair.it (geo; German licence not confirmed), admiral.de (a textile firm), chillbet.de and 1xbet.de (parked), bildbet.de and spielbank.de (no DNS), platincasino.de, happybet.de and vbet.de (left out on rank; happybet failed TLS from here, vbet blocks the country).

## Vantage-point list (geo-redirect from the Italian IP)
tipico.de, pokerstars.de, 888poker.de, leovegas.de (new).

## Skins / shared platforms
- Entain: bwin.de, sportingbet.de (ladbrokes.de redirects to bwin.de).
- Gauselmann/Merkur: merkurbets.de, jokerstar.de, merkur-spielhalle.de (cashpoint.de and x-tip.de redirect to merkurbets.de).
- Novomatic/Greentube: novoline.de, stargames.de; mobilebet.de redirects to sunmaker.de.
- Title pattern "<Brand> Online Spielothek" is shared by stargames, jackpotpiraten, bingbong and drueckglueck. This may mean a shared platform; not verified.

## International list
32 hosts. These are the 36 host-rule drops from the first pass deduplicated to their global hosts: lufthansa.de/.com, eurowings.de/.com, condor.de/.com and dpa.de/.com each collapse to one row. trade-republic.com is merged into traderepublic.com. lottoland.de had no host and is listed as lottoland.com. The two new rows are merkur24.com and crazybuzzer.com. 888casino.it is a geo-redirect, not a global host; it is listed for completeness.

# REVISION 3 — country-dedicated hosts for foreign visitors

Clarified rule: a host dedicated to one country counts for that country even when it addresses foreign visitors.
- In: germany.travel (travel_tourism). The DZT national tourism board; 200, robots.txt served.
- Out: edreams.de. It was the lowest-ranked ranked travel site kept (Tranco 123,025) and duplicates the eDreams ODIGEO group already present through opodo.de.
- No other site had been dropped for its foreign-visitor audience. The regional tourism boards (visitduesseldorf, stuttgart-tourist, harzinfo, reiseland-brandenburg, ltsh, schwarzwald-tourismus, visitfrankfurt.travel) were always eligible. They lost on rank, all below edreams.de, so the rank cut stands.
- germany.travel removed from the international list.

# REVISION 4
- pa tiers: regional = the 16 Länder (city-states Berlin, Hamburg and Bremen included) and kmk.org; local = duesseldorf.de, frankfurt.de, leipzig.de, muenchen.de, stadt-koeln.de, stuttgart.de; the rest central.
