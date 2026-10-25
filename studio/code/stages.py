"""Stages (backgrounds). Canvas 1080x1920. Floor line at FLOOR_Y; characters stand with feet ~FLOOR_Y+40.
Every stage keeps the band y=120..420 free for the caption, and the band y=1500..1800 for the bottom text."""
import math
from PIL import ImageDraw
from props import draw_prop

W, H = 1080, 1920
FLOOR_Y = 1250
OUTL = (40, 30, 30)
WALL = (246, 225, 190)


def _floor(d, col=(176, 118, 76), col2=(150, 98, 60)):
    d.rectangle([0, FLOOR_Y, W, H], fill=col)
    for x in range(0, W + 200, 180):
        d.line([x, FLOOR_Y, x - 120, H], fill=col2, width=6)


def bedroom(d, t, state):
    """state: night(bool), alarm(bool), clock(str)"""
    d.rectangle([0, 0, W, H], fill=WALL); _floor(d)
    shake = int(6*math.sin(t*90)) if state.get("alarm") else 0
    sky = (30, 40, 90) if state.get("night", True) else (140, 200, 250)
    d.rounded_rectangle([640+shake, 400, 1000+shake, 760], radius=24, fill=sky, outline=(120, 80, 50), width=14)
    if state.get("night", True):
        d.ellipse([820+shake, 470, 940+shake, 590], fill=(255, 245, 200)); d.ellipse([850+shake, 455, 955+shake, 565], fill=sky)
        for sx, sy in ((690, 470), (730, 640), (800, 730), (950, 690), (690, 760)):
            d.ellipse([sx+shake-5, sy-5, sx+shake+5, sy+5], fill=(255, 255, 255))
    else:
        d.ellipse([830+shake, 450, 960+shake, 580], fill=(255, 220, 80))
    d.line([820+shake, 400, 820+shake, 760], fill=(120, 80, 50), width=10)
    d.rectangle([760, 1090, 1010, 1270], fill=(140, 85, 45), outline=OUTL, width=8)
    d.rectangle([790, 1130, 980, 1150], fill=(90, 55, 30))
    # bed
    d.rectangle([90, 1000, 700, 1060], fill=(120, 72, 40), outline=OUTL, width=8)
    d.rectangle([60, 1060, 720, 1240], fill=(245, 235, 220), outline=OUTL, width=8)
    d.rectangle([60, 1240, 110, 1300], fill=(120, 72, 40)); d.rectangle([670, 1240, 720, 1300], fill=(120, 72, 40))
    # clock
    cx, cy = 885, 1030
    sh = int(10*math.sin(t*80)) if state.get("alarm") else 0
    d.ellipse([cx-70+sh, cy-110, cx-20+sh, cy-60], fill=(200, 40, 40), outline=OUTL, width=6)
    d.ellipse([cx+20+sh, cy-110, cx+70+sh, cy-60], fill=(200, 40, 40), outline=OUTL, width=6)
    d.ellipse([cx-75+sh, cy-75, cx+75+sh, cy+75], fill=(235, 235, 235), outline=(200, 40, 40), width=12)
    from engine import font
    d.text((cx-56+sh, cy-22), state.get("clock", "5:00"), font=font(44), fill=(30, 30, 30))
    if state.get("alarm"):
        for a in range(0, 360, 45):
            r = math.radians(a + t*500)
            d.line([cx+95*math.cos(r), cy+95*math.sin(r), cx+125*math.cos(r), cy+125*math.sin(r)], fill=(230, 40, 40), width=10)


def blanket(d, up=False):
    """Call AFTER the sleeping character so the blanket covers it."""
    B, B2 = (82, 140, 210), (60, 110, 175)
    if up:
        d.rounded_rectangle([250, 1150, 720, 1240], radius=30, fill=B, outline=OUTL, width=8)
    else:
        d.rounded_rectangle([200, 1090, 720, 1240], radius=40, fill=B, outline=OUTL, width=8)
        for x in range(260, 700, 110):
            d.arc([x, 1080, x+100, 1130], 180, 360, fill=B2, width=8)


