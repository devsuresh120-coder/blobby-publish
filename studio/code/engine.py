"""Blobby & Co. render engine.
An episode is a dict (see EPISODE_TEMPLATE in new_batch.py). render(ep) -> episodes/epNN.mp4 + cover jpg + QA strip.

Beat keys:
  dur        seconds
  stage      dict of stage state (night/alarm/clock/screen/tv/rain/fridge_open ...)
  chars      {name: dict(at=(x,y), angle=0, scale=1.0, eyes, mouth, arms, legs, pose, brows, squash, prop,
                         fx=None|"zzz"|"stars"|"sweat"|"hearts"|"exclaim"|"question"|"sparkle"|"anger"|"impact"|"music",
                         flip=False, tween=True)}   # tween: ease at/angle/scale from previous beat
  caption    top meme text ("\n" for line breaks; auto-wrap otherwise)
  sub        small bottom text (optional)
  sfx        [(name, offset_seconds[, gain])]
  (episode-level) music=True  light generated background loop under the SFX; music=False to turn off
  (episode-level) loop=True   no end card, no end sfx, no voice, music without fade -> the video flows straight back into beat 1 (seamless loop)
  (episode-level) voice=True  spoken end-card line (default "Which one are you? Tell us in the comments!"); voice_line="..." to change
  overlay    None | "blanket" (covers a sleeper) | "blanket_up" (pushed aside, in front) | "blanket_back" (pushed aside, behind the character — use when awake/standing)   (bedroom only)
  shake      camera shake amplitude px
  bubble     (name, text) small thought bubble above that character
  vox        [(char, "Ahh!", offset[, gain[, stretch_to_seconds]])]  short human reaction sounds (no words): "Ahh!", "Haaa...", "Mmm hmm", "Ooh!", "Huh?", "Ugh", "Yay!", "Uh oh"
             voiced per character (Blobby/Boss: male voice, pitched; Pinky: female voice)
"""
import math, os, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont
import stages, sfx as sfxlib
from characters import draw_character, CHAR_SIZE

W, H, FPS = 1080, 1920, 24
HERE = os.path.dirname(os.path.abspath(__file__))
EPISODES = os.path.join(os.path.dirname(HERE), "episodes")
V3 = os.environ.get("BC_FORMAT", "v3") != "v2"   # v3: closer camera, bigger captions, music per episode
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUTL = (40, 30, 30)
_fonts = {}
def font(size):
    if size not in _fonts: _fonts[size] = ImageFont.truetype(FONT_PATH, size)
    return _fonts[size]

def ease(a, b, k):
    k = max(0.0, min(1.0, k)); k = k*k*(3-2*k); return a + (b-a)*k

def wrap(text, width=16):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            if len(line) + len(w) + 1 > width and line:
                out.append(line); line = w
            else:
                line = (line + " " + w).strip()
        out.append(line)
    return out

