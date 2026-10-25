#!/usr/bin/env python3
"""Joke ledger — stops the same premise being used twice.
  python3 jokes.py import MEMORY.txt          merge 'BC_USED_JOKES' lines from a saved MEMORY.md
  python3 jokes.py check "slug | keywords"    exit 1 if too similar to an existing joke
  python3 jokes.py add 3 slug "keywords"      record (prints the MEMORY.md line)
  python3 jokes.py list
Similarity = Jaccard on keyword stems (>= 0.45) OR same slug.
"""
import json, os, re, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jokes_used.json")
SEED = [
    {"ep": 1, "slug": "monday-alarm", "kw": "5am alarm productive flex faceplant bed asleep motivation 3 seconds"},
    {"ep": 2, "slug": "what-do-you-want-to-eat", "kw": "partner anything is fine pizza burger noodles rejected nothing is fine"},
]
STOP = set("the a an of to in on at and or is are be my me i you it this that with for from".split())
def stem(w): return re.sub(r"(ing|ed|es|s)$", "", w.lower())
def toks(s): return {stem(w) for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}
def load():
    if not os.path.exists(P): json.dump(SEED, open(P, "w"), indent=2)
    return json.load(open(P))
def save(d): json.dump(d, open(P, "w"), indent=2)
def similar(a, b):
    A, B = toks(a), toks(b)
    return len(A & B)/max(1, len(A | B))

cmd = sys.argv[1]; data = load()
if cmd == "import":
    for line in open(sys.argv[2], encoding="utf-8"):
        m = re.match(r"\s*-\s*(\d+)\s*\|\s*([\w\-]+)\s*\|\s*(.+)", line)
        if m and not any(j["slug"] == m.group(2) for j in data):
            data.append({"ep": int(m.group(1)), "slug": m.group(2), "kw": m.group(3).strip()})
    save(data); print(len(data), "jokes known")
elif cmd == "check":
    slug, kw = [x.strip() for x in sys.argv[2].split("|", 1)]
    worst = max(((similar(kw, j["kw"]), j) for j in data), key=lambda x: x[0], default=(0, None))
    if any(j["slug"] == slug for j in data) or worst[0] >= 0.45:
        print(f"TOO SIMILAR to ep{worst[1]['ep']} {worst[1]['slug']} ({worst[0]:.2f})"); sys.exit(1)
    print(f"ok (closest {worst[0]:.2f})")
elif cmd == "add":
    ep, slug, kw = int(sys.argv[2]), sys.argv[3], sys.argv[4]
    data.append({"ep": ep, "slug": slug, "kw": kw}); save(data)
    print(f"- {ep} | {slug} | {kw}")
else:
    for j in data: print(f"- {j['ep']} | {j['slug']} | {j['kw']}")