def office(d, t, state):
    """state: screen(str: 'code'|'chart'|'zoom'|'blank'), clock(str)"""
    d.rectangle([0, 0, W, H], fill=(225, 232, 240)); _floor(d, (150, 150, 160), (130, 130, 140))
    d.rectangle([0, 420, W, 440], fill=(190, 198, 210))
    # wall clock
    from engine import font
    d.ellipse([800, 480, 960, 640], fill=(255, 255, 255), outline=OUTL, width=10)
    d.text((838, 540), state.get("clock", "9:00"), font=font(36), fill=OUTL)
    # desk + monitor
    d.rectangle([80, 1130, 1000, 1170], fill=(170, 120, 80), outline=OUTL, width=8)
    d.rectangle([120, 1170, 160, 1300], fill=(140, 95, 60)); d.rectangle([920, 1170, 960, 1300], fill=(140, 95, 60))
    d.rectangle([330, 820, 760, 1090], fill=(50, 50, 60), outline=OUTL, width=8)
    d.rectangle([480, 1090, 610, 1130], fill=(80, 80, 90))
    sc = state.get("screen", "blank")
    if sc == "code":
        d.rectangle([350, 840, 740, 1070], fill=(30, 34, 45))
        for i, w in enumerate((200, 120, 260, 90, 180, 230)):
            d.rectangle([380, 870+i*30, 380+w, 882+i*30], fill=[(120, 200, 255), (255, 180, 100), (160, 230, 140)][i % 3])
    elif sc == "chart":
        d.rectangle([350, 840, 740, 1070], fill=(255, 255, 255))
        pts = [(380, 1040), (450, 990), (520, 1010), (590, 900), (660, 930), (720, 860)]
        d.line(pts, fill=(60, 160, 90), width=10)
    elif sc == "zoom":
        d.rectangle([350, 840, 740, 1070], fill=(40, 40, 40))
        for i in range(4):
            d.rectangle([365+i*95, 860, 445+i*95, 950], fill=(90, 90, 110))
            d.ellipse([385+i*95, 880, 425+i*95, 920], fill=(200, 180, 160))
    else:
        d.rectangle([350, 840, 740, 1070], fill=(120, 180, 240))
    # plant
    d.rectangle([840, 1050, 920, 1130], fill=(200, 110, 70), outline=OUTL, width=6)
    for a in (-40, 0, 40):
        d.ellipse([880+a-40, 940, 880+a+40, 1060], fill=(70, 150, 80), outline=OUTL, width=5)


def kitchen(d, t, state):
    """state: fridge_open(bool)"""
    d.rectangle([0, 0, W, H], fill=(235, 245, 230)); _floor(d, (210, 210, 200), (190, 190, 180))
    for x in range(0, W, 120):
        for y in range(420, 900, 120):
            d.rectangle([x+6, y+6, x+114, y+114], fill=(245, 250, 240), outline=(215, 225, 210), width=3)
    # counter
    d.rectangle([60, 1080, 620, 1120], fill=(120, 120, 130), outline=OUTL, width=8)
    d.rectangle([60, 1120, 620, 1300], fill=(90, 140, 170), outline=OUTL, width=8)
    d.line([340, 1120, 340, 1300], fill=OUTL, width=6)
    d.ellipse([170, 1200, 230, 1215], fill=(200, 200, 200)); d.ellipse([450, 1200, 510, 1215], fill=(200, 200, 200))
    # fridge
    d.rectangle([720, 700, 1000, 1300], fill=(225, 230, 235), outline=OUTL, width=10)
    d.line([720, 900, 1000, 900], fill=OUTL, width=8)
    d.rectangle([740, 760, 760, 860], fill=(120, 120, 130)); d.rectangle([740, 950, 760, 1150], fill=(120, 120, 130))
    if state.get("fridge_open"):
        d.rectangle([740, 920, 990, 1290], fill=(255, 255, 230))
        for y in (1000, 1100, 1200):
            d.line([740, y, 990, y], fill=(200, 200, 180), width=6)
        d.polygon([(720, 900), (520, 850), (520, 1330), (720, 1300)], fill=(200, 205, 215), outline=OUTL)
    # stove pot
    d.ellipse([400, 1040, 560, 1100], fill=(80, 80, 90), outline=OUTL, width=6)


