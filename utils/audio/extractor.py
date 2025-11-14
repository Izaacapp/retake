"""
Audio extraction from video files with high-quality output
"""
import os
from pathlib import Path
from typing import Optional, Tuple
import subprocess
import ffmpeg


class AudioExtractor:
    """Extract audio from video files with various formats and quality settings"""
    
    def __init__(self, output_dir: str = "output/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_audio(
        self, 
        video_path: str, 
        output_format: str = "wav",
        sample_rate: int = 48000,
        channels: int = 2
    ) -> str:
        """
        Extract audio from video file
        
        Args:
            video_path: Path to input video
            output_format: Output format (wav, mp3, flac, etc.)
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels (1=mono, 2=stereo)
        
        Returns:
            Path to extracted audio file
        """
        video_path = Path(video_path)
        output_filename = f"{video_path.stem}_audio.{output_format}"
        output_path = self.output_dir / output_filename
        
        print(f"🎵 Extracting audio from {video_path.name}...")
        
        try:
            # Use ffmpeg-python for extraction
            stream = ffmpeg.input(str(video_path))
            stream = ffmpeg.output(
                stream,
                str(output_path),
                acodec='pcm_s16le' if output_format == 'wav' else 'libmp3lame',
                ar=sample_rate,
                ac=channels,
                **{'q:a': 0} if output_format == 'mp3' else {}
            )
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
            print(f"✅ Audio extracted to: {output_path}")
            return str(output_path)
            
        except ffmpeg.Error as e:
            print(f"❌ Error extracting audio: {e.stderr.decode() if e.stderr else str(e)}")
            raise
    
    def extract_segment(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        output_format: str = "wav"
    ) -> str:
        """
        Extract audio segment from specific time range
        
        Args:
            video_path: Path to input video
            start_time: Start time in seconds
            end_time: End time in seconds
            output_format: Output format
        
        Returns:
            Path to extracted audio segment
        """
        video_path = Path(video_path)
        output_filename = f"{video_path.stem}_segment_{int(start_time)}-{int(end_time)}.{output_format}"
        output_path = self.output_dir / output_filename
        
        print(f"🎵 Extracting audio segment {start_time}s - {end_time}s...")
        
        try:
            stream = ffmpeg.input(str(video_path), ss=start_time, to=end_time)
            stream = ffmpeg.output(
                stream,
                str(output_path),
                acodec='pcm_s16le' if output_format == 'wav' else 'libmp3lame',
                ar=48000,
                ac=2
            )
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
            print(f"✅ Segment extracted to: {output_path}")
            return str(output_path)
            
        except ffmpeg.Error as e:
            print(f"❌ Error extracting segment: {e}")
            raise
    
    def get_audio_info(self, audio_path: str) -> dict:
        """Get audio file metadata"""
        try:
            probe = ffmpeg.probe(audio_path)
            audio_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'audio'),
                None
            )
            
            if audio_stream is None:
                raise ValueError("No audio stream found")
            
            return {
                'duration': float(probe['format']['duration']),
                'sample_rate': int(audio_stream['sample_rate']),
                'channels': int(audio_stream['channels']),
                'codec': audio_stream['codec_name'],
                'bitrate': int(probe['format'].get('bit_rate', 0))
            }
        except Exception as e:
            print(f"❌ Error getting audio info: {e}")
            raise
