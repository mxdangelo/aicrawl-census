# draft notes FR sample (2026-10-02)

## Method
Candidates: 1058 hand-listed (Tranco .fr top ~3000 skim + French-audience .com/.org/.eu from knowledge) + 32 redirect targets. Probed with curl_cffi chrome impersonation, https:// then https://www.. Ranking: Tranco overall rank; non-.fr notable sites given a nominal rank of 3000, obscure ones last.

## Borderline decisions
- amazon.fr, ebay.fr, zalando.fr, vinted.fr, tripadvisor.fr kept: country-localised domains, Italy sample keeps the .it equivalents.
- laposte.fr in telco_utilities (postal/mail; Italy puts poste.it in banking). Alternative: ecommerce/banking.
- meteofrance.fr (public weather agency) is a candidate reassigned to media_lifestyle but fell below the quota cut; meteociel/lachainemeteo kept for weather.
- cnrs, inserm, inrae, cea, cnes, ifremer, inria, ird, cirad in pa (research agencies, as Italy cnr.it).
- bnf.fr, ina.fr: bnf in publishing_education (library), ina in media_lifestyle.
- caissedesdepots.fr, bpifrance.fr, afd.fr in pa (public financial institutions), not banking.
- amf-france.org in pa (regulator); anj.fr (gambling regulator) probed fine but cut by quota ranking.
- lcp/publicsenat not kept (parliament TV).
- hec.edu, essec.edu, polytechnique.edu, psl.eu are non-.fr TLD (.edu/.eu) but French audience; kept as targets of .fr redirects.
- mabanque.bnpparibas: BNP Paribas retail via .bnpparibas TLD (bnpparibas.fr redirects to group.bnpparibas).
- casinosbarriere.com (physical casino group with online poker) and poker-academie.com, betwatch.fr, bettingclosed.fr are trade/affiliate media in betting_gaming.
- joueurs-info-service.fr, mangerbouger.fr in health (public health information), alt: pa.
- pagesjaunes.fr in media_lifestyle (Italy: paginegialle). billetweb/billetreduc/ticketing in media_lifestyle.
- pixpay.fr (kids payment card) in banking_insurance. gites.fr in travel_tourism.
- winamax.fr, betclic.fr: homepage geo-redirect loops/DNS failure from an Italian IP, but robots.txt served on www host; kept (also diplomatie.gouv.fr, turfpronos.fr).
- pokerstars.fr redirects (geo) to pokerstars.it: dropped. zebet.fr -> unibet.fr (alias).

## Redirect replacements (alias -> kept)
- service-public.fr -> service-public.gouv.fr
- developpement-durable.gouv.fr -> ecologie.gouv.fr
- journaldunet.fr -> journaldunet.com
- nextinpact.com -> next.ink
- laffont.fr -> lisez.com
- bayard-editions.com -> bayard-jeunesse.com
- hatier.fr -> editions-hatier.fr
- polytechnique.fr -> polytechnique.edu
- ens.fr -> psl.eu
- hec.fr -> hec.edu
- essec.fr -> essec.edu
- enpc.fr -> ecoledesponts.fr
- orchestra.fr -> shop-orchestra.com
- floabank.fr -> floa.com
- lydia-app.com -> sumeria.eu
- chu-strasbourg.fr -> chru-strasbourg.fr
- zeturf.fr -> zeturf.com
- francetv.fr -> france.tv
- francebleu.fr -> ici.fr
- skyrock.com -> skyrock.fm
- linternaute.fr -> linternaute.com
- animationdigitalnetwork.fr -> animationdigitalnetwork.com
- era-immobilier.fr -> eraimmobilier.com
- gouvernement.fr -> info.gouv.fr
- ovh.com -> ovhcloud.com

