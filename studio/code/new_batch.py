#!/usr/bin/env python3
"""Scaffold a batch file:  python3 new_batch.py 3 12 "office life"  -> ep03_12.py with one template dict per episode."""
import os, sys
start, end = int(sys.argv[1]), int(sys.argv[2]); theme = " ".join(sys.argv[3:]) or "mixed"
TEMPLATE = '''
EP{n:02d} = dict(
    num={n}, slug="TODO-slug", stage="bedroom",      # bedroom | office | kitchen | living | street | blank
    cover=3.0,                                       # second used for the thumbnail (big reaction face)
    loop=True, voice=False,                          # NO end card, NO question on screen, NO voice line
    beats=[
        # HOOK (0-1s): ACTION + SOUND IN FRAME ONE (shake / jump / sfx at 0.0). caption 1-3 words ("5:00 AM").
        dict(dur=0.9, stage=dict(), caption="TODO 1-3 words", shake=5,
             chars=dict(blobby=dict(at=(540, 1120), eyes="wide", mouth="o", arms="up", fx="exclaim")),
             sfx=[("boing", 0.0)], vox=[("blobby", "Ah!", 0.2, 0.8, 0.5)]),   # max 2 vox per episode
        # ESCALATION 1-3: one action per beat, one sound per action. 1.0-2.0s each.
        dict(dur=1.5, stage=dict(),
             chars=dict(blobby=dict(at=(540, 1120), eyes="wide", mouth="o", fx="exclaim")),
             sfx=[("boing", 0.0)]),
        # PUNCHLINE (before 15s): the twist happens, caption = punchline text. Hold 2.5-3.5s.
        dict(dur=3.0, stage=dict(), caption="TODO punchline\\nline two",
             chars=dict(blobby=dict(at=(540, 1120), eyes="spiral", mouth="wavy", fx="stars")),
             sfx=[("boom", 0.0), ("crickets", 0.8)]),
        # LOOP BRIDGE (1.2-1.6s): "Tomorrow:" / "Next day:" — same place + pose as beat 1, so it flows back to the start.
        dict(dur=1.4, stage=dict(), caption="Next day:",
             chars=dict(blobby=dict(at=(540, 1120), eyes="open", mouth="flat", tween=False)),
             sfx=[("whoosh", 0.9)]),
    ],
    # FACEBOOK CUT (epNN_fb.mp4, ~15.8 s): 1-2 extra build-up beats (~3.3 s) inserted BEFORE original beat index 2.
    # "One more try before the fail". No vox here, one sfx each. Render with: python3 epSTART_END.py --fb
    fb_extra={{2: [
        dict(dur=1.7, stage=dict(), caption="TODO try again",
             chars=dict(blobby=dict(at=(540, 1120), eyes="wide", mouth="grin", fx="sweat")),
             sfx=[("boing", 0.0)]),
    ]}},
)
'''
head = f'"""Blobby & Co. — episodes {start}-{end} (theme: {theme})\nRun: python3 ep{start:02d}_{end:02d}.py [num ...]\n"""\nimport sys\nfrom engine import render, render_fb\n'
body = "".join(TEMPLATE.format(n=n) for n in range(start, end+1))
tail = f"\nEPISODES = [{', '.join(f'EP{n:02d}' for n in range(start, end+1))}]\nif __name__ == '__main__':\n    fb = '--fb' in sys.argv\n    only = [int(a) for a in sys.argv[1:] if a != '--fb']\n    for ep in EPISODES:\n        if not only or ep['num'] in only:\n            render_fb(ep) if fb else render(ep)\n"
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"ep{start:02d}_{end:02d}.py")
open(path, "w").write(head + body + tail); print("wrote", path)
