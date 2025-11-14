"""
Audio processing utilities - noise reduction, normalization, effects
"""
import numpy as np
from pathlib import Path
import soundfile as sf


class AudioProcessor:
    """Process and enhance audio quality"""
    
    def __init__(self, output_dir: str = "output/audio/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def reduce_noise(
        self,
        audio_path: str,
        noise_sample_duration: float = 1.0,
        prop_decrease: float = 1.0
    ) -> str:
        """
        Remove background noise from audio (placeholder)
        
        Args:
            audio_path: Path to input audio
            noise_sample_duration: Duration of noise sample from start (seconds)
            prop_decrease: Proportion of noise to reduce (0-1)
        
        Returns:
            Path to noise-reduced audio
        """
        print(f"🔇 Noise reduction (placeholder)...")
        
        # For now, just copy the file
        audio_data, sample_rate = sf.read(audio_path)
        output_filename = f"{Path(audio_path).stem}_denoised.wav"
        output_path = self.output_dir / output_filename
        sf.write(str(output_path), audio_data, sample_rate)
        
        print(f"✅ Audio copied: {output_path}")
        return str(output_path)
    
    def normalize_audio(self, audio_path: str, target_dBFS: float = -20.0) -> str:
        """
        Normalize audio levels
        
        Args:
            audio_path: Path to input audio
            target_dBFS: Target loudness in dBFS
        
        Returns:
            Path to normalized audio
        """
        print(f"📊 Normalizing audio (simple)...")
        
        audio_data, sample_rate = sf.read(audio_path)
        
        # Simple normalization
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            normalized = audio_data / max_val * 0.8
        else:
            normalized = audio_data
        
        output_filename = f"{Path(audio_path).stem}_normalized.wav"
        output_path = self.output_dir / output_filename
        sf.write(str(output_path), normalized, sample_rate)
        
        print(f"✅ Audio normalized: {output_path}")
        return str(output_path)
    
    def apply_compression(self, audio_path: str, threshold: float = -20.0) -> str:
        """
        Apply dynamic range compression (placeholder)
        
        Args:
            audio_path: Path to input audio
            threshold: Compression threshold in dBFS
        
        Returns:
            Path to compressed audio
        """
        print(f"🎚️ Compression (placeholder)...")
        
        audio_data, sample_rate = sf.read(audio_path)
        
        output_filename = f"{Path(audio_path).stem}_compressed.wav"
        output_path = self.output_dir / output_filename
        sf.write(str(output_path), audio_data, sample_rate)
        
        print(f"✅ Saved: {output_path}")
        return str(output_path)
    
    def enhance_voice(self, audio_path: str) -> str:
        """
        Full voice enhancement pipeline
        
        Args:
            audio_path: Path to input audio
        
        Returns:
            Path to enhanced audio
        """
        print(f"✨ Enhancing voice quality...")
        
        # Step 1: Noise reduction
        denoised = self.reduce_noise(audio_path)
        
        # Step 2: Normalization
        normalized = self.normalize_audio(denoised)
        
        # Step 3: Compression
        compressed = self.apply_compression(normalized)
        
        # Rename to final
        final_path = self.output_dir / f"{Path(audio_path).stem}_enhanced.wav"
        Path(compressed).rename(final_path)
        
        # Clean up intermediate files
        Path(denoised).unlink(missing_ok=True)
        Path(normalized).unlink(missing_ok=True)
        
        print(f"✅ Voice enhanced: {final_path}")
        return str(final_path)
    
    def trim_silence(
        self,
        audio_path: str,
        silence_thresh: int = -40,
        min_silence_len: int = 500
    ) -> str:
        """
        Remove silence from beginning and end (placeholder)
        
        Args:
            audio_path: Path to input audio
            silence_thresh: Silence threshold in dBFS
            min_silence_len: Minimum silence length in ms
        
        Returns:
            Path to trimmed audio
        """
        print(f"✂️ Trim (placeholder)...")
        
        audio_data, sample_rate = sf.read(audio_path)
        
        output_filename = f"{Path(audio_path).stem}_trimmed.wav"
        output_path = self.output_dir / output_filename
        sf.write(str(output_path), audio_data, sample_rate)
        
        print(f"✅ Saved: {output_path}")
        return str(output_path)
