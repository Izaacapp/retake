#!/usr/bin/env python3
"""Test transcript processing with grammar fixes"""
from utils.text import GrammarCorrector
from pathlib import Path
import json

corrector = GrammarCorrector()

# Load VTT transcript
transcript_file = "data/source/GMT20251114-035710_Recording.transcript.vtt"
with open(transcript_file, 'r') as f:
    content = f.read()

# Parse VTT
segments = []
lines = content.split('\n')
i = 0
segment_id = 0

while i < len(lines):
    line = lines[i].strip()
    
    if '-->' in line:
        times = line.split('-->')
        start = times[0].strip()
        end = times[1].strip()
        
        # Get text
        text_lines = []
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].strip().isdigit():
            text_lines.append(lines[i].strip())
            i += 1
        
        text = ' '.join(text_lines)
        
        # Extract speaker
        speaker = "Unknown"
        if ':' in text:
            parts = text.split(':', 1)
            speaker = parts[0].strip()
            text = parts[1].strip()
        
        # Correct the text
        corrected = corrector.process_full_script(text)
        
        segments.append({
            'id': segment_id,
            'start': start,
            'end': end,
            'speaker': speaker,
            'original': text,
            'corrected': corrected
        })
        segment_id += 1
    
    i += 1

# Save corrected transcript
output_file = Path("output/corrected_transcript.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(segments, f, indent=2)

print(f"✅ Processed {len(segments)} segments")
print(f"💾 Saved to: {output_file}")

# Show examples
print("\n📝 Sample corrections:")
for i in range(min(5, len(segments))):
    seg = segments[i]
    print(f"\n[{seg['speaker']}] {seg['start']} → {seg['end']}")
    print(f"  Original:  {seg['original'][:80]}...")
    print(f"  Corrected: {seg['corrected'][:80]}...")
