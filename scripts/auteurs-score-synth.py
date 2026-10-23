#!/usr/bin/env python3
"""
"First Cut": original score for /b-is-for-auteurs (bWalletX). Pure numpy synthesis, no samples, no
third-party music. Run:  python3 auteurs-score-synth.py out.wav   (then: ffmpeg -i out.wav -b:a 160k out.mp3)

Form (120 BPM, 4/4, 24 bars = 48 s, bars of 2 s; one 4-bar section per scene of the page):
  bars  1-4   intro        strings pad + sparse piano, the b arrives at beat 1 with a bell
  bars  5-8   "authored"   piano arpeggio joins
  bars  9-12  "minted"     cello melody + frame-drum heartbeat + shaker
  bars 13-16  "funded"     chords lift, toms, snare roll into the bar-17 downbeat
  bars 17-20  "gathered"   everything: strings melody in octaves, timpani, brushed snare, cymbal swell
  bars 21-24  end card     resolve to D major, drums fall away, bells, long add9 tail
Each scene change (every 8 s) is marked by a reverse-swell into a soft low hit so the cut is felt.
Key: B minor to D major. Progression per bar: Bm G D A | Bm G D A | Bm G D A | G D A Bm | G A Bm D | G A D D.
"""
import sys
import numpy as np
import wave

SR = 44100
BPM = 120
BEAT = 60.0 / BPM
BAR = 4 * BEAT
BARS = 24
DUR = BARS * BAR + 2.5  # reverb tail
N = int(SR * DUR)
rng = np.random.default_rng(23)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def n(name):
    """'F#4' -> midi"""
    base = NOTE[name[0]]
    i = 1
    if name[i] == "#":
        base += 1
        i += 1
    elif name[i] == "b":
        base -= 1
        i += 1
    return 12 * (int(name[i:]) + 1) + base


dry = np.zeros((2, N))   # goes to reverb as well
wet_send = np.zeros((2, N))
direct = np.zeros((2, N))


def place(buf, sig, t0, amp=1.0, pan=0.0):
    i = int(t0 * SR)
    if i < 0:
        sig = sig[-i:]
        i = 0
    j = min(N, i + len(sig))
    if i >= N or j <= i:
        return
    s = sig[: j - i] * amp
    l = np.sqrt(0.5 * (1 - pan))
    r = np.sqrt(0.5 * (1 + pan))
    buf[0, i:j] += s * l
    buf[1, i:j] += s * r


def tt(dur):
    return np.arange(int(dur * SR)) / SR


# ---------------------------------------------------------------- instruments
def piano(freq, dur=2.2, vel=0.8):
    t = tt(dur)
    sig = np.zeros_like(t)
    B = 0.00035  # slight inharmonicity
    for h in range(1, 14):
        f = freq * h * np.sqrt(1 + B * h * h)
        if f > 9000:
            break
        amp = (1.0 / h ** 1.15) * (0.75 + 0.25 * np.sin(h * 1.7))
        decay = 1.6 + 0.9 * h * (1.0 / (1 + freq / 400.0))
        sig += amp * np.sin(2 * np.pi * f * t + h) * np.exp(-t * decay * (0.55 + freq / 900.0) * 0.9)
    # hammer: short band of noise
    k = int(0.012 * SR)
    ham = rng.standard_normal(len(t)) * np.exp(-t * 260)
    ham = np.convolve(ham, np.ones(4) / 4, "same")
    sig = sig * (1 - np.exp(-t * 700)) + 0.05 * ham * vel
    sig *= np.exp(-t * 0.35)
    return sig * vel * 0.5


def bell(freq, dur=4.5, vel=0.6):
    t = tt(dur)
    sig = np.zeros_like(t)
    for ratio, a, d in [(1, 1.0, 0.9), (2.0, 0.5, 1.3), (2.76, 0.35, 1.7), (5.4, 0.2, 2.6), (8.93, 0.1, 4.0)]:
        sig += a * np.sin(2 * np.pi * freq * ratio * t) * np.exp(-t * d)
    return sig * (1 - np.exp(-t * 900)) * vel * 0.35