## Alias/duplicate or global domains dropped (not probe failures)
1and1.fr, 6play.fr, adn.fr, aeroportsdeparis.fr, afnic.fr, agefiph.fr, all.accor.com, ars.sante.fr, banquedesterritoires.fr, bbox.fr, bnpparibas.fr, bpce.fr, bricoman.fr, businessinsider.fr, cartoonnetwork.fr, cerema.fr, chronopost.fr, cnav.fr, cnsa.fr, colissimo.fr, credit-agricole.com, crunchyroll.com, dailymotion.com, dalloz.fr, dauphine.fr, deezer.com, discoverychannel.fr, e-cancer.fr, explorimmo.com, fnacspectacles.com, francebleu.fr, franceculture.fr, franceinter.fr, francetvinfo.fr, getyourguide.fr, hellfest.fr, helvetia.fr, hostinger.fr, ikea.fr, immo-entre-particuliers.com, immobilier.notaires.fr, ined.fr, info-retraite.fr, ing.fr, joaonline.fr, la-boite-immo.fr, lastminute.com, lci.fr, lcp.fr, ledauphine.com.x, lesiteimmo.com, mondialrelay.fr, mondocteur.fr, monespacesante.fr, mtv.fr, nickelodeon.fr, nordnet.fr, numericable.fr, numerique.gouv.fr, ocs.fr, onf.fr, ooreka.fr, orias.fr, oui.sncf, pagesjaunes.fr.x, parionssport.fdj.fr, paris-hippiques.fr, particulier-a-particulier.fr, pocket.fr, poker-france.fr, pokerstars.fr, pole-emploi.fr, psychologies.com, publicsenat.fr, rakuten.fr, sante-ra.fr, sciences-po.fr, seloger.fr, sncf.com, societegenerale.fr, strasbourg.eu, suez.fr, sumup.fr, tele-loisirs.fr, tierce.fr, trainline.fr, unibet.com, univ-paris1.fr, voila.fr, wanadoo.fr, yahoo.fr, younited-credit.com, zebet.fr

