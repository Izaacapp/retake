#!/usr/bin/env python3
"""
Batch TTS generation with voice cloning
Optimized for parallel processing and quality
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

class TTSBatchGenerator:
    """Batch TTS generation with voice cloning"""
    
    def __init__(self, device: str = "cpu", parallel_jobs: int = 4):
        self.device = device
        self.parallel_jobs = parallel_jobs
        self.fish_dir = Path(__file__).parent.parent / "fish-speech"
        self.output_dir = Path(__file__).parent.parent / "output/tts_generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🐟 TTS Batch Generator")
        print(f"   Device: {device}")
        print(f"   Parallel jobs: {parallel_jobs}")
        print(f"   Output: {self.output_dir}\n")
    
    def extract_vq_tokens(self, reference_audio: str, speaker_name: str) -> str:
        """Extract VQ tokens from reference audio (Step 1)"""
        
        checkpoint = self.fish_dir / "checkpoints/openaudio-s1-mini/codec.pth"
        output_path = self.output_dir / f"{speaker_name}_ref.wav"
        
        print(f"📍 Extracting VQ tokens for {speaker_name}...")
        
        cmd = [
            str(self.fish_dir / ".venv/bin/python"),
            str(self.fish_dir / "fish_speech/models/dac/inference.py"),
            "-i", str(reference_audio),
            "--checkpoint-path", str(checkpoint),
            "-o", str(output_path),
            "--device", self.device
        ]
        
        result = subprocess.run(cmd, cwd=str(self.fish_dir), capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error extracting VQ tokens: {result.stderr}")
            raise RuntimeError("VQ extraction failed")
        
        print(f"✅ VQ tokens extracted: {output_path}.npy\n")
        return str(output_path.with_suffix('.npy'))
    
    def generate_semantic_tokens(
        self,
        text: str,
        prompt_text: str,
        prompt_tokens: str,
        segment_id: int
    ) -> str:
        """Generate semantic tokens from text (Step 2)"""
        
        cmd = [
            str(self.fish_dir / ".venv/bin/python"),
            str(self.fish_dir / "fish_speech/models/text2semantic/inference.py"),
            "--text", text,
            "--prompt-text", prompt_text,
            "--prompt-tokens", prompt_tokens,
            "--device", self.device
        ]
        
        result = subprocess.run(
            cmd,
            cwd=str(self.fish_dir / "temp"),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"⚠️  Segment {segment_id} failed: {result.stderr}")
            return None
        
        # Find the generated codes file
        codes_file = self.fish_dir / "temp" / "codes_0.npy"
        if codes_file.exists():
            return str(codes_file)
        
        return None
    
    def generate_audio_from_codes(
        self,
        codes_path: str,
        output_name: str
    ) -> str:
        """Generate final audio from semantic codes (Step 3)"""
        
        checkpoint = self.fish_dir / "checkpoints/openaudio-s1-mini/codec.pth"
        output_path = self.output_dir / output_name
        
        cmd = [
            str(self.fish_dir / ".venv/bin/python"),
            str(self.fish_dir / "fish_speech/models/dac/inference.py"),
            "-i", codes_path,
            "--checkpoint-path", str(checkpoint),
            "--device", self.device,
            "-o", str(output_path)
        ]
        
        result = subprocess.run(cmd, cwd=str(self.fish_dir), capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"⚠️  Audio generation failed: {result.stderr}")
            return None
        
        return str(output_path)
    
    def process_segment(self, segment_data: Dict) -> Dict:
        """Process a single segment through full TTS pipeline"""
        
        segment_id = segment_data['id']
        text = segment_data['text']
        speaker = segment_data['speaker']
        prompt_tokens = segment_data['prompt_tokens']
        prompt_text = segment_data['prompt_text']
        
        start_time = time.time()
        
        print(f"🎙️  [{segment_id}] Processing: {text[:50]}...")
        
        try:
            # Step 2: Generate semantic tokens
            codes_path = self.generate_semantic_tokens(
                text=text,
                prompt_text=prompt_text,
                prompt_tokens=prompt_tokens,
                segment_id=segment_id
            )
            
            if not codes_path:
                return {'id': segment_id, 'status': 'failed', 'error': 'semantic generation failed'}
            
            # Step 3: Generate audio
            output_name = f"{speaker}_seg_{segment_id:03d}.wav"
            audio_path = self.generate_audio_from_codes(codes_path, output_name)
            
            if not audio_path:
                return {'id': segment_id, 'status': 'failed', 'error': 'audio generation failed'}
            
            elapsed = time.time() - start_time
            print(f"✅ [{segment_id}] Complete in {elapsed:.1f}s → {output_name}\n")
            
            return {
                'id': segment_id,
                'status': 'success',
                'path': audio_path,
                'time': elapsed
            }
            
        except Exception as e:
            print(f"❌ [{segment_id}] Error: {e}\n")
            return {'id': segment_id, 'status': 'error', 'error': str(e)}
    
    def batch_generate(
        self,
        speaker: str,
        num_segments: int = None
    ) -> List[Dict]:
        """Generate TTS for multiple segments"""
        
        # Load TTS config
        config_file = Path("output/tts_scripts/tts_config.json")
        with open(config_file) as f:
            config = json.load(f)
        
        speaker_config = config.get(speaker)
        if not speaker_config:
            raise ValueError(f"Speaker '{speaker}' not found in config")
        
        # Step 1: Extract VQ tokens once
        vq_tokens = self.extract_vq_tokens(
            speaker_config['voice_sample'],
            speaker
        )
        
        # Prepare segments
        segments = speaker_config['segments']
        if num_segments:
            segments = segments[:num_segments]
        
        # Get reference text (first segment)
        prompt_text = segments[0]['original'] if segments else ""
        
        # Prepare segment data
        segment_tasks = []
        for i, seg in enumerate(segments):
            segment_tasks.append({
                'id': i,
                'text': seg['corrected'],
                'speaker': speaker,
                'prompt_tokens': vq_tokens,
                'prompt_text': prompt_text
            })
        
        print(f"🚀 Generating {len(segment_tasks)} segments for {speaker}...\n")
        
        # Process segments (sequential for now, parallel later)
        results = []
        for task in segment_tasks:
            result = self.process_segment(task)
            results.append(result)
        
        # Summary
        successful = sum(1 for r in results if r['status'] == 'success')
        total_time = sum(r.get('time', 0) for r in results if r['status'] == 'success')
        
        print("\n" + "="*70)
        print(f"✅ Batch complete: {successful}/{len(results)} segments generated")
        print(f"⏱️  Total time: {total_time:.1f}s (avg: {total_time/max(successful,1):.1f}s/segment)")
        print("="*70)
        
        return results


def main():
    parser = argparse.ArgumentParser(description="Batch TTS generation")
    parser.add_argument('--speaker', required=True, choices=['izaac', 'ken', 'all'])
    parser.add_argument('--segments', default='1', help='Number of segments or "all"')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'])
    parser.add_argument('--parallel', type=int, default=1, help='Parallel jobs')
    
    args = parser.parse_args()
    
    num_segments = None if args.segments == 'all' else int(args.segments)
    
    generator = TTSBatchGenerator(device=args.device, parallel_jobs=args.parallel)
    
    speakers = ['izaac', 'ken'] if args.speaker == 'all' else [args.speaker]
    
    for speaker in speakers:
        print(f"\n{'='*70}")
        print(f"Processing speaker: {speaker.upper()}")
        print('='*70 + "\n")
        
        results = generator.batch_generate(speaker, num_segments)
        
        # Save results
        results_file = Path(f"output/tts_generated/{speaker}_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved: {results_file}\n")


if __name__ == "__main__":
    main()
