"""Render one story script to a mixed MP3 plus a cue file for the web player.

Usage: python gen.py <story_module> <out_dir>
Voices come from Gemini TTS when GEMINI_API_KEY is set (TTS_ENGINE=piper forces the free Piper voices).
The story module exposes TITLE, SEGMENTS [(speaker, text)] and optionally AMBIENCE.
"""
import base64, hashlib, importlib, json, os, re, subprocess, sys, time, urllib.error, urllib.request
import numpy as np, soundfile as sf

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
M = os.environ.get("TTS_MODELS", D + "/models")
SR = 24000
MARK = re.compile(r"\[\[([^|\]]*)\|([^|\]]*)\|([^|\]]*)\]\]")

def piper(name):
    import sherpa_onnx
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
    "AVRAHAM": ("gilles", 0, 0.95, 0.0),
    "SARAH":  ("upmc",   0, 0.95, 0.0),
    "MALAKH": ("tom",    0, 0.9,  0.0),
    "EYDEL":  ("upmc",   0, 0.93, 2.5),
    "ARIE":   ("upmc",   1, 1.0,  2.0),
    "HILLEL": ("siwis",  0, 0.93, 4.5),
}
# Gemini voice, style prompt, pitch shift. Hebrew words are sent in Hebrew script.
STYLE_N = "une conteuse française douce qui raconte une histoire du soir à de petits enfants, lentement, avec chaleur"
GEMINI = {
    "N":      ("Achernar",     STYLE_N, 0.0),
    "NOAH":   ("Algenib",      "un vieil homme sage et très gentil, à la voix grave et chaleureuse, qui parle doucement à des enfants", 0.0),
    "AVRAM":  ("Orus",         "un homme bon et courageux, à la voix chaude et posée, qui parle doucement à des enfants", 0.0),
    "SARAI":  ("Vindemiatrix", "une femme tendre et accueillante, comme une maman, qui parle doucement à des enfants", 0.0),
    "AVRAHAM": ("Orus",        "un homme bon et courageux, à la voix chaude et posée, qui parle doucement à des enfants", 0.0),
    "SARAH":  ("Vindemiatrix", "une femme tendre et accueillante, comme une maman, qui parle doucement à des enfants", 0.0),
    "MALAKH": ("Iapetus",      "un ange mystérieux et lumineux, à la voix très douce et apaisante, qui parle lentement", 0.0),
    "EYDEL":  ("Leda",         "une petite fille de huit ans, douce, comme une grande sœur", 3.0),
    "ARIE":   ("Puck",         "un petit garçon de six ans, curieux et plein d'énergie", 3.0),
    "HILLEL": ("Achird",       "un tout petit garçon de quatre ans, mignon et un peu rêveur", 3.0),
}
# Each model has its own daily request quota: when one runs out, the next one takes over.
GEMINI_MODELS = os.environ.get("GEMINI_TTS_MODELS", "gemini-2.5-flash-preview-tts,gemini-3.8-flash-tts").split(",")
CACHE = D + "/.tts-cache"
USE_GEMINI = bool(os.environ.get("GEMINI_API_KEY")) and os.environ.get("TTS_ENGINE") != "piper"

def gemini_call(model, voice, prompt):
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    for attempt in range(5):
        try:
            r = json.load(urllib.request.urlopen(req, timeout=180))
            return base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
        except urllib.error.HTTPError as e:
            if e.code == 429 and "PerDay" in e.read().decode(errors="ignore"): return None
            if e.code not in (429, 500, 503) or attempt == 4: raise
        except (KeyError, IndexError):
            if attempt == 4: raise
        time.sleep(10 * 2 ** attempt)

def gemini(sp, text):
    voice, style, _ = GEMINI[sp]
    who = "Lis ce passage comme " if sp == "N" else "Dis cette réplique avec la voix d'"
    prompts = {"gemini-2.5-flash-preview-tts":
                   f"{who}{style}. Les mots écrits en hébreu sont à prononcer à l'israélienne. "
                   f"Ne lis que le texte après les deux points.\n\n: {text}"}
    # Newer models read a plain-text direction aloud, but not one in brackets
    default = f"[Voix : {style}. Mots hébreux prononcés à l'israélienne.]\n{text}"
    jobs = [(m, prompts.get(m, default)) for m in GEMINI_MODELS]
    paths = [f"{CACHE}/{hashlib.sha1(f'{m}|{voice}|{p}'.encode()).hexdigest()}.pcm" for m, p in jobs]
    path = next((p for p in paths if os.path.exists(p)), None)
    for (model, prompt), p in zip(jobs, paths):
        if path: break
        pcm = gemini_call(model, voice, prompt)
        if pcm is None:
            print(f"   daily quota reached for {model}", flush=True); continue
        os.makedirs(CACHE, exist_ok=True)
        open(p, "wb").write(pcm); path = p
    if not path: sys.exit("All Gemini TTS models are out of daily quota")
    return np.frombuffer(open(path, "rb").read(), dtype="<i2").astype(np.float32) / 32768, 24000

MODELS = {"siwis": "fr_FR-siwis-medium", "tom": "fr_FR-tom-medium", "upmc": "fr_FR-upmc-medium", "gilles": "fr_FR-gilles-low"}
_eng = {}

def synth(sp, text, tmp):
    if USE_GEMINI:
        x, sr = gemini(sp, text); semi = GEMINI[sp][2]
    else:
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
        # Gemini reads Hebrew script (names without one keep their transliteration), Piper the phonetic spelling
        tts = MARK.sub(lambda m: (m.group(1) or m.group(2)) if USE_GEMINI else m.group(3), txt)
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
        c = np.concatenate([[0], np.cumsum(env, dtype=np.float64)])  # 2 s moving average = fades
        i = np.arange(n); lo, hi = np.clip(i - SR, 0, n), np.clip(i + SR, 0, n)
        env = ((c[hi] - c[lo]) / (2*SR)).astype(np.float32)
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
