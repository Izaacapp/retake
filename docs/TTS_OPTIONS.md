# TTS Options for Retake Project

## Current Situation

Fish Speech (openaudio-s1-mini) requires:
1. Visit: https://huggingface.co/fishaudio/openaudio-s1-mini
2. Click "Request Access"  
3. Wait for approval
4. Then download models

## Alternative Options

### Option 1: Wait for Fish Speech Access ⭐ (Recommended)
- **Best quality** voice cloning
- Requires HuggingFace approval (~instant to few hours)
- Steps in `docs/FISH_SPEECH_SETUP.md`

### Option 2: Use System TTS (Quick Testing)
- Mac built-in `say` command
- No voice cloning
- Good for testing workflow

### Option 3: Coqui TTS (Open Source)
```bash
uv pip install TTS
# Use pre-trained voice cloning models
```

### Option 4: Skip TTS, Use Original Audio
- Extract Izaac & Ken's original audio segments
- Clean them up with noise reduction
- No voice cloning needed
- Faster to implement

## Recommendation

**For now**: Use Option 4 (original audio) to continue workflow
- Already have clean voice samples
- Can test full video pipeline
- Switch to Fish Speech TTS later when access approved

**Next**: While waiting for Fish Speech access:
1. Continue with screen recording
2. Extract and clean original audio segments
3. Build final video compositor
4. Later: regenerate with Fish Speech when ready

## Quick Test Without TTS

```bash
# Use original audio segments instead of TTS
python scripts/use_original_audio.py
```
