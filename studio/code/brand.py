"""Blobby & Co. brand assets: logo (avatar), wordmark, YouTube banner, Facebook/IG cover, Shorts intro card.
python3 brand.py  -> ../brand/*.png"""
import math, os
from PIL import Image, ImageDraw, ImageFont
from characters import draw_character, CHAR_SIZE

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "brand"); os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F = lambda s: ImageFont.truetype(FONT, s)
YEL, DARK, CREAM, OUTL = (255, 204, 60), (40, 30, 30), (250, 240, 215), (40, 30, 30)


def text_c(d, s, cx, y, size, fill=(255, 255, 255), stroke=8, stroke_fill=(0, 0, 0)):
    f = F(size); bb = d.textbbox((0, 0), s, font=f)
    d.text((cx-(bb[2]-bb[0])//2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return bb[2]-bb[0]


def wordmark(width=0, bg=None):
    """'BLOBBY & CO.' — yellow letters, dark outline, '&' in red."""
    f = F(150); parts = [("BLOBBY", YEL), (" & ", (230, 60, 60)), ("CO.", YEL)]
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    total = sum(d0.textbbox((0, 0), p, font=f)[2] for p, _ in parts) + 40
    width = max(width, total)
    im = Image.new("RGBA", (width, 260), bg or (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = (width-total)//2 + 20
    for p, c in parts:
        d.text((x, 40), p, font=f, fill=c, stroke_width=10, stroke_fill=OUTL); x += d.textbbox((0, 0), p, font=f)[2]
    return im


def paste(img, layer, x, y, scale=1.0, angle=0):
    if scale != 1.0: layer = layer.resize((int(layer.width*scale), int(layer.height*scale)), Image.LANCZOS)
    if angle: layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(layer, (int(x-layer.width/2), int(y-layer.height/2)))


def logo_square(size=1024):
    """Avatar: Blobby's face bursting out of a yellow circle."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, size, size], fill=(230, 60, 60))
    d.ellipse([28, 28, size-28, size-28], fill=YEL, outline=OUTL, width=16)
    bl = draw_character("blobby", eyes="open", mouth="grin", arms="wave")
    paste(im, bl, size//2, size//2+40, scale=1.3)
    # clip to circle
    mask = Image.new("L", (size, size), 0); ImageDraw.Draw(mask).ellipse([28, 28, size-28, size-28], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0)); out.paste(im, (0, 0), mask)
    d2 = ImageDraw.Draw(out); d2.ellipse([0, 0, size, size], outline=(230, 60, 60), width=28); d2.ellipse([28, 28, size-28, size-28], outline=OUTL, width=12)
    # ribbon
    d2.rounded_rectangle([size*0.18, size*0.80, size*0.82, size*0.93], radius=40, fill=DARK)
    text_c(d2, "BLOBBY & CO.", size//2, int(size*0.815), 86, YEL, 0)
    out.save(os.path.join(OUT, "logo_square_1024.png"))
    out.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, "logo_square_512.png"))


def cast_row(img, cx, cy, scale=1.0, gap=330):
    chars = [("pinky", dict(eyes="happy", mouth="smile")), ("blobby", dict(eyes="open", mouth="grin", arms="wave")),
             ("boss", dict(eyes="half", mouth="flat", arms="cross")), ("meow", dict(eyes="wide", mouth="smile"))]
    xs = [cx + (i-1.5)*gap*scale for i in range(4)]
    for (name, kw), x in zip(chars, xs):
        ly = cy + (90*scale if name == "meow" else 0)
        paste(img, draw_character(name, **kw), x, ly, scale=(0.95 if name != "blobby" else 1.1)*scale)


def youtube_banner():
    """2560x1440; everything important inside the 1546x423 centre safe area."""
    W, H = 2560, 1440; im = Image.new("RGBA", (W, H), CREAM); d = ImageDraw.Draw(im)
    for i in range(0, W, 160):   # soft stripes
        d.polygon([(i, 0), (i+80, 0), (i+80-400, H), (i-400, H)], fill=(245, 230, 195))
    d.rectangle([0, H-260, W, H], fill=(176, 118, 76))
    sx, sy = (W-1546)//2, (H-423)//2
    cast_row(im, sx+1200, sy+300, scale=0.5, gap=260)
    d = ImageDraw.Draw(im)
    wm = wordmark(); im.alpha_composite(wm.resize((640, int(640*wm.height/wm.width)), Image.LANCZOS), (sx+40, sy+60))
    d = ImageDraw.Draw(im)
    d.text((sx+60, sy+215), "Silent comedy about daily life.", font=F(44), fill=DARK)
    d.text((sx+60, sy+275), "New episode every day.", font=F(44), fill=DARK)
    d.rounded_rectangle([sx+60, sy+345, sx+330, sy+410], radius=32, fill=(230, 60, 60))
    d.text((sx+95, sy+357), "@blobbyco", font=F(36), fill=(255, 255, 255))
    im.convert("RGB").save(os.path.join(OUT, "youtube_banner_2560x1440.png"))


def facebook_cover():
    """1640x624 (also fine for Facebook Page + IG highlight)."""
    W, H = 1640, 624; im = Image.new("RGBA", (W, H), CREAM); d = ImageDraw.Draw(im)
    d.rectangle([0, H-120, W, H], fill=(176, 118, 76))
    cast_row(im, 1230, 330, scale=0.7, gap=280)
    d = ImageDraw.Draw(im)
    wm = wordmark(); im.alpha_composite(wm.resize((680, int(680*wm.height/wm.width)), Image.LANCZOS), (60, 110))
    d = ImageDraw.Draw(im)
    d.text((90, 290), "Silent comedy about daily life.", font=F(40), fill=DARK)
    d.text((90, 345), "New episode every day.", font=F(40), fill=DARK)
    d.rounded_rectangle([90, 420, 380, 480], radius=30, fill=(230, 60, 60)); d.text((120, 430), "@blobbyco", font=F(34), fill=(255, 255, 255))
    im.convert("RGB").save(os.path.join(OUT, "facebook_cover_1640x624.png"))


def intro_card():
    """9:16 'meet the cast' card for the first post / Shorts intro."""
    W, H = 1080, 1920; im = Image.new("RGBA", (W, H), CREAM); d = ImageDraw.Draw(im)
    d.rectangle([0, 1400, W, H], fill=(176, 118, 76))
    wm = wordmark(); im.alpha_composite(wm.resize((940, int(940*wm.height/wm.width)), Image.LANCZOS), (70, 190))
    d = ImageDraw.Draw(im); text_c(d, "MEET THE CAST", W//2, 400, 56, DARK, 0)
    for (name, kw, label, x, y) in [("blobby", dict(eyes="open", mouth="grin", arms="wave"), "Blobby", 300, 760),
                                    ("pinky", dict(eyes="happy", mouth="smile"), "Pinky", 780, 760),
                                    ("boss", dict(eyes="half", mouth="flat", arms="cross"), "Boss", 300, 1230),
                                    ("meow", dict(eyes="wide", mouth="smile"), "Meow", 780, 1300)]:
        paste(im, draw_character(name, **kw), x, y, scale=0.9)
        d = ImageDraw.Draw(im); text_c(d, label, x, y+230 if name != "meow" else y+160, 54)
    text_c(d, "Which one are you?", W//2, 1640, 60, YEL)
    text_c(d, "@blobbyco", W//2, 1760, 44, (255, 255, 255), 4)
    im.convert("RGB").save(os.path.join(OUT, "intro_card_1080x1920.png"))


if __name__ == "__main__":
    logo_square(); youtube_banner(); facebook_cover(); intro_card()
    wordmark().save(os.path.join(OUT, "wordmark_transparent.png"))
    print("brand assets ->", OUT)
