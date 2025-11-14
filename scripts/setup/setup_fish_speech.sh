#!/bin/bash
# Setup Fish Speech TTS for voice cloning

echo "🐟 Setting up Fish Speech TTS..."

# Clone fish-speech repo
if [ ! -d "fish-speech" ]; then
    echo "📦 Cloning fish-speech..."
    git clone https://github.com/fishaudio/fish-speech.git
    cd fish-speech
else
    echo "✅ fish-speech already exists"
    cd fish-speech
fi

# Install with uv
echo "📦 Installing fish-speech..."
uv sync --python 3.14 --extra cu129

echo "✅ Fish Speech setup complete!"
echo "Activate with: cd fish-speech && source .venv/bin/activate"
