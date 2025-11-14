#!/usr/bin/env python3
"""Cut up video into key segments based on transcript timing"""
from utils.video import VideoEditor
import json

editor = VideoEditor()

# Define key segments based on who's speaking and what they're showing
segments_to_cut = [
    # Intro - everyone visible
    {"name": "intro", "start": 0, "end": 120, "description": "Team intro"},
    
    # Izaac's main presentation parts
    {"name": "izaac_problem", "start": 120, "end": 260, "description": "Problem explanation"},
    {"name": "izaac_demo_start", "start": 260, "end": 380, "description": "Aether Mail demo"},
    
    # Devon's desktop demo
    {"name": "devon_desktop", "start": 125, "end": 240, "description": "Desktop features"},
    
    # Ken's part (need to identify from transcript)
    {"name": "ken_segment", "start": 122, "end": 140, "description": "Ken intro"},
    
    # Later segments we'll refine based on transcript
]

print("🎬 Cutting video segments...\n")

for seg in segments_to_cut[:3]:  # Cut first 3 for now
    print(f"Cutting: {seg['name']} ({seg['start']}s - {seg['end']}s)")
    output = editor.cut_segment(
        "data/source/GMT20251114-035710_Recording_avo_1280x720.mp4",
        start_time=seg['start'],
        end_time=seg['end'],
        output_name=f"{seg['name']}.mp4"
    )
    print(f"✅ Saved: {output}\n")

print("\n✅ Key segments cut successfully!")