def living(d, t, state):
    """state: tv(str: 'on'|'off'|'static')"""
    d.rectangle([0, 0, W, H], fill=(240, 220, 200)); _floor(d, (140, 95, 70), (120, 80, 60))
    # rug
    d.ellipse([150, 1240, 930, 1420], fill=(190, 80, 80), outline=OUTL, width=6)
    # sofa
    d.rounded_rectangle([80, 1000, 640, 1260], radius=40, fill=(90, 130, 110), outline=OUTL, width=8)
    d.rounded_rectangle([110, 1090, 610, 1150], radius=20, fill=(110, 150, 130))
    d.rounded_rectangle([60, 1080, 120, 1260], radius=20, fill=(80, 115, 100), outline=OUTL, width=6)
    d.rounded_rectangle([600, 1080, 660, 1260], radius=20, fill=(80, 115, 100), outline=OUTL, width=6)
    # TV
    d.rectangle([720, 700, 1020, 920], fill=(30, 30, 35), outline=OUTL, width=10)
    tv = state.get("tv", "on")
    if tv == "on":
        d.rectangle([740, 720, 1000, 900], fill=(120, 190, 250))
        d.ellipse([820, 760, 920, 860], fill=(255, 220, 80))
    elif tv == "static":
        import random
        rnd = random.Random(int(t*30))
        for y in range(720, 900, 10):
            d.line([740, y, 1000, y], fill=(rnd.randint(60, 220),)*3, width=10)
    d.rectangle([840, 920, 900, 1000], fill=(60, 60, 60)); d.rectangle([780, 1000, 960, 1020], fill=(60, 60, 60))
    # window
    d.rounded_rectangle([160, 500, 560, 820], radius=20, fill=(160, 210, 250), outline=(120, 80, 50), width=12)
    d.line([360, 500, 360, 820], fill=(120, 80, 50), width=8); d.line([160, 660, 560, 660], fill=(120, 80, 50), width=8)
    d.ellipse([400, 540, 500, 640], fill=(255, 230, 90))


def street(d, t, state):
    """state: rain(bool), night(bool)"""
    night = state.get("night", False)
    d.rectangle([0, 0, W, H], fill=(30, 40, 80) if night else (150, 205, 250))
    if not night:
        d.ellipse([820, 180, 980, 340], fill=(255, 230, 90))
        for cx, cy in ((200, 300), (650, 220)):
            for dx in (-80, 0, 80):
                d.ellipse([cx+dx-70, cy-50, cx+dx+70, cy+50], fill=(255, 255, 255))
    # buildings
    for i, (x, h, c) in enumerate(((0, 500, (200, 170, 150)), (260, 650, (170, 150, 160)), (560, 450, (190, 160, 140)), (820, 700, (160, 160, 170)))):
        d.rectangle([x, 1150-h, x+240, 1150], fill=c, outline=OUTL, width=6)
        for wy in range(1150-h+40, 1120, 90):
            for wx in range(x+30, x+230, 70):
                d.rectangle([wx, wy, wx+40, wy+50], fill=(255, 240, 150) if night else (120, 170, 220))
    d.rectangle([0, 1150, W, 1250], fill=(190, 190, 190)); d.rectangle([0, 1250, W, H], fill=(70, 70, 75))
    for x in range(0, W, 200):
        d.rectangle([x+30, 1400, x+130, 1420], fill=(240, 220, 90))
    if state.get("rain"):
        import random
        rnd = random.Random(int(t*40))
        for _ in range(140):
            x, y = rnd.randint(0, W), rnd.randint(0, 1250)
            d.line([x, y, x-8, y+40], fill=(120, 160, 220), width=4)


def blank(d, t, state):
    d.rectangle([0, 0, W, H], fill=state.get("color", (250, 240, 215)))
    d.rectangle([0, FLOOR_Y, W, H], fill=state.get("floor", (225, 205, 170)))


STAGES = {"bedroom": bedroom, "office": office, "kitchen": kitchen, "living": living, "street": street, "blank": blank}

# Suggested character anchor points (x, y of layer centre) per stage
ANCHORS = {
    "bedroom": {"bed": (230, 1030), "beside": (520, 1120), "door": (900, 1120)},
    "office": {"chair": (540, 1110), "left": (250, 1120), "right": (850, 1120)},
    "kitchen": {"counter": (330, 1050), "fridge": (640, 1120), "left": (200, 1120)},
    "living": {"sofa": (360, 1080), "sofa2": (520, 1080), "floor": (820, 1180)},
    "street": {"left": (300, 1120), "centre": (540, 1120), "right": (800, 1120)},
    "blank": {"centre": (540, 1120), "left": (300, 1120), "right": (800, 1120)},
}
