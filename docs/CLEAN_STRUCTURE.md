# ✅ Clean Project Structure

## 📁 Directory Organization

```
retake/                           # Root project directory
│
├── data/                         # 📦 SOURCE DATA (never modified)
│   ├── source/                   # Original recordings
│   │   └── GMT20251114-035710_Recording_avo_1280x720.mp4
│   └── reference/                # Reference docs
│       └── TALKING_POINTS.md
│
├── output/                       # 🎯 GENERATED FILES (can regenerate)
│   ├── audio/                    # Extracted & processed audio
│   ├── video/                    # Cut video segments  
│   ├── tts_scripts/              # TTS generation config
│   ├── segments/                 # Processed segments
│   └── final/                    # Final output
│
├── scripts/                      # 🔧 EXECUTABLE SCRIPTS
│   ├── run_pipeline.py           # Main pipeline
│   ├── analyze_speakers.py       # Speaker analysis
│   ├── extract_speaker_audio.py  # Voice sample extraction
│   ├── prepare_tts_script.py     # TTS prep
│   └── test_*.py                 # Test scripts
│
├── utils/                        # 📚 REUSABLE MODULES
│   ├── audio/                    # AudioExtractor, AudioProcessor
│   ├── video/                    # VideoEditor, VideoCompositor
│   ├── voice_clone/              # FishSpeechTTS wrapper
│   └── text/                     # GrammarCorrector
│
├── fish-speech/                  # 🐟 FISH SPEECH (external)
│   └── .venv/                    # Python 3.12 env
│
├── .venv/                        # 🐍 MAIN ENV (Python 3.14)
├── main.py                       # 🎬 Main orchestrator
├── Makefile                      # ⚡ Quick commands
└── pyproject.toml                # 📦 Dependencies

```

## 🎯 Key Principles

### ✅ Clean Separation
- **Source**: `data/` - never touched
- **Generated**: `output/` - can delete anytime  
- **Code**: `utils/` - reusable modules
- **Workflows**: `scripts/` - one-off tasks

### ✅ Clean Imports
```python
from utils.audio import AudioExtractor      # ✅ Good
from utils.video import VideoEditor         # ✅ Good  
from extract_audio import *                 # ❌ Bad
```

### ✅ Clean Commands
```bash
make status           # Check pipeline
make extract-audio    # Extract audio
make analyze          # Analyze speakers
make clean            # Clean outputs
```

## 📊 Current Status

✅ Audio extracted (270MB)
✅ Transcript processed (184 segments)
✅ Speakers analyzed (Izaac: 52, Ken: 8)
✅ Voice samples ready (2.52MB + 1.96MB)
✅ TTS scripts prepared
✅ Video segments cut (intro, demos)

## 🚀 Next Steps

1. Download Fish Speech models
2. Generate TTS audio
3. Record new screen captures
4. Composite final video
