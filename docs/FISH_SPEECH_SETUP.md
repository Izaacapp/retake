# Fish Speech TTS Setup Guide

## 🔑 HuggingFace Authentication Required

Fish Speech models are gated and require authentication.

### Step 1: Get HuggingFace Token

1. Go to https://huggingface.co/settings/tokens
2. Create a new token with **read** access
3. Copy the token

### Step 2: Set Token

```bash
# Export token (temporary)
export HF_TOKEN='hf_your_token_here'

# Or add to your shell profile for persistence
echo 'export HF_TOKEN="hf_your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Download Models

```bash
# Option 1: Interactive (will prompt for token)
python scripts/download_fish_models.py

# Option 2: With token set
HF_TOKEN='your_token' python scripts/download_fish_models.py
```

### Step 4: Test TTS

```bash
# Check setup
python scripts/test_fish_tts.py

# Generate test audio
./scripts/generate_tts.sh
```

## 📦 Model Details

- **Model**: fishaudio/openaudio-s1-mini
- **Size**: ~1-2GB
- **Location**: `fish-speech/checkpoints/`
- **Type**: Voice cloning TTS

## 🚀 Usage

Once models are downloaded:

```bash
# Generate TTS for Izaac's segments
./scripts/generate_tts.sh

# Or manually
cd fish-speech
source .venv/bin/activate
python tools/vqgan/inference.py \
  --text "Your text here" \
  --reference-audio ../output/audio/voice_samples/izaac_voice_sample.wav \
  --output ../output/tts_generated/output.wav
```

## ⚠️ Note

Models must be downloaded before TTS generation. The download requires:
- HuggingFace account
- Access token
- ~2GB disk space
- Internet connection
