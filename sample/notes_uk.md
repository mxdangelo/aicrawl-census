# United Kingdom sample — draft notes (2026-10-02)

804 domains, every sector at quota, no shortfall. Probed from Italy with curl_cffi (chrome). Candidates: Tranco .uk list (top ~4000 skimmed, keyword greps deeper) plus UK-first non-.uk hosts from knowledge, all DNS-checked and probed.

## Per sector

- pa: 115/115
- news: 111/111
- publishing_education: 96/96
- ecommerce: 81/81
- travel_tourism: 73/73
- banking_insurance: 66/66
- media_lifestyle: 64/64
- telco_utilities: 59/59
- health: 53/53
- betting_gaming: 51/51
- real_estate: 35/35

## Borderline sector calls

- bbc.co.uk -> news (public-broadcaster host, news-led); news.sky.com -> news; itv.com, channel4.com, channel5.com, u.co.uk, sky.com, nowtv.com -> media_lifestyle.
- lbc.co.uk, talksport.com -> media_lifestyle (radio); skysports.com, tntsports.co.uk, racingpost.com, sportinglife.com -> news (sport).
- citizensadvice.org.uk, moneyhelper.org.uk -> pa (publicly funded advice services); tvlicensing.co.uk -> pa (licence-fee collection for the BBC); bbfc.co.uk, asa.org.uk -> pa (statutory-designated / co-regulators).
- cqc.org.uk -> pa (regulator); nice.org.uk, nhsbsa, nhsbt, blood.co.uk -> health. nihr.ac.uk, ukri.org and public research centres (bgs, ceh, bas, noc, npl, diamond, turing) -> pa.
- tfl.gov.uk, networkrail.co.uk -> travel_tourism (transport operators, though public bodies).
- moneysupermarket.com, uswitch.com, broadbandchoices.co.uk -> telco_utilities (price comparators go in telco_utilities); comparethemarket.com, gocompare.com, confused.com -> banking_insurance (insurance-led).
- postoffice.co.uk -> telco_utilities (postal network). moneysavingexpert.com, thisismoney.co.uk -> banking_insurance (personal-finance media). bupa.co.uk -> health; vitality.co.uk, saga.co.uk, petplan.co.uk -> banking_insurance.
- which.co.uk -> ecommerce (consumer product testing); just-eat, deliveroo -> ecommerce; autotrader, carwow, cinch, webuyanycar -> ecommerce (car classifieds/retail); hotukdeals, vouchercodes, topcashback, pricespy -> ecommerce (deals).
- specsavers.co.uk -> health (optician); boots.com, superdrug.com -> ecommerce (retail-led).
- checkatrade, mybuilder, ratedpeople, houzz, homebuilding.co.uk -> real_estate (renovation); peabody, clarionhg, placesforpeople, lqgroup -> real_estate (housing associations).
- sbcnews.co.uk, whichbingo.co.uk -> betting_gaming (trade/comparison media); postcodelottery, healthlottery, lottery.co.uk (results) -> betting_gaming; 49s.co.uk (numbers draw) -> betting_gaming.
- lrb.co.uk, the-tls.com -> publishing_education (literary reviews); bailii.org, iclr.co.uk, lexisnexis.co.uk -> publishing_education (legal databases/publishers).
- jet2.com and nationalexpress.com carry de-de/fr-fr hreflang language versions but sell a UK-only product (flights from UK airports, the UK coach network): kept: a single-country host addressing foreign visitors is national. seasaltcornwall, theperfumeshop (cut anyway), comparethemarket: gb+ie only, treated as UK.
- theguardian.com OUT as a multi-country host (UK/US/AU/Europe editions on one host; landed on /europe from Italy). Same for spectator.com (spectator.co.uk now 301s there; gb+us hreflang).
- eurogamer.net, rockpapershotgun.com, vg247.com, pushsquare.com, ladbible.com, unilad.com: UK-HQ English sites with large global audiences, no country editions detected -> kept as UK-first; arguable, given their audiences.

## Alias resolutions (alias -> kept or noted target)

