#!/usr/bin/env python3
"""
Extract reusable voice embeddings from reference audio
This allows us to store small model files instead of large audio samples
"""
import sys
import subprocess
from pathlib import Path
import shutil

def extract_voice_model(speaker_name: str, reference_audio: str):
    """Extract voice embedding for a speaker"""
    
    print(f"🎤 Extracting voice model for {speaker_name}...")
    
    fish_dir = Path(__file__).parent.parent / "fish-speech"
    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)
    
    checkpoint = fish_dir / "checkpoints/openaudio-s1-mini/codec.pth"
    temp_output = fish_dir / "temp" / f"{speaker_name}_ref.wav"
    
    # Use absolute path for reference audio
    abs_ref_audio = Path(__file__).parent.parent / reference_audio
    
    # Extract VQ tokens
    cmd = [
        str(fish_dir / ".venv/bin/python"),
        str(fish_dir / "fish_speech/models/dac/inference.py"),
        "-i", str(abs_ref_audio),
        "--checkpoint-path", str(checkpoint),
        "-o", str(temp_output),
        "--device", "cpu"
    ]
    
    print(f"   Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(fish_dir), capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    
    # Copy .npy embedding to models directory
    npy_file = temp_output.with_suffix('.npy')
    if npy_file.exists():
        model_output = models_dir / f"{speaker_name}_voice_embedding.npy"
        shutil.copy(npy_file, model_output)
        print(f"✅ Voice model saved: {model_output}")
        print(f"   Size: {model_output.stat().st_size / 1024:.1f} KB\n")
        return True
    
    print(f"❌ Embedding file not found: {npy_file}")
    return False

def main():
    """Extract voice models for Izaac and Ken"""
    
    print("🎙️ Voice Model Extractor\n")
    print("This creates small embedding files for TTS generation")
    print("Voice models can be committed to git (small size)\n")
    print("="*70 + "\n")
    
    # Extract Izaac's voice
    izaac_success = extract_voice_model(
        "izaac",
        "output/audio/voice_samples/izaac_voice_sample.wav"
    )
    
    # Extract Ken's voice
    ken_success = extract_voice_model(
        "ken",
        "output/audio/voice_samples/ken_voice_sample.wav"
    )
    
    print("="*70)
    if izaac_success and ken_success:
        print("✅ All voice models extracted successfully!")
        print("\n📦 Models ready to commit:")
        print("   git add models/*.npy")
        print("   git commit -m 'Add voice embeddings for TTS'")
        print("\n🚀 Use these models for fast TTS generation")
    else:
        print("⚠️  Some extractions failed. Check errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
