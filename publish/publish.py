"""Blobby & Co. publisher — runs inside GitHub Actions.

Reads queue/schedule.csv, uploads each video to Cloudflare R2 (public URL), creates the
post in Buffer via its GraphQL API, and records what was done in queue/posted.json so a
row is never posted twice.

schedule.csv columns (header required):
  episode   e.g. 2
  file      path relative to repo root, e.g. videos/ep02.mp4
  platform  youtube | tiktok | facebook
  due_at    optional. "2026-10-17 08:00" in Europe/Berlin (customScheduled) or empty (addToQueue)
  title     YouTube title (required for youtube; ignored elsewhere)
  text      caption / description (use \n for new lines)
  comment   optional first comment (Facebook only; YouTube/TikTok ignore it)

Env (GitHub Secrets): BUFFER_ACCESS_TOKEN, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY,
R2_BUCKET, R2_PUBLIC_URL (e.g. https://pub-xxxx.r2.dev). Optional: DRY_RUN=1, R2_PREFIX (default blobby/ — keeps
this series' files apart from other series sharing the bucket).
"""
import csv, json, os, re, sys, time, datetime as dt
from zoneinfo import ZoneInfo
import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCHEDULE = os.path.join(ROOT, "queue", "schedule.csv")
POSTED = os.path.join(ROOT, "queue", "posted.json")
API = "https://api.buffer.com"
TZ = ZoneInfo("Europe/Berlin")
DRY = os.environ.get("DRY_RUN") == "1"
YT_CATEGORY_COMEDY = "23"

def env(k):
    v = os.environ.get(k, "").strip()
    if not v and not DRY:
        sys.exit(f"missing secret {k}")
    return v

class RateLimited(Exception): pass

def gql(query, variables=None):
    for attempt in range(3):
        r = requests.post(API, json={"query": query, "variables": variables or {}},
                          headers={"Authorization": f"Bearer {env('BUFFER_ACCESS_TOKEN')}"}, timeout=60)
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", "60") or 60)
            print(f"  rate limited by Buffer; waiting {wait}s"); time.sleep(min(wait, 120)); continue
        r.raise_for_status()
        break
    else:
        raise RateLimited("Buffer rate limit (429) persists; stopping this run, the daily run will continue")
    j = r.json()
    if j.get("errors"):
        raise RuntimeError(json.dumps(j["errors"], indent=1))
    return j["data"]

def channels():
    acc = gql("query { account { id organizations { id name } } }")["account"]
    out = {}
    for org in acc["organizations"]:
        for ch in gql("query($o:OrganizationId!){ channels(input:{organizationId:$o}) { id name service } }", {"o": org["id"]})["channels"]:
            out.setdefault(ch["service"].lower(), ch)
    return out

def r2_client():
    import boto3
    return boto3.client("s3", endpoint_url=f"https://{env('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
                        aws_access_key_id=env("R2_ACCESS_KEY_ID"), aws_secret_access_key=env("R2_SECRET_ACCESS_KEY"),
                        region_name="auto")

def upload(path):
    key = os.environ.get("R2_PREFIX", "blobby/").strip("/") + "/" + os.path.basename(path)
    url = f"{env('R2_PUBLIC_URL').rstrip('/')}/{key}"
    if DRY:
        print(f"  [dry] would upload {path} -> {url}"); return url
    s3, bucket = r2_client(), env("R2_BUCKET")
    try:
        s3.head_object(Bucket=bucket, Key=key); print(f"  already in R2: {key}")
    except Exception:
        s3.upload_file(path, bucket, key, ExtraArgs={"ContentType": "video/mp4"}); print(f"  uploaded {key}")
    # verify it is publicly reachable (Buffer fetches it later)
    h = requests.head(url, timeout=30, allow_redirects=False)
    if h.status_code != 200:
        raise RuntimeError(f"{url} not public (HTTP {h.status_code}); enable public access on the bucket")
    return url