os.uk -> ordnancesurvey.co.uk, scotland.gov.uk -> gov.scot, actionfraud.police.uk -> reportfraud.police.uk, mrc.ac.uk -> ukri.org, nerc.ac.uk -> ukri.org, stfc.ac.uk -> ukri.org, epsrc.ac.uk -> ukri.org, bbsrc.ac.uk -> ukri.org, great.gov.uk -> business.gov.uk, ukho.gov.uk -> admiralty.co.uk, food.gov.uk -> gov.uk, companieshouse.gov.uk -> gov.uk, mhra.gov.uk -> gov.uk, dvla.gov.uk -> gov.uk, environment-agency.gov.uk -> gov.uk, number10.gov.uk -> gov.uk, guardian.co.uk -> theguardian.com, thetimes.co.uk -> thetimes.com, theregister.co.uk -> theregister.com, spectator.co.uk -> spectator.com, theweek.co.uk -> theweek.com, pinknews.co.uk -> thepinknews.com, theneweuropean.co.uk -> thenewworld.co.uk, eurosport.co.uk -> tntsports.co.uk, wired.co.uk -> wired.com, pcpro.co.uk -> magazinesdirect.com, itpro.co.uk -> itpro.com, techadvisor.co.uk -> techadvisor.com, honestjohn.co.uk -> drive.co.uk, planetradio.co.uk -> hellorayo.co.uk, whatsontv.co.uk -> whattowatch.com, womanmagazine.co.uk -> goodto.com, yahoo.co.uk -> uk.yahoo.com, goodhousekeeping.co.uk -> goodhousekeeping.com, itvx.com -> itv.com, uktv.co.uk -> u.co.uk, llgc.org.uk -> llyfrgell.cymru, library.wales -> llyfrgell.cymru, the-tls.co.uk -> the-tls.com, open.edu -> open.ac.uk, ic.ac.uk -> imperial.ac.uk, soton.ac.uk -> southampton.ac.uk, bris.ac.uk -> bristol.ac.uk, shef.ac.uk -> sheffield.ac.uk, bham.ac.uk -> birmingham.ac.uk, cf.ac.uk -> cardiff.ac.uk, liv.ac.uk -> liverpool.ac.uk, tandf.co.uk -> taylorandfrancis.com, johnlewis.co.uk -> johnlewis.com, homebargains.co.uk -> home.bargains, motors.co.uk -> cazoo.co.uk, boden.co.uk -> boden.com, trainline.com -> thetrainline.com, holidayextras.co.uk -> holidayextras.com, lloydsbank.co.uk -> lloydsbank.com, nutmeg.com -> personalinvesting.jpmorgan.com, sainsburysbank.co.uk -> money.sainsburys.co.uk, prudential.co.uk -> group.mandg.com, clearpay.co.uk -> clearpay.com, plusnet.co.uk -> plus.net, plusnet.com -> plus.net, krystal.uk -> krystal.io, cable.co.uk -> bestbroadbanddeals.co.uk, dhlecommerce.co.uk -> dhl.com, wales.nhs.uk -> nhs.wales, netdoctor.co.uk -> womenshealthmag.com, chemist4u.com -> chemist-4-u.com, homesandproperty.co.uk -> standard.co.uk, jll.co.uk -> jll.com, vickers.bet -> betvickers.com, footballpools.com -> thepools.com, statisticsauthority.gov.uk -> uksa.statisticsauthority.gov.uk, mod.uk -> gov.uk, charitycommission.gov.uk -> gov.uk, ofsted.gov.uk -> gov.uk, naturalengland.org.uk -> gov.uk, civilservice.gov.uk -> gov.uk, landregistry.gov.uk -> gov.uk, ukhsa.gov.uk -> gov.uk, whsmith.co.uk -> whsmithplc.co.uk (corporate), cex.co.uk -> webuy.com (it.webuy.com from IT)

All ministry/agency hosts that 301 to www.gov.uk (food, companieshouse, mhra, dvla, environment-agency, number10, mod.uk, charitycommission, ofsted, naturalengland, civilservice, landregistry, ukhsa) are counted once as gov.uk.

