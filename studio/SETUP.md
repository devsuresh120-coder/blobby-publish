# Blobby & Co. — setup (accounts → Buffer → publish repo → first batch)

## 1. Claude Project (done by you, once)
1. Project "Blobby & Co." → **Instructions** box: paste `PROJECT_INSTRUCTIONS.md`.
2. **Library**: upload `blobby_pack.zip` and `blobby_co_cast_sheet.png`.
3. Create a Library file **MEMORY.md** with the block from PROJECT_INSTRUCTIONS.md (BC_LAST_EPISODE: 2 …).
4. Skill: copy `skills/blobby-batch/SKILL.md` into your skills (same place as `merge-conflict-batch`). Then `/blobby-batch` works in any thread of the Project.

## 2. Accounts (one new Gmail for the brand, e.g. blobbyco@gmail.com)
| Platform | What to create | Monetisation note (Sri Lanka, Oct 2026) |
|---|---|---|
| YouTube | Brand channel "Blobby & Co." on the new Gmail. Avatar: `brand/logo_square_1024.png`. Banner: `brand/youtube_banner_2560x1440.png`. Enable Shorts, set default language English. | YPP available in SL: 1,000 subs + 10 M Shorts views / 90 days (or 4,000 watch hours). Put a weekly 60 s+ compilation on the channel for watch time. |
| Facebook Page | Page "Blobby & Co." (handle @blobbyco; avatar `brand/logo_square_1024.png`, cover `brand/facebook_cover_1640x624.png`) from a personal profile → Professional dashboard → Monetisation → Set up when eligible. Link an Instagram **professional** account to the Page. | SL is now eligible for Facebook Content Monetisation. Reels auto-cross-post to Instagram. |
| TikTok | Personal account (NOT Business) on the new Gmail or a phone number. One email = one TikTok account; the app holds up to 3 accounts. | Creator Rewards not available in SL and only pays on videos > 1 min. Use TikTok for reach + bio link to YouTube/FB; post the weekly compilation there too. |

Bio line for all three: "Silent comedy about daily life. New episode every day. Which one are you?" + link to the YouTube channel.

Channel URLs: YouTube https://www.youtube.com/@blobbyco · Facebook: (fill in) · TikTok: (fill in)

## 3. Buffer (new account on the new Gmail)
Connect channels: YouTube Shorts, Facebook Page, TikTok (free plan = 3 channels; add Instagram on a paid plan).
Note the three **channel IDs** (Buffer → channel settings) and give them to Claude for the publish config.

## 4. Publish repo (mirror of merge-conflict-publish)
1. GitHub → new repo `blobby-publish` (private). Copy the folders `videos/`, `kits/`, `queue/`, `publish/` and `.github/workflows/` from `merge-conflict-publish`.
2. Settings → Secrets: copy the same secret names (Buffer token, R2 keys) with the **new** Buffer token.
3. In `publish/config` (or the workflow), replace the channel IDs with the three new ones and set 2 posts/day, times 09:00 and 18:00 Europe/Berlin (= 12:30 / 21:30 Sri Lanka; good for US morning + EU evening).
4. `queue/schedule.csv` empty header row. Set `BC_PUBLISH_NEXT_DAY` in MEMORY.md to your launch date.

## 5. Launch plan
- Week 0: render ep 1–20 (two batches). First post on every platform: `brand/intro_card_1080x1920.png` ("Meet the cast") — then the episodes.
- Week 1+: 2 episodes/day on every platform. Reply to the first 20 comments on each video in Blobby's voice (short, emoji-free, in character).
- Every Sunday: 60–75 s compilation of the week's best 4 episodes (Claude: "/blobby-batch compilation").
- After 30 days: look at Shorts analytics (swipe-away rate, which stage/character wins) and tell Claude "more of X".

## 6. Running a batch
In the Project: `/blobby-batch` (10 episodes, next seeds from ROADMAP_100.md) or `/blobby-batch 10 office life` or `/blobby-batch 5 Meow`.
Local test: `cd blobby_pack/code && python3 ep01_02.py` → `episodes/ep01.mp4`, `ep01_cover.jpg`, `ep01_strip.png`.
