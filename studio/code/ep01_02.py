"""Blobby & Co. — episodes 1-2 (reference batch: copy this structure).
Run: python3 ep01_02.py            (renders all)   |   python3 ep01_02.py 2   (renders ep 2 only)
Silent-comedy timing: hook 0-2s, setup, 2-3 escalations, punchline before 15s, hold 1.5-2.5s, end card.
"""
import sys
from engine import render

EP01 = dict(
    num=1, slug="monday-alarm", stage="bedroom", cover=4.6,
    punchline="Monday motivation:\nlasted 3 seconds",
    question="Which one are you?\n(A) Blobby  (B) Still in bed",
    beats=[
        dict(dur=2.2, stage=dict(night=True, clock="5:00"), overlay="blanket", caption="5:00 AM",
             chars=dict(blobby=dict(at=(230, 1030), angle=35, scale=0.9, eyes="closed", fx="zzz")),
             sfx=[("snore", 0.1), ("snore", 1.1)]),
        dict(dur=1.4, stage=dict(night=True, alarm=True), overlay="blanket_back", caption="5:00 AM", shake=4,
             chars=dict(blobby=dict(at=(300, 960), angle=0, scale=0.95, eyes="wide", mouth="o", arms="up", fx="exclaim", tween=False)),
             sfx=[("alarm", 0.0), ("boing", 0.05)]),
        dict(dur=2.6, stage=dict(night=True), overlay="blanket_back", caption="Today I will be\nPRODUCTIVE",
             chars=dict(blobby=dict(at=(520, 1120), eyes="open", mouth="grin", arms="flex", brows=True, fx="sparkle")),
             sfx=[("sparkle", 0.3)]),
        dict(dur=1.2, stage=dict(night=True), overlay="blanket_back", caption="Today I will be\nPRODUCTIVE",
             chars=dict(blobby=dict(at=(600, 1120), eyes="open", mouth="flat", legs="step")),
             sfx=[("steps", 0.0)]),
        dict(dur=1.0, stage=dict(night=True), overlay="blanket_back",
             chars=dict(blobby=dict(at=(560, 1120), angle=-75, eyes="wide", mouth="wavy", arms="flail")),
             sfx=[("slide_whistle_down", 0.0)]),
        dict(dur=0.3, stage=dict(night=True), overlay="blanket", shake=12,
             chars=dict(blobby=dict(at=(400, 1080), angle=90, scale=0.95, squash=0.6, eyes="spiral", mouth="wavy", arms="flail", fx="impact", tween=False)),
             sfx=[("thud", 0.0), ("boom", 0.03)]),
        dict(dur=2.2, stage=dict(night=True), overlay="blanket", caption="3 seconds later...",
             chars=dict(blobby=dict(at=(400, 1080), angle=90, scale=0.95, squash=0.6, eyes="spiral", mouth="wavy", arms="flail", fx="stars", tween=False))),
        dict(dur=3.2, stage=dict(night=True, clock="5:01"), overlay="blanket", caption="Monday motivation:\nlasted 3 seconds",
             chars=dict(blobby=dict(at=(230, 1030), angle=35, scale=0.9, eyes="closed", fx="zzz", tween=False)),
             sfx=[("crickets", 0.0), ("snore", 0.4), ("snore", 1.6)]),
    ],
)

EP02 = dict(
    num=2, slug="what-do-you-want-to-eat", stage="living", cover=5.0,
    punchline="\"Anything is fine\"\n= nothing is fine",
    question="Who is Pinky in your house?",
    beats=[
        dict(dur=2.0, stage=dict(tv="on"), caption="\"What do you want\nto eat?\"",
             chars=dict(pinky=dict(at=(270, 1075), scale=0.85, legs="sit", eyes="open", mouth="smile", prop="remote"),
                        blobby=dict(at=(590, 1075), scale=0.85, legs="sit", eyes="open", mouth="smile"))),
        dict(dur=1.8, stage=dict(tv="on"), bubble=("pinky", "Anything is fine"),
             chars=dict(pinky=dict(at=(270, 1075), scale=0.85, legs="sit", eyes="happy", mouth="smile", prop="remote"),
                        blobby=dict(at=(590, 1075), scale=0.85, legs="sit", eyes="open", mouth="smile")),
             sfx=[("pop", 0.0)]),
        dict(dur=1.6, stage=dict(tv="on"), bubble=("blobby", "Pizza?"),
             chars=dict(pinky=dict(at=(270, 1075), scale=0.85, legs="sit", eyes="half", mouth="flat"),
                        blobby=dict(at=(590, 1075), scale=0.85, legs="sit", eyes="open", mouth="grin", prop="pizza")),
             sfx=[("pop", 0.0), ("bruh", 0.9)]),
        dict(dur=1.6, stage=dict(tv="on"), bubble=("blobby", "Burger?"),
             chars=dict(pinky=dict(at=(270, 1075), scale=0.85, legs="sit", eyes="half", mouth="flat", fx="anger"),
                        blobby=dict(at=(590, 1075), scale=0.85, legs="sit", eyes="open", mouth="smile", prop="burger")),
             sfx=[("pop", 0.0), ("bruh", 0.9)]),
        dict(dur=1.6, stage=dict(tv="on"), bubble=("blobby", "Noodles?"),
             chars=dict(pinky=dict(at=(270, 1075), scale=0.85, legs="sit", eyes="angry", mouth="flat", fx="anger"),
                        blobby=dict(at=(590, 1075), scale=0.85, legs="sit", eyes="wide", mouth="o", fx="sweat")),
             sfx=[("pop", 0.0), ("heartbeat", 0.5)]),
        dict(dur=2.2, stage=dict(tv="on"), caption="20 minutes later",
             chars=dict(pinky=dict(at=(270, 1075), scale=0.85, legs="sit", eyes="angry", mouth="flat", arms="cross"),
                        blobby=dict(at=(590, 1075), scale=0.85, legs="sit", eyes="spiral", mouth="wavy", fx="stars")),
             sfx=[("tick_tock", 0.0)]),
        dict(dur=2.8, stage=dict(tv="off"), caption="\"Anything is fine\"\n= nothing is fine",
             chars=dict(pinky=dict(at=(270, 1075), scale=0.85, legs="sit", eyes="closed", mouth="flat", arms="cross"),
                        blobby=dict(at=(590, 1075), scale=0.85, legs="sit", eyes="closed", mouth="sad", fx="sweat")),
             sfx=[("sad_trombone", 0.0)]),
    ],
)

EPISODES = [EP01, EP02]
if __name__ == "__main__":
    only = [int(a) for a in sys.argv[1:]]
    for ep in EPISODES:
        if not only or ep["num"] in only:
            render(ep)
