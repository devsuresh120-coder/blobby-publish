# Blobby & Co. — project pack
Silent 15–30 s animated meme videos (Blobby, Pinky, Boss, Meow). Everything is code: characters, stages, sound effects, timeline.

- `PROJECT_INSTRUCTIONS.md` — paste into the Claude Project instructions
- `SETUP.md` — accounts, Buffer, publish repo, launch plan
- `HUMOR_GUIDE.md` — the comedy rules and the 15–30 s structure
- `ROADMAP_100.md` — 100 joke seeds with the cast rotation
- `skills/blobby-batch/SKILL.md` — the `/blobby-batch` command
- `code/` — engine.py (render), characters.py, stages.py, props.py, sfx.py, ledger.py, jokes.py, new_batch.py, ep01_02.py (reference episodes)
- `episodes/` — output: epNN.mp4, epNN_cover.jpg, epNN_strip.png
- `blobby_co_cast_sheet.png` — the cast
- `brand/` — logo_square (avatar), wordmark, youtube_banner, facebook_cover, intro_card (regenerate with `python3 code/brand.py`)

Quick test: `bash setup.sh && cd code && python3 ep01_02.py`
