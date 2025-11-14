"""
Speaker diarization and audio separation using pyannote.audio
"""
import os
from pathlib import Path
from typing import List, Dict, Tuple
import torch
import numpy as np
import soundfile as sf


class SpeakerSeparator:
    """Separate speakers in audio using AI-powered diarization"""
    
    def __init__(self, output_dir: str = "output/audio/speakers"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"🔊 Using device: {self.device}")
    
    def identify_speakers(
        self,
        audio_path: str,
        num_speakers: int = None,
        min_speakers: int = 2,
        max_speakers: int = 10
    ) -> List[Dict]:
        """
        Identify and separate speakers in audio file
        
        Args:
            audio_path: Path to audio file
            num_speakers: Exact number of speakers (if known)
            min_speakers: Minimum number of speakers to detect
            max_speakers: Maximum number of speakers to detect
        
        Returns:
            List of speaker segments with timestamps
        """
        print(f"🎙️ Analyzing speakers in {Path(audio_path).name}...")
        
        try:
            # For now, we'll use a simple approach
            # In production, you would use:
            # from pyannote.audio import Pipeline
            # pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
            # diarization = pipeline(audio_path)
            
            # Placeholder for speaker detection
            # This would be replaced with actual pyannote.audio implementation
            segments = self._detect_speakers_simple(audio_path, num_speakers or max_speakers)
            
            print(f"✅ Detected {len(set(s['speaker'] for s in segments))} speakers")
            return segments
            
        except Exception as e:
            print(f"❌ Error in speaker identification: {e}")
            raise
    
    def _detect_speakers_simple(self, audio_path: str, num_speakers: int) -> List[Dict]:
        """Simple speaker detection (placeholder for pyannote.audio)"""
        # This is a placeholder - in production use pyannote.audio
        # For now, return mock data based on the transcript
        
        speakers = {
            'SPEAKER_00': 'Izaac (Zoom user)',
            'SPEAKER_01': 'Devon Villalona',
            'SPEAKER_02': 'Kenith Philip',
            'SPEAKER_03': 'Jhuiwensley Belizaire',
            'SPEAKER_04': 'Jared Zayas'
        }
        
        return [
            {'speaker': 'SPEAKER_00', 'start': 0, 'end': 100, 'label': speakers['SPEAKER_00']},
            {'speaker': 'SPEAKER_01', 'start': 100, 'end': 200, 'label': speakers['SPEAKER_01']},
            # Add more segments as needed
        ]
    
    def extract_speaker_audio(
        self,
        audio_path: str,
        speaker_segments: List[Dict],
        speaker_id: str
    ) -> str:
        """
        Extract all audio segments for a specific speaker
        
        Args:
            audio_path: Path to original audio
            speaker_segments: List of speaker segments from identify_speakers()
            speaker_id: Speaker ID to extract
        
        Returns:
            Path to extracted speaker audio file
        """
        print(f"🎤 Extracting audio for {speaker_id}...")
        
        audio_data, sample_rate = sf.read(audio_path)
        speaker_segments_list = []
        
        # Combine all segments for this speaker
        for segment in speaker_segments:
            if segment['speaker'] == speaker_id:
                start_sample = int(segment['start'] * sample_rate)
                end_sample = int(segment['end'] * sample_rate)
                speaker_segments_list.append(audio_data[start_sample:end_sample])
        
        # Concatenate all segments
        speaker_audio = np.concatenate(speaker_segments_list) if speaker_segments_list else np.array([])
        
        # Export speaker audio
        output_filename = f"{speaker_id}_{Path(audio_path).stem}.wav"
        output_path = self.output_dir / output_filename
        sf.write(str(output_path), speaker_audio, sample_rate)
        
        print(f"✅ Extracted {len(speaker_audio)/sample_rate:.1f}s for {speaker_id}")
        return str(output_path)
    
    def create_speaker_profile(
        self,
        audio_path: str,
        speaker_name: str,
        sample_duration: int = 30
    ) -> str:
        """
        Create a voice profile for voice cloning
        
        Args:
            audio_path: Path to speaker's audio
            speaker_name: Name of the speaker
            sample_duration: Duration in seconds for voice sample
        
        Returns:
            Path to voice profile file
        """
        print(f"👤 Creating voice profile for {speaker_name}...")
        
        audio_data, sample_rate = sf.read(audio_path)
        
        # Take a clean sample from the middle
        total_samples = len(audio_data)
        start_sample = total_samples // 2
        end_sample = start_sample + (sample_duration * sample_rate)
        voice_sample = audio_data[start_sample:int(end_sample)]
        
        profile_path = self.output_dir / f"profile_{speaker_name}.wav"
        sf.write(str(profile_path), voice_sample, sample_rate)
        
        print(f"✅ Voice profile created: {profile_path}")
        return str(profile_path)