## Dropped by probe (domain, status, error)
- legifrance.gouv.fr | 403 | 
- finances.gouv.fr | None | Failed to perform, curl: (6) Could not r
- ccomptes.fr | None | Failed to perform, curl: (28) Connection
- ofb.fr | None | Failed to perform, curl: (6) Could not r
- cnav.fr | None | Failed to perform, curl: (6) Could not r
- dila.fr | None | Failed to perform, curl: (6) Could not r
- permisdeconduire.gouv.fr | None | Failed to perform, curl: (35) TLS connec
- securite-routiere.gouv.fr | None | Failed to perform, curl: (52) Empty repl
- bretagne.bzh | 403 | 
- valdemarne.fr | None | Failed to perform, curl: (28) Connection
- essonne.fr | 418 | 
- nantes.fr | None | Failed to perform, curl: (35) TLS connec
- lepoint.fr | 403 | 
- lamontagne.fr | 403 | 
- leberry.fr | 403 | 
- lechorepublicain.fr | 403 | 
- lepopulaire.fr | 403 | 
- larep.fr | 403 | 
- lejdc.fr | 403 | 
- leveil.fr | 403 | 
- lyonne.fr | 403 | 
- usine-digitale.fr | 403 | 
- forbes.fr | None | Failed to perform, curl: (6) Could not r
- reporterre.net | 403 | 
- lagazettedescommunes.com | 403 | 
- lemoniteur.fr | 403 | 
- usinenouvelle.com | 403 | 
- flammarion.com | None | Failed to perform, curl: (35) TLS connec
- superprof.fr | 403 | 
- mines-paristech.fr | None | Failed to perform, curl: (60) SSL certif
- univ-reims.fr | None | Failed to perform, curl: (60) SSL certif
- conforama.fr | 403 | 
- intersport.fr | 403 | 
- vertbaudet.fr | 403 | 
- cultura.com | 403 | 
- lacentrale.fr | 403 | 
- mr-bricolage.fr | 403 | 
- weldom.fr | 403 | 
- norauto.fr | 403 | 
- oscaro.com | 403 | 
- fruugo.fr | 403 | 
- ubaldi.com | 403 | 
- bhv.fr | 403 | 
- ratp.fr | 403 | 
- autoroutes.fr | None | Failed to perform, curl: (60) SSL certif
- corsair.fr | None | Failed to perform, curl: (60) SSL certif
- notredamedeparis.fr | 403 | 
- camping-car.fr | None | Failed to perform, curl: (35) Recv failu
- creditmaritime.fr | None | Failed to perform, curl: (6) Could not r
- natixis.fr | None | Failed to perform, curl: (6) Could not r
- cm-cic.fr | None | Failed to perform, curl: (7) Failed to c
- aviva.fr | None | Failed to perform, curl: (6) Could not r
- sma.fr | None | Failed to perform, curl: (6) Could not r
- ageas.fr | None | Failed to perform, curl: (28) Connection
- olivierassurance.com | None | Failed to perform, curl: (7) Failed to c
- veolia.fr | 403 | 
- quelleenergie.fr | 403 | 
- changerdefournisseur.fr | None | Failed to perform, curl: (6) Could not r
- club-internet.fr | None | Failed to perform, curl: (60) SSL: no al
- aliceadsl.fr | None | Failed to perform, curl: (60) SSL: no al
- neuf.fr | None | Failed to perform, curl: (60) SSL: no al
- noos.fr | None | Failed to perform, curl: (6) Could not r
- completel.fr | None | Failed to perform, curl: (28) Connection
- outremer-telecom.fr | None | Failed to perform, curl: (28) Connection
- plenitude.fr | None | Failed to perform, curl: (60) SSL certif
- oui-energie.fr | None | Failed to perform, curl: (6) Could not r
- extelia.fr | None | Failed to perform, curl: (7) Failed to c
- pharmacien.fr | None | Failed to perform, curl: (6) Could not r
- chirurgiens-dentistes.fr | None | Failed to perform, curl: (6) Could not r
- medecin.fr | None | Failed to perform, curl: (6) Could not r
- ordre.medecin.fr | None | Failed to perform, curl: (6) Could not r
- hopital-foch.org | None | Failed to perform, curl: (6) Could not r
- institutcurie.org | None | Failed to perform, curl: (60) SSL: no al
- elsan.fr | None | Failed to perform, curl: (60) SSL: no al
- france-pari.fr | None | Failed to perform, curl: (6) Could not r
- joa.fr | 403 | 
- lariviera-casino.fr | None | Failed to perform, curl: (60) SSL certif
- resultat-pmu.fr | None | Failed to perform, curl: (28) Connection
- tierce-magazine.fr | None | Failed to perform, curl: (7) Failed to c
- clubpoker.net | 403 | 
- casinosenligne.fr | 403 | 
- betsson.fr | 403 | 
- tonybet.fr | None | Failed to perform, curl: (6) Could not r
- pronostic-foot.fr | None | Failed to perform, curl: (7) Failed to c
- pronosport.fr | None | Failed to perform, curl: (7) Failed to c
- pokerfr.com | None | Failed to perform, curl: (28) Connection
- poker.fr | None | Failed to perform, curl: (6) Could not r
- sportytrader.fr | None | Failed to perform, curl: (7) Failed to c
- parisportif.fr | None | Failed to perform, curl: (6) Could not r
- pariersportif.fr | None | Failed to perform, curl: (6) Could not r
- stats-turf.fr | None | Failed to perform, curl: (6) Could not r
- turf-infos.com | None | Failed to perform, curl: (6) Could not r
- premiere.fr | 403 | 
- canalplus.fr | None | Failed to perform, curl: (60) SSL: no al
- cheriefm.fr | 403 | 
- ticketmaster.fr | 401 | 
- cgrcinemas.fr | 404 | 
- radioline.fr | None | Failed to perform, curl: (92) HTTP/2 str
- festival-cannes.fr | None | Failed to perform, curl: (35) TLS connec
- discoverychannel.fr | None | Failed to perform, curl: (6) Could not r
- oneesports.fr | None | Failed to perform, curl: (6) Could not r
- pluzz.fr | 403 | 
- avendrealouer.fr | 403 | 
- proprietes-le-figaro.com | None | Failed to perform, curl: (6) Could not r
- stephaneplazaimmobilier.com | 403 | 
- maisonsetappartements.fr | 403 | 
- twimm.fr | None | Failed to perform, curl: (60) SSL: no al
- orpi.fr | None | Failed to perform, curl: (7) Failed to c
- laforet.fr | None | Failed to perform, curl: (60) SSL: no al
- immodvm.com | None | Failed to perform, curl: (6) Could not r
- keller-williams.fr | None | Failed to perform, curl: (6) Could not r
- logic-immo.fr | None | Failed to perform, curl: (35) TLS connec
- bien-ici.com | None | Failed to perform, curl: (6) Could not r
- kelquartier.com | None | Failed to perform, curl: (60) SSL: no al
- lesiteimmoneuf.com | None | Failed to perform, curl: (60) SSL certif
- cheznestor.com | None | Failed to perform, curl: (6) Could not r
- maisonsmedavy.com | None | Failed to perform, curl: (6) Could not r
- lebienpublic.fr | None | Failed to perform, curl: (6) Could not r

