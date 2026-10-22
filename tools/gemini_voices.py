#!/usr/bin/env python3
"""
Dukkan — regenerate every game voice clip with Gemini TTS (natural, expressive voices).

Runs on your Mac. No extra Python packages; needs ffmpeg (brew install ffmpeg).
Your API key is read from the GEMINI_API_KEY environment variable only — never written anywhere.

  1) Listen first (10 lines × 6 voices × 3 languages → samples/index.html):
       python3 tools/gemini_voices.py sample
  2) Generate everything with the voices you liked:
       python3 tools/gemini_voices.py build --ar Sulafat --en Achird --de Vindemiatrix
     Safe to stop and re-run: finished clips are skipped.
  3) Publish:
       python3 tools/gemini_voices.py publish     # copies the new clips into voice/ and refreshes the offline cache
       git add voice sw.js && git commit -m "Gemini voices" && git push
"""
import argparse, base64, html, json, os, pathlib, shutil, subprocess, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "voice" / "manifest.json"
STAGE = ROOT / "voice-gemini"
SAMPLES = ROOT / "samples"
MODEL = "gemini-3.8-flash-tts"
URL = "https://generativelanguage.googleapis.com/v1beta/interactions"

STYLE = {
    "ar": ("Warm, cheerful young Libyan woman playing pretend-shop with two little girls. Gentle, smiling, encouraging, "
           "natural conversational pace, light Libyan Arabic accent. Read exactly the given Arabic text."),
    "en": "Warm, cheerful young woman playing pretend-shop with two little girls. Friendly, smiling, encouraging, natural pace.",
    "de": "Warmherzige, fröhliche junge Frau, die mit zwei kleinen Mädchen Kaufladen spielt. Freundlich, lächelnd, ermutigend, natürliches Tempo.",
}
CANDIDATES = ["Sulafat", "Achird", "Vindemiatrix", "Leda", "Laomedeia", "Aoede"]
SAMPLE_KEYS = ["welcome", "mode_clinic", "p_1003", "guessQ", "guessRight", "v_green", "paid_9001", "treasure", "clue_5007", "closed"]

def die(msg): print("✖ " + msg); sys.exit(1)

def api_key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k: die('Set your key first, e.g.:  export GEMINI_API_KEY="…"   (it stays in this terminal session only)')
    return k

def need_ffmpeg():
    if not shutil.which("ffmpeg"): die("ffmpeg not found. Install it with:  brew install ffmpeg")

def find_audio(obj):
    """Return the last base64 audio payload anywhere in the response."""
    found = []
    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "audio" and isinstance(o.get("data"), str): found.append(o["data"])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(obj)
    return found[-1] if found else None

def tts(text, voice, style, key, tries=6):
    bodies = [  # documented shape first, flat shape as a fallback
        {"model": MODEL, "input": [{"type": "user_input", "content": [{"type": "text", "text": text,
            "annotations": [{"type": "speech_metadata", "style": style}]}]}],
         "response_format": {"type": "audio", "mime_type": "audio/wav", "sample_rate": 24000},
         "generation_config": {"speech_config": [{"voice": voice}]}},
        {"model": MODEL, "input": [{"type": "user_input", "text": text,
            "annotations": [{"type": "speech_metadata", "style": style}]}],
         "response_format": {"type": "audio"}, "generation_config": {"speech_config": [{"voice": voice}]}},
    ]
    wait = 8
    for attempt in range(tries):
        for body in bodies:
            req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                         headers={"Content-Type": "application/json", "x-goog-api-key": key})
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = find_audio(json.load(r))
                    if data: return base64.b64decode(data)
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace")[:300]
                if e.code == 400: continue                      # try the other body shape
                if e.code in (429, 500, 503):
                    ra = e.headers.get("Retry-After")
                    w = int(ra) if ra and ra.isdigit() else wait
                    print(f"   … limit reached ({e.code}), waiting {w}s"); time.sleep(w); wait = min(wait * 2, 120); break
                if e.code in (401, 403): die(f"The key was rejected ({e.code}). Check GEMINI_API_KEY. {msg}")
                print(f"   ! HTTP {e.code}: {msg}"); break
            except Exception as e:
                print(f"   ! {e}"); time.sleep(wait); break
    return None

def to_mp3(wav_bytes, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(".wav"); tmp.write_bytes(wav_bytes)
    af = ("silenceremove=start_periods=1:start_threshold=-48dB:start_silence=0.02,areverse,"
          "silenceremove=start_periods=1:start_threshold=-48dB:start_silence=0.06,areverse,afade=t=in:d=0.01,loudnorm=I=-16:TP=-1.5")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-af", af, "-ac", "1", "-ar", "24000",
                    "-c:a", "libmp3lame", "-b:a", "48k", str(dst)], check=True)
    tmp.unlink()

