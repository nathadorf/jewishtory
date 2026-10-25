# Usage: python qa_elevenlabs.py <story_module> <ep_dir>  -> prints flagged cues, deletes their cache so the next run retakes them
# Gemini listens to each line and flags missing, repeated or added words (ElevenLabs v3 sometimes skips a phrase).
import sys, os, json, re, base64, subprocess, hashlib, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); os.environ["TTS_ENGINE"]="elevenlabs"
import gen
mod, ep = sys.argv[1], sys.argv[2]
cues = json.load(open(f"{ep}/cues.json"))["cues"]
expected = [gen.MARK.sub(lambda m: m.group(2), c["text"]) for c in cues]
flag = []
for b in range(0, len(cues), 12):
    parts = [{"text": "Pour chaque clip numéroté, compare l'audio au texte attendu. Les mots hébreux peuvent être prononcés différemment, c'est normal; 'Noa'h' est prononcé 'No-arr', normal aussi. Signale seulement les clips où des mots ou un morceau de phrase MANQUENT, sont répétés ou ajoutés, ou où une étiquette entre crochets est lue à voix haute. Réponds uniquement en JSON: [{\"n\": numéro, \"pb\": \"...\"}] ([] si rien)."}]
    for i in range(b, min(b+12, len(cues))):
        c = cues[i]
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(c["start"]),"-to",str(c["end"]+0.1),"-i",f"{ep}/story.mp3",f"{ep}/_qa.mp3"],check=True)
        parts += [{"text": f"Clip {i} — texte attendu : {expected[i]}"}, {"inlineData": {"mimeType":"audio/mp3","data": base64.b64encode(open(f"{ep}/_qa.mp3","rb").read()).decode()}}]
    body = {"contents":[{"parts":parts}], "generationConfig":{"responseMimeType":"application/json"}}
    r = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent", data=json.dumps(body).encode(), headers={"Content-Type":"application/json","x-goog-api-key":os.environ["GEMINI_API_KEY"]})
    out = json.loads(json.load(urllib.request.urlopen(r, timeout=300))["candidates"][0]["content"]["parts"][0]["text"])
    flag += out
for f in flag:
    i = int(f["n"]); c = cues[i]; print(i, c["sp"], "|", f["pb"], "|", expected[i][:80])
    if "--retake" in sys.argv:
        sp = c["sp"]; text = expected[i]
        voice, stab, _ = gen.ELEVEN[sp]
        for k, v in gen.ELEVEN_SAY.items(): text = text.replace(k, v)
        text = gen.ELEVEN_TAG.get(sp, "") + text
        bodyx = {"text": text, "model_id": gen.ELEVEN_MODEL, "language_code": "fr", "voice_settings": {"stability": stab, "similarity_boost": 0.8}}
        p = f"{gen.CACHE}/el-{hashlib.sha1(json.dumps([voice, bodyx], sort_keys=True).encode()).hexdigest()}.pcm"
        print("   cache", "deleted" if os.path.exists(p) else "MISSING"); 
        if os.path.exists(p): os.remove(p)
