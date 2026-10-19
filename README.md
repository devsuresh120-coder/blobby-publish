# blobby-publish

Transport + publisher for **Blobby & Co.** (@blobbyco). The Claude project pushes videos and a
schedule here; GitHub Actions uploads the videos to Cloudflare R2 (under `blobby/`) and creates the
posts in Buffer. Same machinery as merge-conflict-publish.

```
videos/epNN.mp4              the episodes (≈1 MB each) + epNN_cover.jpg
kits/epA-B_post_kits.md      post kits written by the project
queue/schedule.csv           what to post where (one row per episode × platform)
queue/posted.json            written by the workflow; a row listed here is never posted again
publish/publish.py           R2 upload + Buffer createPost
publish/kit_to_schedule.py   post-kit markdown → schedule rows
publish/list_channels.py     prints the Buffer channels the token can see
```

## Secrets (repo → Settings → Secrets and variables → Actions → New repository secret)
`BUFFER_ACCESS_TOKEN` (the **Blobby & Co.** Buffer account's token),
`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`, `R2_PUBLIC_URL`
(the same Cloudflare R2 values as merge-conflict-publish — files are kept apart under the `blobby/` prefix).

## How it runs
- Any push to `main` that changes `queue/schedule.csv`, `videos/` or `publish/` runs the workflow; it also runs daily at 04:41 UTC to top up the Buffer queues (free plan: 10 queued posts per channel; extra rows are deferred, not failed).
- Actions → *Publish to Buffer* → *Run workflow* with `list-channels` (checks the Buffer token), `dry-run` (no uploads, no posts) or `publish`.
- Posts go to each channel's Buffer queue (`addToQueue`); Buffer's posting schedule decides the time (Europe/Berlin: YouTube 08:00/18:00, Facebook 08:30/19:00, TikTok 12:00/19:30). A `YYYY-MM-DD HH:MM` (Berlin) in `due_at` pins a time instead.
- A platform with no channel connected in Buffer yet (e.g. TikTok at launch) is skipped and retried on later runs.

## Adding a batch (what the project does)
1. Copy `epNN.mp4` into `videos/`, the kit into `kits/`.
2. `python3 publish/kit_to_schedule.py --kits kits/epA-B_post_kits.md --episodes A … B --start YYYY-MM-DD --append` (add `--skip tiktok` until TikTok is connected).
3. Commit and push to `main`.

## TikTok (manual, since Oct 19 2026)
TikTok mutes Blobby's audio when posted through the API (Buffer) but accepts the same files uploaded in the app or TikTok Studio. So TikTok rows are NOT generated (`kit_to_schedule.py --skip tiktok`); each batch ships a `tiktok_manual/` kit (captions + suggested times) and the owner schedules the videos on tiktok.com/tiktokstudio (up to 10 days ahead).
