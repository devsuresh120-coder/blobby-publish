"""Blobby & Co. cast — Blobby, Pinky, Boss, Meow.
Every character is drawn into a transparent RGBA layer (CHAR_SIZE square), then
placed by engine.place(). Never change colours / shapes here: the look is fixed.
"""
import math
from PIL import Image, ImageDraw

CHAR_SIZE = 520
OUTL = (40, 30, 30)
WHITE = (255, 255, 255)

PALETTE = {
    "blobby": dict(col=(255, 204, 60), col2=(225, 165, 30), hair="tuft", shoes=(200, 40, 40)),
    "pinky":  dict(col=(255, 150, 170), col2=(230, 110, 135), hair="bun", shoes=(200, 40, 40), lash=True, bow=True),
    "boss":   dict(col=(120, 170, 240), col2=(85, 135, 205), hair="side", shoes=(60, 60, 60), glasses=True, blazer=True, tie=True),
}

# eyes: open | wide | closed | half | spiral | happy | angry | hearts
# mouth: smile | grin | o | flat | wavy | sad | tongue
# arms: down | up | flex | flail | hold | wave | cross | point
# legs: stand | step | sit | lie | run


def _eye(d, x, y, kind, col, pupil_dx=0):
    if kind == "closed":
        d.arc([x-36, y-20, x+36, y+30], 0, 180, fill=OUTL, width=10)
    elif kind == "happy":
        d.arc([x-36, y-10, x+36, y+40], 180, 360, fill=OUTL, width=10)
    elif kind == "spiral":
        pts = [(x + i*0.6*math.cos(i*0.45), y + i*0.6*math.sin(i*0.45)) for i in range(60)]
        d.line(pts, fill=OUTL, width=8)
    elif kind == "hearts":
        d.polygon([(x, y+30), (x-34, y-5), (x-18, y-28), (x, y-12), (x+18, y-28), (x+34, y-5)], fill=(230, 50, 90), outline=OUTL)
    else:
        r = 46 if kind == "wide" else 36
        d.ellipse([x-r, y-r, x+r, y+r], fill=WHITE, outline=OUTL, width=8)
        pr = 10 if kind == "wide" else 16
        d.ellipse([x-pr+6+pupil_dx, y-pr+4, x+pr+6+pupil_dx, y+pr+4], fill=OUTL)
        if kind == "half":
            d.chord([x-r-4, y-r-4, x+r+4, y+r+4], 180, 360, fill=col, outline=OUTL, width=8)


def _mouth(d, cx, my, kind):
    if kind == "smile":
        d.arc([cx-40, my-25, cx+40, my+25], 10, 170, fill=OUTL, width=10)
    elif kind == "grin":
        d.chord([cx-55, my-30, cx+55, my+40], 0, 180, fill=(120, 30, 40), outline=OUTL, width=8)
        d.rectangle([cx-45, my-2, cx+45, my+12], fill=WHITE)
    elif kind == "o":
        d.ellipse([cx-28, my-30, cx+28, my+30], fill=(120, 30, 40), outline=OUTL, width=8)
    elif kind == "flat":
        d.line([cx-35, my, cx+35, my], fill=OUTL, width=10)
    elif kind == "wavy":
        d.line([(cx-45+i*9, my + (10 if i % 2 else -10)) for i in range(11)], fill=OUTL, width=9)
    elif kind == "sad":
        d.arc([cx-40, my-5, cx+40, my+45], 190, 350, fill=OUTL, width=10)
    elif kind == "tongue":
        d.chord([cx-45, my-25, cx+45, my+35], 0, 180, fill=(120, 30, 40), outline=OUTL, width=8)
        d.ellipse([cx-18, my+5, cx+18, my+40], fill=(240, 100, 120), outline=OUTL, width=5)


