"""Synthesised sound-effect library. No copyrighted samples — everything is generated.
Use: mixer = Mixer(duration); mixer.add("boom", 6.4); mixer.save("out.wav")
"""
import numpy as np, wave
SR = 44100
_rng = np.random.default_rng(7)


def _env(n, a=0.005, r=0.1):
    e = np.ones(n); na, nr = min(n//2, int(a*SR)), min(n//2, int(r*SR))
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e


def _t(d): return np.arange(int(d*SR))/SR
def tone(f, d, decay=None):
    t = _t(d); x = np.sin(2*np.pi*f*t)
    if decay: x *= np.exp(-t*decay)
    return x*_env(len(x))
def sweep(f0, f1, d, decay=0.0):
    t = _t(d); x = np.sin(2*np.pi*(f0*t + (f1-f0)*t**2/(2*d)))
    return x*_env(len(t), 0.01, 0.1)*np.exp(-t*decay)
def noise(d, decay=30.0):
    t = _t(d); return _rng.normal(0, 1, len(t))*np.exp(-t*decay)


def snore():
    t = _t(0.9)
    x = np.sin(2*np.pi*70*t)*(0.6+0.4*np.sin(2*np.pi*22*t))*np.exp(-t*2.2) + _rng.normal(0, 0.08, len(t))*np.exp(-t*4)
    return x*_env(len(x), 0.05, 0.3)*0.5
def alarm(d=1.2):
    """Cartoon alarm: soft two-tone 'ring-ring' (sine), not a siren."""
    t = _t(d); f = np.where((np.sin(2*np.pi*6*t) > 0), 880, 1175)
    beep = np.sin(2*np.pi*np.cumsum(f)/SR)*0.25 + np.sin(2*np.pi*np.cumsum(f*2)/SR)*0.05
    gate = 0.5+0.5*np.sin(2*np.pi*12*t)
    return beep*gate*_env(len(t), 0.02, 0.15)*0.6
def boing(): return sweep(600, 150, 0.35, 6)*0.6
def sparkle():
    out = np.zeros(int(0.9*SR))
    for i, f in enumerate((880, 1108, 1318, 1760)):
        s = int(i*0.09*SR); x = tone(f, 0.5, 4)*0.35; out[s:s+len(x)] += x
    return out
def steps(n=3, gap=0.18):
    out = np.zeros(int((n*gap+0.1)*SR))
    for i in range(n):
        s = int(i*gap*SR); x = noise(0.08, 60)*0.3; out[s:s+len(x)] += x
    return out
def slide_whistle_down(): return sweep(1500, 300, 0.7)*0.45
def slide_whistle_up(): return sweep(300, 1500, 0.6)*0.45
def thud():
    t = _t(0.6); return (np.sin(2*np.pi*60*t)*np.exp(-t*9) + _rng.normal(0, 1, len(t))*np.exp(-t*40)*0.5)*0.7
def boom():   # "vine boom" style
    t = _t(1.6); return np.sin(2*np.pi*(55*t - 20*t**2/1.6))*np.exp(-t*3)*0.6
def crickets(d=3.0):
    out = np.zeros(int(d*SR))
    for i in range(int(d/0.27)):
        s = int((0.1+i*0.27)*SR); t = _t(0.06)
        ch = np.sin(2*np.pi*4200*t)*(np.sin(2*np.pi*60*t) > 0)*np.exp(-t*30)*0.12
        out[s:s+len(ch)] += ch
    return out
def tada():
    out = np.zeros(int(1.0*SR)); x = tone(523, 0.25, 5)*0.25; out[:len(x)] += x
    y = tone(784, 0.6, 3)*0.3; out[int(0.2*SR):int(0.2*SR)+len(y)] += y; return out
def pop(): return sweep(400, 900, 0.08, 20)*0.5
def ding(): return (tone(2093, 0.8, 4) + tone(2637, 0.8, 6)*0.5)*0.3
def bruh():
    t = _t(0.5); return (np.sin(2*np.pi*110*t)+0.5*np.sin(2*np.pi*165*t))*np.exp(-t*5)*0.5
def sad_trombone():
    out = np.zeros(int(2.2*SR))
    for i, (f, d) in enumerate(((233, 0.45), (220, 0.45), (207, 0.45), (196, 0.8))):
        s = int(i*0.45*SR); t = _t(d); x = np.sign(np.sin(2*np.pi*f*t))*0.15*_env(len(t), 0.02, 0.1)
        if i == 3: x *= np.exp(-t*2)
        out[s:s+len(x)] += x
    return out
def record_scratch():
    t = _t(0.35); return _rng.normal(0, 1, len(t))*np.sin(2*np.pi*(60+400*t)*t)*_env(len(t), 0.01, 0.05)*0.5
def cash():
    out = np.zeros(int(0.8*SR)); x = noise(0.05, 40)*0.4; out[:len(x)] += x
    y = (tone(1800, 0.5, 6)+tone(2400, 0.5, 8))*0.25; out[int(0.08*SR):int(0.08*SR)+len(y)] += y; return out
def heartbeat(n=3):
    out = np.zeros(int((n*0.8+0.3)*SR))
    for i in range(n):
        for k, g in ((0, 1.0), (0.15, 0.7)):
            s = int((i*0.8+k)*SR); t = _t(0.18); x = np.sin(2*np.pi*50*t)*np.exp(-t*20)*g*0.8; out[s:s+len(x)] += x
    return out
def tick_tock(n=4):
    out = np.zeros(int((n*0.5+0.1)*SR))
    for i in range(n):
        s = int(i*0.5*SR); x = noise(0.03, 120)*0.35 + tone(1200 if i % 2 else 900, 0.03, 60)*0.2; out[s:s+len(x)] += x
    return out
def applause(d=1.5):
    t = _t(d); x = _rng.normal(0, 1, len(t))*(0.5+0.5*np.sin(2*np.pi*11*t))*_env(len(t), 0.1, 0.4)
    return x*0.25
def buzz(n=2):
    out = np.zeros(int((n*0.5)*SR))
    for i in range(n):
        s = int(i*0.5*SR); t = _t(0.3); x = np.sign(np.sin(2*np.pi*90*t))*np.sin(2*np.pi*40*t)*_env(len(t), 0.01, 0.05)*0.3
        out[s:s+len(x)] += x
    return out
def whoosh():
    t = _t(0.4); return _rng.normal(0, 1, len(t))*np.sin(np.pi*t/0.4)**2*0.35
def swallow():   # gulp
    return sweep(500, 200, 0.2, 8)*0.4
def kiss(): return sweep(1800, 900, 0.12, 15)*0.4
def meow():
    t = _t(0.5); f = 500 + 300*np.sin(np.pi*t/0.5)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*_env(len(t), 0.03, 0.15)*0.35
def purr(d=1.5):
    t = _t(d); return np.sin(2*np.pi*25*t)*(0.6+0.4*np.sin(2*np.pi*3*t))*_env(len(t), 0.2, 0.3)*0.35
def glass_break():
    t = _t(0.7); return _rng.normal(0, 1, len(t))*np.exp(-t*8)*(0.5+0.5*np.sin(2*np.pi*3000*t))*0.6
def door():
    out = np.zeros(int(0.5*SR)); x = noise(0.1, 30)*0.5; out[:len(x)] += x
    y = tone(90, 0.3, 12)*0.6; out[int(0.05*SR):int(0.05*SR)+len(y)] += y; return out
def yawn(): return sweep(260, 180, 0.9, 1.5)*0.3
def chime(): return (tone(1047, 1.0, 3) + tone(1319, 1.0, 3) + tone(1568, 1.0, 3))*0.2
def explosion():
    t = _t(1.2); return (_rng.normal(0, 1, len(t))*np.exp(-t*5) + np.sin(2*np.pi*50*t)*np.exp(-t*3))*0.5
def squeak(): return sweep(1200, 1600, 0.15, 10)*0.3
def type_keys(n=8):
    out = np.zeros(int((n*0.09+0.1)*SR))
    for i in range(n):
        s = int(i*0.09*SR); x = noise(0.03, 150)*0.3; out[s:s+len(x)] += x
    return out

def music_bed(d, bpm=96, seed=3, fade=True):
    """Soft, warm pad + gentle marimba-style plucks (C major, lo-fi feel). Generated, royalty-free.
    Mixed very low under the SFX; set music=False on an episode to drop it."""
    rng = np.random.default_rng(seed)
    n = int(d*SR); t_all = np.arange(n)/SR; out = np.zeros(n)
    beat = 60.0/bpm; bar = beat*4
    chords = [(261.6, 329.6, 392.0), (220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (196.0, 246.9, 293.7)]  # C Am F G
    # warm pad: slow-attack sines with gentle vibrato, one chord per bar
    for b in range(int(d/bar)+1):
        ch = chords[b % 4]; s0 = int(b*bar*SR); e = min(n, int((b+1)*bar*SR)+int(0.4*SR))
        if s0 >= n: break
        t = np.arange(e-s0)/SR
        env = np.minimum(1, t/0.6)*np.minimum(1, (len(t)/SR-t)/0.5)
        pad = sum(np.sin(2*np.pi*f*t*(1+0.002*np.sin(2*np.pi*4.5*t))) for f in ch)/3
        out[s0:e] += pad*env*0.22
    # sparse marimba plucks on off-beats
    melody = [0, 2, 1, 2, 0, 1, 2, 1]
    for i in range(int(d/(beat*2))+1):
        if rng.random() < 0.6:
            ch = chords[int(i*2*beat/bar) % 4]; f = ch[melody[i % 8]]*2
            t = _t(0.5); x = (np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*f*4*t)*np.exp(-t*30))*np.exp(-t*7)
            s0 = int((i*2*beat + beat)*SR); e = min(n, s0+len(x))
            if s0 < n: out[s0:e] += x[:e-s0]*0.35
    return out*_env(n, 0.8, 1.2) if fade else out*_env(n, 0.03, 0.03)

SFX = {k: v for k, v in globals().items() if callable(v) and k not in ("tone", "sweep", "noise") and not k.startswith("_") and k not in ("Mixer", "music_bed")}


class Mixer:
    def __init__(self, duration, music=True, music_gain=0.045, fade=True, style=None, shift=0):
        self.mix = np.zeros(int(SR*duration))
        if music and style:   # v3 (25 Oct 2026): a different style / key per episode (musicbeds.py)
            import musicbeds
            bed = musicbeds.music_bed(duration, style, shift, sr=SR)
            bed = bed*_env(len(bed), 0.03, 0.03) if not fade else bed*_env(len(bed), 0.8, 1.2)
            self.mix[:len(bed)] += bed[:len(self.mix)]*music_gain*0.9
        elif music: self.mix += music_bed(duration, fade=fade)*music_gain

    def add(self, name, t, gain=1.0, **kw):
        sig = SFX[name](**kw) if kw else SFX[name]()
        s = int(t*SR); e = min(len(self.mix), s+len(sig))
        if e > s: self.mix[s:e] += sig[:e-s]*gain
        return self

    def save(self, path):
        m = np.tanh(self.mix*1.0)*0.8
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((m*32767).astype(np.int16).tobytes())
