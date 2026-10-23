"""Blobby & Co. — TikTok rows posted BY HAND (shown in the social-hub dashboard).

TikTok mutes Blobby's audio when posted through Buffer, so TikTok is never in queue/schedule.csv.
Instead the dashboard reads:
  queue/tiktok_manual.csv   episode,file,platform,due_at,title,text,comment  (due_at in Asia/Colombo)
  queue/tiktok_posted.json  "<ep>:tiktok" -> record, written by the dashboard's "Mark as posted"
publish.py and the GitHub workflow never read these two files, so nothing here goes to Buffer.

  python3 tiktok_manual/make_rows.py                       # add rows for new episodes in schedule.csv
  python3 tiktok_manual/make_rows.py --posted-until "2026-10-27 23:30"   # also mark older ones as posted

Each episode gets the same day as its YouTube row: morning slot -> 15:30, evening slot -> 23:00 Sri Lanka time.
Caption and first comment come from the episode's post kit (kits/*.md: **TikTok:** and **Pinned comment:**).
Existing rows are kept as they are (hand edits survive); only missing episodes are added.
"""
import argparse, csv, glob, json, os, sys, datetime as dt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "publish"))
from kit_to_schedule import parse  # noqa: E402

SCHEDULE = os.path.join(ROOT, "queue", "schedule.csv")
OUT = os.path.join(ROOT, "queue", "tiktok_manual.csv")
POSTED = os.path.join(ROOT, "queue", "tiktok_posted.json")
COLS = ["episode", "file", "platform", "due_at", "title", "text", "comment"]
SLOT_SLT = ("15:30", "23:00")   # Berlin TikTok slots 12:00 / 19:30 in summer time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--posted-until", help='"YYYY-MM-DD HH:MM" Sri Lanka: mark rows at or before this as posted')
    a = ap.parse_args()

    kits = {}
    for k in sorted(glob.glob(os.path.join(ROOT, "kits", "*.md"))):
        kits.update(parse(open(k, encoding="utf-8").read()))

    sched = list(csv.DictReader(open(SCHEDULE, encoding="utf-8")))
    yt = {int(r["episode"]): r for r in sched if r["platform"] == "youtube" and r.get("due_at", "").strip()}
    files = {int(r["episode"]): r["file"] for r in sched if r.get("file")}

    rows = list(csv.DictReader(open(OUT, encoding="utf-8"))) if os.path.exists(OUT) else []
    have = {int(r["episode"]) for r in rows}
    added, missing = [], []
    for ep, r in sorted(yt.items()):
        if ep in have:
            continue
        d = kits.get(ep)
        if not d or not d.get("tiktok"):
            missing.append(ep); continue
        day, hm = r["due_at"].strip().split(" ")
        slot = SLOT_SLT[0] if hm < "12:00" else SLOT_SLT[1]
        text = d["tiktok"].strip()
        if "#blobbyandco" not in text:
            text += " #blobbyandco"
        rows.append(dict(episode=ep, file=files[ep], platform="tiktok", due_at=f"{day} {slot}",
                         title="", text=text, comment=d.get("comment", "").strip()))
        added.append(ep)
    rows.sort(key=lambda r: (r["due_at"], int(r["episode"])))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} TikTok rows ({len(added)} added: {added})")
    if missing:
        print(f"no TikTok caption in kits for episodes {missing} - not added")

    if a.posted_until:
        posted = json.load(open(POSTED)) if os.path.exists(POSTED) else {}
        now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        newly = []
        for r in rows:
            key = f"{r['episode']}:tiktok"
            if r["due_at"] <= a.posted_until and key not in posted:
                posted[key] = {"at": now, "by": "owner (scheduled in TikTok Studio)", "manual": True}
                newly.append(int(r["episode"]))
        json.dump(posted, open(POSTED, "w"), indent=1); open(POSTED, "a").write("\n")
        print(f"marked as posted: {newly}")
    elif not os.path.exists(POSTED):
        json.dump({}, open(POSTED, "w")); open(POSTED, "a").write("\n")


if __name__ == "__main__":
    main()
