#!/usr/bin/env python3
"""
Compare original vs highly professional transcripts
Shows the improvements made for presentations
"""
import json
from pathlib import Path
from typing import List, Dict

def load_speaker_transcript(speaker_name: str) -> List[Dict]:
    """Load highly professional transcript for a speaker"""
    file_path = Path(f'output/speakers/{speaker_name}/transcripts/{speaker_name}_highly_professional.json')
    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)
    return []

def print_comparison(segment: Dict, show_all: bool = False):
    """Print before/after comparison for a segment"""
    print(f"\n{'='*80}")
    print(f"Segment ID: {segment['id']} | Time: {segment['start']} - {segment['end']}")
    print(f"Speaker: {segment['speaker']}")
    print(f"{'='*80}")
    
    if show_all:
        print(f"\n❌ ORIGINAL:")
        print(f"   {segment['original']}")
        print(f"\n🔧 CORRECTED (grammar only):")
        print(f"   {segment['corrected']}")
        print(f"\n✅ PROFESSIONAL:")
        print(f"   {segment.get('professional', segment['corrected'])}")
    
    print(f"\n🎯 HIGHLY PROFESSIONAL:")
    print(f"   {segment['highly_professional']}")
    
    # Show improvements
    original_len = len(segment['original'])
    new_len = len(segment['highly_professional'])
    
    print(f"\n📊 Metrics:")
    print(f"   Length change: {original_len} → {new_len} chars ({new_len - original_len:+d})")
    
    # Check for removed fillers
    fillers = ['obviously', 'essentially', 'basically', 'so...', 'like,', 'boom', 'crazy']
    removed_fillers = [f for f in fillers if f in segment['original'].lower() and f not in segment['highly_professional'].lower()]
    if removed_fillers:
        print(f"   Removed fillers: {', '.join(removed_fillers)}")

def main():
    """Show comparison of transcripts"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare original vs highly professional transcripts')
    parser.add_argument('--speaker', choices=['izaac', 'aaron', 'ken', 'jules', 'jared', 'all'], 
                       default='izaac', help='Speaker to show')
    parser.add_argument('--segment-id', type=int, help='Show specific segment ID')
    parser.add_argument('--all-versions', action='store_true', help='Show all versions (original, corrected, professional, highly_professional)')
    parser.add_argument('--limit', type=int, default=5, help='Number of segments to show')
    
    args = parser.parse_args()
    
    print("🎯 TRANSCRIPT COMPARISON: Original → Highly Professional\n")
    
    speakers = ['izaac', 'aaron', 'ken', 'jules', 'jared'] if args.speaker == 'all' else [args.speaker]
    
    for speaker in speakers:
        segments = load_speaker_transcript(speaker)
        
        if not segments:
            print(f"⚠️  No transcript found for {speaker}")
            continue
        
        print(f"\n{'#'*80}")
        print(f"# {speaker.upper()} - {len(segments)} segments")
        print(f"{'#'*80}")
        
        # Filter to specific segment or show first N
        if args.segment_id is not None:
            segments_to_show = [s for s in segments if s['id'] == args.segment_id]
        else:
            # Show segments with custom rewrites first
            from create_professional_script import HIGHLY_PROFESSIONAL_REWRITES
            custom_segments = [s for s in segments if s['id'] in HIGHLY_PROFESSIONAL_REWRITES]
            auto_segments = [s for s in segments if s['id'] not in HIGHLY_PROFESSIONAL_REWRITES]
            segments_to_show = custom_segments[:args.limit] if custom_segments else auto_segments[:args.limit]
        
        for segment in segments_to_show:
            print_comparison(segment, show_all=args.all_versions)
    
    print(f"\n{'='*80}")
    print("✅ Comparison complete!")
    print("\n💡 Tips:")
    print("   • Use --segment-id N to see a specific segment")
    print("   • Use --all-versions to see all transformation stages")
    print("   • Use --speaker all to see all speakers")
    print("   • Use --limit N to control how many segments to show")

if __name__ == "__main__":
    main()