def meme_text(d, text, y, size=82, fill=(255, 255, 255), width=16):
    f = font(size)
    for i, line in enumerate(wrap(text, width)):
        bb = d.textbbox((0, 0), line, font=f)
        d.text(((W-(bb[2]-bb[0]))//2, y+i*(size+14)), line, font=f, fill=fill, stroke_width=8, stroke_fill=(0, 0, 0))

def place(img, layer, x, y, angle=0, scale=1.0, flip=False):
    if flip: layer = layer.transpose(Image.FLIP_LEFT_RIGHT)
    if scale != 1.0: layer = layer.resize((int(layer.width*scale), int(layer.height*scale)), Image.LANCZOS)
    if angle: layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(layer, (int(x-layer.width/2), int(y-layer.height/2)))

# ---- effects --------------------------------------------------------------
def fx_draw(d, kind, x, y, t, scale=1.0):
    if kind == "zzz":
        for i in range(3):
            ph = (t*0.6 + i*0.33) % 1.0; size = int((40+30*ph)*scale)
            d.text((x+100*scale+40*ph+i*20, y-80*scale-160*ph), "z", font=font(size), fill=(90, 90, 200, int(255*(1-ph))))
    elif kind == "stars":
        for i in range(5):
            a = t*5 + i*2*math.pi/5
            d.text((x+120*scale*math.cos(a)-20, y-140*scale+35*math.sin(a)), "*", font=font(64), fill=(255, 210, 0), stroke_width=4, stroke_fill=OUTL)
    elif kind == "sweat":
        ph = (t*1.5) % 1.0
        d.ellipse([x+110*scale, y-120*scale+60*ph, x+140*scale, y-80*scale+60*ph], fill=(120, 190, 255), outline=OUTL, width=4)
    elif kind == "hearts":
        for i in range(3):
            ph = (t*0.5 + i*0.33) % 1.0; hx, hy = x+(i-1)*70*scale, y-150*scale-140*ph; s = 18+10*ph
            d.polygon([(hx, hy+s), (hx-s, hy-s*0.3), (hx-s*0.5, hy-s), (hx, hy-s*0.4), (hx+s*0.5, hy-s), (hx+s, hy-s*0.3)], fill=(230, 50, 90, int(255*(1-ph))), outline=OUTL)
    elif kind == "exclaim":
        d.text((x+120*scale, y-250*scale+int(8*math.sin(t*20))), "!!", font=font(90), fill=(230, 40, 40), stroke_width=6, stroke_fill=OUTL)
    elif kind == "question":
        d.text((x+110*scale, y-250*scale+int(8*math.sin(t*6))), "?", font=font(100), fill=(255, 255, 255), stroke_width=6, stroke_fill=OUTL)
    elif kind == "sparkle":
        for i in range(4):
            a = t*3 + i*1.57
            d.text((x-200+i*130, y-260*scale+40*math.sin(a)), "+", font=font(64), fill=(255, 230, 80), stroke_width=4, stroke_fill=OUTL)
    elif kind == "anger":
        ax, ay = x+120*scale, y-200*scale
        for dx, dy in ((0, 0), (30, 30)):
            d.line([ax+dx-25, ay+dy, ax+dx+25, ay+dy], fill=(220, 40, 40), width=8); d.line([ax+dx, ay+dy-25, ax+dx, ay+dy+25], fill=(220, 40, 40), width=8)
    elif kind == "impact":
        for a in range(0, 360, 40):
            r = math.radians(a); d.line([x+130*math.cos(r), y+130*math.sin(r), x+250*math.cos(r), y+250*math.sin(r)], fill=OUTL, width=10)
    elif kind == "music":
        for i in range(3):
            ph = (t*0.5 + i*0.33) % 1.0
            d.text((x+90*scale+30*math.sin(ph*6)+i*30, y-150*scale-150*ph), "♪", font=font(70), fill=(90, 90, 200, int(255*(1-ph))), stroke_width=3, stroke_fill=OUTL)

def bubble(d, x, y, text):
    f = font(46); lines = wrap(text, 14)
    bw = max(d.textbbox((0, 0), l, font=f)[2] for l in lines) + 60; bh = len(lines)*58 + 40
    bx, by = x - bw//2, y - 300 - bh
    bx = max(20, min(W-bw-20, bx))
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=30, fill=(255, 255, 255), outline=OUTL, width=6)
    d.ellipse([x-18, by+bh+20, x+18, by+bh+56], fill=(255, 255, 255), outline=OUTL, width=5)
    d.ellipse([x-8, by+bh+70, x+8, by+bh+86], fill=(255, 255, 255), outline=OUTL, width=4)
    for i, l in enumerate(lines):
        d.text((bx+30, by+20+i*58), l, font=f, fill=OUTL)

# ---- voice (piper, offline) ----
VOICE_LINE_DEFAULT = "Which one are you? Tell us in the comments!"
VOICE_DIR = os.path.join(os.path.dirname(HERE), "voices")
_voice_cache = {}
def voice_line(text):
    """Synthesize a short line with the bundled piper voice -> float array at SR. None if piper/voice missing."""
    if text in _voice_cache: return _voice_cache[text]
    try:
        import wave, io, numpy as np
        from piper import PiperVoice
        model = os.path.join(VOICE_DIR, "en-us-amy-low.onnx")
        if not os.path.exists(model): return None
        vc = PiperVoice.load(model)
        tmp = os.path.join(VOICE_DIR, f"_line{os.getpid()}.wav")
        try:
            from piper import SynthesisConfig
            cfg = SynthesisConfig(length_scale=0.9)
            with wave.open(tmp, "wb") as w: vc.synthesize_wav(text, w, syn_config=cfg)
        except Exception:
            with wave.open(tmp, "wb") as w: vc.synthesize_wav(text, w)
        with wave.open(tmp, "rb") as w:
            sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)/32767
        if sr != sfxlib.SR:
            idx = np.linspace(0, len(x)-1, int(len(x)*sfxlib.SR/sr)); x = np.interp(idx, np.arange(len(x)), x)
        x = x*0.9; _voice_cache[text] = x; return x
    except Exception as ex:
        print("voice skipped:", ex); _voice_cache[text] = None; return None

