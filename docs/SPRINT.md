# Sprint: Voice Embeddings Extraction

## Goal
Extract voice embeddings for ALL 5 speakers using GitHub Actions (free compute)

## Speakers
1. **Izaac** (you) - 52 segments ✅ DONE
2. **Ken** - 8 segments ✅ DONE  
3. **Aaron** - 88 segments ❌ NEEDED
4. **Jules** - 21 segments ❌ NEEDED
5. **Jared** - 15 segments ❌ NEEDED

## Current Status

### ✅ Completed
- [x] Extracted audio samples for Aaron, Jules, Jared → `data/audio/voice_samples/`
- [x] Created voice embeddings for ALL 5 speakers → `models/`
  - ✅ Izaac: 51KB
  - ✅ Ken: 39KB  
  - ✅ Aaron: 89KB
  - ✅ Jules: 44KB
  - ✅ Jared: 26KB
- [x] Set up Fish Speech with Python 3.12
- [x] Downloaded models (3.4GB) → `fish-speech/checkpoints/`

### 🔄 In Progress
- [ ] Push voice embeddings to GitHub
- [ ] Create TTS generation GitHub Actions workflow
- [ ] Generate TTS audio using GitHub Actions (free compute)

### 📋 TODO
- [ ] Generate TTS audio for all speakers
- [ ] Overlay audio on video clips
- [ ] Final edit and rendering

## File Organization

```
data/
  audio/
    voice_samples/           # Voice samples extracted from video
      aaron_000.wav
      aaron_001.wav
      aaron_002.wav
      aaron_concat.wav       # Concatenated for embedding
      jules_000.wav
      jules_001.wav
      jules_002.wav  
      jules_concat.wav
      jared_000.wav
      jared_001.wav
      jared_concat.wav

models/
  izaac_voice_embedding.npy  ✅ 51KB
  ken_voice_embedding.npy    ✅ 39KB
  aaron_voice_embedding.npy  ❌ NEEDED
  jules_voice_embedding.npy  ❌ NEEDED
  jared_voice_embedding.npy  ❌ NEEDED

output/
  tts_scripts/               # TTS scripts (professional rewrites)
    PROFESSIONAL_CONTEXT.md
    tts_config.json
  tts_generated/             # Generated TTS audio files
  video/                     # Cut video segments
    intro.mp4
    izaac_problem.mp4
    izaac_demo_start.mp4
```

## GitHub Actions Workflow

**File**: `.github/workflows/extract_voice_embeddings.yml`

**Trigger**: 
- Manual dispatch
- Push to `data/audio/voice_samples/`

**Steps**:
1. Install Python 3.12
2. Setup Fish Speech
3. Download models
4. Run `scripts/extract_all_voice_embeddings.sh`
5. Upload artifacts
6. Commit to repo

## Next Steps

1. **Fix the embedding extraction script** (use correct Fish Speech API)
2. **Push to GitHub**
3. **Trigger GitHub Actions**
4. **Download embeddings** (they'll be committed automatically)
5. **Generate TTS audio** using embeddings
6. **Overlay on video**

## Notes

- Mac CPU is SLOW (30-40s for 3s audio)
- GitHub Actions has free compute
- Embeddings are small (40-50KB each)
- Don't commit large audio files (use LFS or keep in `data/`)
