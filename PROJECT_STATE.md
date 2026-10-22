# PROJECT_STATE — Dukkan (دكان فاطمة وسماء)

Live: https://totofroto.github.io/dukkan/ · Repo: https://github.com/totofroto/dukkan
Static PWA (single `index.html`), GitHub Pages. Voices in `voice/<lang>/<key>.mp3` + `voice/manifest.json`.
Print kits in `kit/`. Tools in `tools/`.

## Active Handoff
**Owner:** Antigravity (on the Mac mini) · **From:** Claude · **Date:** 2026-10-22

**Goal:** replace all game voice clips (ar, en, de — 1167 clips) with natural Gemini TTS voices.

**Red lines:** never print or write the API key into any file or log; read it only from the existing secrets location
in `~/.config/tfatleek/` (or Vaultwarden) into the environment variable `GEMINI_API_KEY` for this terminal session.
No deletions outside the repo's own `samples/` and `voice-gemini/` working folders.

**Steps**
1. Clone or update the repo:
   - `cd ~ && (git -C dukkan pull || git clone https://github.com/totofroto/dukkan.git) && cd ~/dukkan`
2. Make sure ffmpeg exists: `which ffmpeg || brew install ffmpeg`
3. Load the Gemini key into `GEMINI_API_KEY` from the user's secrets location (do not echo it).
4. Samples: `python3 tools/gemini_voices.py sample` then `open samples/index.html`.
   **Stop here and ask Tareg** which voice he prefers per language (candidates: Sulafat, Achird, Vindemiatrix, Leda, Laomedeia, Aoede).
5. Build with his choices, e.g. `python3 tools/gemini_voices.py build --ar Sulafat --en Achird --de Vindemiatrix`
   (8 requests/min to stay in the free tier; takes several hours; re-run the same command to resume or retry failures).
6. When it reports 0 missing: `python3 tools/gemini_voices.py publish`
7. `git add voice sw.js && git commit -m "Gemini voices" && git push`
8. Verify: open https://totofroto.github.io/dukkan/ , tap "افتحي الدكان", scan or type 1001 in the parents' panel → must say "تفاح" + price in the new voice.

**If the API call fails** (HTTP 400 on every request): the Interactions API shape may have changed — check
https://ai.google.dev/gemini-api/docs/speech-generation and adjust `tts()` in `tools/gemini_voices.py`; keep the output as mp3 per key.

## History
- v3 shop/clinic/treasure · v4 neural voices, 3D icons, offline, parent lock · v5 tap-to-hear, scanner input fixes
- v6 real currencies (EUR/USD/GBP/LYD/SAR/AED) + play-money kit, real products via Open Food Facts (IndexedDB catalogue)
- v7 🔍 food detective (card 8104): Nutri-Score, NOVA, sugar cubes game, allergens, additives, halal text check, ranks
