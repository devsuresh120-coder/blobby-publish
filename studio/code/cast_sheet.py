import math
from PIL import Image, ImageDraw, ImageFont
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F = lambda s: ImageFont.truetype(FONT, s)
OUTL = (40, 30, 30)

def body(d, cx, cy, bw, bh, col, col2, hair, eyes="open", mouth="smile", glasses=False, whiskers=False, ears=False, bow=False, tie=False, blazer=False):
    # legs
    for dx in (-bw*0.3, bw*0.3):
        d.line([cx+dx, cy+bh-30, cx+dx, cy+bh+40], fill=OUTL, width=16)
        d.ellipse([cx+dx-38, cy+bh+25, cx+dx+30, cy+bh+60], fill=(200,40,40) if not ears else (90,90,90), outline=OUTL, width=6)
    # arms
    d.line([cx-bw+10, cy+20, cx-bw-40, cy+90], fill=OUTL, width=16)
    d.line([cx+bw-10, cy+20, cx+bw+40, cy+90], fill=OUTL, width=16)
    if ears:
        d.polygon([(cx-bw+20, cy-bh+40), (cx-bw+10, cy-bh-70), (cx-bw+90, cy-bh+5)], fill=col, outline=OUTL)
        d.polygon([(cx+bw-20, cy-bh+40), (cx+bw-10, cy-bh-70), (cx+bw-90, cy-bh+5)], fill=col, outline=OUTL)
        d.line([cx+bw-20, cy+bh-60, cx+bw+90, cy+bh-120, cx+bw+120, cy+bh-40], fill=OUTL, width=18, joint="curve")
        d.line([cx+bw-20, cy+bh-60, cx+bw+90, cy+bh-120, cx+bw+120, cy+bh-40], fill=col, width=8, joint="curve")
    d.ellipse([cx-bw, cy-bh, cx+bw, cy+bh], fill=col, outline=OUTL, width=10)
    d.ellipse([cx-bw+30, cy+bh-110, cx+bw-30, cy+bh-20], fill=col2)
    d.ellipse([cx-bw, cy-bh, cx+bw, cy+bh], outline=OUTL, width=10)
    if blazer:
        jc = (45, 50, 80)
        # jacket panels (left/right), leaving a V for shirt
        for sx in (-1, 1):
            d.polygon([(cx, cy+bh-6), (cx+sx*(bw-6), cy+bh-6), (cx+sx*(bw-2), cy+70), (cx+sx*(bw-22), cy+40), (cx+sx*22, cy+95)], fill=jc, outline=OUTL)
            # lapel
            d.polygon([(cx+sx*22, cy+95), (cx+sx*(bw-22), cy+40), (cx+sx*(bw-70), cy+75), (cx+sx*40, cy+120)], fill=(70,78,115), outline=OUTL)
            # button
        d.ellipse([cx-8, cy+bh-50, cx+8, cy+bh-34], fill=(230,200,90), outline=OUTL, width=3)
        # shirt V
        d.polygon([(cx-22, cy+95), (cx+22, cy+95), (cx, cy+bh-40)], fill=(255,255,255), outline=OUTL)
        # pocket square
        d.polygon([(cx-bw+40, cy+120), (cx-bw+80, cy+112), (cx-bw+70, cy+135)], fill=(230,60,60))
    # hair
    if hair == "tuft":
        d.line([cx, cy-bh+5, cx-30, cy-bh-60], fill=OUTL, width=12)
        d.line([cx, cy-bh+5, cx+15, cy-bh-70], fill=OUTL, width=12)
    elif hair == "bun":
        d.ellipse([cx-35, cy-bh-70, cx+35, cy-bh], fill=(90,50,30), outline=OUTL, width=8)
        d.chord([cx-bw+10, cy-bh-5, cx+bw-10, cy-bh+120], 180, 360, fill=(90,50,30))
    elif hair == "side":
        d.chord([cx-bw+5, cy-bh-5, cx+bw-5, cy-bh+110], 190, 330, fill=(60,40,40))
        d.polygon([(cx-bw+40, cy-bh+25), (cx+20, cy-bh+15), (cx-bw+10, cy-bh+70)], fill=(60,40,40))
    ex, ey = bw*0.37, cy-40
    if whiskers:
        for sx in (-1,1):
            for k in (-1,0,1):
                d.line([cx+sx*40, cy+40+k*4, cx+sx*(bw+50), cy+40+k*22], fill=OUTL, width=6)
        d.polygon([(cx-18, cy+25), (cx+18, cy+25), (cx, cy+45)], fill=(230,120,140), outline=OUTL)
    if eyes == "half":
        for sx in (-1, 1):
            d.ellipse([cx+sx*ex-36, ey-36, cx+sx*ex+36, ey+36], fill=(255,255,255), outline=OUTL, width=8)
            d.ellipse([cx+sx*ex-14+6, ey-14+4, cx+sx*ex+14+6, ey+14+4], fill=OUTL)
            d.chord([cx+sx*ex-40, ey-40, cx+sx*ex+40, ey+40], 180, 360, fill=col, outline=OUTL, width=8)
    elif eyes == "cat":
        for sx in (-1, 1):
            d.ellipse([cx+sx*ex-34, ey-34, cx+sx*ex+34, ey+34], fill=(140,220,120), outline=OUTL, width=8)
            d.ellipse([cx+sx*ex-9, ey-26, cx+sx*ex+9, ey+26], fill=OUTL)
    else:
        for sx in (-1, 1):
            d.ellipse([cx+sx*ex-36, ey-36, cx+sx*ex+36, ey+36], fill=(255,255,255), outline=OUTL, width=8)
            d.ellipse([cx+sx*ex-16+6, ey-16+4, cx+sx*ex+16+6, ey+16+4], fill=OUTL)
            if eyes == "lash":
                for k in range(3):
                    a = math.radians(225 + k*25 if sx<0 else 315 - k*25)
                    x0, y0 = cx+sx*ex+40*math.cos(a), ey+40*math.sin(a)
                    d.line([x0, y0, x0+22*math.cos(a), y0+22*math.sin(a)], fill=OUTL, width=6)
    if glasses:
        for sx in (-1,1):
            d.rounded_rectangle([cx+sx*ex-48, ey-44, cx+sx*ex+48, ey+40], radius=14, outline=OUTL, width=8)
        d.line([cx-ex+48, ey-5, cx+ex-48, ey-5], fill=OUTL, width=8)
    my = cy+45
    if mouth == "smile": d.arc([cx-40, my-25, cx+40, my+25], 10, 170, fill=OUTL, width=10)
    elif mouth == "flat": d.line([cx-35, my+5, cx+35, my+5], fill=OUTL, width=10)
    elif mouth == "cat":
        d.arc([cx-30, my-20, cx, my+10], 0, 180, fill=OUTL, width=7); d.arc([cx, my-20, cx+30, my+10], 0, 180, fill=OUTL, width=7)
    if bow:
        d.polygon([(cx+bw-40, cy-bh+30), (cx+bw+30, cy-bh-20), (cx+bw+30, cy-bh+80)], fill=(230,60,90), outline=OUTL)
        d.polygon([(cx+bw-40, cy-bh+30), (cx+bw-110, cy-bh-20), (cx+bw-110, cy-bh+80)], fill=(230,60,90), outline=OUTL)
        d.ellipse([cx+bw-58, cy-bh+12, cx+bw-22, cy-bh+48], fill=(255,120,150), outline=OUTL, width=5)
    if tie:
        d.polygon([(cx-10, cy+95), (cx+10, cy+95), (cx+16, cy+bh-45), (cx, cy+bh-25), (cx-16, cy+bh-45)], fill=(200,40,40), outline=OUTL)
        d.polygon([(cx-12, cy+86), (cx+12, cy+86), (cx+8, cy+100), (cx-8, cy+100)], fill=(160,30,30), outline=OUTL)

