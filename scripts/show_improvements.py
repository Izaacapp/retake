#!/usr/bin/env python3
"""
Show before/after improvements from professional rewrites
"""
import json
from pathlib import Path
import sys

def show_improvements(speaker_filter=None, limit=10):
    """Show improvements for segments"""
    
    # Load professional transcript
    with open('output/original/professional_transcript.json') as f:
        segments = json.load(f)
    
    # Filter by speaker if specified
    if speaker_filter:
        # Map speaker names
        speaker_map = {
            'izaac': 'Zoom user',
            'aaron': 'Devon Villalona',
            'devon': 'Devon Villalona',
            'ken': 'Kenith Philip',
            'jules': 'Jhuiwensley Belizaire',
            'jared': 'Jared Zayas'
        }
        speaker_name = speaker_map.get(speaker_filter.lower(), speaker_filter)
        segments = [s for s in segments if speaker_name.lower() in s['speaker'].lower()]
    
    # Only show segments that have been rewritten (not just copied from corrected)
    rewritten = [s for s in segments if s['highly_professional'] != s.get('corrected', s['original'])]
    
    print(f"🎯 Professional Rewrites Comparison")
    print(f"   Found {len(rewritten)} rewritten segments")
    if speaker_filter:
        print(f"   Filtered to: {speaker_filter}")
    print()
    
    # Show up to limit
    for i, seg in enumerate(rewritten[:limit]):
        print(f"{'='*80}")
        print(f"Segment #{seg['id']} | {seg['speaker']} | {seg['start']} - {seg['end']}")
        print(f"{'='*80}")
        print()
        print(f"❌ ORIGINAL ({len(seg['original'])} chars):")
        print(f"   {seg['original']}")
        print()
        print(f"✅ HIGHLY PROFESSIONAL ({len(seg['highly_professional'])} chars):")
        print(f"   {seg['highly_professional']}")
        print()
        
        # Show improvements
        improvements = []
        original_lower = seg['original'].lower()
        
        if 'obviously' in original_lower and 'obviously' not in seg['highly_professional'].lower():
            improvements.append("removed 'obviously'")
        if 'essentially' in original_lower and 'essentially' not in seg['highly_professional'].lower():
            improvements.append("removed 'essentially'")
        if 'basically' in original_lower and 'basically' not in seg['highly_professional'].lower():
            improvements.append("removed 'basically'")
        if seg['original'].startswith('So,') or seg['original'].startswith('So '):
            improvements.append("removed leading 'So'")
        
        if improvements:
            print(f"💡 Improvements: {', '.join(improvements)}")
            print()
    
    print(f"{'='*80}")
    print(f"✅ Showing {min(limit, len(rewritten))} of {len(rewritten)} rewritten segments")
    print()
    print("💡 Usage:")
    print(f"   python {sys.argv[0]} [speaker] [limit]")
    print("   Example: python show_improvements.py izaac 5")

if __name__ == "__main__":
    speaker = sys.argv[1] if len(sys.argv) > 1 else None
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    show_improvements(speaker, limit)
