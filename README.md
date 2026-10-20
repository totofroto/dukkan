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
