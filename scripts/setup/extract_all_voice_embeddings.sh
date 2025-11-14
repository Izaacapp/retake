#!/bin/bash
# Extract voice embeddings for ALL speakers using Fish Speech DAC

set -e

FISH_DIR="fish-speech"
FISH_PYTHON="$FISH_DIR/.venv/bin/python3"
CHECKPOINT="$FISH_DIR/checkpoints/openaudio-s1-mini/codec.pth"
# Voice samples are now organized by speaker in output/speakers/
# This script reads from output/speakers/{name}/voice_samples/
MODELS_DIR="models"
TEMP_DIR="$FISH_DIR/temp"

# Check Fish Speech is available
if [ ! -f "$FISH_PYTHON" ]; then
    echo "❌ Fish Speech Python not found at $FISH_PYTHON"
    exit 1
fi

if [ ! -f "$CHECKPOINT" ]; then
    echo "❌ Checkpoint not found at $CHECKPOINT"
    exit 1
fi

echo "🐟 Fish Speech Voice Embedding Extractor"
echo "   Python: $FISH_PYTHON"
echo "   Checkpoint: $CHECKPOINT"
echo ""

# Create temp dir
mkdir -p "$TEMP_DIR"
mkdir -p "$MODELS_DIR"

# Function to extract embedding using DAC
extract_embedding() {
    local speaker=$1
    local audio_file=$2
    
    echo "🎤 Extracting embedding for $speaker..."
    echo "   Audio: $audio_file"
    
    output_wav="$TEMP_DIR/${speaker}_ref.wav"
    output_npy="$TEMP_DIR/${speaker}_ref.npy"
    final_npy="$MODELS_DIR/${speaker}_voice_embedding.npy"
    
    # Run DAC inference to extract VQ codes
    $FISH_PYTHON "$FISH_DIR/fish_speech/models/dac/inference.py" \
        -i "$audio_file" \
        --checkpoint-path "$CHECKPOINT" \
        -o "$output_wav" \
        --device cpu 2>&1 | grep -v "WARNING\|UserWarning" || true
    
    # Check if .npy was created
    if [ -f "$output_npy" ]; then
        # Copy to models dir
        cp "$output_npy" "$final_npy"
        size=$(ls -lh "$final_npy" | awk '{print $5}')
        echo "   ✅ $final_npy ($size)"
    else
        echo "   ❌ Failed to create embedding"
    fi
    echo ""
}

# Concatenate audio files for each speaker
echo "📦 Concatenating audio samples..."

# Aaron
cat > /tmp/aaron_files.txt << EOF
file '$(pwd)/output/speakers/aaron/voice_samples/aaron_000.wav'
file '$(pwd)/output/speakers/aaron/voice_samples/aaron_001.wav'
file '$(pwd)/output/speakers/aaron/voice_samples/aaron_002.wav'
EOF
ffmpeg -f concat -safe 0 -i /tmp/aaron_files.txt -ar 44100 -ac 1 -y output/speakers/aaron/voice_samples/aaron_concat.wav 2>/dev/null
echo "  ✅ Aaron samples concatenated"

# Jules  
cat > /tmp/jules_files.txt << EOF
file '$(pwd)/output/speakers/jules/voice_samples/jules_000.wav'
file '$(pwd)/output/speakers/jules/voice_samples/jules_001.wav'
file '$(pwd)/output/speakers/jules/voice_samples/jules_002.wav'
EOF
ffmpeg -f concat -safe 0 -i /tmp/jules_files.txt -ar 44100 -ac 1 -y output/speakers/jules/voice_samples/jules_concat.wav 2>/dev/null
echo "  ✅ Jules samples concatenated"

# Jared
cat > /tmp/jared_files.txt << EOF
file '$(pwd)/output/speakers/jared/voice_samples/jared_000.wav'
file '$(pwd)/output/speakers/jared/voice_samples/jared_001.wav'
EOF
ffmpeg -f concat -safe 0 -i /tmp/jared_files.txt -ar 44100 -ac 1 -y output/speakers/jared/voice_samples/jared_concat.wav 2>/dev/null
echo "  ✅ Jared samples concatenated"

echo ""

# Extract embeddings
extract_embedding "aaron" "output/speakers/aaron/voice_samples/aaron_concat.wav"
extract_embedding "jules" "output/speakers/jules/voice_samples/jules_concat.wav" 
extract_embedding "jared" "output/speakers/jared/voice_samples/jared_concat.wav"

echo "✅ All voice embeddings extracted!"
echo ""
echo "📊 Summary:"
ls -lh $MODELS_DIR/*.npy | awk '{print "   " $9, "(" $5 ")"}'
