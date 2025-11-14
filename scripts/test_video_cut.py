#!/usr/bin/env python3
"""Test video cutting - extract intro segment"""
from utils.video import VideoEditor

editor = VideoEditor()

# Cut intro (first 2 minutes where everyone is visible)
intro = editor.cut_segment(
    "data/source/GMT20251114-035710_Recording_avo_1280x720.mp4",
    start_time=0,
    end_time=120,  # 2 minutes
    output_name="intro_segment.mp4"
)

print(f"\n✅ Intro segment: {intro}")
