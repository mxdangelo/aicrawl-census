"""Stage 2+3 — Validation, parsing, normalization into verdicts.

Usage: python run_parse.py [--lite]
Reads the fetches table, writes files, verdicts, robots_meta, llms_meta,
tdmrep_meta and updates site_meta with the CMS fingerprint.

--lite re-derives what a database without raw bodies still allows
(census-lite*.db and the snapshots kept in git history): verdicts from
robots_meta.parsed_json and the TDMRep header channel from the homepage
headers. Everything else is left as it is; a robots.txt whose first group was
lost to a UTF-8 BOM stays lost, since parsed_json never saw it.
"""
import argparse
import json

import config
from censuslib import db, fingerprint, robots as rb, textfiles as tf


def decode(body: bytes) -> str:
    for enc in ("utf-8-sig", "latin-1"):  # -sig: drop a leading BOM
        try:
            return body.decode(enc)
        except (UnicodeDecodeError, AttributeError):
            continue
    return ""


def write_verdicts(con, dom, parsed):
    """One verdicts row per AI crawler; parsed=None means no valid robots.txt."""
    for token, (op, purpose) in config.AI_CRAWLERS.items():
        if parsed is None:
            row = (dom, token, op, purpose, 0, "allowed", "no_robots")
        else:
            verdict, source, mentioned = rb.verdict_for(parsed, token)
            row = (dom, token, op, purpose, int(mentioned), verdict, source)
        con.execute("INSERT OR REPLACE INTO verdicts VALUES (?,?,?,?,?,?,?)", row)


def lite(con):
    """Rebuild verdicts from the parsed robots.txt kept in robots_meta, and the
    TDMRep header flag from the stored headers. Only robots.txt files still
    valid count: robots_meta can hold rows of files that have since
    disappeared."""
    rows = con.execute("""SELECT f.domain, r.parsed_json FROM files f
                           LEFT JOIN robots_meta r USING (domain)
                           WHERE f.resource = 'robots'""").fetchall()
    present = {d for d, in con.execute(
        "SELECT domain FROM files WHERE resource = 'robots' AND present = 1")}
    con.execute("DELETE FROM verdicts")
    for dom, pj in rows:
        parsed = None
        if dom in present and pj:
            p = json.loads(pj)
            parsed = rb.Robots(groups=[
                rb.Group(agents=g["agents"], rules=[tuple(r) for r in g["rules"]])
                for g in p["groups"]])
        write_verdicts(con, dom, parsed)
    for dom, hdrs in con.execute("""SELECT t.domain, x.headers_json FROM tdmrep_meta t
                                    JOIN fetches x ON x.domain = t.domain
                                    AND x.resource = 'home'""").fetchall():
        con.execute("UPDATE tdmrep_meta SET via_header = ? WHERE domain = ?",
                    (int(tf.tdm_headers(json.loads(hdrs))), dom))
    con.commit()
    print(f"Verdicts and TDMRep headers re-derived for {len(rows)} domains.")


