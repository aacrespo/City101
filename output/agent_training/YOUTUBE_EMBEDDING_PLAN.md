# YouTube Rhino Tutorial Embedding — Implementation Plan

## Overview

Embed Rhino modeling tutorial keyframes into the same ChromaDB `vision_construction` collection used for PDF pages. Agents query once, get both construction details (from books) AND modeling procedures (from tutorials).

## Pipeline

```
YouTube URL → yt-dlp (720p) → ffmpeg (1 frame/10s) → [optional: Gemini Flash describe] → Gemini Embedding 2 → ChromaDB
```

## Tool: `archibase/tools/youtube_embedder.py`

```bash
python tools/youtube_embedder.py video "https://youtube.com/watch?v=..." --source "howtorhino"
python tools/youtube_embedder.py batch "tools/video_urls.txt"
python tools/youtube_embedder.py search "timber wall section modeling"
```

### Dependencies
- `brew install ffmpeg yt-dlp`
- `pip install Pillow` (google-genai, chromadb already installed)

### Frame extraction
- Default: 1 frame every 10 seconds (configurable)
- Skip first 15s (intro) and last 10s (outro)
- JPEG quality 85, 1280x720
- 15-min video = ~90 frames

### Metadata per frame
```python
{
    "source": "yt_{channel_slug}",
    "type": "video_frame",
    "video_id": "...",
    "video_title": "...",
    "channel": "...",
    "timestamp_s": 120,
    "timestamp_fmt": "2:00",
    "video_url": "https://...",
    "description": "...",  # optional, from Gemini Flash
}
```

## Recommended initial batch (10 videos)

| # | Topic | Target channels |
|---|-------|-----------------|
| 1 | Wall section modeling (layer buildup) | How to Rhino, TheEveryArchitect |
| 2 | Floor slab detail with structural connection | How to Rhino |
| 3 | Roof assembly (pitched, eaves/overhang) | Architecture Inspirations |
| 4 | Window/door opening with frame + lintel | TheEveryArchitect |
| 5 | Foundation-to-wall connection | Construction-focused channel |
| 6 | Timber frame wall assembly | ParametricCamp |
| 7 | Boolean operations for openings | Simply Rhino |
| 8 | Multi-layer wall with proper thickness | PJ Architecture |
| 9 | Stair modeling (stringers, treads, railings) | How to Rhino |
| 10 | Flat roof parapet detail | Architecture Inspirations |

### Channels
- **Tier 1** (construction detail): How to Rhino, TheEveryArchitect, ParametricCamp, Architecture Inspirations
- **Tier 2** (Rhino fundamentals): Simply Rhino, PJ Architecture, Rhinoceros3d official
- **Tier 3** (European context): DETAIL magazine, ETH/EPFL channels

## Cost estimate (10 videos, ~150 min)

| Item | Count | Cost (paid) |
|------|-------|-------------|
| Frames (10s interval, minus intro/outro) | ~870 | ~$0.22 |
| Optional Gemini Flash descriptions | 870 calls | ~$0.08 |
| **Total** | | **~$0.30** (free during preview) |

## Integration

Same `vision_embedder.py search` command — unified collection. Add `--type video_frame` filter for video-only search.

Agent workflow: PDF pages = WHAT to build (dimensions, layers). Video frames = HOW to build it (Rhino operations).

## Implementation steps

1. Install ffmpeg + yt-dlp (~5 min)
2. Build youtube_embedder.py (~45 min)
3. Add --type filter to vision_embedder.py search (~5 min)
4. Curate 10 video URLs (~30 min, needs human review)
5. Run batch embedding (~20 min runtime)
6. Update archibase docs (~10 min)