## Dropped

- DNS failure (bare and www): thenationalinvestmentbank.com, evening-times.co.uk, bbcgoodfood.co.uk, iplayer.bbc.co.uk, readersdigest.co.uk, practicallaw.thomsonreuters.com, reeds-rains.co.uk, golfmonthly.co.uk
- Bad redirect / not the intended site: fool.co.uk (redirects to unrelated twelfthmagpie.com), plum.com (not Plum (redirects to pacs.com))
- Host rule (multi-country/global host) -> international list: theguardian.com, planetrugby.com, itpro.com, t3.com, pocket-lint.com, theconversation.com, womanandhome.com, hellomagazine.com, seetickets.com, loudersound.com, timeout.com, usborne.com, ospreypublishing.com, tes.com, senecalearning.com, timeshighereducation.com, futurelearn.com, cambridge.org, bloomsbury.com, dk.com, britishcouncil.org, teachingenglish.org.uk, asos.com, lookfantastic.com, selfridges.com, whitestuff.com, newlook.com, riverisland.com, mandmdirect.com, tkmaxx.com, shpock.com, depop.com, megabus.com, premierinn.com, virginatlantic.com, britishairways.com, easyjet.com, eurostar.com, skyscanner.net, doctify.com, bet365.com, betfair.com, boylesports.com, 888sport.com, 888casino.com, livescorebet.com, oddschecker.com, videoslots.com, spectator.com, givemesport.com, squawka.com, thetrainline.com, clearpay.com, thomsonreuters.co.uk, oup.co.uk, vodafone.com
- Excluded: rialtocasino.com (unverified operator), mrvegas.com (forbidden-country page, low rank)
- Infrastructure: nominet.uk (.uk registry) cut. Tranco infra skipped at skim: awsdns-*, livedns, nominetdns, amzndns, ultradns, bbci/guim/ophan CDN hosts, adult/piracy/spam (urban*bets*.uk farm, manga mirrors, togel).
- Cut for caps/quota (eligible, not selected):
  - pa: ukaea.uk thecrownestate.co.uk nomisweb.co.uk apprenticeships.gov.uk planningportal.co.uk ipo.gov.uk gro.gov.uk lawcom.gov.uk iwf.org.uk ipso.co.uk admiralty.co.uk
  - news: drive.co.uk boxingnewsonline.net theconstructionindex.co.uk farminguk.com broadcastnow.co.uk fenews.co.uk civilsociety.co.uk thirdsector.co.uk communitycare.co.uk legalfutures.co.uk travelweekly.co.uk fleetnews.co.uk thelincolnite.co.uk islandecho.co.uk blogpreston.co.uk churchtimes.co.uk catholicherald.co.uk thetablet.co.uk socialistworker.co.uk tribunemag.co.uk spiked-online.com labourlist.org leftfootforward.org order-order.com londonworld.com
  - publishing_education: ukdataservice.ac.uk webarchive.org.uk quarto.com encyclopedia.com wellcome.org letterjoin.co.uk
  - ecommerce: preloved.co.uk freeads.co.uk cargurus.co.uk motorpoint.co.uk idealo.co.uk latestdeals.co.uk groupon.co.uk funkypigeon.com blackwells.co.uk foyles.co.uk appliancesdirect.co.uk markselectrical.co.uk richersounds.com scan.co.uk overclockers.co.uk box.co.uk laptopsdirect.co.uk autodoc.co.uk zooplus.co.uk viovet.co.uk hellofresh.co.uk wilko.com fenwick.co.uk jacamo.co.uk simplybe.co.uk jdwilliams.co.uk fatface.com seasaltcornwall.com theperfumeshop.com thefragranceshop.co.uk ernestjones.co.uk hsamuel.co.uk lovehoney.co.uk thomann.co.uk ebuyer.com cazoo.co.uk
  - travel_tourism: eastmidlandsrailway.co.uk thameslinkrailway.com southernrailway.com tpexpress.co.uk westmidlandsrailway.co.uk bristolairport.co.uk london-luton.co.uk arrivabus.co.uk flixbus.co.uk stenaline.co.uk brittany-ferries.co.uk redfunnel.co.uk wightlink.co.uk condorferries.co.uk kayak.co.uk opodo.co.uk trivago.co.uk cottages.com holidaycottages.co.uk parkdeanresorts.co.uk warnerhotels.co.uk visitcornwall.com visitbath.co.uk npg.org.uk thorpepark.com caravanclub.co.uk avis.co.uk hertz.co.uk europcar.co.uk ncp.co.uk justpark.com nationalexpress.co.uk liverpoolmuseums.org.uk royalparks.org.uk canalrivertrust.org.uk dayoutwiththekids.co.uk haystravel.co.uk kuoni.co.uk travelrepublic.co.uk sixt.co.uk
  - banking_insurance: sheilaswheels.com hiscox.co.uk adrianflux.co.uk bennetts.co.uk staysure.co.uk aegon.co.uk sjp.co.uk transunion.co.uk unbiased.co.uk citywire.co.uk investorschronicle.co.uk moneyfactscompare.co.uk money.co.uk lse.co.uk interactivebrokers.co.uk kroo.com chip.co.uk moneybox.com freetrade.io quidco.com marcus.co.uk ukfinance.org.uk abi.org.uk cii.co.uk
  - media_lifestyle: tidetimes.org.uk yourweather.co.uk redonline.co.uk prima.co.uk closeronline.co.uk houseandgarden.co.uk countrylife.co.uk ticketsource.co.uk atgtickets.com londontheatre.co.uk thetab.com chortle.co.uk comedy.co.uk royalalberthall.com barbican.org.uk kerrang.com freeview.co.uk thegreatbritishbakeoff.co.uk uncut.co.uk gramophone.co.uk filmstories.co.uk downdetector.co.uk goodto.com whattowatch.com
  - telco_utilities: heartinternet.uk names.co.uk nominet.uk enwl.co.uk northernpowergrid.com dpdlocal.co.uk energysavingtrust.org.uk mobiles.co.uk carphonewarehouse.co.uk lycamobile.co.uk sse.co.uk bestbroadbanddeals.co.uk
  - health: jobs.nhs.uk healthcareers.nhs.uk e-lfh.org.uk hra.nhs.uk simpleonlinepharmacy.co.uk rcseng.ac.uk rcpsych.ac.uk rcog.org.uk rcpch.ac.uk hcpc-uk.org gdc-uk.org csp.org.uk stroke.org.uk asthmaandlung.org.uk parkinsons.org.uk mssociety.org.uk rethink.org mariecurie.org.uk nuffieldtrust.org.uk health.org.uk visionexpress.com drinkaware.co.uk topdoctors.co.uk diabetes.co.uk healthwatch.co.uk travelhealthpro.org.uk fitfortravel.nhs.uk hee.nhs.uk babycentre.co.uk counselling-directory.org.uk
  - betting_gaming: 10bet.co.uk 7bet.co.uk hollywoodbets.co.uk megacasino.co.uk thesunvegas.co.uk wikibingo.co.uk tombolaarcade.co.uk gamstop.co.uk casino.co.uk betvickers.com
  - real_estate: millerhomes.co.uk bovishomes.co.uk homegroup.org.uk nhg.org.uk propertymark.co.uk landlordzone.co.uk unihomes.co.uk accommodationforstudents.com getagent.co.uk eigpropertyauctions.co.uk cbre.co.uk estatesgazette.co.uk landlordtoday.co.uk estateagenttoday.co.uk insidehousing.co.uk newhomesforsale.co.uk chimnie.co.uk housemetric.co.uk nethouseprices.com propertyredress.co.uk sanctuary.co.uk homeflow.co.uk sequencehome.co.uk dexters.co.uk
  - university cap: durham.ac.uk ncl.ac.uk qmul.ac.uk bath.ac.uk lancaster.ac.uk lboro.ac.uk arts.ac.uk liverpool.ac.uk york.ac.uk exeter.ac.uk
  - council cap: cityoflondon.gov.uk westminster.gov.uk liverpool.gov.uk sheffield.gov.uk hants.gov.uk greatermanchester-ca.gov.uk
  - council association, council cap: londoncouncils.gov.uk
  - police cap: btp.police.uk college.police.uk
  - trust cap: moorfields.nhs.uk
  - Reach cap: bristolpost.co.uk football.london mylondon.news nottinghampost.com business-live.co.uk
  - Newsquest cap: dailyecho.co.uk yorkpress.co.uk glasgowtimes.co.uk eadt.co.uk thenational.scot
  - National World cap: lep.co.uk

