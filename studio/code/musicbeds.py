"""Generated music beds (royalty-free), shared by Blobby & Co. and Merge Conflict (25 Oct 2026).
A different style / key / tempo per episode so videos never share one soundtrack.
music_bed(dur, style, shift, bpm=None, gain=1.0, sr=44100) -> float array, peak = gain."""
import numpy as np

STYLES = ["marimba", "ukulele", "sneaky", "funk", "jazz", "chip", "lofi"]

def _lp(x, fc, sr):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / sr); X[f > fc] *= np.exp(-(f[f > fc] - fc) / (fc * 0.25)); return np.fft.irfft(X, len(x))
def _bp(x, lo, hi, sr):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / sr); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def _hz(semi): return 220.0 * 2 ** (semi / 12)

def _note(f, L, kind, sr):
    x = np.arange(L) / sr
    if kind == "pluck":     o = sum(np.sin(2 * np.pi * f * h * x) / h ** 1.3 for h in (1, 2, 3, 4)) * np.exp(-x * 7)
    elif kind == "uke":     o = sum(np.sin(2 * np.pi * f * h * x) / h ** 1.1 for h in (1, 2, 3, 5)) * np.exp(-x * 11)
    elif kind == "marimba": o = (np.sin(2 * np.pi * f * x) + 0.35 * np.sin(2 * np.pi * f * 4 * x) * np.exp(-x * 30)) * np.exp(-x * 9)
    elif kind == "square":  o = np.sign(np.sin(2 * np.pi * f * x)) * np.exp(-x * 5) * 0.5
    elif kind == "rhodes":  o = (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(2 * np.pi * f * 2 * x + np.sin(2 * np.pi * f * x))) * np.exp(-x * 2.2)
    elif kind == "bass":    o = (np.sin(2 * np.pi * f * x) + 0.25 * np.sin(2 * np.pi * f * 2 * x)) * np.exp(-x * 4)
    elif kind == "pizz":    o = sum(np.sin(2 * np.pi * f * h * x) / h ** 1.6 for h in (1, 2, 3)) * np.exp(-x * 16)
    elif kind == "pad":     o = (np.sin(2 * np.pi * f * x) + 0.5 * np.sin(2 * np.pi * f * 1.005 * x)) * np.minimum(1, x / 0.3)
    else:                   o = np.sin(2 * np.pi * f * x) * np.exp(-x * 3)
    a = min(L, int(0.004 * sr)); o[:a] *= np.linspace(0, 1, a); return o