def lines():
    if not MANIFEST.exists(): die(f"{MANIFEST} not found — run this inside the dukkan repository.")
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {lang: {k: t for k, t in m[lang].items() if t} for lang in ("ar", "en", "de")}

def cmd_sample(a):
    key = api_key(); need_ffmpeg(); L = lines()
    rows = []
    for lang in ("ar", "en", "de"):
        for voice in a.voices:
            for k in SAMPLE_KEYS:
                if k not in L[lang]: continue
                dst = SAMPLES / lang / voice / f"{k}.mp3"
                if not dst.exists():
                    print(f"{lang} {voice:13} {k}")
                    wav = tts(L[lang][k], voice, STYLE[lang], key)
                    if wav: to_mp3(wav, dst)
                    time.sleep(60 / a.rpm)
                rows.append((lang, voice, k, L[lang][k]))
    page = ['<!doctype html><meta charset="utf-8"><title>Dukkan voice samples</title><style>body{font:16px system-ui;margin:24px;max-width:1100px}'
            'h2{margin-top:32px}table{border-collapse:collapse;width:100%}td{border-bottom:1px solid #ddd;padding:6px;vertical-align:middle}'
            'td.t{width:45%}audio{height:32px}</style><h1>اختر الصوت · Choose the voice</h1>']
    for lang in ("ar", "en", "de"):
        page.append(f"<h2>{lang.upper()}</h2><table>")
        for k in SAMPLE_KEYS:
            if k not in L[lang]: continue
            cells = "".join(f'<td>{v}<br><audio controls preload="none" src="{lang}/{v}/{k}.mp3"></audio></td>' for v in a.voices)
            page.append(f'<tr><td class="t" dir="auto">{html.escape(L[lang][k])}</td>{cells}</tr>')
        page.append("</table>")
    (SAMPLES / "index.html").write_text("\n".join(page), encoding="utf-8")
    print(f"\n✔ Open {SAMPLES/'index.html'} in your browser, listen, then run build with your favourites.")

def cmd_build(a):
    key = api_key(); need_ffmpeg(); L = lines()
    voice = {"ar": a.ar, "en": a.en, "de": a.de}
    langs = [x for x in ("ar", "en", "de") if voice[x]]
    total = sum(len(L[x]) for x in langs); done = 0; failed = []
    for lang in langs:
        for k, text in L[lang].items():
            done += 1
            dst = STAGE / lang / f"{k}.mp3"
            if dst.exists() and dst.stat().st_size > 800: continue
            print(f"[{done}/{total}] {lang} {k}: {text[:48]}")
            wav = tts(text, voice[lang], STYLE[lang], key)
            if wav: to_mp3(wav, dst)
            else: failed.append(f"{lang}/{k}")
            time.sleep(60 / a.rpm)
    (STAGE / "voices.json").write_text(json.dumps({"model": MODEL, "voices": voice, "style": STYLE}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n✔ Finished. Missing: {len(failed)} {failed[:10]}" + ("\n  Run the same command again to retry them." if failed else "\n  Next:  python3 tools/gemini_voices.py publish"))

def cmd_publish(a):
    if not STAGE.exists(): die("Nothing to publish — run build first.")
    n = 0
    for f in STAGE.rglob("*.mp3"):
        dst = ROOT / "voice" / f.relative_to(STAGE); dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dst); n += 1
    sw = ROOT / "sw.js"; s = sw.read_text()
    import re
    s = re.sub(r'dukkan-assets-v(\d+)', lambda m: f"dukkan-assets-v{int(m.group(1)) + 1}", s, count=1)   # devices drop the old cached clips
    sw.write_text(s)
    print(f"✔ Copied {n} clips into voice/ and refreshed the offline cache version.\n  Now:  git add voice sw.js && git commit -m \"Gemini voices\" && git push")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("sample"); s1.add_argument("--voices", nargs="+", default=CANDIDATES); s1.add_argument("--rpm", type=float, default=8)
    s2 = sub.add_parser("build");  s2.add_argument("--ar"); s2.add_argument("--en"); s2.add_argument("--de"); s2.add_argument("--rpm", type=float, default=8)
    sub.add_parser("publish")
    a = ap.parse_args()
    {"sample": cmd_sample, "build": cmd_build, "publish": cmd_publish}[a.cmd](a)

if __name__ == "__main__":
    main()