## Kept with homepage OK but no robots.txt text detected (25)
ants.gouv.fr culture.gouv.fr sante.gouv.fr travail-emploi.gouv.fr cnrs.fr paris.fr franceconnect.gouv.fr vie-publique.fr francecompetences.fr courdecassation.fr conseil-etat.fr hachette-education.com reseau-canope.fr fun-mooc.fr synonymo.fr alinea.com galerieslafayette.com king-jouet.com jdsports.fr cite-sciences.fr ag2rlamondiale.fr engie.fr enercoop.fr mangerbouger.fr oneturf.fr

## Clusters kept
- Municipal pa: paris.fr, lyon.fr, marseille.fr, toulouse.fr, bordeaux.fr (5; cap 6). Regions: auvergnerhonealpes, iledefrance, maregionsud, nouvelle-aquitaine, laregion, grandest. No departments except none selected by rank.
- Local press: Ebra (leprogres, ledauphine, lejsl, estrepublicain), Dépêche (ladepeche, midilibre, lindependant), Sud Ouest (sudouest, charentelibre, larepubliquedespyrenees), Rossel (lavoixdunord, paris-normandie, courrier-picard, lunion), Centre France (lanouvellerepublique), Ouest (ouest-france, actu.fr).
- Universities capped at 14 and ac-* at 2 in publishing_education.
- Radio (France Radio via radiofrance.fr, ici.fr, rtl.fr, skyrock.fm) in media_lifestyle; horse-racing media cluster (turf sites ~16 of 31) in betting_gaming.

## Shortfalls
None: all 11 sectors at quota. betting_gaming had only 33 reachable candidates for 31 slots; the sector leans on horse-racing media.

# REVISION 2 (rules aligned with the Italian sample)
- Drop rule: only no-DNS, parked/for-sale, infra and true redirect aliases are dropped. Of 118 earlier probe-dropped, 27 fail DNS and 91 resolve; 24 of the 91 are in the revised file (rest cut by quota rank).
- No-DNS (dropped): finances.gouv.fr, ofb.fr, cnav.fr, forbes.fr, natixis.fr, aviva.fr, sma.fr, changerdefournisseur.fr, noos.fr, pharmacien.fr, chirurgiens-dentistes.fr, medecin.fr, ordre.medecin.fr, hopital-foch.org, parisportif.fr, pariersportif.fr, stats-turf.fr, turf-infos.com, discoverychannel.fr, oneesports.fr, proprietes-le-figaro.com, immodvm.com, keller-williams.fr, bien-ici.com, cheznestor.com, maisonsmedavy.com, lebienpublic.fr
- Probe-failed domains that resolve but are not in file: kept out by Tranco rank / representativeness only.
- Non-Tranco guessed domains that failed the probe were ranked last (only filled if needed).
- Alias re-check (actual redirect check): real aliases kept out: 1and1, 6play(->m6.fr added), aeroportsdeparis, bbox, bnpparibas.fr(->group.bnpparibas; mabanque.bnpparibas kept), bpce(->groupebpce.com corporate), bricoman(->tecnomat.fr), colissimo, dauphine(->psl.eu), e-cancer, francebleu, franceculture, franceinter, francetvinfo, lci, mondocteur, ocs, oui.sncf, pocket, pole-emploi, sciences-po, societegenerale, seloger.fr, tele-loisirs, univ-paris1(->pantheonsorbonne.fr), wanadoo, zebet, club-internet/aliceadsl/neuf (http redirect to sfr/free), elsan.fr (see REVISION 3), twimm.fr, immobilier.notaires.fr and ars.sante.fr (subdomains).
- Redirect to a global .com (registrable differs; kept OUT): ikea.fr->ikea.com, rakuten.fr->fr.shopping.rakuten.com, trainline.fr->thetrainline.com, getyourguide.fr, helvetia.fr, hostinger.fr, ing.fr->ingwb.com, nordnet.fr, suez.fr, sumup.fr, younited-credit.com, yahoo.fr->fr.yahoo.com, businessinsider.fr, nickelodeon/cartoonnetwork/mtv, pokerstars.fr->pokerstars.it (geo).
- Not redirects, reinstated as candidates: afnic? no (registry, infra, out); agefiph, cerema, cnsa, ined, onf, orias, numerique.gouv.fr, info-retraite, banquedesterritoires, monespacesante, lcp, publicsenat, psychologies, hellfest, dalloz, fnacspectacles, strasbourg.eu.
- Global .com with no French site, out: deezer.com, dailymotion.com, crunchyroll.com, lastminute.com, all.accor.com, unibet.com (unibet.fr kept).
- Added: anj.fr (pa), meteofrance.fr (media_lifestyle). lcp.fr/publicsenat.fr: no room, out.

