# PROJECT_STATE — Dukkan (دكان فاطمة وسماء)

Live: https://totofroto.github.io/dukkan/ · Repo: https://github.com/totofroto/dukkan
Static PWA (single `index.html`), GitHub Pages. Voices in `voice/<lang>/<key>.mp3` + `voice/manifest.json`.
Print kits in `kit/`. Tools in `tools/`.

## Active Handoff
| Date | From → To | Status | Task / Notes |
|---|---|---|---|
| 2026-11-03 | Antigravity → Tareg | ✅ done | All 1167 clips regenerated with natural Gemini TTS voice (Achird for ar, en, de) across all languages. Published to `voice/`, bumped service worker cache in `sw.js` (offline ready), and pushed to GitHub main. |
| 2026-10-22 | Claude → Antigravity | ✅ done | Handed off task to replace all game voice clips with Gemini TTS voices. |

## History
- v3 shop/clinic/treasure · v4 neural voices, 3D icons, offline, parent lock · v5 tap-to-hear, scanner input fixes
- v6 real currencies (EUR/USD/GBP/LYD/SAR/AED) + play-money kit, real products via Open Food Facts (IndexedDB catalogue)
- v7 🔍 food detective (card 8104): Nutri-Score, NOVA, sugar cubes game, allergens, additives, halal text check, ranks