def strings(freq, dur, vib=0.0045, att=0.9, rel=1.1, harm=14, bright=1.25):
    """Warm ensemble: detuned additive saws (no filter needed), slow attack, gentle vibrato."""
    t = tt(dur)
    sig = np.zeros_like(t)
    for d, ph in [(-0.0065, 0.0), (0.0, 1.3), (0.0072, 2.1), (-0.0021, 4.0)]:
        vibr = 1 + vib * np.sin(2 * np.pi * (5.1 + d * 30) * t + ph) * np.minimum(1, t / 1.2)
        f0 = freq * (1 + d) * vibr
        phase = 2 * np.pi * np.cumsum(f0) / SR + ph
        for h in range(1, harm + 1):
            if freq * h > 7000:
                break
            sig += np.sin(h * phase) / (h ** bright)
    env = np.minimum(1, t / att) ** 1.5 * np.minimum(1, np.maximum(0, (dur - t) / rel))
    return sig * env * 0.16


def cello(freq, dur, vel=1.0):
    t = tt(dur)
    vibr = 1 + 0.006 * np.sin(2 * np.pi * 5.4 * t) * np.minimum(1, np.maximum(0, (t - 0.3) / 0.6))
    phase = 2 * np.pi * np.cumsum(freq * vibr) / SR
    sig = np.zeros_like(t)
    for h in range(1, 20):
        sig += np.sin(h * phase) / (h ** 1.05) * (1 + 0.5 * np.sin(h * 0.9 + 0.4))
    bow = rng.standard_normal(len(t))
    bow = np.convolve(bow, np.ones(3) / 3, "same") * 0.02
    env = np.minimum(1, t / 0.12) * np.minimum(1, np.maximum(0, (dur - t) / 0.28))
    # body: swell
    env *= 0.75 + 0.25 * np.minimum(1, t / 0.6)
    return (sig + bow) * env * 0.12 * vel


def frame_drum(dur=0.7, f0=95, vel=1.0):
    t = tt(dur)
    ph = 2 * np.pi * (f0 * t + 20 * (1 - np.exp(-t * 22)) * 2.0)
    body = np.sin(ph) * np.exp(-t * 9) + 0.4 * np.sin(2 * ph * 1.5) * np.exp(-t * 16)
    skin = rng.standard_normal(len(t))
    skin = skin - np.convolve(skin, np.ones(9) / 9, "same")
    return (body * 0.9 + skin * np.exp(-t * 55) * 0.12) * vel


def timpani(freq=73.4, dur=1.6, vel=1.0):
    t = tt(dur)
    f = freq * (1 + 0.5 * np.exp(-t * 40))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 2.7) + 0.35 * np.sin(1.504 * ph) * np.exp(-t * 4) + 0.2 * np.sin(2.0 * ph) * np.exp(-t * 6)
    thump = rng.standard_normal(len(t))
    thump = np.convolve(thump, np.ones(12) / 12, "same") * np.exp(-t * 90) * 0.5
    return (s + thump) * vel * 0.9


def snare_soft(vel=1.0, dur=0.3):
    t = tt(dur)
    no = rng.standard_normal(len(t))
    no = no - np.convolve(no, np.ones(4) / 4, "same")
    return (no * np.exp(-t * 20) * 0.5 + np.sin(2 * np.pi * 210 * t) * np.exp(-t * 30) * 0.35) * vel


def shaker(vel=1.0, dur=0.1):
    t = tt(dur)
    no = rng.standard_normal(len(t))
    no = no - np.convolve(no, np.ones(3) / 3, "same")
    return no * np.exp(-t * 55) * vel * 0.18 * np.minimum(1, t / 0.006)


def swell_noise(dur, reverse=True, bright=1.0):
    """Cymbal-ish / reverse swell: highpassed noise with exponential envelope."""
    t = tt(dur)
    no = rng.standard_normal(len(t))
    no = no - np.convolve(no, np.ones(7) / 7, "same")
    no2 = np.convolve(no, np.ones(2) / 2, "same")
    sig = (no * 0.6 + no2 * 0.4 * bright)
    env = (t / dur) ** 2.4 if reverse else np.exp(-t * 2.2)
    return sig * env * 0.28


def low_hit(dur=2.2, f=49.0):
    t = tt(dur)
    ph = 2 * np.pi * (f * t + 8 * (1 - np.exp(-t * 18)))
    return np.sin(ph) * np.exp(-t * 2.0) * 0.9


