#!/usr/bin/env python3
"""
Download Fish Speech models - use public models that don't require gating
"""
import os
import sys
from pathlib import Path
from huggingface_hub import hf_hub_download

def download_models():
    """Download Fish Speech models from public repos"""
    
    print("🐟 Fish Speech Model Downloader (Alternative)\n")
    
    # Load token from .env
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        print("📄 Loading token from .env file...")
        with open(env_file) as f:
            for line in f:
                if line.startswith('RETAKE_API='):
                    token = line.split('=', 1)[1].strip()
                    os.environ['HF_TOKEN'] = token
                    break
    
    token = os.environ.get('HF_TOKEN')
    
    # Try alternative models
    checkpoints_dir = Path(__file__).parent.parent / "fish-speech/checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    
    print("📦 Trying alternative model sources...\n")
    
    # Option 1: Try fishaudio/fish-speech-1.5 (may be public)
    try:
        print("Attempting: fishaudio/fish-speech-1.5")
        model_dir = checkpoints_dir / "fish-speech-1.5"
        model_dir.mkdir(exist_ok=True)
        
        # Download just the essential files
        files = [
            "config.json",
            "model.pt",
        ]
        
        for file in files:
            try:
                print(f"  Downloading {file}...")
                hf_hub_download(
                    repo_id="fishaudio/fish-speech-1.5",
                    filename=file,
                    local_dir=str(model_dir),
                    token=token
                )
            except Exception as e:
                print(f"  ⚠️  Skipped {file}: {e}")
        
        print("✅ Downloaded fish-speech-1.5\n")
        
    except Exception as e:
        print(f"❌ fish-speech-1.5 failed: {e}\n")
    
    # Option 2: Request access instruction
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("⚠️  Official Model Requires Access Request")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\n📝 To use fishaudio/openaudio-s1-mini:")
    print("   1. Visit: https://huggingface.co/fishaudio/openaudio-s1-mini")
    print("   2. Click 'Request Access'")
    print("   3. Wait for approval (usually instant)")
    print("   4. Then run: python scripts/download_fish_models.py")
    print("\n💡 Or use alternative TTS (Coqui TTS, Bark, etc.)")
    
    return 0

if __name__ == "__main__":
    sys.exit(download_models())
