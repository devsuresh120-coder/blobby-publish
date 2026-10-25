---
name: "blobby-batch"
description: "Produce a batch of Blobby & Co. episodes (default 10): silent 12-13s looping animated meme videos with Blobby, Pinky, Boss and Meow. Reserves episode numbers AND jokes from the shared ledger, writes beats, renders mp4s + covers, writes post kits, then pushes to the publish repo so GitHub Actions schedules them in Buffer. Use for /blobby-batch, 'new batch', 'make 10 episodes', 'compilation', with or without a theme."
---

# Blobby & Co. — batch producer

You produce one batch of *Blobby & Co.* episodes end to end, in the background: numbers, jokes, beats, render, QA, post kits, publishing. Silent comedy: no dialogue — actions, generated sound effects, max 2 short human reaction sounds, short English captions. 12–13 s, seamless loop, no end card. The viewer question goes in the description/pinned comment only.

## Arguments (all optional)
`/blobby-batch [count] [theme or notes...]`
- `count`: episodes (default **10**). `compilation` → instead of new episodes, build one 60–75 s video from the 4–5 best recent episodes (concatenate with ffmpeg, add "Best of the week" title card) and queue it as a long post.
- theme/notes: "office life", "Meow", "couple", "poll", a specific premise. None → next unused seeds in `ROADMAP_100.md`, keeping the rotation (4 solo · 3 Pinky · 2 Boss · 1 Meow, one of them a poll episode).
- "Fresh start" → re-unzip the pack. "No publish" → skip Step 8.

## Step 0 — acknowledge, then run in the background
Reply with ONE line: "Starting batch of N (theme: …). Reserving numbers and jokes first; I'll report when rendered and queued." Then do everything below in a background thread.

## Step 1 — workspace
1. If `blobby_pack/` is missing (or "Fresh start"): unzip the newest `blobby_pack.zip` from the Project Library and run `bash blobby_pack/setup.sh`. Confirm `code/engine.py`, `code/ledger.py`, `code/jokes.py` exist.
2. Read `FORMAT_RULES.md` (hard rules), `PROJECT_INSTRUCTIONS.md`, `HUMOR_GUIDE.md`, `ROADMAP_100.md`, and `code/ep33_42.py` (THE reference style: loop bridge, vox, fast hook). `code/ep01_02.py` is the old format — do not copy its end card/question/length.

## Step 2 — reserve episode numbers (before any writing)
MEMORY.md (Project Library) holds `BC_LAST_EPISODE: <n>`, `BC_OPEN_BATCHES:`, `BC_DONE_BATCHES:`.
1. Read MEMORY.md; take `BC_LAST_EPISODE` (missing → 2).
2. `python3 code/ledger.py set-last <n>` then `python3 code/ledger.py reserve <count> "<label>"` → `START END`.
3. **Immediately** write `BC_LAST_EPISODE: <END>` and `START-END <label> <date>` under `BC_OPEN_BATCHES` in MEMORY.md. Re-read once; if another thread moved it above your START, re-reserve.
4. One line to the owner: "Reserved episodes START–END."

## Step 3 — reserve the jokes (before any writing)
1. Save MEMORY.md to a local file; `python3 code/jokes.py import <file>`.
2. Draft the batch as (slug | keywords) one-liners. For each: `python3 code/jokes.py check "<slug> | <keywords>"`; exit 1 → replace. Also reject by judgment any premise that is the same situation with other words.
3. For each accepted: `python3 code/jokes.py add <ep> <slug> "<keywords>"` and append the printed line under `BC_USED_JOKES` in MEMORY.md now. Re-read once for collisions.
4. Only then write beats.

## Step 4 — write the batch
1. `python3 code/new_batch.py START END <theme>` → `code/epSTART_END.py`. Fill each dict; keep slugs.
2. Per episode (FORMAT_RULES.md): `loop=True, voice=False` · frame one = action + sound (`sfx` at 0.0, shake/jump), first caption 1–3 words · 2–3 escalation beats · punchline by ~8 s · hold 2.5–3.5 s · last beat = loop bridge ("Next day:") in the same place/pose as beat 1 · **sum of `dur` = 12–13 s** (no end card is added) · **max 2 `vox`** reaction sounds, non-verbal only ("Ah!", "Oh no!", "Ugh!", "Mm-hm.", "Haaa...") · one joke · caption ≤ 2 lines, ≤ 16 chars/line · bubble ≤ 4 words, max 2 · one SFX per action · `cover` = the second with the biggest reaction face. No `question`/`punchline` on screen.
3. Per batch: rotation above; stages rotate (bedroom/office/kitchen/living/street/blank, none > 4×).
4. Layering: a character standing/awake in the bedroom uses `overlay="blanket_back"` (blanket behind him); `overlay="blanket"` only while someone is lying in bed. Never leave a character half-covered.
5. Allowed values: see the docstring in `code/engine.py` (eyes/mouth/arms/legs/pose/fx), `code/props.py` (props), `code/sfx.py` (SFX names). Never edit `characters.py`.

