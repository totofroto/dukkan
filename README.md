# دكان فاطمة وسماء · Fatima & Sama's Shop

Barcode pretend-play for the Zebra DS2278 (HID keyboard mode): shop & bank, clinic, treasure hunt — Arabic, English, Deutsch.

- Play: open the GitHub Pages URL on the tablet → *Add to Home screen*.
- Print kit (duplex, long edge, 100 %): `kit/print-kit-duplex.pdf` — pages 1–14 duplex, page 15 single-sided on sticker paper.
- Codes: 1001–1020 products · 3001–3006 patients · 4001–4008 treatments · 5001–5010 treasure spots · 7001–7020 money · 8001–8103 controls & modes · 9001/9002 bank cards.

## v4
- Human neural voices (Microsoft Edge TTS): Arabic `ar-LY-ImanNeural` (Libyan), English `en-US-EmmaNeural`, German `de-DE-SeraphinaMultilingualNeural` — `voice/`, rendered by `make_voices.py` in the dev folder.
- Family voice: parents can record key lines in the parents' panel (stored in IndexedDB on the device).
- 3D icons: [Microsoft Fluent Emoji](https://github.com/microsoft/fluentui-emoji) (MIT) in `fx/`.
- Offline: `sw.js` caches the game, icons and voices.
- Parents' panel opens with a long press on ⚙︎.

## v6 — real money & real products
- Currencies: EUR, USD, GBP, LYD, SAR, AED (+ the original stars). Fixed play rates; "simple prices" option rounds to whole units.
- Money cards: `7` + currency digit (1 EUR, 2 USD, 3 GBP, 4 LYD, 5 SAR, 6 AED) + value in hundredths (5 digits). Print `kit/money-kit-duplex.pdf`.
- Real products: scan any EAN-8/EAN-13 → looked up on Open Food Facts / Open Products Facts → stored locally (IndexedDB `catalog`, schema 1). Edit names/prices, back up and restore as JSON in the parents' panel.

## v7 — 🔍 Food detective (4th world, card 8104)
- Scan any food barcode → Open Food Facts: photo, brand, everyday/sometimes/treat light, sugar cubes per 100 g and per serving,
  Nutri-Score, NOVA processing, fat/saturated fat/sugar/salt levels, allergens & traces, vegan/vegetarian/palm oil,
  ingredients, additives with short notes, and a halal text check for parents (gelatine, pork, alcohol, carmine, L-cysteine).
- Guess-the-sugar-cubes game before the answer, case file with "least sugar" winner, detective ranks.
- Everything spoken with the human voices; product names via device voice.
