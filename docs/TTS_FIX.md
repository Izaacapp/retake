# TTS Generation Workflow Fix

## Issues Identified

### 1. Wrong Reference Audio Format
**Problem**: The generated bash script was trying to use `.npy` voice embedding files as reference audio for the Fish Speech API client.

**Root Cause**: The `generate_tts_10min.py` script was incorrectly passing `models/{speaker}_voice_embedding.npy` files to the API client, but the Fish Speech `api_client.py` expects actual audio files (WAV, MP3, FLAC, M4A).

**Fix**: Use Fish Speech's **reference_id** system instead:
1. Created `scripts/setup_fish_references.py` to setup reference voices
2. Updated TTS generation to use `--reference_id {speaker}` instead of `--reference_audio`
3. References are pre-loaded into `fish-speech/references/{speaker}/` with audio + text pairs

### 2. API Server Log Path
**Problem**: The workflow was looking for logs at `fish-speech/api_server.log` but the file didn't exist.

**Root Cause**: The log file was being created inside the `fish-speech/` directory, but the workflow was checking from the wrong location.

**Fix**: 
- Changed log path to `../api_server.log` (parent directory)
- Updated workflow to read from `api_server.log` in root
- Added process ID tracking to verify server is running

### 3. Better Error Handling
**Added**:
- Process ID capture for the API server
- Health check to verify server started successfully
- Early exit with log output if server fails to start

## Changes Made

### NEW: scripts/setup_fish_references.py
```python
# Creates Fish Speech reference directories for all speakers
# Structure: fish-speech/references/{speaker}/
#   - sample.{wav|m4a}  (audio file)
#   - sample.lab         (reference text)

speaker_samples = {
    'izaac': 'data/source/GMT20251114-035710_Recording.m4a',
    'ken': 'data/source/GMT20251114-025308_Recording.m4a',
    'jules': 'output/speakers/jules/voice_samples/jules_000.wav',
    'aaron': 'output/speakers/aaron/voice_samples/aaron_000.wav',
    'jared': 'output/speakers/jared/voice_samples/jared_000.wav',
}
```

### scripts/generate_tts_10min.py
```python
# Changed from reference_audio to reference_id
speaker_ref_map = {
    'Izaac': 'izaac',
    'Ken': 'ken',
    'Jules': 'jules',
    'Aaron': 'aaron',
    'Jared': 'jared',
}

# Updated manifest to use reference_id instead of voice_model/reference_audio
# Updated bash script to use --reference_id {speaker}
# Changed --play False to --no-play (correct argparse syntax)
```

### .github/workflows/generate-tts-10min.yml
```yaml
# Added setup step:
- Run scripts/setup_fish_references.py before TTS generation
- Creates reference directories in fish-speech/references/

# Updated API server startup:
- Log to ../api_server.log instead of api_server.log
- Capture process ID with API_PID=$!
- Verify server is running with ps -p check
- Early exit if server fails to start

# Updated log check step:
- Read from api_server.log (root) instead of fish-speech/api_server.log
```

## Testing the Fix

### Local Testing
```bash
# 1. Setup Fish Speech reference voices
python scripts/setup_fish_references.py

# 2. Regenerate the TTS scripts (optional, already done)
python scripts/generate_tts_10min.py

# 3. Start Fish Speech server
cd fish-speech && python tools/api_server.py --device cpu

# 4. In another terminal, run the generation
bash output/tts/10min/generate_with_fish_speech.sh
```

### GitHub Actions Testing
1. Push the changes
2. Go to Actions tab
3. Run "Generate TTS for 10-Minute Script" workflow
4. Check the logs for proper execution

## Expected Behavior

The workflow should now:
1. ✅ Clone Fish Speech successfully
2. ✅ Install dependencies
3. ✅ Download models
4. ✅ Setup reference voices in `fish-speech/references/`
5. ✅ Generate TTS preparation files with reference_id mappings
6. ✅ Start API server and verify it's running
7. ✅ Generate TTS audio using reference_id (pre-loaded voice clones)
8. ✅ Upload generated WAV files as artifacts
9. ✅ Show proper logs if anything fails

## Voice Reference System

Fish Speech uses a **reference_id** system where you upload voice samples to the server:

### Reference Structure
```
fish-speech/references/
├── izaac/
│   ├── sample.m4a       (voice audio)
│   └── sample.lab       (reference text)
├── ken/
│   ├── sample.m4a
│   └── sample.lab
├── jules/
│   ├── sample.wav
│   └── sample.lab
├── aaron/
│   ├── sample.wav
│   └── sample.lab
└── jared/
    ├── sample.wav
    └── sample.lab
```

### Reference Sources

| Speaker | Reference Audio File | Usage |
|---------|---------------------|-------|
| Izaac   | `data/source/GMT20251114-035710_Recording.m4a` | Your voice from Zoom |
| Ken     | `data/source/GMT20251114-025308_Recording.m4a` | Ken's voice from Zoom |
| Jules   | `output/speakers/jules/voice_samples/jules_000.wav` | Extracted sample |
| Aaron   | `output/speakers/aaron/voice_samples/aaron_000.wav` | Extracted sample |
| Jared   | `output/speakers/jared/voice_samples/jared_000.wav` | Extracted sample |

### Why This Works Better

1. **Pre-encoding**: Fish Speech encodes the voice once when loading reference_id
2. **Caching**: Encoded voice embeddings are cached in memory (faster generation)
3. **API efficiency**: Use `--reference_id izaac` instead of passing audio every time
4. **Clean separation**: Voice clones are stored separately from scripts

Note: The `.npy` voice embeddings are NOT directly used by Fish Speech. They are for other TTS systems. Fish Speech creates its own embeddings from the audio files.
