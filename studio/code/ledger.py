#!/usr/bin/env python3
"""Episode-number ledger (local mirror of MEMORY.md BC_LAST_EPISODE).
  python3 ledger.py set-last 2
  python3 ledger.py reserve 10 "batch-A"     -> prints START END
  python3 ledger.py done 3 12
  python3 ledger.py show
"""
import json, os, sys, datetime
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledger.json")
def load(): return json.load(open(P)) if os.path.exists(P) else {"last": 2, "open": [], "done": []}
def save(d): json.dump(d, open(P, "w"), indent=2)
cmd = sys.argv[1] if len(sys.argv) > 1 else "show"; d = load()
if cmd == "set-last":
    d["last"] = max(d["last"], int(sys.argv[2])); save(d); print("last =", d["last"])
elif cmd == "reserve":
    n = int(sys.argv[2]); label = sys.argv[3] if len(sys.argv) > 3 else "batch"
    start, end = d["last"]+1, d["last"]+n; d["last"] = end
    d["open"].append({"start": start, "end": end, "label": label, "date": datetime.date.today().isoformat()}); save(d)
    print(start, end)
elif cmd == "done":
    s, e = int(sys.argv[2]), int(sys.argv[3])
    d["open"] = [b for b in d["open"] if not (b["start"] == s and b["end"] == e)]
    d["done"].append({"start": s, "end": e, "date": datetime.date.today().isoformat()}); save(d); print("closed", s, e)
else:
    print(json.dumps(d, indent=2))
