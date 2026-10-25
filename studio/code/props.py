"""Small props drawn at a point (held by a character or placed on a stage)."""
from PIL import ImageDraw
OUTL = (40, 30, 30)


def draw_prop(d, name, x, y, scale=1.0):
    s = scale
    if name == "phone":
        d.rounded_rectangle([x-35*s, y-60*s, x+35*s, y+60*s], radius=10, fill=(40, 40, 50), outline=OUTL, width=6)
        d.rectangle([x-28*s, y-50*s, x+28*s, y+45*s], fill=(120, 200, 255))
    elif name == "coffee":
        d.rectangle([x-35*s, y-40*s, x+35*s, y+40*s], fill=(250, 250, 250), outline=OUTL, width=6)
        d.arc([x+25*s, y-25*s, x+65*s, y+20*s], 270, 90, fill=OUTL, width=8)
        d.ellipse([x-28*s, y-50*s, x+28*s, y-30*s], fill=(110, 70, 40))
        for k in (-15, 0, 15):
            d.line([x+k*s, y-60*s, x+k*s+6, y-95*s], fill=(180, 180, 180), width=4)
    elif name == "laptop":
        d.rectangle([x-90*s, y-70*s, x+90*s, y+5*s], fill=(70, 70, 80), outline=OUTL, width=6)
        d.rectangle([x-80*s, y-62*s, x+80*s, y-3*s], fill=(150, 210, 255))
        d.polygon([(x-110*s, y+25*s), (x+110*s, y+25*s), (x+95*s, y+5*s), (x-95*s, y+5*s)], fill=(90, 90, 100), outline=OUTL)
    elif name == "pizza":
        d.pieslice([x-70*s, y-70*s, x+70*s, y+70*s], 200, 340, fill=(240, 200, 90), outline=OUTL, width=6)
        d.pieslice([x-55*s, y-55*s, x+55*s, y+55*s], 205, 335, fill=(220, 70, 50))
        for px, py in ((-15, -40), (15, -30), (0, -15)):
            d.ellipse([x+px*s-8, y+py*s-8, x+px*s+8, y+py*s+8], fill=(150, 40, 40))
    elif name == "money":
        d.rectangle([x-60*s, y-30*s, x+60*s, y+30*s], fill=(110, 190, 110), outline=OUTL, width=5)
        d.ellipse([x-18*s, y-18*s, x+18*s, y+18*s], outline=OUTL, width=4)
        d.text((x-9*s, y-12*s), "$", fill=OUTL)
    elif name == "burger":
        d.chord([x-55*s, y-55*s, x+55*s, y+5*s], 180, 360, fill=(230, 170, 90), outline=OUTL, width=5)
        d.rectangle([x-55*s, y-20*s, x+55*s, y-5*s], fill=(120, 200, 80), outline=OUTL, width=4)
        d.rectangle([x-55*s, y-5*s, x+55*s, y+12*s], fill=(110, 60, 40), outline=OUTL, width=4)
        d.rounded_rectangle([x-55*s, y+12*s, x+55*s, y+35*s], radius=8, fill=(230, 170, 90), outline=OUTL, width=5)
    elif name == "gift":
        d.rectangle([x-50*s, y-40*s, x+50*s, y+50*s], fill=(230, 80, 110), outline=OUTL, width=6)
        d.rectangle([x-8*s, y-40*s, x+8*s, y+50*s], fill=(255, 220, 80))
        d.rectangle([x-50*s, y-5*s, x+50*s, y+8*s], fill=(255, 220, 80))
    elif name == "ball":
        d.ellipse([x-30*s, y-30*s, x+30*s, y+30*s], fill=(230, 60, 60), outline=OUTL, width=5)
    elif name == "paper":
        d.rectangle([x-45*s, y-60*s, x+45*s, y+60*s], fill=(255, 255, 255), outline=OUTL, width=5)
        for k in range(4):
            d.line([x-30*s, y-40*s+k*25*s, x+30*s, y-40*s+k*25*s], fill=(150, 150, 150), width=4)
    elif name == "remote":
        d.rounded_rectangle([x-20*s, y-60*s, x+20*s, y+60*s], radius=8, fill=(60, 60, 60), outline=OUTL, width=5)
        for k in range(4):
            d.ellipse([x-8, y-45+k*22, x+8, y-29+k*22], fill=(200, 200, 200))
    elif name == "ring":
        d.ellipse([x-30*s, y-20*s, x+30*s, y+30*s], outline=(240, 200, 60), width=12)
        d.polygon([(x-15*s, y-25*s), (x+15*s, y-25*s), (x, y-50*s)], fill=(160, 230, 255), outline=OUTL)
