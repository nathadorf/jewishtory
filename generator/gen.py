"""Render one story script to a mixed MP3 plus a cue file for the web player.

Usage: python gen.py <story_module> <out_dir>
The story module exposes TITLE, SEGMENTS [(speaker, text)] and optionally AMBIENCE.
"""
import importlib, json, os, re, subprocess, sys
import numpy as np, soundfile as sf, sherpa_onnx

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
M = os.environ.get("TTS_MODELS", D + "/models")
SR = 24000
MARK = re.compile(r"\[\[([^|\]]*)\|([^|\]]*)\|([^|\]]*)\]\]")

def piper(name):
    d = f"{M}/vits-piper-{name}"
    onnx = [x for x in os.listdir(d) if x.endswith(".onnx")][0]
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=f"{d}/{onnx}", tokens=f"{d}/tokens.txt", data_dir=f"{d}/espeak-ng-data"),
        num_threads=4))
    return sherpa_onnx.OfflineTts(cfg)

# engine, speaker id, speed, pitch shift (semitones, formants follow -> child/adult size)
VOICE = {
    "N":      ("siwis",  0, 0.95, 0.0),
    "NOAH":   ("tom",    0, 0.95, 0.0),
    "AVRAM":  ("gilles", 0, 0.95, 0.0),
    "SARAI":  ("upmc",   0, 0.95, 0.0),
    "EYDEL":  ("upmc",   0, 0.93, 2.5),
    "ARIE":   ("upmc",   1, 0.97, 3.5),
    "HILLEL": ("siwis",  0, 0.93, 4.5),
}
MODELS = {"siwis": "fr_FR-siwis-medium", "tom": "fr_FR-tom-medium", "upmc": "fr_FR-upmc-medium", "gilles": "fr_FR-gilles-low"}
_eng = {}

def synth(sp, text, tmp):
    eng, sid, speed, semi = VOICE[sp]
    if eng not in _eng: _eng[eng] = piper(MODELS[eng])
    a = _eng[eng].generate(text, sid=sid, speed=speed)
    x = np.array(a.samples, dtype=np.float32); sr = a.sample_rate
    sf.write(f"{tmp}/_in.wav", x, sr)
    r = 2 ** (semi / 12)
    filt = f"asetrate={int(sr*r)},aresample={SR},atempo={1/r:.5f}" if semi else f"aresample={SR}"
    filt += ",highpass=f=60"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmp}/_in.wav", "-af", filt, f"{tmp}/_out.wav"], check=True)
    y, _ = sf.read(f"{tmp}/_out.wav", dtype="float32")
    # trim silence, normalize RMS
    nz = np.where(np.abs(y) > 0.01)[0]
    if len(nz): y = y[max(nz[0]-240, 0): nz[-1]+2400]
    y = y * (0.085 / (np.sqrt(np.mean(y**2)) + 1e-9))
    return np.clip(y, -0.98, 0.98)

def chime():
    t = np.arange(int(SR*2.2))/SR; y = np.zeros_like(t)
    for i, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        s = (t - i*0.18).clip(0)
        y += np.where(t >= i*0.18, np.sin(2*np.pi*f*s) * np.exp(-s*2.8), 0) * 0.06
    return y.astype(np.float32)

def music_box():
    # "Twinkle"-like lullaby phrase, music-box timbre
    notes = [523.25,523.25,783.99,783.99,880,880,783.99,0,698.46,698.46,659.25,659.25,587.33,587.33,523.25]
    d = 0.42; out = np.zeros(int(SR*(len(notes)*d+2.5)), np.float32)
    for i, f in enumerate(notes):
        if not f: continue
        t = np.arange(int(SR*2.2))/SR
        n = (np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*2*f*t) + 0.1*np.sin(2*np.pi*3.01*f*t)) * np.exp(-t*3.2) * 0.07
        s = int(i*d*SR); out[s:s+len(n)] += n[:len(out)-s]
    return out

def silence(s): return np.zeros(int(SR*s), np.float32)

def noise_bed(kind, n, tmp):
    x = np.random.default_rng(1).standard_normal(n).astype(np.float32) * 0.3
    sf.write(f"{tmp}/_noise.wav", x, SR)
    filt = {"rain": "highpass=f=600,lowpass=f=5000,volume=0.6",
            "wind": "lowpass=f=500,highpass=f=80,volume=2.2,tremolo=f=0.15:d=0.7"}[kind]
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{tmp}/_noise.wav","-af",filt,f"{tmp}/_noise2.wav"],check=True)
    y, _ = sf.read(f"{tmp}/_noise2.wav", dtype="float32")
    return y[:n]

def main(story_name, out):
    story = importlib.import_module(story_name)
    os.makedirs(out, exist_ok=True)
    parts, cues, scenes, t = [], [], [0], 0.0
    def add(y):
        nonlocal t; parts.append(y); t += len(y)/SR
    add(music_box()); add(silence(0.4))
    prev = None
    for i, (sp, txt) in enumerate(story.SEGMENTS):
        if sp == "~":
            add(silence(0.5)); add(chime()); prev = None; scenes.append(len(cues)); continue
        tts = MARK.sub(lambda m: m.group(3), txt)
        if prev is not None:
            add(silence(0.55 if sp == prev else 0.8))
        y = synth(sp, tts, out)
        start = t; add(y)
        cues.append({"sp": sp, "start": round(start, 2), "end": round(t, 2), "text": txt})
        prev = sp
        print(f"{i:02d} {sp:6s} {start:6.1f}s  {tts[:60]}", flush=True)
    add(silence(1.0)); add(music_box()); add(silence(1.0))
    mix = np.concatenate(parts); n = len(mix)

    # ambience beds: (start text, end text, level, kind); None start = from the top
    def at(sub): return int([c for c in cues if sub in c["text"]][0]["start"] * SR)
    for start, end, level, kind in getattr(story, "AMBIENCE", []):
        env = np.zeros(n, np.float32)
        env[(at(start) if start else 0):at(end)] = level
        env = np.convolve(env, np.ones(2*SR)/(2*SR), mode="same").astype(np.float32)
        mix += noise_bed(kind, n, out) * env

    mix = np.clip(mix, -0.99, 0.99)
    sf.write(f"{out}/story.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{out}/story.wav","-ac","1","-b:a","64k",f"{out}/story.mp3"],check=True)
    for f in ("_in.wav", "_out.wav", "_noise.wav", "_noise2.wav", "story.wav"):
        if os.path.exists(f"{out}/{f}"): os.remove(f"{out}/{f}")
    json.dump({"title": story.TITLE, "duration": round(t, 2), "scenes": scenes, "cues": cues},
              open(f"{out}/cues.json", "w"), ensure_ascii=False, indent=1)
    print("DURATION", round(t, 1))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
