#!/usr/bin/env bash
# Blobby & Co. pack — one-time setup in a fresh workspace
set -e
cd "$(dirname "$0")"
python3 -c "import PIL, numpy" 2>/dev/null || pip install --break-system-packages pillow numpy
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
ls /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf >/dev/null 2>&1 || apt-get install -y -qq fonts-dejavu-core
pip install -q --break-system-packages piper-tts librosa 2>/dev/null || true
mkdir -p episodes voices
if [ ! -f voices/en-us-amy-low.onnx ]; then (cd voices && curl -sL -o v.tar.gz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-en-us-amy-low.tar.gz && tar xzf v.tar.gz && rm v.tar.gz); fi
if [ ! -f voices/en-us-ryan-medium.onnx ]; then (cd voices && curl -sL -o v.tar.gz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-en-us-ryan-medium.tar.gz && tar xzf v.tar.gz && rm v.tar.gz); fi
cd code && python3 -c "import engine, characters, stages, sfx, props; print('Blobby & Co. engine OK —', len(sfx.SFX), 'sound effects')"