## Clusters kept

- gov.uk counted once; separate gov.uk-family hosts kept: blog.gov.uk, data.gov.uk, legislation.gov.uk, business.gov.uk, nationalarchives.gov.uk, ons.gov.uk etc.
- Devolved: gov.scot, mygov.scot, parliament.scot, gov.wales, senedd.wales, nidirect.gov.uk, niassembly.gov.uk + Scottish/NI agencies (nrscotland, scotlandspeople, revenue.scot, transport.gov.scot, nature.scot, historicenvironment.scot, sepa, nisra, finance-ni, daera-ni).
- Councils (10): birmingham, leeds, manchester, bristol, cornwall, kent, glasgow, edinburgh, cardiff, belfastcity. london.gov.uk (GLA) counted as regional government.
- Police (4 forces + national): met, gmp, scotland, psni + police.uk, reportfraud.police.uk.
- NHS trusts (6): guysandstthomas, mft, gosh, uclh, cuh, ouh.
- Universities (20): ox, cam, ucl, ed, lse, manchester, gla, imperial, warwick, kcl, leeds, open, bristol, nottingham, southampton, birmingham, st-andrews, sheffield, cardiff, qub.
- UKRI family: ukri.org only (mrc/nerc/stfc/epsrc/bbsrc all 301 there); research centres bgs, ceh, bas, noc, diamond kept as own hosts.
- Reach regionals (5): manchestereveningnews, walesonline, liverpoolecho, birminghammail, chroniclelive (+ Reach nationals mirror, express, dailystar, dailyrecord counted as national titles).
- Newsquest (5): heraldscotland, oxfordmail, thenorthernecho, theargus, edp24. National World (5): scotsman, yorkshirepost, newsletter, thestar, portsmouth. DC Thomson (2): thecourier, pressandjournal.
- Global radio (Global Media): globalplayer, heart, capitalfm, classicfm, smoothradio, radiox, lbc (7, distinct brands not template sites). Bauer: hellorayo.
- Flutter UK: paddypower, skybet; Entain: ladbrokes, coral, foxybingo, galabingo, galaspins; Rank: grosvenorcasinos, meccabingo; Broadway Gaming: sunbingo, heartbingo; water companies (12) and DNOs (ukpowernetworks, ssen, nationalgrid, cadent, sgn).

