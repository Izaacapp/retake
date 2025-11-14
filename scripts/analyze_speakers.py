#!/usr/bin/env python3
"""Analyze transcript to find Izaac and Ken's speaking segments"""
import json
from collections import defaultdict

# Load corrected transcript
with open('output/corrected_transcript.json', 'r') as f:
    segments = json.load(f)

# Count speaker segments
speaker_stats = defaultdict(lambda: {'count': 0, 'segments': []})

for seg in segments:
    speaker = seg['speaker']
    speaker_stats[speaker]['count'] += 1
    speaker_stats[speaker]['segments'].append({
        'id': seg['id'],
        'start': seg['start'],
        'end': seg['end'],
        'text': seg['corrected'][:60] + '...' if len(seg['corrected']) > 60 else seg['corrected']
    })

print("📊 Speaker Analysis:\n")
for speaker, stats in sorted(speaker_stats.items(), key=lambda x: x[1]['count'], reverse=True):
    print(f"{speaker}: {stats['count']} segments")

# Focus on Izaac (Zoom user) and Ken (Kenith Philip)
print("\n" + "="*70)
print("🎤 IZAAC (Zoom user) SEGMENTS:")
print("="*70)
izaac_segments = speaker_stats['Zoom user']['segments'][:10]
for seg in izaac_segments:
    print(f"[{seg['id']}] {seg['start']} → {seg['end']}")
    print(f"    {seg['text']}\n")

print("\n" + "="*70)
print("🎤 KEN (Kenith Philip) SEGMENTS:")
print("="*70)
ken_segments = speaker_stats['Kenith Philip']['segments']
for seg in ken_segments:
    print(f"[{seg['id']}] {seg['start']} → {seg['end']}")
    print(f"    {seg['text']}\n")

# Save speaker-specific segments
izaac_all = [s for s in segments if s['speaker'] == 'Zoom user']
ken_all = [s for s in segments if s['speaker'] == 'Kenith Philip']

with open('output/izaac_segments.json', 'w') as f:
    json.dump(izaac_all, f, indent=2)

with open('output/ken_segments.json', 'w') as f:
    json.dump(ken_all, f, indent=2)

print(f"\n💾 Saved {len(izaac_all)} Izaac segments to output/izaac_segments.json")
print(f"💾 Saved {len(ken_all)} Ken segments to output/ken_segments.json")