# ---------------------------------------------------------------- harmony
CH = {
    "Bm": dict(bass="B2", pad=["F#3", "B3", "D4", "F#4"], arp=["B3", "D4", "F#4", "B4", "D5"]),
    "G":  dict(bass="G2", pad=["D3", "G3", "B3", "D4"],   arp=["G3", "B3", "D4", "G4", "B4"]),
    "D":  dict(bass="D3", pad=["A3", "D4", "F#4", "A4"],  arp=["D4", "F#4", "A4", "D5", "F#5"]),
    "A":  dict(bass="A2", pad=["E3", "A3", "C#4", "E4"],  arp=["A3", "C#4", "E4", "A4", "C#5"]),
}
PROG = (
    ["Bm", "G", "D", "A"] * 3
    + ["G", "D", "A", "Bm"]
    + ["G", "A", "Bm", "D"]
    + ["G", "A", "D", "D"]
)

# Melody: (bar, beat, note, beats)
MEL = [
    # bars 9-12 (cello)
    (9, 0, "F#4", 4), (10, 0, "G4", 2), (10, 2, "B4", 2), (11, 0, "A4", 3), (11, 3, "F#4", 1), (12, 0, "E4", 2), (12, 2, "C#5", 2),
    # bars 13-16 (cello up an octave region)
    (13, 0, "B4", 2), (13, 2, "D5", 2), (14, 0, "A4", 2), (14, 2, "F#5", 2), (15, 0, "E5", 3), (15, 3, "C#5", 1), (16, 0, "D5", 2), (16, 2, "F#5", 2),
    # bars 17-20 (strings + piano, the lift)
    (17, 0, "B4", 1), (17, 1, "D5", 1), (17, 2, "G5", 2), (18, 0, "E5", 2), (18, 2, "A5", 2), (19, 0, "F#5", 2), (19, 2, "D5", 1), (19, 3, "B4", 1), (20, 0, "A4", 2), (20, 2, "D5", 2),
    # bars 21-24 (resolve)
    (21, 0, "B4", 4), (22, 0, "E5", 2), (22, 2, "C#5", 2), (23, 0, "D5", 4), (24, 0, "F#5", 4),
]


def bar_t(bar, beat=0):
    return (bar - 1) * BAR + beat * BEAT


