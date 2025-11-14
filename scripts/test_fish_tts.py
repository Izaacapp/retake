#!/usr/bin/env python3
"""
Test Fish Speech TTS with a simple example
This will use CPU inference (slower but works on Mac)
"""
import sys
import json
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_tts():
    """Test Fish Speech TTS"""
    print("🐟 Testing Fish Speech TTS\n")
    
    # Check if models exist
    models_dir = Path(__file__).parent.parent / "fish-speech/checkpoints"
    if not models_dir.exists():
        print("❌ Models not found!")
        print("   Run: python scripts/download_fish_models.py")
        return 1
    
    print("✅ Models found at:", models_dir)
    
    # Load TTS config
    config_file = Path("output/tts_scripts/tts_config.json")
    if not config_file.exists():
        print("❌ TTS config not found!")
        print("   Run: make tts-prep")
        return 1
    
    with open(config_file) as f:
        config = json.load(f)
    
    print("\n📝 Test configuration:")
    print(f"   Izaac voice: {config['izaac']['voice_sample']}")
    print(f"   Ken voice: {config['ken']['voice_sample']}")
    print(f"   Segments to generate: {len(config['izaac']['segments'])}")
    
    # Test with Izaac's first segment
    test_text = config['izaac']['segments'][0]['corrected']
    print(f"\n🎤 Test text: {test_text[:80]}...")
    
    print("\n💡 To generate TTS:")
    print("   cd fish-speech")
    print("   source .venv/bin/activate")
    print(f"   python tools/vqgan/inference.py \\")
    print(f"     --text \"{test_text}\" \\")
    print(f"     --reference-audio ../output/audio/voice_samples/izaac_voice_sample.wav \\")
    print(f"     --output ../output/tts_generated/test_izaac.wav")
    
    print("\n🔄 Setting up automated TTS generation...")
    
    # Create TTS generation script
    gen_script = Path(__file__).parent / "generate_tts.sh"
    with open(gen_script, 'w') as f:
        f.write("""#!/bin/bash
# Automated TTS generation using Fish Speech

cd fish-speech
source .venv/bin/activate

OUTPUT_DIR="../output/tts_generated"
mkdir -p "$OUTPUT_DIR"

# Test with Izaac's voice
echo "🎤 Generating test audio for Izaac..."
python tools/vqgan/inference.py \\
    --text "So, this is the first thing the user would see when they enter our platform." \\
    --reference-audio ../output/audio/voice_samples/izaac_voice_sample.wav \\
    --output "$OUTPUT_DIR/test_izaac.wav"

echo "✅ Test generation complete!"
echo "📁 Output: $OUTPUT_DIR/test_izaac.wav"
""")
    
    gen_script.chmod(0o755)
    print(f"✅ Created: {gen_script}")
    print(f"\n🚀 Run: ./scripts/generate_tts.sh")
    
    return 0

if __name__ == "__main__":
    sys.exit(test_tts())
