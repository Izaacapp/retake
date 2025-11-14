#!/bin/bash
# Batch TTS generation for 10-minute script
# Uses Fish Speech with voice embeddings

set -e

echo "🎬 Batch TTS Generation for 10-Minute Script"
echo ""

# Check if Fish Speech is set up
if [ ! -d "fish-speech/.venv" ]; then
    echo "❌ Fish Speech not set up. Run: make fish-setup"
    exit 1
fi

# Check if voice models exist
echo "📦 Checking voice models..."
for model in models/*_voice_embedding.npy; do
    if [ -f "$model" ]; then
        echo "   ✅ $(basename $model)"
    fi
done
echo ""

# Check if 10-minute script exists
if [ ! -f "output/original/10min_professional_script.json" ]; then
    echo "❌ 10-minute script not found. Run: make create-10min"
    exit 1
fi

# Create output directory
mkdir -p output/tts/10min

# Activate Fish Speech environment
source fish-speech/.venv/bin/activate

# Device selection
DEVICE="${1:-cpu}"
echo "🖥️  Using device: $DEVICE"
echo ""

# Generate TTS
echo "🎙️  Generating TTS audio..."
python scripts/generate_tts_10min.py "$DEVICE"

echo ""
echo "✅ TTS generation complete!"
echo "📁 Output: output/tts/10min/"
echo ""
echo "Generated files:"
ls -lh output/tts/10min/*.wav 2>/dev/null || echo "No audio files generated"
