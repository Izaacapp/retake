#!/usr/bin/env python3
"""
Use original audio segments instead of TTS while waiting for Fish Speech access
This is faster and lets us continue the workflow
"""
import sys
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

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

def main():
    """Extract original audio segments"""
    print("🎤 Using Original Audio (No TTS needed)\n")
    
    # Load segments
    with open('output/izaac_segments.json') as f:
        izaac_segments = json.load(f)
    
    with open('output/ken_segments.json') as f:
        ken_segments = json.load(f)
    
    source_audio = "output/audio/GMT20251114-035710_Recording_avo_1280x720_audio.wav"
    output_dir = Path("output/audio/segments")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📊 Processing segments:")
    print(f"   Izaac: {len(izaac_segments)} segments")
    print(f"   Ken: {len(ken_segments)} segments\n")
    
    # Extract Izaac's demo segments (the ones we care about)
    izaac_demo = [s for s in izaac_segments if s['id'] >= 25 and s['id'] <= 45]
    
    print(f"🎬 Extracting Izaac's demo audio ({len(izaac_demo)} segments)...")
    for i, seg in enumerate(izaac_demo[:5]):  # First 5 for demo
        start = time_to_seconds(seg['start'])
        end = time_to_seconds(seg['end'])
        duration = end - start
        
        output = output_dir / f"izaac_demo_{i:03d}.wav"
        
        subprocess.run([
            'ffmpeg', '-i', source_audio,
            '-ss', str(start),
            '-t', str(duration),
            '-acodec', 'pcm_s16le',
            '-ar', '44100',
            '-y',
            str(output)
        ], capture_output=True, check=True)
        
        print(f"   [{i}] {seg['corrected'][:60]}...")
        print(f"       → {output.name} ({duration:.1f}s)")
    
    # Extract Ken's segments
    ken_demo = [s for s in ken_segments if s['id'] >= 48]
    
    print(f"\n🎬 Extracting Ken's demo audio ({len(ken_demo)} segments)...")
    for i, seg in enumerate(ken_demo):
        start = time_to_seconds(seg['start'])
        end = time_to_seconds(seg['end'])
        duration = end - start
        
        output = output_dir / f"ken_demo_{i:03d}.wav"
        
        subprocess.run([
            'ffmpeg', '-i', source_audio,
            '-ss', str(start),
            '-t', str(duration),
            '-acodec', 'pcm_s16le',
            '-ar', '44100',
            '-y',
            str(output)
        ], capture_output=True, check=True)
        
        print(f"   [{i}] {seg['corrected'][:60]}...")
        print(f"       → {output.name} ({duration:.1f}s)")
    
    print(f"\n✅ Audio segments extracted to: {output_dir}")
    print(f"\n💡 Next steps:")
    print(f"   1. Record new screen captures for Izaac & Ken")
    print(f"   2. Sync these audio segments with new videos")
    print(f"   3. Composite final video")
    print(f"\n📝 Note: These are original audio clips")
    print(f"   Later: Replace with Fish Speech TTS when access granted")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
