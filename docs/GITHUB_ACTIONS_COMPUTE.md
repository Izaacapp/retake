# GitHub Actions Free Compute Strategy

## Free Resources Available

### GitHub Actions Free Tier
- **2,000 minutes/month** for private repos
- **Unlimited** for public repos
- **20 concurrent jobs**
- **6-core CPU** per job
- **14GB RAM** per job

## TTS Generation Strategy

### Current Setup
✅ GitHub Actions workflow: `.github/workflows/generate-tts.yml`
✅ Batch generator: `scripts/batch_generate_tts.py`

### How to Use

1. **Add HuggingFace token to GitHub Secrets**
   ```bash
   # Go to: https://github.com/Izaacapp/retake/settings/secrets/actions
   # Add secret: HF_TOKEN = your_huggingface_token
   ```

2. **Trigger workflow manually**
   ```bash
   # Go to: https://github.com/Izaacapp/retake/actions
   # Click: Generate TTS with GPU
   # Select: speaker (izaac/ken/all)
   # Select: segments (1/5/10/all)
   # Click: Run workflow
   ```

3. **Download generated audio**
   ```bash
   # After workflow completes:
   # Download artifacts from Actions page
   # Or use GitHub CLI:
   gh run download
   ```

## Performance Estimates

### GitHub Actions (CPU)
- **Izaac**: 5 segments × ~40s = 3-4 minutes
- **Ken**: 6 segments × ~40s = 4-5 minutes
- **Total**: ~8 minutes (well within free tier)

### Future: Self-Hosted Runner with GPU
```yaml
# Add to workflow for 10-100x speedup
runs-on: self-hosted-gpu
```

## Voice Model Extraction

### Strategy
1. **Extract voice embeddings** (one-time, local)
2. **Store embeddings** in repo (small files)
3. **Generate TTS** using embeddings (GitHub Actions)

### Implementation
```python
# Extract voice model (run locally once)
python scripts/extract_voice_model.py \
  --speaker izaac \
  --reference output/audio/voice_samples/izaac_voice_sample.wav \
  --output models/izaac_voice_embedding.npy

# Commit models to repo
git add models/*.npy
git commit -m "Add voice embeddings"

# GitHub Actions uses embeddings (no need to upload audio)
```

## Optimizations for GitHub Actions

### 1. Cache Dependencies
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### 2. Parallel Processing
```yaml
strategy:
  matrix:
    speaker: [izaac, ken]
jobs:
  generate:
    runs-on: ubuntu-latest
    # Runs both speakers in parallel
```

### 3. Artifact Storage
- Generated audio → GitHub Artifacts (7 days retention)
- Final outputs → GitHub Releases (permanent)

## Cost Comparison

| Method | Time | Cost | Complexity |
|--------|------|------|------------|
| Mac CPU | 15-25 min | $0 | Low |
| GitHub Actions | 8-10 min | $0 | Medium |
| GPU VPS | 2-3 min | $0.50-1 | Low |
| Self-hosted GPU | 1-2 min | $0 | High |

## Next Steps

1. ✅ Push workflow to GitHub
2. ⬜ Add HF_TOKEN secret
3. ⬜ Test workflow with 1 segment
4. ⬜ Run full batch
5. ⬜ Download and integrate audio

## Advanced: Go Parallel Processing

For local development with Go:

```go
// parallel_tts.go
package main

import (
    "sync"
    "os/exec"
)

func generateSegment(segment Segment, wg *sync.WaitGroup) {
    defer wg.Done()
    cmd := exec.Command("python", "generate_tts.py", segment.ID)
    cmd.Run()
}

func main() {
    var wg sync.WaitGroup
    for _, seg := range segments {
        wg.Add(1)
        go generateSegment(seg, &wg)
    }
    wg.Wait()
}
```

**Performance**: 4-6x faster than sequential Python
