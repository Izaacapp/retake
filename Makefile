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
	@echo "Commands:"
	@echo "  make status            - Show project status"
	@echo "  make extract-embeddings - Extract voice embeddings for all speakers"
	@echo ""
	@echo "Scripts:"
	@echo "  make create-scripts    - Create highly professional scripts from transcripts"
	@echo "  make compare           - Compare original vs professional scripts"
	@echo "  make compare-izaac     - Show Izaac's script improvements"
	@echo "  make compare-ken       - Show Ken's script improvements"
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
	@echo "📊 Project Status"
	@echo ""
	@echo "Voice Embeddings:"
	@ls -lh models/*.npy 2>/dev/null || echo "  No models found"
	@echo ""
	@echo "Speakers:"
	@ls -d output/speakers/*/ 2>/dev/null | xargs -n1 basename || echo "  No speakers"

extract-embeddings:
	@./scripts/setup/extract_all_voice_embeddings.sh

generate-tts:
	@echo "🎙️ Generating TTS for 10-minute script..."
	@./scripts/batch_generate_tts_10min.sh cpu

generate-tts-gpu:
	@echo "🎙️ Generating TTS for 10-minute script (GPU)..."
	@./scripts/batch_generate_tts_10min.sh cuda

test:
	@echo "🧪 No tests configured yet"

test-audio:
	@echo "🧪 No audio tests configured yet"

test-video:
	@echo "🧪 No video tests configured yet"

clean:
	@echo "🧹 Cleaning build artifacts and generated outputs..."
	@echo "Cleaning TTS outputs..."
	rm -f output/tts/10min/*.wav
	rm -f output/tts/10min/*.log
	rm -f output/tts/10min/test_*.wav
	@echo "Cleaning speaker audio segments..."
	rm -f output/speakers/*/audio/*.wav
	@echo "Cleaning speaker video segments..."
	rm -f output/speakers/*/video/*.mp4
	@echo "Cleaning concatenated voice samples..."
	rm -f output/speakers/*/voice_samples/*_concat.wav
	@echo "Cleaning Fish Speech temp/cache..."
	rm -f fish-speech/temp/*.wav fish-speech/temp/*.npy
	rm -rf fish-speech/.cache/
	@echo "Cleaning Fish Speech reference samples (keeping merged)..."
	rm -rf fish-speech/references/*/samples/
	rm -f fish-speech/references/*/sample_trimmed*.wav
	@echo "Cleaning test outputs..."
	rm -f test_*.wav
	rm -f *.log
	@echo "Cleaning Python cache..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Build artifacts cleaned!"

clean-models:
	@echo "🧹 Cleaning Fish Speech models (3.4GB)..."
	rm -rf fish-speech/checkpoints/
	@echo "Cleaning Windows binaries (164MB)..."
	rm -f fish-speech/ffmpeg.exe fish-speech/ffprobe.exe fish-speech/asr-label-win-x64.exe
	@echo "✅ Models cleaned! (~3.6GB reclaimed)"

clean-all: clean
	@echo "🧹 Deep cleaning everything..."
	rm -rf .venv/
	rm -rf fish-speech/.venv/
	rm -rf fish-speech/checkpoints/
	rm -f fish-speech/ffmpeg.exe fish-speech/ffprobe.exe fish-speech/asr-label-win-x64.exe
	@echo "Cleaning all generated TTS..."
	rm -f output/tts/**/*.wav
	@echo "Cleaning all Fish Speech references..."
	rm -rf fish-speech/references/
	@echo "✅ Everything cleaned! (~5GB reclaimed)"

# Quick shortcuts
all: status
	@echo "✅ Use 'make extract-embeddings' to generate voice models"

# Create highly professional scripts
create-scripts:
	@echo "📝 Creating highly professional scripts..."
	@$(PYTHON) scripts/create_highly_professional_rewrites.py
	@echo "✅ Professional transcript created: output/original/professional_transcript.json"

# Create 10-minute organized script
create-10min:
	@echo "📝 Creating 10-minute professional script..."
	@$(PYTHON) scripts/create_10min_speaker_scripts.py
	@echo "✅ 10-minute script created: output/scripts/10min/"
	@echo ""
	@echo "📁 Files created:"
	@ls -lh output/scripts/10min/

# Compare original vs professional
compare:
	@$(PYTHON) scripts/show_improvements.py all 5

compare-izaac:
	@$(PYTHON) scripts/show_improvements.py izaac 10

compare-ken:
	@$(PYTHON) scripts/show_improvements.py ken 10

compare-aaron:
	@$(PYTHON) scripts/show_improvements.py aaron 10

compare-all:
	@$(PYTHON) scripts/show_improvements.py all 20


generate-tts-gpu:
	@echo "🎙️ Generating TTS for 10-minute script (GPU)..."
	@./scripts/batch_generate_tts_10min.sh cuda
