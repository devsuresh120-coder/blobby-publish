# Blobby & Co. — Episode format (hard rules — from our own analytics, Oct 2026)
ep1 (13 s, action in frame one) kept 58% of viewers and was watched 111% (replays); ep2 (17 s, slow start) kept 27%. So:
- **12–13 s total.** No end card, no question on screen, no voice line: `loop=True, voice=False` on every episode.
- **Frame one = action + sound** (shake, jump, crash, `sfx` at 0.0). Never open on characters just standing or sitting.
- **First caption = the joke's premise as a statement, 4–7 words**, readable in 1 second ("Monday motivation: lasted 3 seconds", "Sharing a blanket at 2 AM"). Never a vague 1–3 word label ("Chef mode", "Quick call"). Changed 25 Oct 2026 from YouTube data: Monday motivation 58.6% stayed (11k views) vs "Chef mode" 29.1%. Punchline by ~8 s.
- **Loop bridge:** the last beat (1.2–1.6 s, "Tomorrow:", "Next day:", "Next night:", "One more?") puts the character back in the place and pose of beat 1, so the video flows straight into the start and the viewer does not feel it ended.
- **Human reaction sounds (`vox`): at most 2 per video**, short and non-verbal only ("Ah!", "Ooh!", "Oh no!", "Ugh!", "Mm-hm.", "Haaa...", "Hmph!"). Never words or sentences.
- One joke. Caption ≤ 2 lines, ≤ 16 chars/line. Thought bubble ≤ 4 words, max 2 bubbles. One SFX per action.
- The viewer question lives only in the description, IG/FB text and pinned comment — never highlighted in the video.
- `cover` = the second with the biggest reaction face.
- Reference batch for this format: `code/ep33_42.py`.

## Facebook cut (owner decision 30 Oct 2026: Facebook only) — `epNN_fb.mp4`, ~15.8 s
Facebook favours 15–30 s Reels. YouTube and TikTok keep the 12–13 s `epNN.mp4`; Facebook gets a longer cut of the same episode.
- Still NO end card, NO on-screen question, NO voice line. Same frame-one hook, same punchline, same loop bridge.
- Each loop episode dict gets `fb_extra = {index: [beat, ...]}`: 1–2 extra build-up beats (≈3.3 s) inserted BEFORE original beat `index` — "one more try before the fail" (rule of three). No `vox` in extra beats (2-vox limit still holds), one SFX each, safe-zone rules apply.
- `engine.facebook_cut(ep)` inserts them, stretches to ~15.8 s and keeps `cover` on the same moment. Episodes already 15 s+ (mini-stories) get no cut. A loop episode without `fb_extra` falls back to playing the loop twice (~25 s).
- Render: `python3 epSTART_END.py --fb [nums]` (reference: `FB_EXTRA` in `code/ep33_42.py`). Punchline lands ~9–11 s in this cut.
- Copy `epNN_fb.mp4` to `videos/` with `epNN.mp4`; `publish/kit_to_schedule.py` then uses it for the Facebook row automatically.
