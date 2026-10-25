# Blobby & Co. studio (render code)

Moved here from the claude.ai Project on 2026-10-25 so any chat can render episodes.
Setup: `bash studio/setup.sh`. Render: `cd studio/code && python3 ep33_42.py 41` → `studio/episodes/ep41.mp4`.
`MEMORY.md` = episode counter + used jokes (was the Project memory). Keep it updated with every batch.

v3 (25 Oct 2026, default; `BC_FORMAT=v2` restores the old look): closer camera (`zoom`, default 1.2),
bigger top captions, a different music style + key per episode (`code/musicbeds.py`; `music_style=` to choose:
marimba, ukulele, sneaky, funk, jazz, chip, lofi).