def blob(name, eyes="open", mouth="smile", arms="down", legs="stand", brows=False,
         squash=1.0, pupil_dx=0, prop=None):
    p = PALETTE[name]
    col, col2, shoes = p["col"], p["col2"], p["shoes"]
    S = CHAR_SIZE
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = S//2, S//2 - 20
    bw, bh = 150, int(170*squash)
    # legs
    if legs == "stand":
        for dx in (-45, 45):
            d.line([cx+dx, cy+bh-30, cx+dx, cy+bh+40], fill=OUTL, width=16)
            d.ellipse([cx+dx-38, cy+bh+25, cx+dx+30, cy+bh+60], fill=shoes, outline=OUTL, width=6)
    elif legs in ("step", "run"):
        k = 1.6 if legs == "run" else 1.0
        d.line([cx-45, cy+bh-30, cx-45-35*k, cy+bh+40], fill=OUTL, width=16)
        d.ellipse([cx-80*k-35, cy+bh+25, cx-80*k+30, cy+bh+60], fill=shoes, outline=OUTL, width=6)
        d.line([cx+45, cy+bh-30, cx+45+45*k, cy+bh+10-20*(k-1)], fill=OUTL, width=16)
        d.ellipse([cx+60*k, cy+bh-10-20*(k-1), cx+60*k+65, cy+bh+25-20*(k-1)], fill=shoes, outline=OUTL, width=6)
    elif legs == "sit":
        for dx in (-45, 45):
            d.line([cx+dx, cy+bh-40, cx+dx+70, cy+bh-40], fill=OUTL, width=16)
            d.ellipse([cx+dx+55, cy+bh-65, cx+dx+110, cy+bh-15], fill=shoes, outline=OUTL, width=6)
    # arms
    if arms == "down":
        d.line([cx-bw+10, cy+20, cx-bw-40, cy+90], fill=OUTL, width=16)
        d.line([cx+bw-10, cy+20, cx+bw+40, cy+90], fill=OUTL, width=16)
    elif arms == "flex":
        for sx in (-1, 1):
            d.line([cx+sx*(bw-10), cy+10, cx+sx*(bw+50), cy-20, cx+sx*(bw+30), cy-90], fill=OUTL, width=16, joint="curve")
            d.ellipse([cx+sx*(bw+30)-25, cy-115, cx+sx*(bw+30)+25, cy-65], fill=col, outline=OUTL, width=6)
    elif arms == "up":
        d.line([cx-bw+10, cy, cx-bw-30, cy-120], fill=OUTL, width=16)
        d.line([cx+bw-10, cy, cx+bw+30, cy-120], fill=OUTL, width=16)
    elif arms == "flail":
        d.line([cx-bw+10, cy, cx-bw-60, cy-60], fill=OUTL, width=16)
        d.line([cx+bw-10, cy, cx+bw+60, cy+30], fill=OUTL, width=16)
    elif arms == "wave":
        d.line([cx-bw+10, cy+20, cx-bw-40, cy+90], fill=OUTL, width=16)
        d.line([cx+bw-10, cy, cx+bw+45, cy-100], fill=OUTL, width=16)
        d.ellipse([cx+bw+20, cy-125, cx+bw+70, cy-75], fill=col, outline=OUTL, width=6)
    elif arms == "hold":   # both hands in front (holding a prop at chest)
        d.line([cx-bw+10, cy+30, cx-60, cy+70], fill=OUTL, width=16)
        d.line([cx+bw-10, cy+30, cx+60, cy+70], fill=OUTL, width=16)
    elif arms == "cross":
        d.line([cx-bw+10, cy+20, cx+50, cy+60], fill=OUTL, width=16)
        d.line([cx+bw-10, cy+20, cx-50, cy+60], fill=OUTL, width=16)
    elif arms == "point":
        d.line([cx-bw+10, cy+20, cx-bw-40, cy+90], fill=OUTL, width=16)
        d.line([cx+bw-10, cy+10, cx+bw+110, cy-10], fill=OUTL, width=16)
    # body
    d.ellipse([cx-bw, cy-bh, cx+bw, cy+bh], fill=col, outline=OUTL, width=10)
    d.ellipse([cx-bw+30, cy+bh-110, cx+bw-30, cy+bh-20], fill=col2)
    d.ellipse([cx-bw, cy-bh, cx+bw, cy+bh], outline=OUTL, width=10)
    if p.get("blazer"):
        jc, lap = (45, 50, 80), (70, 78, 115)
        for sx in (-1, 1):
            d.polygon([(cx, cy+bh-6), (cx+sx*(bw-6), cy+bh-6), (cx+sx*(bw-2), cy+70), (cx+sx*(bw-22), cy+40), (cx+sx*22, cy+95)], fill=jc, outline=OUTL)
            d.polygon([(cx+sx*22, cy+95), (cx+sx*(bw-22), cy+40), (cx+sx*(bw-70), cy+75), (cx+sx*40, cy+120)], fill=lap, outline=OUTL)
        d.ellipse([cx-8, cy+bh-50, cx+8, cy+bh-34], fill=(230, 200, 90), outline=OUTL, width=3)
        d.polygon([(cx-22, cy+95), (cx+22, cy+95), (cx, cy+bh-40)], fill=WHITE, outline=OUTL)
        d.polygon([(cx-bw+40, cy+120), (cx-bw+80, cy+112), (cx-bw+70, cy+135)], fill=(230, 60, 60))
    if p.get("tie"):
        d.polygon([(cx-10, cy+95), (cx+10, cy+95), (cx+16, cy+bh-45), (cx, cy+bh-25), (cx-16, cy+bh-45)], fill=(200, 40, 40), outline=OUTL)
        d.polygon([(cx-12, cy+86), (cx+12, cy+86), (cx+8, cy+100), (cx-8, cy+100)], fill=(160, 30, 30), outline=OUTL)
    # hair
    hair = p["hair"]
    if hair == "tuft":
        d.line([cx, cy-bh+5, cx-30, cy-bh-60], fill=OUTL, width=12)
        d.line([cx, cy-bh+5, cx+15, cy-bh-70], fill=OUTL, width=12)
    elif hair == "bun":
        d.ellipse([cx-35, cy-bh-70, cx+35, cy-bh], fill=(90, 50, 30), outline=OUTL, width=8)
        d.chord([cx-bw+10, cy-bh-5, cx+bw-10, cy-bh+120], 180, 360, fill=(90, 50, 30))
    elif hair == "side":
        d.chord([cx-bw+5, cy-bh-5, cx+bw-5, cy-bh+110], 190, 330, fill=(60, 40, 40))
        d.polygon([(cx-bw+40, cy-bh+25), (cx+20, cy-bh+15), (cx-bw+10, cy-bh+70)], fill=(60, 40, 40))
    if p.get("bow"):
        d.polygon([(cx+bw-40, cy-bh+30), (cx+bw+30, cy-bh-20), (cx+bw+30, cy-bh+80)], fill=(230, 60, 90), outline=OUTL)
        d.polygon([(cx+bw-40, cy-bh+30), (cx+bw-110, cy-bh-20), (cx+bw-110, cy-bh+80)], fill=(230, 60, 90), outline=OUTL)
        d.ellipse([cx+bw-58, cy-bh+12, cx+bw-22, cy-bh+48], fill=(255, 120, 150), outline=OUTL, width=5)
    # eyes
    ex, ey = 55, cy-40
    for sx in (-1, 1):
        _eye(d, cx+sx*ex, ey, eyes, col, pupil_dx)
    if p.get("lash") and eyes in ("open", "wide", "half"):
        for sx in (-1, 1):
            for k in range(3):
                a = math.radians(225 + k*25 if sx < 0 else 315 - k*25)
                x0, y0 = cx+sx*ex+40*math.cos(a), ey+40*math.sin(a)
                d.line([x0, y0, x0+22*math.cos(a), y0+22*math.sin(a)], fill=OUTL, width=6)
    if brows or eyes == "angry":
        d.line([cx-ex-45, ey-70, cx-ex+30, ey-45], fill=OUTL, width=12)
        d.line([cx+ex+45, ey-70, cx+ex-30, ey-45], fill=OUTL, width=12)
    if p.get("glasses"):
        for sx in (-1, 1):
            d.rounded_rectangle([cx+sx*ex-48, ey-44, cx+sx*ex+48, ey+40], radius=14, outline=OUTL, width=8)
        d.line([cx-ex+48, ey-5, cx+ex-48, ey-5], fill=OUTL, width=8)
    _mouth(d, cx, cy+45, mouth)
    if prop:
        from props import draw_prop
        draw_prop(d, prop, cx, cy+70)
    return im


