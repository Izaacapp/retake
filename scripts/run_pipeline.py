#!/usr/bin/env python3
"""
Main pipeline runner - orchestrates the full retake process
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.audio import AudioExtractor, AudioProcessor
from utils.video import VideoEditor
from utils.text import GrammarCorrector

def main():
    """Run the full pipeline"""
    print("🎬 Starting Retake Pipeline\n")
    
    # Paths
    source_video = "data/source/GMT20251114-035710_Recording_avo_1280x720.mp4"
    
    # Step 1: Extract audio (if not already done)
    audio_output = "output/audio/GMT20251114-035710_Recording_avo_1280x720_audio.wav"
    if not Path(audio_output).exists():
        print("📍 Step 1: Extracting audio...")
        extractor = AudioExtractor()
        extractor.extract_audio(source_video)
        print("✅ Audio extracted\n")
    else:
        print("✅ Step 1: Audio already extracted\n")
    
    # Step 2: Process transcript (if not already done)
    transcript_output = "output/corrected_transcript.json"
    if not Path(transcript_output).exists():
        print("📍 Step 2: Processing transcript...")
        print("💡 Run: python scripts/test_transcript.py")
        print("⚠️  Transcript not processed yet\n")
    else:
        print("✅ Step 2: Transcript processed\n")
    
    # Step 3: Speaker analysis
    izaac_segments = Path("output/izaac_segments.json")
    if not izaac_segments.exists():
        print("📍 Step 3: Analyzing speakers...")
        print("💡 Run: python scripts/analyze_speakers.py")
        print("⚠️  Speaker analysis not done yet\n")
    else:
        print("✅ Step 3: Speakers analyzed\n")
    
    # Step 4: Voice samples
    voice_samples = Path("output/audio/voice_samples")
    if not voice_samples.exists() or not list(voice_samples.glob("*.wav")):
        print("📍 Step 4: Extracting voice samples...")
        print("💡 Run: python scripts/extract_speaker_audio.py")
        print("⚠️  Voice samples not extracted yet\n")
    else:
        print("✅ Step 4: Voice samples extracted\n")
    
    # Step 5: TTS scripts
    tts_config = Path("output/tts_scripts/tts_config.json")
    if not tts_config.exists():
        print("📍 Step 5: Preparing TTS scripts...")
        print("💡 Run: python scripts/prepare_tts_script.py")
        print("⚠️  TTS scripts not prepared yet\n")
    else:
        print("✅ Step 5: TTS scripts ready\n")
    
    print("🎯 Pipeline status checked!")
    print("\nNext: Download Fish Speech models and generate TTS")

if __name__ == "__main__":
    main()
