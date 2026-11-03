#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

export GEMINI_API_KEY=$(cat ~/.config/tfatleek/gemini_api_key | tr -d '\r\n ')

TOTAL=1167

echo "=== Starting Gemini voice generation (Achird for ar, en, de) ==="
echo "Target: $TOTAL clips at 8 RPM"

while true; do
    echo "--- Running build: $(date) ---"
    python3 tools/gemini_voices.py build --ar Achird --en Achird --de Achird --rpm 8 || true
    
    COUNT=$(find voice-gemini -name "*.mp3" -size +800c 2>/dev/null | wc -l | tr -d ' ')
    echo "Progress: $COUNT / $TOTAL clips generated"
    
    if [ "$COUNT" -ge "$TOTAL" ]; then
        echo "=== All $TOTAL clips generated successfully! ==="
        break
    fi
    
    echo "Clips remaining: $((TOTAL - COUNT)). Waiting 20 seconds before resuming..."
    sleep 20
done

echo "=== Publishing clips to voice/ ==="
python3 tools/gemini_voices.py publish

echo "=== Updating PROJECT_STATE.md ==="
# Mark completed in PROJECT_STATE.md
python3 -c "
import pathlib, datetime
p = pathlib.Path('PROJECT_STATE.md')
txt = p.read_text(encoding='utf-8')
replacement = '''## Active Handoff
**Owner:** Antigravity (on the Mac mini) · **Date:** 2026-10-22

**Status:** Completed. All 1167 clips regenerated with Gemini TTS voice (Achird for ar, en, de) and published to voice/.
Service worker cache version incremented and deployed.
'''
if '## Active Handoff' in txt:
    parts = txt.split('## Active Handoff')
    rest = parts[1].split('## History')
    txt = parts[0] + replacement + '\n## History' + rest[1]
    p.write_text(txt, encoding='utf-8')
"

echo "=== Committing and pushing to GitHub ==="
git add voice sw.js PROJECT_STATE.md tools/build_and_publish.sh
git commit -m "Gemini voices: regenerated 1167 clips using Achird (ar, en, de)"
git push origin main

echo "=== DEPLOYMENT COMPLETE ==="
