#!/usr/bin/env python3
"""Prepare script for TTS generation - Izaac and Ken's corrected lines"""
import json
from pathlib import Path

# Load segments
with open('output/izaac_segments.json', 'r') as f:
    izaac_segments = json.load(f)

with open('output/ken_segments.json', 'r') as f:
    ken_segments = json.load(f)

# Prepare TTS scripts
output_dir = Path('output/tts_scripts')
output_dir.mkdir(parents=True, exist_ok=True)

print("📝 Preparing TTS scripts...\n")

# Izaac's script - first demo section
izaac_demo_segments = [s for s in izaac_segments if s['id'] >= 23 and s['id'] <= 45]
print(f"Izaac demo section: {len(izaac_demo_segments)} segments")

with open(output_dir / 'izaac_demo.txt', 'w') as f:
    for seg in izaac_demo_segments[:10]:  # First 10 for demo
        f.write(f"{seg['corrected']}\n")
        print(f"  [{seg['id']}] {seg['corrected'][:60]}...")

print(f"\n✅ Saved to {output_dir / 'izaac_demo.txt'}")

# Ken's script
print(f"\nKen section: {len(ken_segments)} segments")

with open(output_dir / 'ken_demo.txt', 'w') as f:
    for seg in ken_segments[2:]:  # Skip the intro
        f.write(f"{seg['corrected']}\n")
        print(f"  [{seg['id']}] {seg['corrected'][:60]}...")

print(f"\n✅ Saved to {output_dir / 'ken_demo.txt'}")

# Create a combined script for reference
print("\n📋 Creating combined reference script...")

with open(output_dir / 'full_corrected_script.txt', 'w') as f:
    f.write("# IZAAC SECTIONS\n\n")
    for seg in izaac_segments:
        f.write(f"[{seg['start']} - {seg['end']}]\n")
        f.write(f"{seg['corrected']}\n\n")
    
    f.write("\n# KEN SECTIONS\n\n")
    for seg in ken_segments:
        f.write(f"[{seg['start']} - {seg['end']}]\n")
        f.write(f"{seg['corrected']}\n\n")

print(f"✅ Saved to {output_dir / 'full_corrected_script.txt'}")

# Create JSON for programmatic access
scripts = {
    'izaac': {
        'voice_sample': 'output/audio/voice_samples/izaac_voice_sample.wav',
        'segments': izaac_demo_segments[:10]
    },
    'ken': {
        'voice_sample': 'output/audio/voice_samples/ken_voice_sample.wav',
        'segments': ken_segments[2:]
    }
}

with open(output_dir / 'tts_config.json', 'w') as f:
    json.dump(scripts, f, indent=2)

print(f"✅ Saved to {output_dir / 'tts_config.json'}")
print("\n🎯 Ready for Fish Speech TTS generation!")
