"""
Fish Speech TTS integration wrapper
"""
import subprocess
import json
from pathlib import Path


class FishSpeechTTS:
    """Wrapper for Fish Speech TTS"""
    
    def __init__(self, fish_speech_dir: str = "fish-speech"):
        self.fish_speech_dir = Path(fish_speech_dir)
        self.python_path = self.fish_speech_dir / ".venv/bin/python"
        self.output_dir = Path("output/tts_generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.python_path.exists():
            raise RuntimeError(f"Fish Speech not found at {self.fish_speech_dir}")
        
        print(f"🐟 Fish Speech TTS initialized")
        print(f"   Python: {self.python_path}")
    
    def generate_speech(
        self,
        text: str,
        reference_audio: str,
        output_path: str,
        reference_text: str = None
    ) -> str:
        """
        Generate speech using Fish Speech
        
        Args:
            text: Text to synthesize
            reference_audio: Path to reference voice sample
            output_path: Output audio file path
            reference_text: Optional transcript of reference audio
        
        Returns:
            Path to generated audio
        """
        print(f"🗣️ Generating speech: {text[:50]}...")
        
        # Fish Speech CLI command
        cmd = [
            str(self.python_path),
            "-m", "tools.vqgan.inference",
            "--text", text,
            "--reference-audio", reference_audio,
            "--output", output_path
        ]
        
        if reference_text:
            cmd.extend(["--reference-text", reference_text])
        
        try:
            # Run Fish Speech inference
            result = subprocess.run(
                cmd,
                cwd=str(self.fish_speech_dir),
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f"✅ Generated: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generating speech: {e.stderr}")
            raise
    
    def batch_generate(
        self,
        segments: list,
        reference_audio: str,
        prefix: str = "segment"
    ) -> list:
        """
        Generate speech for multiple segments
        
        Args:
            segments: List of text segments
            reference_audio: Reference voice sample
            prefix: Output filename prefix
        
        Returns:
            List of generated audio files
        """
        print(f"🎙️ Batch generating {len(segments)} segments...")
        
        output_files = []
        for i, segment in enumerate(segments):
            text = segment.get('corrected', segment.get('text', ''))
            if not text.strip():
                continue
            
            output_path = self.output_dir / f"{prefix}_{i:03d}.wav"
            
            try:
                self.generate_speech(
                    text=text,
                    reference_audio=reference_audio,
                    output_path=str(output_path)
                )
                output_files.append(str(output_path))
            except Exception as e:
                print(f"⚠️ Skipping segment {i}: {e}")
                continue
        
        print(f"✅ Generated {len(output_files)} audio files")
        return output_files


def test_fish_speech():
    """Test Fish Speech TTS"""
    tts = FishSpeechTTS()
    
    # Load config
    with open('output/tts_scripts/tts_config.json', 'r') as f:
        config = json.load(f)
    
    # Test Izaac's voice
    print("\n🎤 Testing Izaac's voice clone...")
    izaac_config = config['izaac']
    
    test_text = izaac_config['segments'][0]['corrected']
    output = tts.generate_speech(
        text=test_text,
        reference_audio=izaac_config['voice_sample'],
        output_path=str(tts.output_dir / 'test_izaac.wav')
    )
    
    print(f"✅ Test complete: {output}")


if __name__ == "__main__":
    test_fish_speech()
