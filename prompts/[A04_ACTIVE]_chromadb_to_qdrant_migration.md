# ChromaDB → Qdrant Migration

## Resume from

This continues the session saved at `state/sessions/2026-03-22_1838.md`. That session:
- Built the vision embedder + embedded 2,480 PDF pages (Deplazes + Vittone) via Gemini
- Hit ChromaDB segfault on large collections (>2000 entries + 3072-dim vectors)
- Recovered the 2,480 entries but couldn't proceed with SIA + Bloomsbury embedding
- The resume line was: *"Migrate ChromaDB → Qdrant (recover 2,480 entries without re-embedding). Then embed SIA + Bloomsbury + Dicobat. Then resume YouTube embedding."*

Three days later this is still the blocker. Migration was marked ON HOLD in the LOCKBOARD but the decision to migrate was already made.

## Context

The archibase knowledge system (Layer 4 — RAG) currently uses ChromaDB to store 35K+ embedding chunks across multiple collections. ChromaDB has had intermittent segfaults (Abort trap: 6) that crash Claude Code sessions. Even if stable now, Qdrant is the better long-term choice — better performance, proper client-server architecture, and no in-process crashes.

This migration unblocks the embedding pipeline: YouTube tutorials, remaining PDFs, and any future sources.

## Scope

**What moves:** Everything in `$ARCHIBASE_PATH/vectordb/` (ChromaDB data) → Qdrant.

**What changes:** 6 Python files in archibase that import/use chromadb, plus 2 copies in city101.

### Files to migrate (archibase)

| File | Role | ChromaDB usage |
|------|------|----------------|
| `tools/dicobat_embeddings.py` | Build pipeline — chunks Dicobat markdown, generates embeddings, stores in ChromaDB | `chromadb.PersistentClient`, collection CRUD, `add()` |
| `tools/dicobat_query.py` | Query interface — `DicobatRAG` class used by knowledge_bridge | `chromadb.PersistentClient`, `collection.query()` |
| `tools/pdf_to_rag.py` | PDF extraction → embeddings → ChromaDB | `chromadb.PersistentClient`, `add()` |
| `tools/vision_embedder.py` | Gemini vision embedding (image-based PDF pages) | `chromadb.PersistentClient`, `add()` |
| `tools/youtube_embedder.py` | Video frame embedding pipeline | `chromadb.PersistentClient`, `add()` |
| `tools/rag_source_fetchers.py` | bSDD, Wikidata, Designing Buildings Wiki → ChromaDB | `chromadb.PersistentClient`, `add()` |

### Files to update (city101)

| File | Action |
|------|--------|
| `tools/data/dicobat_embeddings.py` | Replace with updated archibase version or symlink |
| `tools/data/dicobat_query.py` | Replace with updated archibase version or symlink |

### Downstream consumers (do not break these)

- `tools/data/knowledge_bridge.py` — imports `DicobatRAG` from `dicobat_query.py`
- Parametric scripts and agent workflows query through the bridge
- The `DicobatRAG` class interface (`query()`, `query_for_context()`) must stay identical

## Instructions

### Phase 0 — Diagnose current state

```bash
# Check if ChromaDB segfault reproduces
cd $ARCHIBASE_PATH
python3 -c "
import chromadb
client = chromadb.PersistentClient(path='vectordb')
collections = client.list_collections()
print(f'Collections: {len(collections)}')
for c in collections:
    print(f'  {c.name}: {c.count()} chunks')
"
```

Run a query too — the segfault often hits during query, not just load:
```bash
python3 tools/dicobat_query.py "fondation semelle filante" --top-k 3
```

Log the result (works / segfault / other error). Proceed with migration either way.

### Phase 1 — Install Qdrant

Use Qdrant in **local/embedded mode** (no Docker needed) — same simplicity as ChromaDB's PersistentClient.

```bash
pip install qdrant-client
```

Qdrant's local mode stores data on disk at a path you specify, just like ChromaDB. No server process to manage.

### Phase 2 — Export all ChromaDB data

Before touching any code, dump everything to a portable format:

```python
# Export script — save as tools/export_chromadb.py
# For each collection: dump all IDs, embeddings, documents, metadatas to JSON
# This is your backup and migration source
```

Write a self-contained export script. Output: one JSON file per collection in `vectordb/export/`. Include:
- All document texts
- All metadata dicts
- All embedding vectors
- Collection name and count

Verify row counts match `collection.count()` before proceeding.

### Phase 3 — Migrate each tool

For each of the 6 Python files:

1. Replace `import chromadb` with `from qdrant_client import QdrantClient, models`
2. Replace `chromadb.PersistentClient(path=...)` with `QdrantClient(path=...)` (local mode)
3. Replace `client.get_or_create_collection(name=...)` with Qdrant collection creation (specify vector size from the embedding model — likely 384 for `all-MiniLM-L6-v2` or 768 for the multilingual model)
4. Replace `collection.add(ids=, documents=, embeddings=, metadatas=)` with Qdrant `upsert(points=...)`
5. Replace `collection.query(query_embeddings=, n_results=)` with Qdrant `query_points()` or `search()`
6. Replace any `collection.count()` with Qdrant equivalent
7. Keep the same embedding model — don't re-embed, just move the vectors

**Critical: The `DicobatRAG` class public interface must not change.** Same method signatures, same return format. Only internals change.

### Phase 4 — Import data into Qdrant

Write an import script that reads the Phase 2 exports and populates Qdrant collections. Run it. Verify counts match.

### Phase 5 — Verify

```bash
# Same queries, same results
python3 tools/dicobat_query.py "fondation semelle filante" --top-k 3
python3 tools/dicobat_query.py "béton armé dalle" --top-k 5
python3 tools/dicobat_query.py "charpente assemblage" --theme charpente
```

Compare results against ChromaDB output from Phase 0. They should be identical (same embeddings, same distance metric).

### Phase 6 — Update city101

Copy the updated `dicobat_query.py` and `dicobat_embeddings.py` to `city101/tools/data/`. Test the knowledge bridge still works:

```python
from tools.data.knowledge_bridge import DicobatRAG
rag = DicobatRAG()
results = rag.query("fondation semelle filante", top_k=5)
print(results)
```

### Phase 7 — Update docs

- `archibase/CLAUDE.md` — change "ChromaDB" references to "Qdrant"
- `archibase/README.md` — update dependencies and quick start
- `city101/CLAUDE.md` — update archibase description if it mentions ChromaDB
- `city101/LOCKBOARD.md` — mark migration complete
- Update `pip install` lines: `chromadb` → `qdrant-client`

### Phase 8 — Clean up

- Keep `vectordb/export/` as backup until verified in production use
- Old ChromaDB `vectordb/` data can be archived or deleted after confidence period
- Remove `chromadb` from any requirements files

## Success criteria

- [ ] All 6 archibase tools work with Qdrant
- [ ] `DicobatRAG` public API unchanged
- [ ] city101 knowledge_bridge queries return results
- [ ] No segfaults during sustained querying
- [ ] Embedding pipeline unblocked — ready for YouTube + new PDFs
- [ ] All docs updated

## Dependencies

```
pip install qdrant-client
# removes: chromadb (after verification)
# keeps: sentence-transformers, google-genai (for Gemini embeddings)
```

## Estimated token budget

This is a focused infrastructure task. Expect ~1 session. Most time is in Phase 3 (6 files to update) and Phase 5 (verification).
