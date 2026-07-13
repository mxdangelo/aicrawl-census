"""Stage 0 — Build the stratified sample (domains.csv).

Usage: python build_sample.py
Hand-curated sector lists (July 2026), cross-checked against tranco_it.csv
(Tranco top-1M filtered to .it) for the popularity backbone. Foreign domain
hacks (redd.it, kahoot.it, iiko.it...) are excluded by construction.
Every domain is DNS-validated (bare host, else www. — run_fetch.py applies
the same fallback); domains that resolve neither way are dropped and listed.
"""
import csv
import socket
from concurrent.futures import ThreadPoolExecutor

import config

SECTORS = {
    # National/local press, wire services, broadcast news, sport and tech news.
    # Sources: ADS-audited outlets, Tranco .it top ranks.
    "news": [
        "repubblica.it", "corriere.it", "lastampa.it", "ilmessaggero.it",
        "ilmattino.it", "ilgiornale.it", "ilfattoquotidiano.it", "fanpage.it",
        "ansa.it", "adnkronos.com", "agi.it", "askanews.it", "ilpost.it",
        "huffingtonpost.it", "open.online", "linkiesta.it", "ilfoglio.it",
        "avvenire.it", "liberoquotidiano.it", "iltempo.it", "ilsecoloxix.it",
        "ilgazzettino.it", "leggo.it", "lanazione.it", "ilrestodelcarlino.it",
        "ilgiorno.it", "quotidiano.net", "gazzettadelsud.it", "lasicilia.it",
        "giornaledisicilia.it", "unionesarda.it", "lanuovasardegna.it",
        "iltirreno.it", "gazzettadiparma.it", "ecodibergamo.it",
        "giornaledibrescia.it", "messaggeroveneto.it", "varesenews.it",
        "bergamonews.it", "dire.it", "tpi.it", "rainews.it",
        "tgcom24.mediaset.it", "la7.it", "editorialedomani.it",
        "internazionale.it", "valigiablu.it", "ilmanifesto.it",
        "ilriformista.it", "italiaoggi.it", "milanofinanza.it",
        "ilsole24ore.com", "teleborsa.it", "affaritaliani.it", "dagospia.com",
        "gazzetta.it", "corrieredellosport.it", "tuttosport.com",
        "calciomercato.com", "tuttomercatoweb.com", "diretta.it",
        "transfermarkt.it", "eurosport.it", "giroditalia.it", "wired.it",
        "hdblog.it", "tomshw.it", "dday.it", "ilsoftware.it", "hwupgrade.it",
        "punto-informatico.it",
    ],
    # Marketplaces, price comparison, large retail with e-commerce.
    "ecommerce": [
        "amazon.it", "ebay.it", "zalando.it", "vinted.it", "subito.it",
        "bakeca.it", "trovaprezzi.it", "idealo.it", "eprice.it", "unieuro.it",
        "mediaworld.it", "euronics.it", "trony.it", "yeppon.it", "ibs.it",
        "lafeltrinelli.it", "mondadoristore.it", "hoepli.it", "libraccio.it",
        "abebooks.it", "decathlon.it", "leroymerlin.it", "tecnomat.it",
        "obi-italia.it", "bricofer.it", "manomano.it", "lidl.it",
        "esselunga.it", "carrefour.it", "conad.it", "eataly.it", "cortilia.it",
        "tannico.it", "vino.com", "callmewine.com", "bottegaverde.it",
        "douglas.it", "sephora.it", "notino.it", "pinalli.it",
        "kikocosmetics.com", "farmae.it", "luisaviaroma.com", "yoox.com",
        "ovs.it", "upim.com", "rinascente.it", "terranovastyle.com",
        "piazzaitalia.it", "benetton.com", "calzedonia.com", "intimissimi.com",
        "tezenis.com", "arcaplanet.it", "maxizoo.it", "zooplus.it",
        "westwing.it", "autoscout24.it", "automobile.it", "moto.it",
    ],
    # Central government, agencies/authorities, regions, major municipalities.
    # Sources: institutional directories; regions and top-population comuni.
    "pa": [
        "governo.it", "quirinale.it", "senato.it", "camera.it",
        "gazzettaufficiale.it", "normattiva.it", "esteri.it", "interno.gov.it",
        "giustizia.it", "difesa.it", "mef.gov.it", "mimit.gov.it",
        "mur.gov.it", "istruzione.it", "salute.gov.it", "lavoro.gov.it",
        "mase.gov.it", "cultura.gov.it", "mit.gov.it", "masaf.gov.it",
        "poliziadistato.it", "carabinieri.it", "gdf.gov.it", "vigilfuoco.it",
        "inps.it", "inail.it", "agenziaentrate.gov.it", "adm.gov.it",
        "istat.it", "bancaditalia.it", "consob.it", "ivass.it", "agcom.it",
        "arera.it", "garanteprivacy.it", "anac.gov.it", "agid.gov.it",
        "aifa.gov.it", "iss.it", "cnr.it", "aci.it", "pagopa.gov.it",
        "ilportaledellautomobilista.it", "gse.it",
        "regione.lombardia.it", "regione.lazio.it", "regione.veneto.it",
        "regione.piemonte.it", "regione.puglia.it",
        "regione.emilia-romagna.it", "regione.toscana.it",
        "regione.campania.it", "regione.liguria.it", "regione.marche.it",
        "regione.abruzzo.it", "regione.calabria.it", "regione.sardegna.it",
        "regione.sicilia.it", "regione.fvg.it", "regione.umbria.it",
        "regione.basilicata.it", "regione.molise.it", "regione.vda.it",
        "provincia.tn.it", "provincia.bz.it",
        "comune.roma.it", "comune.milano.it", "comune.napoli.it",
        "comune.torino.it", "comune.palermo.it", "comune.genova.it",
        "comune.bologna.it", "comune.firenze.it", "comune.bari.it",
        "comune.catania.it", "comune.venezia.it", "comune.verona.it",
        "comune.messina.it", "comune.padova.it", "comune.trieste.it",
        "comune.brescia.it", "comune.parma.it", "comune.prato.it",
        "comune.modena.it", "comune.perugia.it", "comune.cagliari.it",
    ],
    # Banks, payments, trading, insurance, financial comparators.
    "banking_insurance": [
        "intesasanpaolo.com", "unicredit.it", "bancobpm.it", "bper.it",
        "mps.it", "credem.it", "popso.it", "bancaifis.it", "mediobanca.com",
        "mediobancapremier.com", "finecobank.com", "ing.it",
        "bancamediolanum.it", "widiba.it", "sella.it", "bancagenerali.it",
        "bnl.it", "credit-agricole.it", "deutsche-bank.it", "poste.it",
        "nexi.it", "satispay.com", "hype.it", "scalapay.com", "moneyfarm.com",
        "directa.it", "borsaitaliana.it", "mutuionline.it", "facile.it",
        "segugio.it", "prestitionline.it",
        "generali.it", "unipol.it", "unipolsai.it", "allianz.it", "axa.it",
        "zurich.it", "realemutua.it", "vittoriaassicurazioni.com",
        "genertel.it", "quixa.it", "prima.it", "verti.it", "conte.it",
        "linear.it", "allianzdirect.it", "groupama.it", "helvetia.it",
        "gruppoitas.it",
    ],
    # Hospitals/care groups, health information, doctor booking,
    # online pharmacies, professional bodies.
    "health": [
        "humanitas.it", "grupposandonato.it", "policlinicogemelli.it",
        "hsr.it", "auxologico.it", "ieo.it", "ospedalebambinogesu.it",
        "gaslini.org", "meyer.it", "multimedica.it", "gvmnet.it",
        "ospedaleniguarda.it", "airc.it", "fondazioneveronesi.it",
        "telethon.it", "my-personaltrainer.it", "miodottore.it", "dottori.it",
        "idoctors.it", "paginemediche.it", "medicitalia.it", "pazienti.it",
        "nurse24.it", "quotidianosanita.it", "issalute.it", "vaccinarsi.org",
        "uppa.it", "ok-salute.it", "farmacosmo.it", "efarma.com",
        "1000farmacie.it", "farmaciauno.it", "docpeter.it",
        "farmacialoreto.it", "amicafarmacia.com", "drmax.it", "federfarma.it",
        "fnomceo.it", "fofi.it",
    ],
    # Transport, OTAs, regional tourism boards, hotels, museums.
    "travel_tourism": [
        "trenitalia.com", "lefrecce.it", "italotreno.com", "trenord.it",
        "flixbus.it", "itabus.it", "marinobus.it", "ita-airways.com",
        "aeroitalia.com", "adr.it", "moby.it", "tirrenia.it", "gnv.it",
        "snav.it", "grimaldi-lines.com", "traghettilines.it",
        "directferries.it", "edreams.it", "opodo.it", "volagratis.com",
        "lastminute.com", "skyscanner.it", "expedia.it", "tripadvisor.it",
        "thefork.it", "italia.it", "sardegnaturismo.it", "visittuscany.com",
        "visittrentino.info", "suedtirol.info", "veneto.eu",
        "in-lombardia.it", "visitpiemonte.com", "emiliaromagnaturismo.it",
        "viaggiareinpuglia.it", "visitlazio.com", "visitsicily.info",
        "touringclub.it", "siviaggia.it", "turistipercaso.it",
        "viamichelin.it", "agriturismo.it", "casevacanza.it", "campeggi.com",
        "bestwestern.it", "gruppouna.it", "nh-hotels.it", "starhotels.com",
        "uffizi.it", "pompeiisites.org", "museoegizio.it",
        "pinacotecabrera.org", "colosseo.it",
    ],
    # Listing portals, agency networks, renovation/building portals.
    "real_estate": [
        "immobiliare.it", "casa.it", "idealista.it", "wikicasa.it",
        "tecnocasa.it", "gabetti.it", "remax.it", "tempocasa.it",
        "professionecasa.it", "toscano.it", "fondocasa.it", "casavo.com",
        "dovevivo.com", "facileristrutturare.it", "habitissimo.it",
        "instapro.it", "edilportale.com", "infobuild.it", "lavorincasa.it",
        "cosedicasa.com", "borsinoimmobiliare.it", "monitorimmobiliare.it",
        "requadro.com", "scenari-immobiliari.it", "nomisma.it",
        "luxuryestate.com",
    ],
    # Book publishers, encyclopedias, universities, school/edu platforms.
    "publishing_education": [
        "treccani.it", "mondadori.it", "feltrinelli.it", "einaudi.it",
        "adelphi.it", "sellerio.it", "laterza.it", "ilmulino.it",
        "zanichelli.it", "loescher.it", "deagostini.it", "giunti.it",
        "garzanti.it", "longanesi.it", "salani.it", "edizionipiemme.it",
        "marsilioeditori.it", "minimumfax.com", "edizionisur.it",
        "nottetempo.it", "edizionieo.it", "ilsaggiatore.com", "neripozza.it",
        "bollatiboringhieri.it",
        "unibo.it", "unimi.it", "uniroma1.it", "uniroma2.it", "uniroma3.it",
        "polimi.it", "polito.it", "unito.it", "unipd.it", "unina.it",
        "unifi.it", "unipi.it", "unive.it", "unige.it", "univr.it",
        "unitn.it", "units.it", "unimib.it", "unibg.it", "unibs.it",
        "unisa.it", "uniba.it", "unict.it", "unipa.it", "unical.it",
        "unicatt.it", "luiss.it", "unibocconi.it", "sns.it",
        "santannapisa.it", "uniecampus.it", "unicusano.it", "unimarconi.it",
        "uninettunouniversity.net",
        "skuola.net", "studenti.it", "docsity.com", "redooc.com",
        "weschool.com", "orizzontescuola.it", "tecnicadellascuola.it",
        "tuttoscuola.com", "portaleargo.it", "madisoft.it", "cineca.it",
    ],
    # Telcos, ISPs, hosting, energy/water utilities, tariff comparators.
    "telco_utilities": [
        "tim.it", "vodafone.it", "windtre.it", "iliad.it", "fastweb.it",
        "tiscali.it", "eolo.it", "sky.it", "postemobile.it", "kenamobile.it",
        "verymobile.it", "coopvoce.it", "homobile.it", "aruba.it",
        "register.it", "seeweb.it", "netsons.com", "serverplan.com",
        "enel.it", "eni.com", "eniplenitude.com", "a2a.it", "gruppohera.it",
        "gruppoiren.it", "acea.it", "edison.it", "sorgenia.it", "engie.it",
        "octopusenergy.it", "eon-energia.com", "pulsee.it", "wekiwi.it",
        "illumia.it", "dolomitienergia.it", "terna.it", "snam.it",
        "italgas.it", "aqp.it", "gruppocap.it", "smatorino.it", "abbanoa.it",
        "sostariffe.it", "selectra.net", "switcho.it",
    ],
    # TV/streaming, radio, cinema/gaming/music media, food, weather,
    # women's magazines, tickets, mass portals.
    "media_lifestyle": [
        "rai.it", "raiplay.it", "mediaset.it", "comingsoon.it", "mymovies.it",
        "movieplayer.it", "badtaste.it", "everyeye.it", "multiplayer.it",
        "spaziogames.it", "rockol.it", "rollingstone.it", "allmusicitalia.it",
        "radioitalia.it", "deejay.it", "rtl.it", "radio105.it", "rds.it",
        "virginradio.it", "giallozafferano.it", "cucchiaio.it", "misya.info",
        "fattoincasadabenedetta.it", "cookist.it", "dissapore.com",
        "gamberorosso.it", "agrodolce.it", "ilmeteo.it", "3bmeteo.it",
        "meteo.it", "vanityfair.it", "vogue.it", "grazia.it", "iodonna.it",
        "amica.it", "dilei.it", "alfemminile.com", "donnamoderna.com",
        "nostrofiglio.it", "pianetamamma.it", "ticketone.it",
        "ticketmaster.it", "vivaticket.com", "aranzulla.it", "virgilio.it",
        "libero.it", "paginegialle.it", "paginebianche.it",
    ],
}