# ---------------------------------------------------------------- arrange
for bi, ch in enumerate(PROG):
    bar = bi + 1
    c = CH[ch]
    t0 = bar_t(bar)
    sec = (bar - 1) // 4  # 0..5

    # strings pad, always present, thicker later
    for k, nm in enumerate(c["pad"]):
        f = mtof(n(nm))
        g = 0.55 if sec == 0 else (0.8 if sec < 3 else 1.0)
        place(dry, strings(f, BAR + 1.4, att=1.0 if sec == 0 else 0.7), t0 - 0.05, g * (0.9 if k == 3 else 1.0), pan=(-0.35 + 0.23 * k))
    # bass (cellos low) from bar 5
    if bar >= 5:
        f = mtof(n(c["bass"]))
        place(direct, strings(f, BAR + 0.8, vib=0.002, att=0.35, rel=0.8, harm=8, bright=1.6), t0, 1.15 if bar < 17 else 1.5, pan=0.0)

    # piano
    if sec == 0:
        # sparse: bar 1 starts with the b bell; two notes per bar
        pn = c["arp"]
        place(dry, piano(mtof(n(pn[2])), 3.0, 0.7), t0 + 0.0 * BEAT, 0.9, pan=-0.1)
        place(dry, piano(mtof(n(pn[3])), 3.0, 0.55), t0 + 2.5 * BEAT, 0.8, pan=0.15)
    elif sec in (1, 2, 3, 4):
        # 8th-note arpeggio, soft; fuller in later sections
        order = [0, 2, 1, 3, 2, 4, 3, 2] if sec != 4 else [0, 2, 3, 4, 3, 2, 4, 3]
        for k in range(8):
            vel = (0.5 + 0.15 * (k % 2 == 0)) * (0.8 if sec == 1 else 1.0) * (1.25 if sec == 4 else 1.0)
            place(dry, piano(mtof(n(c["arp"][order[k] % 5])), 1.7, vel), t0 + k * BEAT / 2, 0.8, pan=-0.25 + 0.5 * (k / 7))
    else:
        # end card: slow broken chord, then sparse
        if bar <= 22:
            for k, idx in enumerate([0, 2, 3, 4]):
                place(dry, piano(mtof(n(c["arp"][idx])), 2.6, 0.55), t0 + k * BEAT, 0.8, pan=-0.2 + 0.13 * k)
        elif bar == 23:
            for k, idx in enumerate([0, 1, 2, 3, 4]):
                place(dry, piano(mtof(n(c["arp"][idx])), 3.4, 0.5 - 0.04 * k), t0 + k * BEAT * 0.75, 0.8, pan=-0.2 + 0.1 * k)
        else:
            place(dry, piano(mtof(n("D4")), 6.0, 0.55), t0, 0.8, pan=-0.1)
            place(dry, piano(mtof(n("A4")), 6.0, 0.45), t0 + BEAT, 0.8, pan=0.1)
            place(dry, piano(mtof(n("E5")), 6.0, 0.42), t0 + 2 * BEAT, 0.8, pan=0.2)  # add9

    # percussion
    if 9 <= bar <= 12:
        place(direct, frame_drum(0.7, 92, 0.8), t0, 0.5, pan=-0.1)
        place(direct, frame_drum(0.6, 118, 0.5), t0 + 2.5 * BEAT, 0.4, pan=0.1)
        for k in range(8):
            if k % 2 == 1:
                place(direct, shaker(0.8 + 0.2 * (k % 4 == 3)), t0 + k * BEAT / 2, 0.8, pan=0.3)
    if 13 <= bar <= 16:
        for k in range(4):
            place(direct, frame_drum(0.7, 88 + 6 * (k % 2), 0.9), t0 + k * BEAT, 0.55, pan=-0.15 + 0.1 * k)
        for k in range(8):
            place(direct, shaker(0.7 + 0.3 * (k % 2)), t0 + k * BEAT / 2, 0.9, pan=0.3)
        if bar == 16:
            # snare roll, accelerating, crescendo into bar 17
            tpos = t0 + 2 * BEAT
            steps = 16
            for k in range(steps):
                frac = k / steps
                tpos2 = t0 + 2 * BEAT + (2 * BEAT) * (1 - (1 - frac) ** 1.6)
                place(direct, snare_soft(0.5 + 0.9 * frac, 0.18), tpos2, 0.55, pan=-0.1 + 0.2 * frac)
    if 17 <= bar <= 20:
        place(direct, timpani(73.4 if ch in ("G", "D", "Bm") else 55.0, 1.6, 1.0), t0, 0.7)
        place(direct, timpani(73.4, 1.2, 0.7), t0 + 2.5 * BEAT, 0.5)
        place(direct, snare_soft(0.9), t0 + 1 * BEAT, 0.7, pan=0.1)
        place(direct, snare_soft(1.0), t0 + 3 * BEAT, 0.8, pan=0.1)
        for k in range(8):
            place(direct, shaker(0.9 + 0.2 * (k % 2)), t0 + k * BEAT / 2, 0.9, pan=0.3)
        if bar % 2 == 0:
            place(direct, frame_drum(0.6, 70, 0.9), t0 + 3.5 * BEAT, 0.6)
    if bar == 21:
        place(direct, timpani(73.4, 2.4, 0.9), t0, 0.7)
    if bar == 22:
        place(direct, frame_drum(1.0, 80, 0.7), t0, 0.35)


# melody
for bar, beat, nm, beats in MEL:
    t0 = bar_t(bar, beat)
    dur = beats * BEAT
    f = mtof(n(nm))
    if 9 <= bar <= 16:
        place(dry, cello(f, dur + 0.25, 1.0), t0, 1.35, pan=-0.12)
    elif 17 <= bar <= 20:
        place(dry, cello(f, dur + 0.3, 1.0), t0, 1.0, pan=-0.12)
        place(dry, strings(f * 2 if f < 700 else f, dur + 0.5, att=0.25, rel=0.4, harm=8), t0, 0.7, pan=0.18)
        place(dry, piano(f * 2 if f < 600 else f, dur + 0.8, 0.55), t0, 0.7, pan=0.05)
    else:
        place(dry, cello(f, dur + 0.4, 1.0), t0, 0.85 if bar < 23 else 0.55, pan=-0.12)
        place(dry, bell(f * 2 if f < 700 else f, 3.5, 0.5), t0, 0.7, pan=0.2)