def main():
    con = db.connect(config.DB_PATH)
    domains = [r[0] for r in con.execute("SELECT domain FROM site_meta")]
    ai_tokens = list(config.AI_CRAWLERS)

    # Full rebuild from fetches. Each branch below writes only when a file is
    # valid, so a row left from an earlier pass would outlive its file (a site
    # now answering 403 kept counting as an llms.txt publisher).
    for t in ("files", "verdicts", "robots_meta", "llms_meta", "tdmrep_meta"):
        con.execute(f"DELETE FROM {t}")
    con.execute("UPDATE site_meta SET cms = NULL, seo_plugin = NULL, cdn = NULL")

    for dom in domains:
        rows = {r[0]: r for r in con.execute(
            "SELECT resource, status, content_type, body, headers_json "
            "FROM fetches WHERE domain = ?", (dom,))}

        # ---- robots.txt ----
        if "robots" in rows:
            _, status, ctype, body, _ = rows["robots"]
            text = decode(body)
            ok, reason = tf.validate_robots(status, ctype, text)
            con.execute("INSERT OR REPLACE INTO files VALUES (?,?,?,?)",
                        (dom, "robots", int(ok), reason))
            if ok:
                parsed = rb.parse(text)
                block_text, block_hash = rb.ai_block(parsed, ai_tokens)
                comments = " ".join(c for _, c in parsed.comments)
                con.execute(
                    "INSERT OR REPLACE INTO robots_meta VALUES (?,?,?,?,?,?,?,?)",
                    (dom, len(parsed.groups), parsed.n_lines,
                     len(parsed.comments), block_hash, block_text,
                     ",".join(rb.signatures(comments)),
                     json.dumps(rb.as_dict(parsed))))
                write_verdicts(con, dom, parsed)
            else:
                write_verdicts(con, dom, None)

        # ---- llms.txt + llms-full.txt ----
        full_ok, full_text = False, ""
        if "llms_full" in rows:
            _, status, ctype, body, _ = rows["llms_full"]
            full_text = decode(body)
            full_ok, full_reason = tf.validate_llms(status, ctype, full_text)
            con.execute("INSERT OR REPLACE INTO files VALUES (?,?,?,?)",
                        (dom, "llms_full", int(full_ok), full_reason))
        if "llms" in rows:
            _, status, ctype, body, _ = rows["llms"]
            text = decode(body)
            ok, reason = tf.validate_llms(status, ctype, text)
            con.execute("INSERT OR REPLACE INTO files VALUES (?,?,?,?)",
                        (dom, "llms", int(ok), reason))
            # structure from the index if present, else from the -full
            # (sites with only llms-full.txt: valid=0, has_llms_full=1)
            src = text if ok else (full_text if full_ok else None)
            if src is not None:
                m = tf.parse_llms(src)
                llms_hash = tf.norm_hash(text) if ok else ""
                full_hash = tf.norm_hash(full_text) if full_ok else ""
                same = int(ok and full_ok and llms_hash == full_hash)
                similarity = (round(tf.text_similarity(text, full_text), 3)
                              if ok and full_ok else None)
                # instruction language: union over whichever files are valid
                signals = tf.instruction_signals(
                    (text if ok else "") + "\n" + (full_text if full_ok else ""))
                has_instr = int(any(s not in tf.WEAK_SIGNALS for s in signals))
                con.execute(
                    "INSERT OR REPLACE INTO llms_meta "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (dom, int(ok), m["h1"], m["has_blockquote"],
                     m["n_sections"], m["n_links"], m["n_chars"],
                     int(full_ok), llms_hash, full_hash, same, similarity,
                     has_instr, ",".join(signals),
                     ",".join(rb.signatures(src)),
                     json.dumps(tf.parse_llms_sections(src))))

        # ---- tdmrep.json ----
        if "tdmrep" in rows:
            _, status, ctype, body, hdrs_json = rows["tdmrep"]
            text = decode(body)
            ok, reason = tf.validate_tdmrep(status, ctype, text)
            con.execute("INSERT OR REPLACE INTO files VALUES (?,?,?,?)",
                        (dom, "tdmrep", int(ok), reason))
            via_header, via_meta = 0, 0
            if "home" in rows:
                via_header = int(tf.tdm_headers(json.loads(rows["home"][4])))
                via_meta = int(tf.tdm_meta(decode(rows["home"][3])))
            if ok:
                m = tf.parse_tdmrep(text)
                con.execute(
                    "INSERT OR REPLACE INTO tdmrep_meta VALUES (?,?,?,?,?,?,?,?)",
                    (dom, 1, m["n_rules"], m["reservation_root"],
                     m["has_policy"], via_header, via_meta,
                     json.dumps(json.loads(text))))
            elif via_header or via_meta:
                con.execute(
                    "INSERT OR REPLACE INTO tdmrep_meta VALUES (?,?,?,?,?,?,?,?)",
                    (dom, 0, 0, None, 0, via_header, via_meta, None))

        # ---- homepage: fingerprint ----
        if "home" in rows:
            _, status, _, body, hdrs_json = rows["home"]
            if status == 200:
                fp = fingerprint.fingerprint(decode(body), json.loads(hdrs_json))
                con.execute(
                    "UPDATE site_meta SET cms=?, seo_plugin=?, cdn=? "
                    "WHERE domain=?",
                    (fp["cms"], fp["seo_plugin"], fp["cdn"], dom))

    con.commit()
    print("Parsing done.")
    for row in con.execute(
        "SELECT resource, present, COUNT(*) FROM files "
        "GROUP BY resource, present ORDER BY resource"):
        print(f"  {row[0]}: present={row[1]} -> {row[2]} domains")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lite", action="store_true")
    if ap.parse_args().lite:
        lite(db.connect(config.DB_PATH))
    else:
        main()
