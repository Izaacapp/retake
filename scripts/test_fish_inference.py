#!/usr/bin/env python3
"""
Test Fish Speech TTS inference with proper API
"""
import subprocess
from pathlib import Path
import sys

def test_tts():
    """Test Fish Speech TTS generation"""
    
    fish_dir = Path(__file__).parent.parent / "fish-speech"
    output_dir = Path(__file__).parent.parent / "output/tts_generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Paths
    ref_audio = Path(__file__).parent.parent / "output/audio/voice_samples/izaac_voice_sample.wav"
    checkpoint = fish_dir / "checkpoints/openaudio-s1-mini/codec.pth"
    
    print("🐟 Testing Fish Speech TTS\n")
    print(f"Reference audio: {ref_audio}")
    print(f"Checkpoint: {checkpoint}")
    print(f"Output dir: {output_dir}\n")
    
    # Step 1: Extract VQ tokens from reference audio
    print("📍 Step 1: Extracting VQ tokens from reference audio...")
    
    vq_output = output_dir / "izaac_ref.wav"
    
    cmd1 = [
        str(fish_dir / ".venv/bin/python"),
        str(fish_dir / "fish_speech/models/dac/inference.py"),
        "-i", str(ref_audio),
        "--checkpoint-path", str(checkpoint),
        "-o", str(vq_output),
        "--device", "cpu"
    ]
    
    print(f"Running: {' '.join(cmd1)}\n")
    
    result = subprocess.run(cmd1, cwd=str(fish_dir), capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Error extracting VQ tokens:")
        print(result.stderr)
        return 1
    
    print("✅ VQ tokens extracted\n")
    
    # Step 2: Generate semantic tokens from text
    print("📍 Step 2: Generating semantic tokens from text...")
    
    test_text = "So, this is the first thing the user would see when they enter our platform."
    ref_text = "Hello, everyone. We're going to start off with who we are."
    
    cmd2 = [
        str(fish_dir / ".venv/bin/python"),
        str(fish_dir / "fish_speech/models/text2semantic/inference.py"),
        "--text", test_text,
        "--prompt-text", ref_text,
        "--prompt-tokens", str(output_dir / "izaac_ref.npy"),
        "--device", "cpu"
    ]
    
    print(f"Running: {' '.join(cmd2)}\n")
    
    result = subprocess.run(cmd2, cwd=str(fish_dir), capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Error generating semantic tokens:")
        print(result.stderr)
        return 1
    
    print("✅ Semantic tokens generated\n")
    print(f"📊 Output: {result.stdout}")
    
    print("\n✅ Fish Speech TTS test complete!")
    print("🎯 Next: Generate full batch of audio segments")
    
    return 0

if __name__ == "__main__":
    sys.exit(test_tts())
