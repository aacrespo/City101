# Re-embed 2,204 Lost Entries — Overnight Recovery

**Context:** ChromaDB → Qdrant migration (2026-03-25) recovered 35,520 of 37,724 entries. 2,204 entries were lost to ChromaDB corruption and need re-embedding from source files.

**IMPORTANT — COST AWARENESS:**
- Dicobat and construction_knowledge use LOCAL models (sentence-transformers). Zero cost. Run freely.
- Vision_construction uses GEMINI API (gemini-embedding-2-preview). This costs real money (~$0.65 per 2,500 pages). Do NOT re-embed vision entries without confirming the API key works and budget is acceptable.
- The GOOGLE_API_KEY env var must be set for vision embedding.

---

## Step 1 — Assess what's missing

Run stats on all three collections to see current counts:

```bash
cd ~/CLAUDE/archibase
python3 tools/dicobat_embeddings.py stats
python3 tools/vision_embedder.py stats
```

Compare against the MANIFEST.md expected totals and original ChromaDB counts. The export files in `vectordb/export/` contain the recovered data — the gap between original ChromaDB totals and current Qdrant counts is what needs re-embedding.

**Expected original totals** (from before corruption):
- dicobat: 8,634 terms → should produce ~32,000+ chunks (4 chunk types per term)
- construction_knowledge: ~3,000+ entries
- vision_construction: ~2,100+ entries (470 Deplazes + 1,016 Vittone + YouTube frames)

---

## Step 2 — Re-embed dicobat (FREE, ~70 seconds)

```bash
cd ~/CLAUDE/archibase
python3 tools/dicobat_embeddings.py build
```

This rebuilds from the extracted markdown files in `source/dicobat/`. Local sentence-transformers model, no API cost. The tool upserts, so existing entries won't be duplicated — only missing ones get added.

After completion, run `stats` again and confirm the count increased.

---

## Step 3 — Re-embed construction_knowledge (FREE, ~5 min)

```bash
cd ~/CLAUDE/archibase
python3 tools/pdf_to_rag.py bloomsbury
python3 tools/rag_source_fetchers.py embed
```

Same local model. Rebuilds from Bloomsbury PDFs, SIA norms, Designing Buildings Wiki, Alexander patterns. Upserts only.

---

## Step 4 — Re-embed vision_construction (COSTS MONEY — ~$0.65)

**Before running:**
1. Confirm GOOGLE_API_KEY is set: `echo $GOOGLE_API_KEY | head -c 10`
2. Confirm you're OK spending ~$0.65 on Gemini Embedding API

```bash
cd ~/CLAUDE/archibase

# Re-embed Deplazes pages (source PDF must exist)
python3 tools/vision_embedder.py file "source/deplazes.pdf" --source "deplazes"

# Re-embed Vittone pages
python3 tools/vision_embedder.py file "source/vittone.pdf" --source "vittone"
```

The tool renders each PDF page as an image and sends it to Gemini for multimodal embedding. Rate-limited internally. Takes ~15-30 min depending on page count.

**YouTube video frames:** The YouTube embedding pipeline (`youtube_embedder.py`) is now unblocked but has NOT been run yet. This is a separate task — do NOT include it in this recovery run. It would add new entries, not recover lost ones.

---

## Step 5 — Verify

```bash
cd ~/CLAUDE/archibase
python3 tools/dicobat_embeddings.py stats
python3 tools/vision_embedder.py stats
```

All three collections should now exceed or match the pre-corruption totals. Update `vectordb/MANIFEST.md` with the new counts.

---

## Step 6 — Commit

```bash
cd ~/CLAUDE/archibase
git add vectordb/MANIFEST.md
git commit -m "[DATA] Re-embed 2,204 entries lost during ChromaDB migration"
```

---

## Summary of costs

| Step | Collection | Model | Cost | Time |
|------|-----------|-------|------|------|
| 2 | dicobat | sentence-transformers (local) | FREE | ~70s |
| 3 | construction_knowledge | sentence-transformers (local) | FREE | ~5 min |
| 4 | vision_construction | gemini-embedding-2-preview (API) | ~$0.65 | ~15-30 min |
| **Total** | | | **~$0.65** | **~40 min** |

Run steps 2-3 freely. Only run step 4 if budget is confirmed.