def cat(d, cx, cy):
    orange=(240,150,60); dark=(205,110,35); cream=(255,235,200)
    # tail
    d.line([cx+100, cy+70, cx+165, cy+25, cx+150, cy-60], fill=OUTL, width=24, joint="curve")
    d.line([cx+100, cy+70, cx+165, cy+25, cx+150, cy-60], fill=orange, width=12, joint="curve")
    # body (sitting loaf)
    d.ellipse([cx-120, cy-20, cx+120, cy+130], fill=orange, outline=OUTL, width=9)
    d.ellipse([cx-70, cy+40, cx+70, cy+125], fill=cream)
    d.ellipse([cx-120, cy-20, cx+120, cy+130], outline=OUTL, width=9)
    for dx in (-60, -20, 20):
        d.line([cx+dx+60, cy-10, cx+dx+75, cy+20], fill=dark, width=10)
    # paws
    for dx in (-55, 55):
        d.ellipse([cx+dx-32, cy+100, cx+dx+32, cy+140], fill=orange, outline=OUTL, width=7)
    # ears
    d.polygon([(cx-95, cy-70), (cx-120, cy-180), (cx-30, cy-120)], fill=orange, outline=OUTL)
    d.polygon([(cx+95, cy-70), (cx+120, cy-180), (cx+30, cy-120)], fill=orange, outline=OUTL)
    d.polygon([(cx-90, cy-85), (cx-105, cy-155), (cx-45, cy-115)], fill=(255,170,170))
    d.polygon([(cx+90, cy-85), (cx+105, cy-155), (cx+45, cy-115)], fill=(255,170,170))
    # head (wide)
    d.ellipse([cx-125, cy-150, cx+125, cy+20], fill=orange, outline=OUTL, width=9)
    for dx in (-30, 0, 30):   # forehead stripes
        d.line([cx+dx, cy-145, cx+dx*1.3, cy-105], fill=dark, width=11)
    # eyes: big, round, mischievous half-moon lids
    for sx in (-1, 1):
        d.ellipse([cx+sx*50-34, cy-80, cx+sx*50+34, cy-12], fill=(255,255,255), outline=OUTL, width=7)
        d.ellipse([cx+sx*50-18, cy-62, cx+sx*50+18, cy-26], fill=(90,170,60))
        d.ellipse([cx+sx*50-8, cy-56, cx+sx*50+8, cy-32], fill=OUTL)
        d.ellipse([cx+sx*50-2, cy-58, cx+sx*50+8, cy-48], fill=(255,255,255))
    # muzzle, nose, mouth, whiskers
    d.ellipse([cx-45, cy-25, cx+45, cy+15], fill=cream)
    d.polygon([(cx-12, cy-22), (cx+12, cy-22), (cx, cy-8)], fill=(230,110,120), outline=OUTL)
    d.arc([cx-28, cy-18, cx, cy+8], 0, 180, fill=OUTL, width=6); d.arc([cx, cy-18, cx+28, cy+8], 0, 180, fill=OUTL, width=6)
    for sx in (-1,1):
        for k in (-1,0,1):
            d.line([cx+sx*40, cy-12+k*5, cx+sx*150, cy-20+k*22], fill=OUTL, width=5)
    # collar with bell
    d.arc([cx-92, cy-30, cx+92, cy+50], 25, 155, fill=(200,40,40), width=14)
    d.ellipse([cx-16, cy+32, cx+16, cy+64], fill=(240,200,60), outline=OUTL, width=5)

