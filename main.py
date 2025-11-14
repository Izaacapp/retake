#!/usr/bin/env python3
"""
Retake Video Editor - Main Orchestration Script
Professional video editing pipeline with voice cloning and audio processing
"""
import sys
from pathlib import Path
from typing import List, Dict
import json

# Import our utilities
from utils.audio import AudioExtractor, SpeakerSeparator, AudioProcessor
from utils.video import VideoEditor
from utils.voice_clone import VoiceCloner
from utils.text import GrammarCorrector


class RetakeVideoProducer:
    """Main orchestrator for video retake production"""
    
    def __init__(self, original_video: str, transcript_file: str = None):
        self.original_video = Path(original_video)
        self.transcript_file = Path(transcript_file) if transcript_file else None
        
        # Initialize utilities
        print("🎬 Initializing Retake Video Producer...")
        self.audio_extractor = AudioExtractor()
        self.speaker_separator = SpeakerSeparator()
        self.audio_processor = AudioProcessor()
        self.video_editor = VideoEditor()
        self.voice_cloner = VoiceCloner()
        self.grammar_corrector = GrammarCorrector()
        
        # Project state
        self.extracted_audio = None
        self.speaker_segments = {}
        self.corrected_scripts = {}
        self.voice_models = {}
        
        print("✅ Producer initialized")
    
    def extract_audio_from_video(self) -> str:
        """Step 1: Extract audio from original video"""
        print("\n" + "="*60)
        print("STEP 1: AUDIO EXTRACTION")
        print("="*60)
        
        self.extracted_audio = self.audio_extractor.extract_audio(
            str(self.original_video),
            output_format="wav",
            sample_rate=48000,
            channels=2
        )
        
        # Get audio info
        info = self.audio_extractor.get_audio_info(self.extracted_audio)
        print(f"\n📊 Audio Info:")
        print(f"   Duration: {info['duration']:.2f}s ({info['duration']/60:.2f} min)")
        print(f"   Sample Rate: {info['sample_rate']} Hz")
        print(f"   Channels: {info['channels']}")
        
        return self.extracted_audio
    
    def identify_and_separate_speakers(self) -> Dict[str, str]:
        """Step 2: Identify speakers and separate their audio"""
        print("\n" + "="*60)
        print("STEP 2: SPEAKER DIARIZATION")
        print("="*60)
        
        # Identify speakers
        segments = self.speaker_separator.identify_speakers(
            self.extracted_audio,
            min_speakers=2,
            max_speakers=5
        )
        
        # Define our team members
        speakers = {
            'izaac': 'SPEAKER_00',
            'devon': 'SPEAKER_01',
            'ken': 'SPEAKER_02',
            'jewel': 'SPEAKER_03',
            'jared': 'SPEAKER_04'
        }
        
        # Extract audio for Izaac and Ken (our focus)
        for name, speaker_id in speakers.items():
            if name in ['izaac', 'ken']:
                print(f"\n🎤 Extracting audio for {name.title()}...")
                speaker_audio = self.speaker_separator.extract_speaker_audio(
                    self.extracted_audio,
                    segments,
                    speaker_id
                )
                self.speaker_segments[name] = speaker_audio
        
        return self.speaker_segments
    
    def create_voice_models(self) -> Dict[str, str]:
        """Step 3: Create voice cloning models"""
        print("\n" + "="*60)
        print("STEP 3: VOICE MODEL CREATION")
        print("="*60)
        
        for name, audio_path in self.speaker_segments.items():
            print(f"\n👤 Creating voice model for {name.title()}...")
            
            # First, enhance the audio quality
            enhanced = self.audio_processor.enhance_voice(audio_path)
            
            # Create voice profile
            profile = self.speaker_separator.create_speaker_profile(
                enhanced,
                speaker_name=name,
                sample_duration=30
            )
            
            # Clone voice
            voice_model = self.voice_cloner.clone_voice_from_sample(
                profile,
                speaker_name=name
            )
            
            self.voice_models[name] = voice_model
            print(f"✅ Voice model ready for {name.title()}")
        
        return self.voice_models
    
    def load_and_correct_transcript(self) -> Dict[str, List[Dict]]:
        """Step 4: Load transcript and correct grammar/consistency"""
        print("\n" + "="*60)
        print("STEP 4: TRANSCRIPT PROCESSING")
        print("="*60)
        
        if not self.transcript_file or not self.transcript_file.exists():
            print("⚠️ No transcript file provided")
            return {}
        
        # Parse VTT transcript
        with open(self.transcript_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract segments
        segments = self._parse_vtt(content)
        
        # Correct each segment
        corrected_segments = []
        for segment in segments:
            original_text = segment['text']
            corrected_text = self.grammar_corrector.process_full_script(original_text)
            
            corrected_segments.append({
                'id': segment['id'],
                'start': segment['start'],
                'end': segment['end'],
                'speaker': segment.get('speaker', 'Unknown'),
                'original': original_text,
                'corrected': corrected_text
            })
        
        print(f"\n✅ Processed {len(corrected_segments)} transcript segments")
        
        # Save corrected transcript
        self._save_corrected_transcript(corrected_segments)
        
        return corrected_segments
    
    def _parse_vtt(self, content: str) -> List[Dict]:
        """Parse VTT transcript file"""
        segments = []
        lines = content.split('\n')
        
        i = 0
        segment_id = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for timestamp line
            if '-->' in line:
                times = line.split('-->')
                start = times[0].strip()
                end = times[1].strip()
                
                # Next line(s) contain the text
                text_lines = []
                i += 1
                while i < len(lines) and lines[i].strip() and not lines[i].strip().isdigit():
                    text_lines.append(lines[i].strip())
                    i += 1
                
                text = ' '.join(text_lines)
                
                # Extract speaker if present
                speaker = "Unknown"
                if ':' in text:
                    parts = text.split(':', 1)
                    speaker = parts[0].strip()
                    text = parts[1].strip()
                
                segments.append({
                    'id': segment_id,
                    'start': start,
                    'end': end,
                    'speaker': speaker,
                    'text': text
                })
                segment_id += 1
            
            i += 1
        
        return segments
    
    def _save_corrected_transcript(self, segments: List[Dict]):
        """Save corrected transcript to file"""
        output_path = Path("output/corrected_transcript.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(segments, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Corrected transcript saved: {output_path}")
    
    def generate_new_audio(self, segments: List[Dict], speaker: str) -> List[str]:
        """Step 5: Generate new audio with corrected script"""
        print("\n" + "="*60)
        print(f"STEP 5: AUDIO GENERATION FOR {speaker.upper()}")
        print("="*60)
        
        # Filter segments for this speaker
        speaker_segments = [
            s for s in segments 
            if speaker.lower() in s['speaker'].lower()
        ]
        
        print(f"📝 Generating audio for {len(speaker_segments)} segments...")
        
        # Get voice model
        voice_model = self.voice_models.get(speaker.lower())
        if not voice_model:
            print(f"⚠️ No voice model found for {speaker}")
            return []
        
        # Generate audio for each segment
        audio_files = []
        for segment in speaker_segments:
            text = segment['corrected']
            if text.strip():
                audio_file = self.voice_cloner.synthesize_speech(
                    text=text,
                    speaker_model=voice_model,
                    output_filename=f"{speaker}_seg_{segment['id']:03d}"
                )
                audio_files.append(audio_file)
        
        print(f"✅ Generated {len(audio_files)} audio segments")
        return audio_files
    
    def run_full_pipeline(self):
        """Execute the complete video retake pipeline"""
        print("\n" + "="*70)
        print("🎬 RETAKE VIDEO PRODUCTION PIPELINE")
        print("="*70)
        print(f"Original Video: {self.original_video.name}")
        print(f"Transcript: {self.transcript_file.name if self.transcript_file else 'N/A'}")
        print("="*70)
        
        try:
            # Step 1: Extract audio
            self.extract_audio_from_video()
            
            # Step 2: Separate speakers (commented out for now - requires models)
            # self.identify_and_separate_speakers()
            
            # Step 3: Create voice models (commented out for now)
            # self.create_voice_models()
            
            # Step 4: Process transcript
            if self.transcript_file:
                corrected_segments = self.load_and_correct_transcript()
            
            # Step 5: Generate new audio (commented out - requires voice models)
            # for speaker in ['izaac', 'ken']:
            #     self.generate_new_audio(corrected_segments, speaker)
            
            print("\n" + "="*70)
            print("✅ PIPELINE COMPLETE")
            print("="*70)
            print("\nNext steps:")
            print("1. Record new screen captures for Izaac and Ken")
            print("2. Sync generated audio with new video")
            print("3. Combine intro + new segments + outro")
            print("4. Add smooth transitions")
            print("="*70)
            
        except Exception as e:
            print(f"\n❌ Error in pipeline: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Main entry point"""
    # Configuration
    ORIGINAL_VIDEO = "data/source/GMT20251114-035710_Recording_avo_1280x720.mp4"
    TRANSCRIPT = "data/source/GMT20251114-035710_Recording.transcript.vtt"
    
    # Create producer
    producer = RetakeVideoProducer(
        original_video=ORIGINAL_VIDEO,
        transcript_file=TRANSCRIPT
    )
    
    # Run pipeline
    producer.run_full_pipeline()


if __name__ == "__main__":
    main()
