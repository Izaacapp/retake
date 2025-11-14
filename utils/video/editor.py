"""
Video editing utilities using MoviePy and OpenCV
"""
from pathlib import Path
from typing import List, Tuple, Optional
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip
import moviepy.video.fx as vfx
import numpy as np


class VideoEditor:
    """Professional video editing capabilities"""
    
    def __init__(self, output_dir: str = "output/video"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def cut_segment(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        output_name: str = None
    ) -> str:
        """
        Extract a segment from video
        
        Args:
            video_path: Path to input video
            start_time: Start time in seconds
            end_time: End time in seconds
            output_name: Optional output filename
        
        Returns:
            Path to extracted segment
        """
        print(f"✂️ Cutting segment {start_time}s - {end_time}s...")
        
        clip = VideoFileClip(video_path).subclipped(start_time, end_time)
        
        if output_name is None:
            output_name = f"{Path(video_path).stem}_segment_{int(start_time)}-{int(end_time)}.mp4"
        
        output_path = self.output_dir / output_name
        clip.write_videofile(
            str(output_path),
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(self.output_dir / 'temp-audio.m4a'),
            remove_temp=True,
            logger=None
        )
        clip.close()
        
        print(f"✅ Segment saved: {output_path}")
        return str(output_path)
    
    def replace_audio(
        self,
        video_path: str,
        audio_path: str,
        output_name: str = None
    ) -> str:
        """
        Replace video audio track
        
        Args:
            video_path: Path to input video
            audio_path: Path to new audio
            output_name: Optional output filename
        
        Returns:
            Path to video with new audio
        """
        print(f"🔊 Replacing audio track...")
        
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # Set new audio
        final = video.set_audio(audio)
        
        if output_name is None:
            output_name = f"{Path(video_path).stem}_new_audio.mp4"
        
        output_path = self.output_dir / output_name
        final.write_videofile(
            str(output_path),
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(self.output_dir / 'temp-audio.m4a'),
            remove_temp=True,
            logger=None
        )
        
        video.close()
        audio.close()
        final.close()
        
        print(f"✅ Audio replaced: {output_path}")
        return str(output_path)
    
    def concatenate_videos(
        self,
        video_paths: List[str],
        output_name: str = "concatenated.mp4",
        transition_duration: float = 0.5
    ) -> str:
        """
        Concatenate multiple videos with transitions
        
        Args:
            video_paths: List of video file paths
            output_name: Output filename
            transition_duration: Duration of crossfade in seconds
        
        Returns:
            Path to concatenated video
        """
        print(f"🎬 Concatenating {len(video_paths)} videos...")
        
        clips = [VideoFileClip(str(path)) for path in video_paths]
        
        # Apply fade transitions
        processed_clips = []
        for i, clip in enumerate(clips):
            if i == 0:
                # First clip: fade in
                clip = clip.with_effects([vfx.FadeIn(transition_duration)])
            elif i == len(clips) - 1:
                # Last clip: fade out
                clip = clip.with_effects([vfx.FadeOut(transition_duration)])
            else:
                # Middle clips: fade in and out
                clip = clip.with_effects([vfx.FadeIn(transition_duration), vfx.FadeOut(transition_duration)])
            
            processed_clips.append(clip)
        
        # Concatenate
        final = concatenate_videoclips(processed_clips, method="compose")
        
        output_path = self.output_dir / output_name
        final.write_videofile(
            str(output_path),
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(self.output_dir / 'temp-audio.m4a'),
            remove_temp=True,
            logger=None
        )
        
        # Cleanup
        for clip in clips:
            clip.close()
        final.close()
        
        print(f"✅ Videos concatenated: {output_path}")
        return str(output_path)
    
    def add_fade_transition(
        self,
        video_path: str,
        fade_in: float = 1.0,
        fade_out: float = 1.0
    ) -> str:
        """
        Add fade in/out transitions
        
        Args:
            video_path: Path to input video
            fade_in: Fade in duration in seconds
            fade_out: Fade out duration in seconds
        
        Returns:
            Path to video with fades
        """
        print(f"✨ Adding fade transitions...")
        
        clip = VideoFileClip(video_path)
        
        effects = []
        if fade_in > 0:
            effects.append(vfx.FadeIn(fade_in))
        if fade_out > 0:
            effects.append(vfx.FadeOut(fade_out))
        
        if effects:
            clip = clip.with_effects(effects)
        
        output_path = self.output_dir / f"{Path(video_path).stem}_faded.mp4"
        clip.write_videofile(
            str(output_path),
            codec='libx264',
            audio_codec='aac',
            logger=None
        )
        clip.close()
        
        print(f"✅ Fades added: {output_path}")
        return str(output_path)
    
    def get_video_info(self, video_path: str) -> dict:
        """Get video metadata"""
        clip = VideoFileClip(video_path)
        info = {
            'duration': clip.duration,
            'fps': clip.fps,
            'size': clip.size,
            'width': clip.w,
            'height': clip.h,
            'has_audio': clip.audio is not None
        }
        clip.close()
        return info