## Step 5 — render and QA
1. `cd code && python3 epSTART_END.py` (≈ 45 s per episode; split the run if a shell call would exceed 10 min). Output: `episodes/epNN.mp4`, `epNN_cover.jpg`, `epNN_strip.png`.
2. Look at every `epNN_strip.png`: captions readable and not over faces, bubbles above heads, characters not overlapping, NO end card, last frame resembles first frame (loop), duration 12–13 s (ffprobe), max 2 vox. Fix and re-render failures.

## Step 6 — post kits + ledger close
1. Write `episodes/epSTART-END_post_kits.md`, one block per episode, exactly these keys (a script parses it):
```
## Ep N — <joke name> (<characters>) · cover: <second>s
**YouTube title:** <≤ 60 chars, relatable hook, no clickbait caps>
**Description:** <2–3 lines + the question + 3–5 hashtags incl. #shorts #blobbyco #relatable>
**Tags:** <15–20 comma-separated>
**TikTok:** <≤ 150 chars + 4–6 hashtags (#fyp #relatable #comedy #animation …)>
**IG/FB:** <question first, 1–2 lines, "Ep.N."> (+ #blobbyco #relatable #meme)
**Pinned comment:** <ask the question again, offer A/B>
**Replies:** <5 in-character replies by Blobby separated by " / ">
```
2. `python3 code/ledger.py done START END`; move the batch to `BC_DONE_BATCHES` in MEMORY.md; tick the seeds in `ROADMAP_100.md`.

## Step 7 — deliver
Send the mp4s, covers and the post-kit file with a 3–5 line summary: numbers, one-line joke each, cast/stage, anything skipped. Reply in the owner's language (English or Sinhala). No step recap.

## Step 8 — publish (push to the publish repo; GitHub Actions does the rest)
Repo **`devsuresh120-coder/blobby-publish`** (same layout as merge-conflict-publish: `videos/`, `kits/`, `queue/schedule.csv`, `publish/kit_to_schedule.py`). No secrets here.
1. Attach/clone the repo, `git pull`.
2. Copy `episodes/epNN.mp4` → `videos/`, covers → `videos/`, kit → `kits/`.
3. Start day = day after the last `due_at` in `queue/schedule.csv` (MEMORY.md `BC_PUBLISH_NEXT_DAY` should match; trust the repo). Run `python3 publish/kit_to_schedule.py --kits kits/epSTART-END_post_kits.md --episodes START … END --start YYYY-MM-DD --append --out queue/schedule.csv`, then **delete every `tiktok` row** from `queue/schedule.csv` (TikTok is manual — API posts get muted). Check rows = 2 × episodes (youtube + facebook) and no empty YouTube title / text.
4. `git add -A && git commit -m "Queue ep START-END" && git push origin main`; update `BC_PUBLISH_NEXT_DAY`; tell the owner "Queued ep START–END for <first>–<last>."
5. **TikTok manual kit:** write `tiktok_manual/captions_epSTART-END.md` in the repo (per episode: file, day + Sri Lanka time = Berlin TikTok slot 12:00/19:30 + 3:30 in summer / + 4:30 in winter, the **TikTok:** caption, the pinned comment) and send the owner `tiktok_manual_epSTART-END.zip` (mp4s + that file) to schedule in TikTok Studio.
6. GitHub unreachable → zip videos + kit + new schedule rows as `publish_epSTART-END.zip`, send it, tell the owner to upload via GitHub's web UI.

## Never
- Never mark or describe the content as AI-generated anywhere: no `isAiGenerated`/"altered content" flags in the publisher, no "made with AI" in titles, descriptions, captions, hashtags, comments or replies. It is an original, code-drawn cartoon series.
- Write a beat before BOTH numbers and jokes are in MEMORY.md.
- Reuse a premise from `BC_USED_JOKES` with other words or another character.
- Redesign characters, colours, fonts or the BLOBBY & CO. mark.
- Put an end card, an on-screen question or a voice line in a video, or more than 2 reaction sounds.
- Add dialogue, words in reaction sounds, real brands, song lyrics, or sounds not generated by `code/sfx.py` / `vox`.
- Go outside 12–13 s or land the punchline after ~8 s.
- Queue TikTok rows in Buffer.
- Put API keys in the project.
