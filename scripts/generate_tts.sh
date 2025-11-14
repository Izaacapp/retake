#!/bin/bash
# Automated TTS generation using Fish Speech

cd fish-speech
source .venv/bin/activate

OUTPUT_DIR="../output/tts_generated"
mkdir -p "$OUTPUT_DIR"

# Test with Izaac's voice
echo "🎤 Generating test audio for Izaac..."
python tools/vqgan/inference.py \
    --text "So, this is the first thing the user would see when they enter our platform." \
    --reference-audio ../output/audio/voice_samples/izaac_voice_sample.wav \
    --output "$OUTPUT_DIR/test_izaac.wav"

echo "✅ Test generation complete!"
echo "📁 Output: $OUTPUT_DIR/test_izaac.wav"
