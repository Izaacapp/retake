# ACTUAL PROJECT STRUCTURE

## What We Have (REALITY)

### ✅ DONE - Voice Models
```
models/
├── aaron_voice_embedding.npy    89KB
├── izaac_voice_embedding.npy    51KB  
├── jared_voice_embedding.npy    26KB
├── jules_voice_embedding.npy    44KB
└── ken_voice_embedding.npy      39KB
```

### ✅ DONE - Source Data
```
data/
├── source/                      # Original recordings
│   ├── GMT20251114-035710_Recording_avo_1280x720.mp4  (MAIN VIDEO)
│   └── GMT20251114-035710_Recording.transcript.vtt
├── voice_samples/               # For voice embeddings  
│   ├── aaron_*.wav
│   ├── jules_*.wav
│   └── jared_*.wav
└── reference/                   # Reference docs
    └── TALKING_POINTS.md
```

### ✅ DONE - Processed Outputs
```
output/
├── corrected_transcript.json    # 184 segments, grammar-fixed
├── izaac_segments.json          # 52 segments  
├── ken_segments.json            # 8 segments
├── audio/
│   ├── GMT20251114-035710_Recording_avo_1280x720_audio.wav
│   └── segments/                # Audio cut by speaker
│       ├── izaac_demo_*.wav     (5 files)
│       └── ken_demo_*.wav       (6 files)
└── video/                       # Video segments cut
    ├── intro.mp4
    ├── izaac_problem.mp4
    └── izaac_demo_start.mp4
```

### ❌ PROBLEM - Scripts Reference OLD Structure
```
scripts/pipeline/
├── analyze_speakers.py          # References output/audio/voice_samples/ (DOESNT EXIST)
├── extract_speaker_audio.py     # References output/audio/voice_samples/ (DOESNT EXIST)  
├── prepare_tts_script.py        # References output/tts_scripts/ (DOESNT EXIST)
└── run_pipeline.py              # References output/audio/voice_samples/ (DOESNT EXIST)
```

## WHAT WE NEED

### Speaker Mapping (for scripts)
- Izaac = "Zoom user" (52 segments)
- Aaron = "Devon Villalona" (88 segments)  
- Ken = "Kenith Philip" (8 segments)
- Jules = "Jhuiwensley Belizaire" (21 segments)
- Jared = "Jared Zayas" (15 segments)

### Scripts that Work
1. `scripts/setup/extract_all_voice_embeddings.sh` ✅ WORKS
2. Everything else ❌ BROKEN (references old paths)

### Next Step
**FIX THE FUCKING SCRIPTS** or DELETE THEM
