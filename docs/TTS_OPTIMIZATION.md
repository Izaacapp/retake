# TTS Performance Optimization

## Current Performance
- **3 seconds of audio** took ~30-40 seconds on Mac CPU
- **Estimated time for full project**: 
  - Izaac: 5 segments × 31.8s = ~5-10 minutes
  - Ken: 6 segments × 77.6s = ~10-15 minutes
  - **Total: 15-25 minutes on CPU**

## Optimization Options

### 1. GPU Acceleration (Fastest - 10-100x speedup)
```bash
# On VPS with CUDA GPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Run with GPU
python fish_speech/models/dac/inference.py --device cuda
```
**Speed**: 3 seconds → 0.3 seconds (10x faster)

### 2. Batch Processing (2-3x speedup)
Process multiple segments in parallel:
```bash
# Process 4 segments simultaneously
parallel -j 4 python generate_segment.py ::: segment1 segment2 segment3 segment4
```

### 3. Use Compiled Models (1.5-2x speedup)
```bash
# Add --compile flag (requires Linux/compatible system)
python fish_speech/models/text2semantic/inference.py --compile
```

### 4. Lower Sample Rate (2x speedup, slight quality loss)
```bash
# Use 22050 Hz instead of 44100 Hz
--sample-rate 22050
```

### 5. Skip TTS Entirely (INSTANT)
**Use original audio segments** (already extracted):
- `output/audio/segments/izaac_demo_*.wav`
- Already clean, just needs sync with video
- No compute needed!

## Recommended Approach

### Option A: VPS with GPU (Best Quality + Speed)
**Cost**: $0.50-2.00/hour on RunPod, Vast.ai, Lambda Labs
**Time**: 2-3 minutes total
**Quality**: Perfect

### Option B: Use Original Audio (Free + Instant)
**Cost**: $0
**Time**: 0 seconds
**Quality**: Good (original recording)

### Option C: Mac CPU Overnight
**Cost**: $0
**Time**: 15-25 minutes
**Quality**: Perfect

## VPS Setup Script

```bash
# Quick VPS setup (RunPod, Vast.ai, etc.)
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech
pip install -e .[cu121]  # CUDA 12.1

# Copy your data
scp -r output/audio/voice_samples/ vps:~/
scp -r output/tts_scripts/ vps:~/

# Run batch generation (with GPU)
python batch_generate.py --device cuda

# Download results
scp vps:~/output/tts_generated/*.wav ./output/
```

## My Recommendation

**For now**: Use **original audio segments** (Option B)
- Already extracted and ready
- Perfect quality
- Continue with video workflow

**Later**: If you want perfect TTS:
- Spin up GPU VPS for 30 minutes
- Generate all TTS in 2-3 minutes
- Cost: ~$1

## Time Comparison

| Method | Time | Cost |
|--------|------|------|
| Mac CPU | 15-25 min | $0 |
| Mac CPU Parallel | 5-8 min | $0 |
| GPU VPS | 2-3 min | $0.50-1 |
| Original Audio | 0 sec | $0 |