W, H = 1600, 1000
im = Image.new("RGB", (W, H), (246, 225, 190)); d = ImageDraw.Draw(im)
d.rectangle([0, 760, W, H], fill=(176,118,76))
d.text((W//2-330, 40), "BLOBBY & CO.  -  THE CAST", font=F(60), fill=(255,255,255), stroke_width=8, stroke_fill=OUTL)
cy = 560
body(d, 250, cy, 150, 170, (255,204,60), (225,165,30), "tuft")
body(d, 650, cy, 140, 165, (255,150,170), (230,110,135), "bun", eyes="lash", bow=True)
body(d, 1050, cy, 160, 180, (120,170,240), (85,135,205), "side", eyes="half", mouth="flat", glasses=True, tie=True, blazer=True)
cat(d, 1400, cy+95)
for x, name, role in [(250,"BLOBBY","the hero"),(650,"PINKY","the partner"),(1050,"BOSS","boss / friend"),(1400,"MEOW","the cat")]:
    bb = d.textbbox((0,0), name, font=F(48)); d.text((x-(bb[2]-bb[0])//2, 820), name, font=F(48), fill=(255,255,255), stroke_width=6, stroke_fill=OUTL)
    bb = d.textbbox((0,0), role, font=F(30)); d.text((x-(bb[2]-bb[0])//2, 885), role, font=F(30), fill=(255,230,80), stroke_width=4, stroke_fill=OUTL)
im.save("/home/claude/blobby_co_cast_sheet.png")
print("ok")
