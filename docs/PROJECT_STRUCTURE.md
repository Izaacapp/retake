# Retake Project Structure

```
retake/
├── data/                          # Source data (gitignored)
│   ├── source/                    # Original recordings
│   │   ├── GMT20251114-035710_Recording_avo_1280x720.mp4  # Main video (23.44 min)
│   │   ├── GMT20251114-035710_Recording.transcript.vtt     # Transcript
│   │   └── ...                    # Other recordings
│   └── reference/                 # Reference materials
│       └── TALKING_POINTS.md      # Original talking points
│
├── output/                        # Generated outputs (gitignored)
│   ├── audio/                     # Audio processing
│   │   ├── voice_samples/         # Speaker voice samples for TTS
│   │   └── *.wav                  # Extracted audio
│   ├── video/                     # Video segments
│   │   ├── intro.mp4
│   │   ├── izaac_*.mp4
│   │   └── ken_*.mp4
│   ├── tts_scripts/               # TTS generation scripts
│   │   ├── tts_config.json
│   │   ├── izaac_demo.txt
│   │   └── ken_demo.txt
│   ├── segments/                  # Processed segments
│   ├── final/                     # Final output videos
│   ├── corrected_transcript.json  # Grammar-corrected transcript
│   ├── izaac_segments.json        # Izaac's segments
│   └── ken_segments.json          # Ken's segments
│
├── scripts/                       # Workflow scripts
│   ├── analyze_speakers.py        # Analyze transcript speakers
│   ├── extract_speaker_audio.py   # Extract voice samples
│   ├── prepare_tts_script.py      # Prepare TTS scripts
│   ├── test_extract.py            # Test audio extraction
│   ├── test_cut_segments.py       # Test video cutting
│   └── test_transcript.py         # Test transcript processing
│
├── utils/                         # Core utilities (importable modules)
│   ├── audio/                     # Audio processing
│   │   ├── extractor.py           # AudioExtractor class
│   │   ├── separator.py           # SpeakerSeparator class
│   │   └── processor.py           # AudioProcessor class
│   ├── video/                     # Video processing
│   │   ├── editor.py              # VideoEditor class
│   │   ├── compositor.py          # VideoCompositor class
│   │   └── recorder.py            # ScreenRecorder class
│   ├── voice_clone/               # Voice cloning
│   │   ├── cloner.py              # VoiceCloner class
│   │   └── fish_speech_wrapper.py # Fish Speech integration
│   ├── text/                      # Text processing
│   │   ├── grammar.py             # GrammarCorrector class
│   │   └── script.py              # ScriptProcessor class
│   └── transitions/               # Video transitions
│
├── fish-speech/                   # Fish Speech TTS (separate repo)
│   └── .venv/                     # Python 3.12 environment
│
├── tools/                         # Helper tools
│   └── (future utilities)
│
├── docs/                          # Documentation
│   └── (project docs)
│
├── .venv/                         # Main Python 3.14 environment
├── main.py                        # Main pipeline orchestrator
├── pyproject.toml                 # UV/Python project config
├── STATUS.md                      # Current status tracker
├── PROJECT_STRUCTURE.md           # This file
├── TALKING_POINTS.md              # Presentation talking points
└── run.sh                         # Quick runner script

```

## Key Principles

### 1. Separation of Concerns
- **data/**: Source files (never modified)
- **output/**: Generated files (can be regenerated)
- **scripts/**: Workflow automation (executable)
- **utils/**: Reusable modules (importable)

### 2. Clean Imports
```python
# Good - clean module imports
from utils.audio import AudioExtractor
from utils.video import VideoEditor
from utils.voice_clone import FishSpeechTTS

# Bad - polluting namespace
from audio_extractor import *
```

### 3. Output Organization
- All generated files go to `output/`
- Subdirectories by type: audio, video, tts_scripts, etc.
- Easy to clean: `rm -rf output/*`
- Easy to backup: `tar -czf backup.tar.gz output/`

### 4. Environment Separation
- **Main project**: Python 3.14 (`.venv/`)
- **Fish Speech**: Python 3.12 (`fish-speech/.venv/`)
- Use UV for fast dependency management

## Quick Commands

```bash
# Activate main environment
source .venv/bin/activate

# Run a script
./run.sh scripts/analyze_speakers.py

# Clean outputs
rm -rf output/*

# Full rebuild
rm -rf output/ && python main.py
```

## File Paths Reference

### Source Files
- Main video: `data/source/GMT20251114-035710_Recording_avo_1280x720.mp4`
- Transcript: `data/source/GMT20251114-035710_Recording.transcript.vtt`

### Voice Samples
- Izaac: `output/audio/voice_samples/izaac_voice_sample.wav`
- Ken: `output/audio/voice_samples/ken_voice_sample.wav`

### Segments
- Izaac: `output/izaac_segments.json`
- Ken: `output/ken_segments.json`
- Full transcript: `output/corrected_transcript.json`

### TTS Config
- Config: `output/tts_scripts/tts_config.json`
- Scripts: `output/tts_scripts/{izaac,ken}_demo.txt`