def due_iso(s):
    s = (s or "").strip()
    if not s: return None
    local = dt.datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=TZ)
    return local.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def build_input(row, channel_id, video_url):
    text = row["text"].replace("\\n", "\n").strip()
    inp = {"channelId": channel_id, "text": text, "schedulingType": "automatic",
           "assets": [{"video": {"url": video_url, "metadata": {"thumbnailOffset": 2500}}}]}
    due = due_iso(row.get("due_at"))
    if due and due > dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"):
        inp.update(mode="customScheduled", dueAt=due)
    else:
        inp["mode"] = "addToQueue"   # no date, or the date already passed -> next free slot
    p = row["platform"].lower()
    if p == "youtube":
        inp["metadata"] = {"youtube": {"title": row["title"].strip()[:100], "categoryId": YT_CATEGORY_COMEDY,
                                       "privacy": "public", "madeForKids": False, "notifySubscribers": True,
                                       "isAiGenerated": False}}
    elif p == "tiktok":
        inp["metadata"] = {"tiktok": {"isAiGenerated": False}}
    elif p == "facebook":
        fb = {"type": "reel"}
        # firstComment needs a paid Buffer plan; send it only when FIRST_COMMENT=1
        if os.environ.get("FIRST_COMMENT") == "1" and row.get("comment", "").strip():
            fb["firstComment"] = row["comment"].strip()
        inp["metadata"] = {"facebook": fb}
    return inp

CREATE = """mutation($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id text dueAt } }
    ... on MutationError { message }
  }
}"""

def main():
    posted = json.load(open(POSTED)) if os.path.exists(POSTED) else {}
    rows = list(csv.DictReader(open(SCHEDULE, encoding="utf-8")))
    horizon = (dt.datetime.now(TZ) + dt.timedelta(days=6)).strftime("%Y-%m-%d %H:%M")
    todo = [r for r in rows if f"{r['episode']}:{r['platform'].lower()}" not in posted and r.get("file")
            and (not r.get("due_at", "").strip() or r["due_at"].strip() <= horizon)]
    # earliest first: Buffer's free plan holds only 10 queued posts per channel, so what is due soonest must get the free slots
    todo.sort(key=lambda r: (r.get("due_at", "").strip() or "9999", int(r["episode"])))
    print(f"{len(rows)} rows, {len(todo)} due within 6 days and not yet posted")
    if not todo: return
    chans = {} if DRY else channels()
    if not DRY: print("channels:", {k: v["name"] for k, v in chans.items()})
    urls, failures, deferred = {}, 0, 0
    for r in todo:
        key = f"{r['episode']}:{r['platform'].lower()}"
        print(f"== ep {r['episode']} -> {r['platform']}")
        try:
            path = os.path.join(ROOT, r["file"])
            if not os.path.exists(path): raise FileNotFoundError(path)
            if path not in urls: urls[path] = upload(path)
            ch = chans.get(r["platform"].lower())
            if not DRY and not ch:
                print(f"  ep{r['episode']} {r['platform']}: no such channel connected in Buffer yet - deferred"); continue
            inp = build_input(r, ch["id"] if ch else "dry", urls[path])
            if DRY:
                print("  [dry] createPost", json.dumps(inp, indent=1)[:600]); continue
            res = gql(CREATE, {"input": inp})["createPost"]
            if "message" in res and "post" not in res: raise RuntimeError(res["message"])
            post = res["post"]
            posted[key] = {"post_id": post["id"], "due_at": post.get("dueAt"), "url": urls[path],
                           "at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
            print(f"  ok post {post['id']} due {post.get('dueAt')}")
            json.dump(posted, open(POSTED, "w"), indent=1)
            time.sleep(3)
        except RateLimited as e:
            print(f"  {e}"); print("::warning title=Buffer rate limit::" + str(e)); break
        except Exception as e:
            msg = str(e)
            if re.search(r"limit|queue is full|upgrade|plan", msg, re.I):
                deferred += 1; print(f"  DEFERRED (Buffer plan limit, retried on the next run): {msg[:160]}")
            else:
                failures += 1; print(f"  FAILED: {msg}"); print("::error title=Buffer publish failed (ep " + str(r["episode"]) + " " + r["platform"] + ")::" + msg.replace("\n", " ")[:900])
    json.dump(posted, open(POSTED, "w"), indent=1)
    print(f"done: {len(posted)} recorded, {deferred} deferred, {failures} failed")
    if failures: sys.exit(f"{failures} row(s) failed; the rest are recorded in posted.json")

if __name__ == "__main__":
    main()
