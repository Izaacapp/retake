#!/usr/bin/env python3
"""
Generate TTS audio for the 10-minute professional script using Fish Speech
Uses Fish Speech inference engine directly
"""
import json
import sys
from pathlib import Path

def generate_all_tts_simple():
    """Generate TTS using a simpler approach - create text files for manual processing"""
    
    print("🎬 Preparing TTS Generation for 10-Minute Script\n")
    
    # Load the script
    script_file = Path('output/original/10min_professional_script.json')
    if not script_file.exists():
        print(f"❌ Script file not found: {script_file}")
        return 1
    
    with open(script_file) as f:
        segments = json.load(f)
    
    # Create output directory
    output_dir = Path('output/tts/10min')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Output directory: {output_dir}\n")
    
    # Create a script for each segment
    for i, seg in enumerate(segments, 1):
        section_safe = seg['section'].replace(' ', '_').replace(':', '')
        
        # Create text file with the script
        text_file = output_dir / f"{i:02d}_{seg['speaker']}_{section_safe}.txt"
        with open(text_file, 'w') as f:
            f.write(seg['script'])
        
        print(f"[{i:02d}/{len(segments)}] {seg['speaker']}: {seg['section']} ({seg['duration']})")
        print(f"    ✅ Created: {text_file.name}")
    
    # Map speakers to their reference IDs
    speaker_ref_map = {
        'Izaac': 'izaac',
        'Ken': 'ken',
        'Jules': 'jules',
        'Aaron': 'aaron',
        'Jared': 'jared',
    }
    
    # Create manifest
    manifest_file = output_dir / 'manifest.json'
    manifest = []
    for i, seg in enumerate(segments, 1):
        section_safe = seg['section'].replace(' ', '_').replace(':', '')
        text_file = f"{i:02d}_{seg['speaker']}_{section_safe}.txt"
        audio_file = f"{i:02d}_{seg['speaker']}_{section_safe}.wav"
        reference_id = speaker_ref_map.get(seg['speaker'], 'izaac')
        
        manifest.append({
            'segment': i,
            'section': seg['section'],
            'speaker': seg['speaker'],
            'time_start': seg['time_start'],
            'time_end': seg['time_end'],
            'duration': seg['duration'],
            'text_file': text_file,
            'audio_file': audio_file,
            'script': seg['script'],
            'reference_id': reference_id
        })
    
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"✅ TTS Preparation Complete!")
    print(f"   📝 Text files: {len(segments)}")
    print(f"   📄 Manifest: {manifest_file}")
    print(f"\n💡 Next Steps:")
    print(f"   1. Setup references: python scripts/setup_fish_references.py")
    print(f"   2. Use the text files in {output_dir}/")
    print(f"   3. Generate audio using Fish Speech API or GitHub Actions")
    
    # Create a bash script for batch generation using Fish Speech API
    bash_script = output_dir / 'generate_with_fish_speech.sh'
    with open(bash_script, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Batch TTS generation using Fish Speech API\n")
        f.write("# Prerequisites:\n")
        f.write("#   1. Setup references: python scripts/setup_fish_references.py\n")
        f.write("#   2. Start API server: cd fish-speech && python tools/api_server.py --device cpu\n\n")
        f.write("set -e\n\n")
        
        for item in manifest:
            reference_id = item['reference_id']
            text_file = item['text_file']
            audio_file = item['audio_file']
            
            f.write(f"# Segment {item['segment']}: {item['section']}\n")
            f.write(f"echo 'Generating {audio_file}...'\n")
            f.write(f"python fish-speech/tools/api_client.py \\\n")
            f.write(f"  --text \"$(cat output/tts/10min/{text_file})\" \\\n")
            f.write(f"  --reference_id {reference_id} \\\n")
            f.write(f"  --output output/tts/10min/{audio_file.replace('.wav', '')} \\\n")
            f.write(f"  --format wav \\\n")
            f.write(f"  --no-play\n\n")
    
    bash_script.chmod(0o755)
    print(f"   📜 Bash script: {bash_script}")
    print(f"\n📌 To generate all audio:")
    print(f"   1. Setup Fish Speech references:")
    print(f"      python scripts/setup_fish_references.py")
    print(f"   2. Start Fish Speech API server:")
    print(f"      cd fish-speech && python tools/api_server.py --device cpu")
    print(f"   3. Run the generation script:")
    print(f"      {bash_script}")
    
    return 0

if __name__ == "__main__":
    sys.exit(generate_all_tts_simple())
