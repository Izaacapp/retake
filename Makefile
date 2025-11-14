# Retake Video Project - Quick Commands

.PHONY: help setup status clean test

# Python executables
PYTHON := .venv/bin/python
FISH_PYTHON := fish-speech/.venv/bin/python

help:
	@echo "🎬 Retake Video Project"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Initial setup (create venv, install deps)"
	@echo "  make fish-setup     - Setup Fish Speech TTS"
	@echo ""
	@echo "Pipeline:"
	@echo "  make status         - Check pipeline status"
	@echo "  make extract-audio  - Extract audio from source video"
	@echo "  make process-text   - Process transcript with grammar fixes"
	@echo "  make analyze        - Analyze speakers"
	@echo "  make voice-samples  - Extract voice samples"
	@echo "  make tts-prep       - Prepare TTS scripts"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all tests"
	@echo "  make test-audio     - Test audio extraction"
	@echo "  make test-video     - Test video cutting"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Clean output directory"
	@echo "  make clean-all      - Clean everything (outputs + venvs)"

setup:
	@echo "📦 Setting up Python 3.14 environment..."
	uv venv --python 3.14
	uv pip install moviepy ffmpeg-python torch torchaudio numpy scipy soundfile pillow tqdm pyyaml imageio imageio-ffmpeg
	@echo "✅ Setup complete! Activate with: source .venv/bin/activate"

fish-setup:
	@echo "🐟 Setting up Fish Speech..."
	./scripts/setup_fish_speech.sh

status:
	@$(PYTHON) scripts/run_pipeline.py

extract-audio:
	@$(PYTHON) scripts/test_extract.py

process-text:
	@$(PYTHON) scripts/test_transcript.py

analyze:
	@$(PYTHON) scripts/analyze_speakers.py

voice-samples:
	@$(PYTHON) scripts/extract_speaker_audio.py

tts-prep:
	@$(PYTHON) scripts/prepare_tts_script.py

test:
	@echo "🧪 Running tests..."
	@$(PYTHON) scripts/test_extract.py
	@$(PYTHON) scripts/test_video_cut.py
	@echo "✅ All tests passed!"

test-audio:
	@$(PYTHON) scripts/test_extract.py

test-video:
	@$(PYTHON) scripts/test_video_cut.py

clean:
	@echo "🧹 Cleaning output directory..."
	rm -rf output/audio/*.wav
	rm -rf output/video/*.mp4
	rm -rf output/tts_scripts/*.txt
	@echo "✅ Output cleaned!"

clean-all: clean
	@echo "🧹 Cleaning environments..."
	rm -rf .venv/
	rm -rf fish-speech/.venv/
	@echo "✅ Everything cleaned!"

# Quick shortcuts
all: extract-audio process-text analyze voice-samples tts-prep
	@echo "✅ All preprocessing complete!"
