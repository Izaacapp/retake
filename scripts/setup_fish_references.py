#!/usr/bin/env python3
"""
Setup Fish Speech reference voices from existing voice samples
Creates reference directories that can be used with --reference_id
"""
import shutil
from pathlib import Path

def setup_references():
    """Setup reference directories for all speakers"""
    
    # Speaker to voice sample mapping
    speaker_samples = {
        'izaac': {
            'audio': 'data/source/GMT20251114-035710_Recording.m4a',
            'text': 'This is the first screen users see when entering our platform.'
        },
        'ken': {
            'audio': 'data/source/GMT20251114-025308_Recording.m4a',
            'text': 'As you can see, once logged in, we have a clean interface.'
        },
        'jules': {
            'audio': 'output/speakers/jules/voice_samples/jules_000.wav',
            'text': 'Security and privacy are fundamental to our platform design.'
        },
        'aaron': {
            'audio': 'output/speakers/aaron/voice_samples/aaron_000.wav',
            'text': 'The password vault provides secure storage for all credentials.'
        },
        'jared': {
            'audio': 'output/speakers/jared/voice_samples/jared_000.wav',
            'text': 'Our technology enables automated credential management.'
        },
    }
    
    refs_dir = Path('fish-speech/references')
    refs_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎙️ Setting up Fish Speech reference voices\n")
    
    for speaker, config in speaker_samples.items():
        speaker_dir = refs_dir / speaker
        audio_path = Path(config['audio'])
        
        # Skip if audio doesn't exist
        if not audio_path.exists():
            print(f"⚠️  {speaker}: Audio file not found, skipping")
            continue
        
        # Create speaker reference directory
        speaker_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy audio file
        target_audio = speaker_dir / f"sample{audio_path.suffix}"
        shutil.copy2(audio_path, target_audio)
        
        # Create .lab text file
        lab_file = speaker_dir / "sample.lab"
        lab_file.write_text(config['text'], encoding='utf-8')
        
        print(f"✅ {speaker:8} → {target_audio.name} + sample.lab")
    
    print(f"\n📂 References directory: {refs_dir}")
    print("\n💡 Usage:")
    print("   python fish-speech/tools/api_client.py \\")
    print("     --text 'Your text here' \\")
    print("     --reference_id izaac \\")
    print("     --output output.wav")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(setup_references())