# b bell at beat 1: the logo pops with the first letter; later cadence bells on every scene start
place(dry, bell(mtof(n("F#5")), 6, 0.85), 0.35, 0.8, pan=0.0)
place(dry, bell(mtof(n("B5")), 6, 0.6), 0.35, 0.6, pan=0.1)
for sb in (5, 9, 13, 17, 21):
    place(dry, bell(mtof(n("D6")), 5, 0.5), bar_t(sb), 0.5, pan=0.25)
place(dry, bell(mtof(n("D6")), 9, 0.8), bar_t(24), 0.9, pan=0.0)
place(dry, bell(mtof(n("A5")), 9, 0.6), bar_t(24, 1), 0.7, pan=-0.2)

# scene seams: reverse swell into the barline + a soft low hit on the cut
for sb in (5, 9, 13, 17, 21):
    tb = bar_t(sb)
    sw = swell_noise(1.9, True, 1.0)
    place(direct, sw, tb - 1.9, 0.5 if sb != 17 else 0.9, pan=-0.3)
    place(direct, low_hit(2.4, 49.0 if sb != 21 else 36.7), tb, 0.5 if sb != 17 else 0.85)
# big cymbal-ish crash on 17 and 21
place(direct, swell_noise(3.0, False, 1.2), bar_t(17), 0.9, pan=0.1)
place(direct, swell_noise(3.5, False, 1.0), bar_t(21), 0.75, pan=-0.1)

# ---------------------------------------------------------------- reverb
def make_ir(sec=2.6):
    n_ = int(sec * SR)
    t = np.arange(n_) / SR
    out = []
    for ch in range(2):
        noise = rng.standard_normal(n_)
        # darken progressively: cumulative lowpass by blending with smoothed copies
        sm = np.convolve(noise, np.ones(6) / 6, "same")
        noise = noise * np.exp(-t * 3.0) * 0.4 + sm * (1 - np.exp(-t * 3.0)) * 0.9
        env = np.exp(-t * 2.15) * (1 - np.exp(-t * 90))
        out.append(noise * env)
    ir = np.stack(out)
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    return ir


def fft_conv(x, h):
    L = len(x) + len(h) - 1
    nfft = 1 << (L - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(h, nfft), nfft)[: len(x)]


ir = make_ir()
wet = np.stack([fft_conv(dry[0], ir[0]), fft_conv(dry[1], ir[1])])
wet_d = np.stack([fft_conv(direct[0], ir[0]), fft_conv(direct[1], ir[1])])

mix = dry * 0.55 + wet * 0.85 + direct * 0.9 + wet_d * 0.22

# gentle low cut + soft clip
for ch in range(2):
    x = mix[ch]
    x = x - 0.9 * np.roll(fft_conv(x, np.ones(900) / 900), -450)  # light sub-rumble removal
    mix[ch] = x
# keep the low hits: add back direct low end
mix += direct * 0.25

# fades: in 1.2s, out over the last 2.3 s
fi = int(1.2 * SR)
mix[:, :fi] *= np.linspace(0, 1, fi) ** 1.5
fo = int(2.3 * SR)
mix[:, -fo:] *= np.linspace(1, 0, fo) ** 1.3
# level: keep the arrangement's dynamics (quiet intro, big climax); only the rare peaks are soft-limited
mix *= 0.62 / np.percentile(np.abs(mix), 99.9)
mix = np.tanh(mix * 0.9) / np.tanh(0.9)
mix *= 0.89 / np.abs(mix).max()

out = sys.argv[1] if len(sys.argv) > 1 else "auteurs-score.wav"
w = wave.open(out, "wb")
w.setnchannels(2)
w.setsampwidth(2)
w.setframerate(SR)
w.writeframes((mix.T * 32767).astype("<i2").tobytes())
w.close()
print("wrote", out, "%.1fs" % DUR)
