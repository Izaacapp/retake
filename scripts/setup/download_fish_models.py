#!/usr/bin/env python3
"""
Download Fish Speech models with token authentication
Run this interactively or set HF_TOKEN environment variable
"""
import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def download_models():
    """Download Fish Speech models"""
    
    print("🐟 Fish Speech Model Downloader\n")
    
    # Check for token in .env file first
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        print("📄 Loading token from .env file...")
        with open(env_file) as f:
            for line in f:
                if line.startswith('RETAKE_API='):
                    token = line.split('=', 1)[1].strip()
                    os.environ['HF_TOKEN'] = token
                    break
    
    # Check for token in environment
    token = os.environ.get('HF_TOKEN')
    if not token:
        print("⚠️  HuggingFace token required!")
        print("\n📝 To get a token:")
        print("   1. Go to https://huggingface.co/settings/tokens")
        print("   2. Create a new token (read access)")
        print("   3. Add to .env file: RETAKE_API=hf_your_token")
        print("\n   Or paste it here:")
        token = input("Token: ").strip()
        
        if not token:
            print("❌ No token provided. Exiting.")
            return
    
    # Set token for huggingface_hub
    os.environ['HF_TOKEN'] = token
    
    print("\n📦 Downloading models...")
    print("   This may take a while (models are ~1-2GB)\n")
    
    # Change to fish-speech directory
    fish_dir = Path(__file__).parent.parent / "fish-speech"
    os.chdir(fish_dir)
    
    # Run download script
    import subprocess
    result = subprocess.run(
        [str(fish_dir / ".venv/bin/python"), "tools/download_models.py"],
        env={**os.environ, 'HF_TOKEN': token}
    )
    
    if result.returncode == 0:
        print("\n✅ Models downloaded successfully!")
        print("📁 Location: fish-speech/checkpoints/")
    else:
        print("\n❌ Download failed. Check your token and try again.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(download_models())