# REVISION 3 (final decisions)
- Added as notable candidates: conseil-national.medecin.fr, ordre.pharmacien.fr, ordre-chirurgiens-dentistes.fr, hopital-foch.com (health; correct spellings of earlier no-DNS guesses); abeille-assurances.fr (banking); proprietes.lefigaro.fr (real_estate); fr.shopping.rakuten.com (ecommerce) and fr.yahoo.com (media_lifestyle) under the host rule.
- Host rule: a French-specific host counts as a French observation even on a global registrable domain (robots.txt is per host). Redirects landing on a global host with a /fr/ path (ikea.com/fr, thetrainline.com) stay out.
- chronopost.fr, mondialrelay.fr: telco_utilities (postal/parcel, consistent with laposte.fr).
- abeille-assurances.fr swapped in for pixpay.fr (banking_insurance).
- bienpublic.com (Ebra): no Tranco rank, so it does not outrank the four Ebra titles; kept out.
- Confirmed out: ikea.fr, trainline.fr (global host + /fr/ path); deezer.com, dailymotion.com (single global host; international list); tierce.fr, adn.fr, poker-france.fr, paris-hippiques.fr (unidentified); ing.fr, helvetia.fr, hostinger.fr, nordnet.fr, suez.fr, sumup.fr, younited-credit.com, getyourguide.fr, businessinsider.fr, nickelodeon/cartoonnetwork/mtv.
- elsan.fr: verified, http://elsan.fr and http://www.elsan.fr both 301 to https://elsan.co.uk ("Home - ELSAN"); https fails with a certificate name mismatch. Likely the UK sanitation company Elsan Ltd, not the hospital group (hypothesis, not checked further). Unrelated to elsan.care, which stays in the file; elsan.fr stays out.
- Context to verify: the French betting sector leans on horse racing likely because online casino games are not licensed in France (only sports betting, horse-race betting and poker are open under ANJ).

## Geo-redirect / vantage-point sites
- pokerstars.fr: geo-redirects to pokerstars.it from our Italian IP; French-licensed operator, eligible (Tranco rank 174035, cut by quota ranking).
- winamax.fr, betclic.fr: homepage redirect loop / DNS failure from Italy; robots.txt served on www host. In file.
- turfpronos.fr (in file), diplomatie.gouv.fr (cut by quota ranking in revision 2): homepage failed, robots.txt served.

# REVISION 4
- sensacine.com removed: it is AlloCiné's Spanish site and belongs to the Spanish sample. lcp.fr in (media_lifestyle).
- pa tiers: local = paris.fr, lyon.fr, marseille.fr, toulouse.fr, bordeaux.fr, strasbourg.eu; regional = auvergnerhonealpes.fr, iledefrance.fr, maregionsud.fr; the rest central.
