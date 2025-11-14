#!/usr/bin/env python3
"""Quick test - extract audio from video"""
from utils.audio import AudioExtractor

# Quick audio extraction
extractor = AudioExtractor()
audio = extractor.extract_audio("data/source/GMT20251114-035710_Recording_avo_1280x720.mp4")
print(f"\n✅ DONE: {audio}")