def resolves(domain: str) -> bool:
    for host in (domain, f"www.{domain}"):
        try:
            socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
            return True
        except OSError:
            continue
    return False


def main():
    socket.setdefaulttimeout(5)
    rows, seen = [], set()
    for sector, domains in SECTORS.items():
        for dom in domains:
            dom = dom.strip().lower()
            if dom in seen:
                print(f"  duplicate skipped: {dom} ({sector})")
                continue
            seen.add(dom)
            rows.append((dom, sector))

    print(f"{len(rows)} domains, checking DNS...")
    with ThreadPoolExecutor(max_workers=16) as ex:
        ok_flags = list(ex.map(resolves, (d for d, _ in rows)))

    # parallel bursts can exhaust the local resolver: recheck failures slowly
    for i, ((dom, _), ok) in enumerate(zip(rows, ok_flags)):
        if not ok:
            ok_flags[i] = resolves(dom)

    dropped = [d for (d, _), ok in zip(rows, ok_flags) if not ok]
    kept = [(d, s) for (d, s), ok in zip(rows, ok_flags) if ok]

    with open(config.DOMAINS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["domain", "sector"])
        w.writerows(kept)

    print(f"\nWritten {config.DOMAINS_CSV}: {len(kept)} domains "
          f"({len(dropped)} dropped for DNS).")
    per_sector = {}
    for _, s in kept:
        per_sector[s] = per_sector.get(s, 0) + 1
    for s, n in sorted(per_sector.items(), key=lambda kv: -kv[1]):
        print(f"  {s}: {n}")
    if dropped:
        print("\nDropped (no DNS, bare or www.):")
        for d in dropped:
            print(f"  {d}")


if __name__ == "__main__":
    main()
