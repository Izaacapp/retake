#!/usr/bin/env python3
"""Extract audio samples for Izaac and Ken for voice cloning"""
import json
import subprocess
from pathlib import Path

def time_to_seconds(time_str):
    """Convert VTT timestamp to seconds"""
    parts = time_str.split(':')
    h, m, s = 0, 0, 0
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        m, s = parts
    else:
        s = parts[0]
    
    h = int(h)
    m = int(m)
    s = float(s)
    
    return h * 3600 + m * 60 + s

# Load speaker segments
with open('output/izaac_segments.json', 'r') as f:
    izaac_segments = json.load(f)

with open('output/ken_segments.json', 'r') as f:
    ken_segments = json.load(f)

output_dir = Path('output/audio/voice_samples')
output_dir.mkdir(parents=True, exist_ok=True)

source_audio = 'output/audio/GMT20251114-035710_Recording_avo_1280x720_audio.wav'

print("🎤 Extracting voice samples...\n")

# Extract Izaac's first 30 seconds of clear speech
print("Extracting Izaac's voice sample...")
izaac_start = time_to_seconds(izaac_segments[0]['start'])
izaac_end = time_to_seconds(izaac_segments[4]['end'])  # First ~50 seconds
izaac_duration = izaac_end - izaac_start

subprocess.run([
    'ffmpeg', '-i', source_audio,
    '-ss', str(izaac_start),
    '-t', str(min(30, izaac_duration)),
    '-acodec', 'pcm_s16le',
    '-ar', '44100',
    '-ac', '1',  # Mono
    '-y',
    str(output_dir / 'izaac_voice_sample.wav')
], check=True, capture_output=True)

print(f"✅ Izaac voice sample: {izaac_start:.2f}s - {izaac_start + 30:.2f}s")

# Extract Ken's voice sample (combine his segments)
print("\nExtracting Ken's voice sample...")
if len(ken_segments) > 1:
    # Get Ken's longest segment
    longest_seg = max(ken_segments[1:], key=lambda x: time_to_seconds(x['end']) - time_to_seconds(x['start']))
    ken_start = time_to_seconds(longest_seg['start'])
    ken_end = time_to_seconds(longest_seg['end'])
    ken_duration = ken_end - ken_start
    
    subprocess.run([
        'ffmpeg', '-i', source_audio,
        '-ss', str(ken_start),
        '-t', str(min(30, ken_duration)),
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '1',
        '-y',
        str(output_dir / 'ken_voice_sample.wav')
    ], check=True, capture_output=True)
    
    print(f"✅ Ken voice sample: {ken_start:.2f}s - {ken_start + min(30, ken_duration):.2f}s")

print("\n📊 Voice samples extracted:")
for sample in output_dir.glob('*.wav'):
    size = sample.stat().st_size / 1024 / 1024
    print(f"  {sample.name}: {size:.2f}MB")

print("\n✅ Voice samples ready for Fish Speech!")
