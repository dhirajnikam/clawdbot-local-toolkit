# Clawdbot Local Toolkit

A small collection of **local/offline utilities** I built alongside Clawdbot (hosted on AWS EC2) to automate common tasks.

This repo intentionally **does not include** any broker integrations (e.g., Angel One / SmartAPI) or sensitive credentials.

## What’s inside

### 1) Local human-like TTS (offline)
- **Engine:** Piper (offline)
- **Output:** WhatsApp-friendly `ogg/opus` (or WAV/MP3)
- Script: `tools/tts/tts`

### 1b) Offline voice-to-text (STT) for WhatsApp voice notes
- **Engine:** whisper.cpp (offline)
- Wrapper script: `tools/stt/whisper-transcribe`
- Model: recommended **tiny** (~75MB) for lightweight setup

### 2) PDF generation (proposals/quotes)
- **Engine:** ReportLab (Python)
- Script: `tools/pdf/proposal_generator.py`

### 3) Image tools (pixel/dot style)
- Procedural “tree” generator + photo pixelation
- Script: `tools/image/image_tools.py`
- HTML canvas demo: `tools/image/tree_canvas_demo.html`

---

## Quick start

### Prereqs
- Ubuntu 22.04+ (or similar)
- `python3`
- `ffmpeg`
- `pip`

```bash
sudo apt-get update -y
sudo apt-get install -y ffmpeg python3-pip wget ca-certificates
```

### Python deps
```bash
pip3 install --user pillow reportlab
```

---

## 1) TTS setup (Piper)

## 1b) STT setup (whisper.cpp)

### Install whisper.cpp + whisper-cli
```bash
sudo apt-get update -y
sudo apt-get install -y git build-essential cmake ffmpeg

cd /tmp
git clone --depth 1 https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make build
sudo install -m 0755 ./build/bin/whisper-cli /usr/local/bin/whisper-cli
```

### Download a lightweight model (tiny)
```bash
cd /tmp/whisper.cpp
bash ./models/download-ggml-model.sh tiny
sudo mkdir -p /opt/whisper-cpp
sudo cp ./models/ggml-tiny.bin /opt/whisper-cpp/ggml-tiny.bin
```

### Install the wrapper script
```bash
sudo install -m 0755 ./tools/stt/whisper-transcribe /usr/local/bin/whisper-transcribe
```

### Enable in Clawdbot config
Add this to your `clawdbot.json`:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 15728640,
        timeoutSeconds: 60,
        models: [
          {
            type: "cli",
            command: "whisper-transcribe",
            args: ["{{MediaPath}}"],
            timeoutSeconds: 60
          }
        ]
      }
    }
  }
}
```

Then restart the gateway.


### Install Piper
```bash
mkdir -p ~/clawd/tts/piper && cd ~/clawd/tts/piper
wget -q https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz -O piper.tar.gz
tar -xzf piper.tar.gz
```

### Download an English (US) voice
```bash
mkdir -p ~/clawd/tts/voices/en_US-lessac-medium
cd ~/clawd/tts/voices/en_US-lessac-medium
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx -O model.onnx
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json -O model.onnx.json
```

### Run
```bash
./tools/tts/tts "Hello from EC2" out.ogg
```

> Note: This script assumes the same directory structure used in the Clawdbot workspace:
> - `~/clawd/tts/piper/piper/piper`
> - `~/clawd/tts/voices/en_US-lessac-medium/model.onnx`
>
> Adjust paths inside `tools/tts/tts` if your layout differs.

---

## 2) PDF generator

```bash
python3 tools/pdf/proposal_generator.py
# outputs PDFs to /home/ubuntu/clawd/output in the original environment
```

Tip: Update constants in the script (product name, timeline, payment milestones) to match your proposal.

---

## 3) Image tools

### Generate a sample tree
```bash
python3 tools/image/image_tools.py tree --square 128 --portrait 128x192 --outdir out
```

### Pixelate a photo
```bash
python3 tools/image/image_tools.py pixelate --in photo.jpg --square 128 --portrait 128x192 --grid 64 --outdir out
```

### HTML canvas demo
Open `tools/image/tree_canvas_demo.html` in a browser and keep the referenced PNGs in the same folder.

---

## Security notes
- Don’t commit credentials.
- Don’t commit large model binaries; download them in setup steps.

## License
MIT
