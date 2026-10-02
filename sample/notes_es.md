# Spain sample (domains.es.csv): draft notes

361 domains, every sector at quota. Probes run 2026-10-02 from the Italian vantage point with curl_cffi (impersonate chrome).

## The big .com outlets (superseded in revision 2)

These four hosts serve country editions on the main host, so the strict host rule sent them to the international list:

- elpais.com: /mexico/, /argentina/, /chile/, /america-colombia/ and /us/ editions (verified, "EL PAÍS Edición México").
- marca.com: hreflang es-MX points to /mx/ and en-US to /en/ (verified, "MARCA México").
- as.com: /us/ ("AS USA Latino") and /america/ (verified).
- hola.com: hreflang en-US, es-US and es-MX point to /us/ and /us-es/ (verified).

All four are the largest Spanish titles. If the rule is relaxed for news with secondary editions, they should come back in place of the four lowest-ranked news picks (diariodesevilla.es, ultimahora.es, maldita.es, relevo.com).

Kept: mundodeportivo.com, whose US edition is on a separate host (us.mundodeportivo.com), and elespanol.com, whose /usa/ is a topic section.

## Borderline sector calls

- rtve.es goes in news. RTVE has no separate news host. Italy puts rai.it in media and rainews.it in news.
- 3cat.cat (ccma.cat redirects there), telemadrid.es, canalsur.es and eitb.eus are public broadcasters' portals. The first three are in media_lifestyle; eitb.eus is not used.
- sanitas.es and asisa.es are health insurers that also run hospitals. They go in health. segurcaixaadeslas.es goes in banking_insurance.
- rankia.com and helpmycash.com are personal-finance media, so they go in banking_insurance. LatAm editions of rankia are on separate domains.
- legalbet.es and academiadeapuestas.es are betting trade media, so they go in betting_gaming. Their other countries are on separate domains.
- bolsasymercados.es (BME, the stock exchange) and bizum.com (payments) go in banking_insurance.
- selectra.es is a tariff comparator, so it goes in telco_utilities. rastreator.com is an insurance and finance comparator, so it goes in banking_insurance.
- coches.net and milanuncios.com are classifieds, so they go in ecommerce. casadellibro.com is a bookstore, so it goes in ecommerce (Italy's convention).
- dialnet.unirioja.es, the bibliographic database host, goes in publishing_education. The registrable domain unirioja.es is not used.
- metromadrid.es, tmb.cat and emtmadrid.es are urban transport, so they go in travel_tourism.
- portaventuraworld.com is a theme park in Spain, so it goes in travel_tourism. Its language paths are for foreign visitors.
- balearia.com has fr-FR and it-IT on the same host. I read these as language editions for travellers, since the ferry network is centred on Spain. This is a borderline host-rule call.

## Alias resolutions (A redirects to B: B kept once, A dropped)

agenciatributaria.es → agenciatributaria.gob.es; elcorteingles.com → elcorteingles.es; bcn.cat → barcelona.cat; ccma.cat → 3cat.cat; mitele.es → mediasetinfinity.es; masorange.es → orange.es (corporate subdomain); jazztel.es → jazztel.com; euskaltel.es → euskaltel.com; sergas.es → sergas.gal; osakidetza.eus → osakidetza.euskadi.eus; quironsalud.es → quironsalud.com; hospitalclinic.org → clinicbarcelona.org; aecc.es → contraelcancer.es; bizum.es → bizum.com; barcelonaturisme.com → thisisbarcelona.com; portaventura.es → portaventuraworld.com.

These aliases were dropped and their targets not used:
- lainformacion.com → 20minutos.es (path)
- niusdiario.es → telecinco.es
- elcultural.com → elespanol.com
- recetasderechupete.com → abc.es
- computerhoy.com → computerhoy.20minutos.es
- trasmediterranea.es → armastrasmediterranea.com
- turismodecanarias.com → turismodeislascanarias.com (hellocanaryislands.com used instead)
- ruralvia.com → grupocajarural.es
- raiolanetworks.es → raiolanetworks.com

These aliases went to the international list: cervantes.es → cervantes.org, wolterskluwer.es → wolterskluwer.com/es-es, elsevier.es → elsevier.com/es-es, smartick.es → smartick.com, hostinger.es → hostinger.com, gls-spain.es → gls-group.com, nh-hoteles.es → nh-hotels.com.

Redirects within the same registrable domain are kept as is: alcampo.es (compraonline.), kutxabank.es (portal.), guardiacivil.es (web.), larioja.org (web.).

## Dropped

- DNS failure on both bare and www: aeat.es (in Tranco). These knowledge-based guesses do not exist: seg-social.gob.es, sepe.gob.es, dgt.gob.es, trabajo.gob.es, aliexpress.es, bancoevo.es and jugarbien.es. The real hosts are seg-social.es, sepe.es and dgt.es.
- Host rule (20, moved to the international list):
  - news: elpais.com, marca.com, as.com
  - media_lifestyle: hola.com
  - publishing_education: penguinlibros.com, tirant.com, grupo-sm.com, smartick.com, wolterskluwer.com, elsevier.com, cervantes.org
  - travel_tourism: iberia.com, vueling.com, volotea.com, aireuropa.com (country selector known, JS shell, not verified here), destinia.com, centraldereservas.com, nh-hotels.com
  - telco_utilities: hostinger.com, gls-group.com
- Other:
  - 888.es and 888sport.es: same operator as 888casino.es, under the skin cap.
  - meteored.com: global host. tiempo.com is Meteored's Spain host.
  - efe.com: 403 here, and EFE runs regional editions (not verified). Left out rather than guessed.

## Clusters kept

- Autonomous communities (10): juntadeandalucia.es, gencat.cat, comunidad.madrid, gva.es, xunta.gal, euskadi.eus, jcyl.es, castillalamancha.es, aragon.es, gobiernodecanarias.org. Not used: navarra.es, carm.es, caib.es, juntaex.es, asturias.es, cantabria.es, larioja.org.
- Cities (3): madrid.es, barcelona.cat, valencia.es.
- Regional health services (6): sergas.gal, osakidetza.euskadi.eus, saludcastillayleon.es, murciasalud.es, ibsalut.es, astursalud.es.
- Universities (10): ucm.es, uned.es, ugr.es, upm.es, uv.es, us.es, uab.cat, unizar.es, ehu.eus, uoc.edu. dialnet.unirioja.es is a database host, not a university site.
- Vocento (4): elcorreo.com, diariovasco.com, diariosur.es, ideal.es.
- Prensa Ibérica regional (4): lne.es, farodevigo.es, levante-emv.com, informacion.es. elperiodico.com and sport.es also belong to Prensa Ibérica but are national/Catalan titles, not regional skins.
- Henneo: heraldo.es plus the national 20minutos.es.
- Mediaset: telecinco.es and mediasetinfinity.es. Atresmedia: antena3.com, atresplayer.com, lasexta.com.
- Adevinta: fotocasa.es, habitaclia.com, milanuncios.com, coches.net. These are distinct sites, not skins.

## Vantage-point sites (geo-redirect or geo-block from Italy)

- Redirect to the Italian .it site: betfair.es → betfair.it, williamhill.es → williamhill.it, 888casino.es → 888casino.it, pokerstars.es → pokerstars.it, betway.es → betway.it (then 522). Also not kept: 888.es, 888sport.es, daznbet.es.
- Redirect to the Italian subdomain: wallapop.com → it.wallapop.com.
- Geo-blocked (451 "Acceso no disponible"): luckia.es, leovegas.es. betsson.es ("403 Not Available") was not kept.
- iberia.com and vueling.com served their /it/ edition, but both are out under the host rule.

## Kept but not observable from here (48)

These returned 403, a challenge, 5xx or a timeout, or no robots.txt with a user-agent line:

lamoncloa.gob.es sedecatastro.gob.es citapreviadnie.es educacionfpydeportes.gob.es interior.gob.es guardiacivil.es ign.es xunta.gal hipertextual.com ucm.es alianzaeditorial.es santillana.es xtec.cat educarex.es educa.madrid.org superprof.es fnac.es decathlon.es leroymerlin.es manomano.es obramat.es ebay.es primor.eu sephora.es notino.es kiabi.es iryo.eu rumbo.es tripadvisor.es paradores.es turismo.gal museodelprado.es emtmadrid.es segurcaixaadeslas.es bizum.com filmin.es correos.es mrw.es loteriesdecatalunya.cat bwin.es luckia.es kirolbet.es retabet.es casinobarcelona.es leovegas.es betway.es idealista.com indomio.es

Several of these returned 403 but did serve robots.txt.

## Shortfalls

None. One gap: there is no horse-racing betting operator; nothing suitable was found among the candidates. ONCE is represented by juegosonce.es; the organisation site once.es is not used.

## Spam excluded from the Tranco tail

The Tranco tail has many unlicensed casino and SEO hosts (magius*, kinbet*, casinossinlicencia*, aviamasters*, chicken-road*, etc.). None were considered.

# REVISION 2 (primary market)
- Multi-country hosts are judged on their primary market; root routing and hreflang editions are evidence. From Italy, elpais.com, marca.com, as.com and hola.com serve their Spanish edition at the root, and Spain is their main market. From a US vantage elpais.com routes to /us/, so the root test alone does not decide.
- IN: elpais.com, marca.com, as.com (news), hola.com (media_lifestyle). OUT: diariodesevilla.es, ultimahora.es, relevo.com (news), mediasetinfinity.es (lowest-ranked media_lifestyle). maldita.es kept.
- sensacine.com stays here; it was removed from the French sample.
- pa tiers: regional = the 10 autonomous communities; local = madrid.es, barcelona.cat, valencia.es; the rest central.
