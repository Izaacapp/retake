# TTS Generation Workflow Fix

## Issues Identified

### 1. Wrong Reference Audio Format
**Problem**: The generated bash script was trying to use `.npy` voice embedding files as reference audio for the Fish Speech API client.

**Root Cause**: The `generate_tts_10min.py` script was incorrectly passing `models/{speaker}_voice_embedding.npy` files to the API client, but the Fish Speech `api_client.py` expects actual audio files (WAV, MP3, FLAC, M4A).

**Fix**: Updated the script to use actual audio files:
- Izaac, Ken: Use original Zoom recordings from `data/source/`
- Jules, Aaron, Jared: Use extracted voice samples from `output/speakers/*/voice_samples/`

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

### scripts/generate_tts_10min.py
```python
# Added speaker-to-audio mapping
speaker_audio_map = {
    'Izaac': 'data/source/GMT20251114-035710_Recording.m4a',
    'Ken': 'data/source/GMT20251114-025308_Recording.m4a',
    'Jules': 'output/speakers/jules/voice_samples/jules_000.wav',
    'Aaron': 'output/speakers/aaron/voice_samples/aaron_000.wav',
    'Jared': 'output/speakers/jared/voice_samples/jared_000.wav',
}

# Updated manifest to use reference_audio instead of voice_model
# Updated bash script to use --reference_audio with actual audio files
# Changed --play False to --no-play (correct argparse syntax)
```

### .github/workflows/generate-tts-10min.yml
```yaml
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
# 1. Regenerate the TTS scripts
python scripts/generate_tts_10min.py

# 2. Start Fish Speech server
cd fish-speech && python tools/api_server.py --device cpu

# 3. In another terminal, run the generation
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
4. ✅ Generate TTS preparation files with correct audio references
5. ✅ Start API server and verify it's running
6. ✅ Generate TTS audio using actual audio files as reference
7. ✅ Upload generated WAV files as artifacts
8. ✅ Show proper logs if anything fails

## Voice Reference Files Used

| Speaker | Reference Audio File |
|---------|---------------------|
| Izaac   | `data/source/GMT20251114-035710_Recording.m4a` |
| Ken     | `data/source/GMT20251114-025308_Recording.m4a` |
| Jules   | `output/speakers/jules/voice_samples/jules_000.wav` |
| Aaron   | `output/speakers/aaron/voice_samples/aaron_000.wav` |
| Jared   | `output/speakers/jared/voice_samples/jared_000.wav` |

Note: The original Zoom recordings are used for Izaac and Ken since they don't have extracted voice samples yet.