def music_bed(dur, style="lofi", shift=0, bpm=None, gain=1.0, sr=44100):
    n = int(sr * dur) + 1; out = np.zeros(n); rng = np.random.default_rng(11)
    bpm = bpm or {"marimba": 112, "ukulele": 118, "sneaky": 100, "funk": 104, "jazz": 96, "chip": 128, "lofi": 84}[style]; beat = 60 / bpm
    def put(t, sig, g):
        i = int(t * sr); L = min(len(sig), n - i)
        if L > 0: out[i:i + L] += sig[:L] * g
    def noise(L): return rng.uniform(-1, 1, L)
    def drums(t0, kick=(0, 2), snare=(1, 3), hat=8, swing=0.0, g=1.0, wood=False, shaker=False):
        for q in kick:
            L = int(0.25 * sr); x = np.arange(L) / sr; put(t0 + q * beat, np.sin(2 * np.pi * (55 + 60 * np.exp(-x * 30)) * x) * np.exp(-x * 12), 0.8 * g)
        for q in snare:
            L = int(0.15 * sr); put(t0 + q * beat, _bp(noise(L), 1500, 5000, sr) * np.exp(-np.arange(L) / sr * 35), 0.3 * g)
        for q in range(hat):
            L = int(0.04 * sr); dt = q * 4 * beat / hat + (swing * beat / 2 if q % 2 else 0)
            put(t0 + dt, _bp(noise(L), 6000, 12000, sr) * np.exp(-np.arange(L) / sr * 150), (0.12 if q % 2 else 0.2) * g)
        if wood:
            for q in range(4): L = int(0.06 * sr); x = np.arange(L) / sr; put(t0 + q * beat, np.sin(2 * np.pi * (900 if q % 2 else 1300) * x) * np.exp(-x * 60), 0.25)
        if shaker:
            for q in range(8): L = int(0.07 * sr); put(t0 + q * beat / 2, _bp(noise(L), 4000, 9000, sr) * np.exp(-np.arange(L) / sr * 50), 0.08)
    for b in range(int(dur / (4 * beat)) + 1):
        t0 = b * 4 * beat
        if style == "marimba":
            root = (0, 7, 9, 5)[b % 4] + shift; tri = (0, 3, 7) if b % 4 == 2 else (0, 4, 7)
            for q in range(8): put(t0 + q * beat / 2, _note(_hz(root + 12 + tri[q % 3] + (12 if q in (3, 7) else 0)), int(0.5 * sr), "marimba", sr), 0.35)
            put(t0, _note(_hz(root - 12), int(1.6 * sr), "bass", sr), 0.5); drums(t0, snare=(), g=0.6)
        elif style == "ukulele":   # strummed bouncy major, handclaps
            root = (0, 5, 7, 5)[b % 4] + shift
            for q, acc in enumerate((1, 0, 1, 1, 0, 1, 1, 0)):
                if acc:
                    for k, iv in enumerate((0, 4, 7, 12)): put(t0 + q * beat / 2 + k * 0.012, _note(_hz(root + 12 + iv), int(0.4 * sr), "uke", sr), 0.12)
            drums(t0, kick=(0, 2), snare=(1, 3), hat=0, g=0.5, shaker=True)
        elif style == "sneaky":
            walk = ((0, 3, 5, 6), (7, 6, 5, 3))[b % 2]
            for q, sm in enumerate(walk):
                put(t0 + q * beat, _note(_hz(sm + shift), int(0.3 * sr), "pizz", sr), 0.45); put(t0 + q * beat + beat / 2, _note(_hz(sm + shift + 12), int(0.2 * sr), "pizz", sr), 0.2)
            drums(t0, kick=(0,), snare=(), hat=0, wood=True)
        elif style == "funk":
            root = (0, 0, 5, 7)[b % 4] + shift - 12
            for q, on in enumerate((1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0)):
                if on: put(t0 + q * beat / 4, _note(_hz(root + (7 if q in (6, 13) else 0)), int(0.22 * sr), "bass", sr), 0.6)
            for q in (1, 3):
                for iv in (10, 14, 16): put(t0 + q * beat + beat / 2, _note(_hz(root + 12 + iv), int(0.12 * sr), "pluck", sr), 0.12)
            drums(t0, kick=(0, 2.5), snare=(1, 3), hat=16, g=0.9)
        elif style == "jazz":
            root = (2, 7, 0, 9)[b % 4] + shift; ch = (0, 3, 7, 10) if b % 4 in (0, 3) else ((0, 4, 7, 10) if b % 4 == 1 else (0, 4, 7, 11))
            for iv in ch: put(t0 + 1.5 * beat, _note(_hz(root + 12 + iv), int(1.4 * sr), "rhodes", sr), 0.13)
            for q, sm in enumerate((0, 4, 7, 9)): put(t0 + q * beat, _note(_hz(root - 12 + sm), int(0.5 * sr), "bass", sr), 0.55)
            drums(t0, kick=(0,), snare=(), hat=8, swing=0.33, g=0.7)
        elif style == "chip":
            root = (0, 9, 5, 7)[b % 4] + shift; tri = (0, 3, 7) if b % 4 == 1 else (0, 4, 7)
            for q in range(16): put(t0 + q * beat / 4, _note(_hz(root + 12 + tri[q % 3] + 12 * (q // 8)), int(0.12 * sr), "square", sr), 0.18)
            for q in range(4): put(t0 + q * beat, _note(_hz(root - 12), int(0.3 * sr), "square", sr), 0.3)
            drums(t0, g=0.7)
        else:  # lofi: warm pad chords + soft drums
            root = (0, 9, 5, 7)[b % 4] + shift; tri = (0, 3, 7) if b % 4 == 1 else (0, 4, 7)
            for iv in tri: put(t0, _note(_hz(root + iv), int(4 * beat * sr), "pad", sr) * np.exp(-np.arange(int(4 * beat * sr)) / sr * 0.5), 0.12)
            drums(t0, kick=(0, 2), snare=(1, 3), hat=8, g=0.8)
    out = _lp(out, 7500, sr)[: int(sr * dur)]
    return out / (np.max(np.abs(out)) + 1e-9) * gain

def pick(num, style=None):
    """Style + key shift for an episode: explicit style, else rotation by episode number."""
    return (style or STYLES[num % len(STYLES)]), (num * 5) % 7 - 3
