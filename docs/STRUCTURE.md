# FINAL ORGANIZED STRUCTURE

## By Speaker/Model

```
output/
├── original/                                    # Source files
│   ├── GMT20251114-035710_Recording_avo_1280x720_audio.wav
│   └── corrected_transcript.json (184 segments, all speakers)
│
└── speakers/                                    # Each speaker gets their own folder
    │
    ├── izaac/                                   # MODEL 1 - IZAAC (YOU)
    │   ├── izaac_voice_embedding.npy            # Voice model
    │   ├── audio/                               # His audio segments
    │   │   ├── izaac_demo_000.wav
    │   │   ├── izaac_demo_001.wav
    │   │   ├── izaac_demo_002.wav
    │   │   ├── izaac_demo_003.wav
    │   │   └── izaac_demo_004.wav
    │   ├── video/                               # His video segments
    │   │   ├── izaac_demo_start.mp4
    │   │   └── izaac_problem.mp4
    │   ├── transcripts/                         # His transcript
    │   │   └── izaac_segments.json (52 segments)
    │   └── voice_samples/                       # Empty (were in data/)
    │
    ├── ken/                                     # MODEL 2 - KEN
    │   ├── ken_voice_embedding.npy
    │   ├── audio/
    │   │   ├── ken_demo_000.wav
    │   │   ├── ken_demo_001.wav
    │   │   ├── ken_demo_002.wav
    │   │   ├── ken_demo_003.wav
    │   │   ├── ken_demo_004.wav
    │   │   └── ken_demo_005.wav
    │   ├── video/                               # Empty
    │   ├── transcripts/
    │   │   └── ken_segments.json (8 segments)
    │   └── voice_samples/                       # Empty
    │
    ├── aaron/                                   # MODEL 3 - AARON
    │   ├── aaron_voice_embedding.npy
    │   ├── audio/                               # Empty (no segments cut yet)
    │   ├── video/                               # Empty
    │   ├── transcripts/                         # Empty (not extracted yet)
    │   └── voice_samples/
    │       ├── aaron_000.wav
    │       ├── aaron_001.wav
    │       ├── aaron_002.wav
    │       ├── aaron_003.wav
    │       ├── aaron_004.wav
    │       └── aaron_concat.wav
    │
    ├── jules/                                   # MODEL 4 - JULES
    │   ├── jules_voice_embedding.npy
    │   ├── audio/                               # Empty
    │   ├── video/                               # Empty
    │   ├── transcripts/                         # Empty
    │   └── voice_samples/
    │       ├── jules_000.wav → jules_004.wav
    │       └── jules_concat.wav
    │
    └── jared/                                   # MODEL 5 - JARED
        ├── jared_voice_embedding.npy
        ├── audio/                               # Empty
        ├── video/                               # Empty
        ├── transcripts/                         # Empty
        └── voice_samples/
            ├── jared_000.wav → jared_004.wav
            └── jared_concat.wav
```

## Summary

✅ **Each speaker has:**
- Their voice embedding model (`.npy`)
- Their audio segments (if cut)
- Their video segments (if cut)
- Their transcript (if extracted)
- Their voice samples (for training)

✅ **Original files at root:**
- `output/original/` - Full audio + full transcript

✅ **Models also in root:**
- `models/` - All 5 voice embeddings (for easy access)
