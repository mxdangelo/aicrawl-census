"""Stage 4 — Clustering of AI templates in robots.txt.

Exact match via hash, then near-duplicates via Jaccard on lines.
Output: clusters table + on-screen report of the largest clusters
for manual attribution to generators.
"""
import sqlite3
from collections import defaultdict

import config

JACCARD_THRESHOLD = 0.8


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def main():
    con = sqlite3.connect(config.DB_PATH)
    rows = con.execute(
        "SELECT domain, ai_block_hash, ai_block_text FROM robots_meta "
        "WHERE ai_block_hash != ''").fetchall()

    # 1. Exact: group by hash
    by_hash = defaultdict(list)
    for dom, h, text in rows:
        by_hash[h].append((dom, text))

    # 2. Near-dup: merge hashes with high Jaccard (simple union-find)
    hashes = list(by_hash)
    line_sets = {h: set(by_hash[h][0][1].splitlines()) for h in hashes}
    parent = {h: h for h in hashes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, h1 in enumerate(hashes):
        for h2 in hashes[i + 1:]:
            if find(h1) != find(h2) and \
               jaccard(line_sets[h1], line_sets[h2]) >= JACCARD_THRESHOLD:
                parent[find(h2)] = find(h1)

    clusters = defaultdict(list)
    for h in hashes:
        clusters[find(h)].extend(by_hash[h])

    con.execute("DROP TABLE IF EXISTS clusters")
    con.execute("CREATE TABLE clusters (domain TEXT PRIMARY KEY, "
                "cluster_id TEXT, cluster_size INTEGER)")
    ordered = sorted(clusters.items(), key=lambda kv: -len(kv[1]))
    for cid, members in ordered:
        for dom, _ in members:
            con.execute("INSERT OR REPLACE INTO clusters VALUES (?,?,?)",
                        (dom, cid, len(members)))
    con.commit()

    print(f"{len(rows)} domains with an AI block, {len(ordered)} clusters.\n")
    print("=== Largest clusters (for manual attribution) ===")
    for cid, members in ordered[:10]:
        print(f"\n--- cluster {cid} | {len(members)} domains "
              f"| e.g.: {', '.join(d for d, _ in members[:5])}")
        print(members[0][1][:600])


if __name__ == "__main__":
    main()