def cat(eyes="open", mouth="smile", pose="sit", prop=None):
    """Meow — orange tabby. poses: sit | pounce | sleep | stare(eyes=half)"""
    orange, dark, cream = (240, 150, 60), (205, 110, 35), (255, 235, 200)
    S = CHAR_SIZE
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = S//2, S//2 + 60
    if pose == "sleep":
        d.ellipse([cx-150, cy-10, cx+150, cy+120], fill=orange, outline=OUTL, width=9)
        d.ellipse([cx-110, cy-110, cx+40, cy+10], fill=orange, outline=OUTL, width=9)
        d.polygon([(cx-100, cy-90), (cx-120, cy-170), (cx-50, cy-110)], fill=orange, outline=OUTL)
        d.polygon([(cx-10, cy-95), (cx+20, cy-165), (cx+30, cy-90)], fill=orange, outline=OUTL)
        for sx in (-70, -5):
            d.arc([cx+sx-18, cy-65, cx+sx+18, cy-35], 0, 180, fill=OUTL, width=6)
        d.line([cx+140, cy+60, cx+200, cy+10, cx+180, cy-60], fill=OUTL, width=22, joint="curve")
        d.line([cx+140, cy+60, cx+200, cy+10, cx+180, cy-60], fill=orange, width=10, joint="curve")
        return im
    tail = [cx+100, cy+70, cx+165, cy+25, cx+150, cy-60]
    if pose == "pounce":
        tail = [cx+100, cy+40, cx+190, cy+10, cx+230, cy-40]
    d.line(tail, fill=OUTL, width=24, joint="curve"); d.line(tail, fill=orange, width=12, joint="curve")
    if pose == "pounce":
        d.ellipse([cx-140, cy-10, cx+120, cy+110], fill=orange, outline=OUTL, width=9)
        for dx in (-120, 100):
            d.ellipse([cx+dx-32, cy+40, cx+dx+32, cy+80], fill=orange, outline=OUTL, width=7)
        hx, hy = cx-70, cy-20
    else:
        d.ellipse([cx-120, cy-20, cx+120, cy+130], fill=orange, outline=OUTL, width=9)
        d.ellipse([cx-70, cy+40, cx+70, cy+125], fill=cream)
        d.ellipse([cx-120, cy-20, cx+120, cy+130], outline=OUTL, width=9)
        for dx in (0, 40, 80):
            d.line([cx+dx, cy-10, cx+dx+15, cy+20], fill=dark, width=10)
        for dx in (-55, 55):
            d.ellipse([cx+dx-32, cy+100, cx+dx+32, cy+140], fill=orange, outline=OUTL, width=7)
        hx, hy = cx, cy
    # head
    d.polygon([(hx-95, hy-70), (hx-120, hy-180), (hx-30, hy-120)], fill=orange, outline=OUTL)
    d.polygon([(hx+95, hy-70), (hx+120, hy-180), (hx+30, hy-120)], fill=orange, outline=OUTL)
    d.polygon([(hx-90, hy-85), (hx-105, hy-155), (hx-45, hy-115)], fill=(255, 170, 170))
    d.polygon([(hx+90, hy-85), (hx+105, hy-155), (hx+45, hy-115)], fill=(255, 170, 170))
    d.ellipse([hx-125, hy-150, hx+125, hy+20], fill=orange, outline=OUTL, width=9)
    for dx in (-30, 0, 30):
        d.line([hx+dx, hy-145, hx+dx*1.3, hy-105], fill=dark, width=11)
    for sx in (-1, 1):
        x = hx+sx*50; y = hy-46
        if eyes == "closed":
            d.arc([x-30, y-15, x+30, y+20], 0, 180, fill=OUTL, width=8)
        elif eyes == "angry":
            d.ellipse([x-34, y-34, x+34, y+34], fill=WHITE, outline=OUTL, width=7)
            d.ellipse([x-9, y-26, x+9, y+26], fill=OUTL)
            d.line([x-40, y-50 if sx < 0 else y-25, x+40, y-25 if sx < 0 else y-50], fill=OUTL, width=10)
        else:
            d.ellipse([x-34, y-34, x+34, y+34], fill=WHITE, outline=OUTL, width=7)
            d.ellipse([x-18, y-18, x+18, y+18], fill=(90, 170, 60))
            if eyes == "wide":
                d.ellipse([x-16, y-20, x+16, y+20], fill=OUTL)
            else:
                d.ellipse([x-8, y-22, x+8, y+22], fill=OUTL)
            d.ellipse([x-2, y-24, x+8, y-14], fill=WHITE)
            if eyes == "half":
                d.chord([x-38, y-38, x+38, y+38], 180, 360, fill=orange, outline=OUTL, width=7)
    d.ellipse([hx-45, hy-25, hx+45, hy+15], fill=cream)
    d.polygon([(hx-12, hy-22), (hx+12, hy-22), (hx, hy-8)], fill=(230, 110, 120), outline=OUTL)
    if mouth == "o":
        d.ellipse([hx-14, hy-8, hx+14, hy+14], fill=(120, 30, 40), outline=OUTL, width=5)
    elif mouth == "grin":
        d.chord([hx-35, hy-15, hx+35, hy+20], 0, 180, fill=(120, 30, 40), outline=OUTL, width=5)
    else:
        d.arc([hx-28, hy-18, hx, hy+8], 0, 180, fill=OUTL, width=6); d.arc([hx, hy-18, hx+28, hy+8], 0, 180, fill=OUTL, width=6)
    for sx in (-1, 1):
        for k in (-1, 0, 1):
            d.line([hx+sx*40, hy-12+k*5, hx+sx*150, hy-20+k*22], fill=OUTL, width=5)
    d.arc([hx-92, hy-30, hx+92, hy+50], 25, 155, fill=(200, 40, 40), width=14)
    d.ellipse([hx-16, hy+32, hx+16, hy+64], fill=(240, 200, 60), outline=OUTL, width=5)
    if prop:
        from props import draw_prop
        draw_prop(d, prop, hx+80, hy+60)
    return im


def draw_character(name, **kw):
    if name == "meow":
        return cat(**{k: v for k, v in kw.items() if k in ("eyes", "mouth", "pose", "prop")})
    return blob(name, **{k: v for k, v in kw.items() if k in ("eyes", "mouth", "arms", "legs", "brows", "squash", "pupil_dx", "prop")})