VOX_VOICES = {"blobby": ("en-us-ryan-medium", 1.22), "boss": ("en-us-ryan-medium", 0.88), "pinky": ("en-us-amy-low", 1.12)}
_vox_models = {}
def vox(text, who="blobby", length=1.15, dur=None):
    """Short non-verbal reaction (\"Ahh!\", \"Mmm hmm\") with a per-character pitch. None if unavailable."""
    key = (text, who, dur)
    if key in _voice_cache: return _voice_cache[key]
    try:
        import wave, numpy as np
        from piper import PiperVoice
        name, pitch = VOX_VOICES.get(who, VOX_VOICES["blobby"])
        model = os.path.join(VOICE_DIR, name + ".onnx")
        if not os.path.exists(model): return None
        if name not in _vox_models: _vox_models[name] = PiperVoice.load(model)
        vc = _vox_models[name]; tmp = os.path.join(VOICE_DIR, f"_vox{os.getpid()}.wav")
        try:
            from piper import SynthesisConfig
            with wave.open(tmp, "wb") as w: vc.synthesize_wav(text, w, syn_config=SynthesisConfig(length_scale=length))
        except Exception:
            with wave.open(tmp, "wb") as w: vc.synthesize_wav(text, w)
        with wave.open(tmp, "rb") as w:
            sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)/32767
        # trim silence
        a = np.where(np.abs(x) > 0.02)[0]
        if len(a): x = x[max(0, a[0]-200):a[-1]+400]
        # pitch (resample: higher = cartoon), then to mixer SR
        step = pitch*sr/sfxlib.SR
        idx = np.arange(0, len(x)-1, step); x = np.interp(idx, np.arange(len(x)), x)
        f = min(len(x)//4, int(0.01*sfxlib.SR))
        if f > 0: x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
        if dur and len(x) > 0:   # stretch "Ah!" into "Aaaah..." (phase vocoder, keeps pitch)
            try:
                import librosa
                x = librosa.effects.time_stretch(x.astype(np.float32), rate=len(x)/(dur*sfxlib.SR)).astype(float)
                f = int(0.03*sfxlib.SR); x[-f:] *= np.linspace(1, 0, f)
            except Exception as ex: print("stretch skipped:", ex)
        x = x/ (np.abs(x).max()+1e-9)*0.75; _voice_cache[key] = x; return x
    except Exception as ex:
        print("vox skipped:", ex); _voice_cache[key] = None; return None

# ---- timeline -------------------------------------------------------------
DEFAULT_CHAR = dict(at=(540, 1120), angle=0, scale=1.0, eyes="open", mouth="smile", arms="down", legs="stand",
                    pose="sit", brows=False, squash=1.0, prop=None, fx=None, flip=False, tween=True, pupil_dx=0)

def _beat_times(beats):
    t0 = 0.0; out = []
    for b in beats:
        out.append((t0, t0+b["dur"])); t0 += b["dur"]
    return out, t0

def _char_state(beats, times, i, name, t):
    b = beats[i]; cur = dict(DEFAULT_CHAR); cur.update(b["chars"][name])
    # tween from previous beat where this character existed
    if cur.get("tween") and i > 0 and name in beats[i-1].get("chars", {}):
        prev = dict(DEFAULT_CHAR); prev.update(beats[i-1]["chars"][name])
        k = (t - times[i][0]) / min(0.5, b["dur"])
        cur["at"] = (ease(prev["at"][0], cur["at"][0], k), ease(prev["at"][1], cur["at"][1], k))
        cur["angle"] = ease(prev["angle"], cur["angle"], k); cur["scale"] = ease(prev["scale"], cur["scale"], k)
    return cur

def render_frame(ep, beats, times, t, no_text=False):
    i = next(j for j, (a, b) in enumerate(times) if t < b)
    beat = beats[i]
    if no_text: beat = {k: v for k, v in beat.items() if k not in ("caption", "sub", "bubble")}
    img = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(img, "RGBA")
    stages.STAGES[ep["stage"]](d, t, beat.get("stage", {}))
    if beat.get("overlay") == "blanket_back": stages.blanket(d, up=True)   # pushed-aside blanket BEHIND the characters
    for name, _ in beat.get("chars", {}).items():
        c = _char_state(beats, times, i, name, t)
        layer = draw_character(name, **{k: c[k] for k in ("eyes", "mouth", "arms", "legs", "pose", "brows", "squash", "prop", "pupil_dx")})
        x, y = c["at"]
        place(img, layer, x, y, c["angle"], c["scale"], c["flip"])
        d = ImageDraw.Draw(img, "RGBA")
        if c.get("fx"): fx_draw(d, c["fx"], x, y, t, c["scale"])
    ov = beat.get("overlay")
    if ov == "blanket": stages.blanket(d)
    elif ov == "blanket_up": stages.blanket(d, up=True)
    if beat.get("bubble"):
        name, text = beat["bubble"]; c = _char_state(beats, times, i, name, t); bubble(d, c["at"][0], c["at"][1], text)
    if V3:   # closer camera: bigger cast, less empty floor (25 Oct 2026)
        z = ep.get("zoom", 1.2); cw, ch = int(W / z), int(H / z); x0 = (W - cw) // 2 + ep.get("zoom_dx", 0)
        img = img.crop((x0, 0, x0 + cw, ch)).resize((W, H), Image.LANCZOS); d = ImageDraw.Draw(img, "RGBA")
    if beat.get("caption"): meme_text(d, beat["caption"], 120 if V3 else 160, 104 if V3 else 82, width=13 if V3 else 16)
    if beat.get("sub"): meme_text(d, beat["sub"], 1560, 50, (255, 230, 80))
    if beat.get("shake"):
        s = beat["shake"]; img = img.transform(img.size, Image.AFFINE, (1, 0, s*math.sin(t*90), 0, 1, s*math.cos(t*70)))
    return img

def endcard(base, ep, t):
    img = base.copy()
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 150)); img.alpha_composite(ov)
    d = ImageDraw.Draw(img, "RGBA")
    k = min(1.0, t/0.3)
    meme_text(d, ep.get("punchline", ""), int(ease(560, 520, k)), 84, width=18)
    if t > 0.8:
        meme_text(d, ep.get("question", "Which one are you?"), 1380, 60, (255, 230, 80), 22)
        d.text((W//2-95, 1580), "↓ ↓ ↓", font=font(64), fill=(255, 255, 255))
    d.text((W//2-190, 1700), "BLOBBY & CO.", font=font(54), fill=(255, 204, 60), stroke_width=6, stroke_fill=OUTL)
    return img

def render(ep, out_dir=EPISODES, endcard_dur=3.0, keep_frames=False, suffix=""):
    os.makedirs(out_dir, exist_ok=True)
    beats = ep["beats"]; times, total = _beat_times(beats)
    loop = ep.get("loop", False)
    if loop: endcard_dur = 0.0
    dur = total + endcard_dur
    tmp = os.path.join(out_dir, f"_frames_ep{ep['num']:02d}"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    n = int(dur*FPS); last = None; strip = []
    for f in range(n):
        t = f/FPS
        if t < total:
            img = render_frame(ep, beats, times, t)
        else:
            if last is None: last = render_frame(ep, beats, times, total-1/FPS, no_text=True)
            img = endcard(last, ep, t-total)
        img.convert("RGB").save(os.path.join(tmp, f"f{f:05d}.png"))
        if f in {int(n*k/5) for k in range(5)} | {n-1}: strip.append(img.convert("RGB").resize((270, 480)))
    # audio
    import musicbeds
    mstyle, mshift = musicbeds.pick(ep["num"], ep.get("music_style"))
    mx = sfxlib.Mixer(dur, music=ep.get("music", True), fade=not loop, style=mstyle if V3 else None, shift=mshift)
    for i, b in enumerate(beats):
        for s in b.get("sfx", []):
            name, off = s[0], s[1]; gain = s[2] if len(s) > 2 else 1.0
            mx.add(name, times[i][0]+off, gain)
        for v in b.get("vox", []):
            who, text, off = v[0], v[1], v[2]; gain = v[3] if len(v) > 3 else 1.0
            x = vox(text, who, dur=v[4] if len(v) > 4 else None)
            if x is not None:
                st = int((times[i][0]+off)*sfxlib.SR); e_ = min(len(mx.mix), st+len(x))
                if e_ > st: mx.mix[st:e_] += x[:e_-st]*gain
    for name, off in ([] if loop else ep.get("end_sfx", [("tada", 0.1)])):
        mx.add(name, total+off)
    if ep.get("voice", not loop):   # spoken end-card line (keeps the audio "speech-like" for platform filters)
        v = voice_line(ep.get("voice_line", VOICE_LINE_DEFAULT))
        if v is not None:
            s = int((total+0.25)*sfxlib.SR); e_ = min(len(mx.mix), s+len(v)); mx.mix[s:e_] += v[:e_-s]
    wav = os.path.join(tmp, "sfx.wav"); mx.save(wav)
    mp4 = os.path.join(out_dir, f"ep{ep['num']:02d}{suffix}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.png"), "-i", wav,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-shortest", mp4], check=True)
    # cover + QA strip
    cf = int(ep.get("cover", 1.0)*FPS)
    Image.open(os.path.join(tmp, f"f{min(cf, n-1):05d}.png")).save(os.path.join(out_dir, f"ep{ep['num']:02d}{suffix}_cover.jpg"), quality=92)
    sheet = Image.new("RGB", (270*len(strip), 480))
    for k, im in enumerate(strip): sheet.paste(im, (270*k, 0))
    sheet.save(os.path.join(out_dir, f"ep{ep['num']:02d}{suffix}_strip.png"))
    if not keep_frames: shutil.rmtree(tmp, ignore_errors=True)
    print(f"ep{ep['num']:02d}{suffix}: {dur:.1f}s -> {mp4}")
    return mp4


# ---- Facebook cut (15-30 s; FB favours longer Reels) ----
FB_MIN, FB_TARGET = 15.0, 15.8

def stretch(beats, target):
    """Stretch the longer beats (> 0.6 s) so the beats sum to `target`. Quick hits stay quick. Never shrinks."""
    long_ = [b for b in beats if b["dur"] > 0.6]; fixed = sum(b["dur"] for b in beats if b["dur"] <= 0.6)
    k = (target - fixed) / sum(b["dur"] for b in long_)
    if k > 1:
        for b in long_: b["dur"] = round(b["dur"]*k, 2)

def facebook_cut(ep):
    """Episode dict for the Facebook upload (epNN_fb.mp4). Same hook, same punchline, same loop bridge, still no end card.
    ep["fb_extra"] = {index: [beat, ...]} inserts extra build-up beats BEFORE original beat `index` (rule of three:
    one more try before the fail). Extra beats carry no vox (the 2-vox limit still holds). Then stretched to >= 15 s.
    No fb_extra -> fallback: the loop plays twice (~24.6 s), which is what a looping viewer sees anyway."""
    import copy
    if sum(b["dur"] for b in ep["beats"]) >= FB_MIN: return None   # already 15 s+ (e.g. mini-story): Facebook uses epNN.mp4
    fb = copy.deepcopy({k: v for k, v in ep.items() if k != "fb_extra"})
    extra = ep.get("fb_extra")
    if extra:
        # cover: keep it on the same moment of the same original beat
        times, _ = _beat_times(fb["beats"]); c = fb.get("cover", 1.0)
        ci = next((i for i, (a, b) in enumerate(times) if c < b), len(times)-1); cf = (c - times[ci][0]) / fb["beats"][ci]["dur"]
        cover_beat = fb["beats"][ci]
        beats = []
        for i, b in enumerate(fb["beats"]):
            beats += copy.deepcopy(extra.get(i, [])); beats.append(b)
        stretch(beats, FB_TARGET)
        times, _ = _beat_times(beats); j = next(i for i, b in enumerate(beats) if b is cover_beat)
        fb["cover"] = round(times[j][0] + cf*beats[j]["dur"], 2)
        nvox = sum(len(b.get("vox", [])) for b in beats)
        assert nvox <= 2, f"ep{ep['num']}: fb cut has {nvox} vox (extra beats must not add vox)"
    else:
        beats = fb["beats"] + copy.deepcopy(fb["beats"])
    fb["beats"] = beats
    assert sum(b["dur"] for b in beats) >= FB_MIN, ep["num"]
    return fb

def render_fb(ep, **kw):
    fb = facebook_cut(ep)
    if fb is None: print(f"ep{ep['num']:02d}: already 15 s+, no Facebook cut needed"); return None
    return render(fb, suffix="_fb", **kw)
