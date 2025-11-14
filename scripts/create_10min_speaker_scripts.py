#!/usr/bin/env python3
"""
Create individual speaker scripts from the 10-minute professional script
Outputs separate TXT files for each speaker for easy recording/TTS
"""
import json
from pathlib import Path
from collections import defaultdict

def create_speaker_scripts():
    """Generate individual scripts for each speaker"""
    
    print("📝 Creating 10-Minute Professional Speaker Scripts\n")
    
    # Load the 10-minute script
    with open('output/original/10min_professional_script.json') as f:
        segments = json.load(f)
    
    # Group by speaker
    speaker_segments = defaultdict(list)
    for seg in segments:
        speaker_segments[seg['speaker']].append(seg)
    
    # Create output directory
    output_dir = Path('output/scripts/10min')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate script for each speaker
    for speaker, segs in speaker_segments.items():
        output_file = output_dir / f"{speaker.lower()}_script.txt"
        
        with open(output_file, 'w') as f:
            f.write(f"# {speaker}'s Script - Deeply Profound 10-Minute Demo\n")
            f.write(f"# Total Segments: {len(segs)}\n")
            f.write(f"# Total Time: {sum([parse_duration(s['duration']) for s in segs])} seconds\n")
            f.write("\n" + "="*80 + "\n\n")
            
            for i, seg in enumerate(segs, 1):
                f.write(f"## Segment {i}: {seg['section']}\n")
                f.write(f"Time: {seg['time_start']} - {seg['time_end']} ({seg['duration']})\n")
                f.write(f"\n{seg['script']}\n")
                if seg.get('notes'):
                    f.write(f"\n[Note: {seg['notes']}]\n")
                f.write("\n" + "-"*80 + "\n\n")
        
        print(f"✅ {speaker}: {len(segs)} segments → {output_file}")
    
    # Create combined script
    combined_file = output_dir / "FULL_SCRIPT.txt"
    with open(combined_file, 'w') as f:
        f.write("# Deeply Profound - 10-Minute Professional Demo Script\n")
        f.write("# Complete Presentation Flow\n\n")
        f.write("="*80 + "\n\n")
        
        for seg in segments:
            f.write(f"[{seg['time_start']} - {seg['time_end']}] {seg['speaker']}\n")
            f.write(f"Section: {seg['section']}\n")
            f.write(f"\n{seg['script']}\n")
            f.write("\n" + "-"*80 + "\n\n")
    
    print(f"✅ Combined script → {combined_file}")
    
    # Create timeline visualization
    timeline_file = output_dir / "TIMELINE.md"
    with open(timeline_file, 'w') as f:
        f.write("# 10-Minute Demo Timeline\n\n")
        f.write("```\n")
        for seg in segments:
            duration = parse_duration(seg['duration'])
            bar = "█" * int(duration / 5)  # Scale: 1 bar = 5 seconds
            f.write(f"{seg['time_start']} {bar} {seg['speaker']}: {seg['section']}\n")
        f.write("```\n\n")
        
        f.write("## Section Breakdown\n\n")
        for seg in segments:
            f.write(f"- **{seg['section']}** ({seg['duration']}) - {seg['speaker']}\n")
    
    print(f"✅ Timeline → {timeline_file}")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 Summary:")
    print(f"   Total sections: {len(segments)}")
    print(f"   Total duration: ~10 minutes")
    print(f"   Speakers: {', '.join(speaker_segments.keys())}")
    print(f"\n📁 Output: {output_dir}/")
    print(f"   • Individual speaker scripts (.txt)")
    print(f"   • FULL_SCRIPT.txt (complete presentation)")
    print(f"   • TIMELINE.md (visual timeline)")

def parse_duration(duration_str):
    """Parse duration string like '45s' or '60s' to seconds"""
    return int(duration_str.replace('s', ''))

if __name__ == "__main__":
    create_speaker_scripts()