## Vantage-point sites (geo-redirect or geo-block from the Italian IP; UK host kept)

dailymail.co.uk (301 to dailymail.com from IT), williamhill.com (301 to williamhill.it), betway.co.uk (redirects to betway.it), pokerstars.uk (redirects to pokerstars.it), nowtv.com (307 to nowtv.it), channel5.com (geo-restriction page), betano.co.uk (HTTP 451 (unavailable for legal reasons)), betmgm.co.uk (HTTP 451 (unavailable for legal reasons)), betuk.com (HTTP 451 (unavailable for legal reasons)), betvictor.com (HTTP 451 (unavailable for legal reasons)), heartbingo.co.uk (HTTP 451 (unavailable for legal reasons)), leovegas.co.uk (HTTP 451 (unavailable for legal reasons)), parimatch.co.uk (HTTP 451 (unavailable for legal reasons)), pinkcasino.co.uk (HTTP 451 (unavailable for legal reasons))

## Not observable from here (kept)

- 98 kept sites returned >=400 / challenge / connection error on the homepage: accountingweb.co.uk anglianwater.co.uk ao.com argos.co.uk artscouncil.org.uk asda.com autotrader.co.uk betano.co.uk betfred.com betmgm.co.uk betuk.com betvictor.com betway.co.uk birminghamairport.co.uk broadbandchoices.co.uk cardiff.gov.uk checkatrade.com circlehealthgroup.co.uk conservativehome.com coral.co.uk corbettmaths.com crosscountrytrains.co.uk decathlon.co.uk dfs.co.uk digital.nhs.uk ebay.co.uk electoralcommission.org.uk equalityhumanrights.com expedia.co.uk faber.co.uk fca.org.uk fitzdares.com foxybingo.com galabingo.com galaspins.com glasgow.gov.uk gmp.police.uk greateranglia.co.uk hamptons.co.uk heartbingo.co.uk hesa.ac.uk historicengland.org.uk historylearningsite.co.uk hobbycraft.co.uk homebase.co.uk idmobile.co.uk insidermedia.com jisc.ac.uk kentonline.co.uk ladbrokes.com leovegas.co.uk liverpooluniversitypress.co.uk loveholidays.com lv.com manchesteruniversitypress.co.uk met.police.uk moneyhelper.org.uk moneysupermarket.com nationalgrid.co.uk news.sky.com nhm.ac.uk northernrailway.co.uk notino.co.uk obr.uk odeon.co.uk ofcom.org.uk open.ac.uk paddypower.com parimatch.co.uk pinkcasino.co.uk police.uk pressandjournal.co.uk quinnbet.com ratedpeople.com retailgazette.co.uk royal.uk sephora.co.uk severntrent.com skybet.com southbankcentre.co.uk southernwater.co.uk stagecoachbus.com starsports.bet stwater.co.uk superprof.co.uk telegraph.co.uk thecourier.co.uk thepools.com tripadvisor.co.uk tui.co.uk tvlicensing.co.uk ucl.ac.uk unbound.co.uk universitiesuk.ac.uk very.co.uk walker.co.uk waterstones.com wowcher.co.uk
- 49 more answered but /robots.txt had no user-agent line: affinitywater.co.uk bailii.org bas.ac.uk belfastcity.gov.uk bfi.org.uk blood.co.uk bma.org.uk caa.co.uk channel5.com chase.co.uk chemguide.co.uk citizensadvice.org.uk costco.co.uk diamond.ac.uk educationendowmentfoundation.org.uk england.nhs.uk gchq.gov.uk giffgaff.com gwr.com hfea.gov.uk homeswapper.co.uk jdsports.co.uk justice.gov.uk justiceinspectorates.gov.uk leeds.ac.uk legislation.gov.uk loganair.co.uk lqgroup.org.uk manchester.gov.uk ncsc.gov.uk nhsbt.nhs.uk ocado.com ons.gov.uk organdonation.nhs.uk ouh.nhs.uk pen-and-sword.co.uk petplan.co.uk private-eye.co.uk rcplondon.ac.uk scottishwater.co.uk sentencingcouncil.org.uk sepa.org.uk size.co.uk so.energy sportinglife.com tote.co.uk weatheronline.co.uk yorkshirewater.com zoopla.co.uk

## Shortfalls

None.

# REVISION 2 (primary market)
- Multi-country hosts are judged on their primary market. Root routing seen from a third country and country-coded hreflang editions are evidence; neither decides alone.
- asos.com IN (ecommerce): its root serves the UK edition (en-GB) to a visitor from Italy, and the UK is its main market. gousto.co.uk OUT (lowest-ranked ecommerce site).
- theguardian.com and bet365.com stay on the international list: the Guardian routes foreign visitors to its European or US edition; bet365.com declares 19 country editions.
- pa tiers: regional = the devolved administrations of Scotland, Wales and Northern Ireland and their bodies, the Greater London Authority, territorial police forces (met.police.uk, gmp.police.uk, psni.police.uk, scotland.police.uk); local = the 10 councils; everything else central, including police.uk and England-only bodies.
