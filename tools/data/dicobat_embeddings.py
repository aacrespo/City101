#!/usr/bin/env python3
"""
Dicobat Embeddings Pipeline
============================
Chunks extracted Dicobat markdown files and generates embeddings
using a multilingual sentence-transformer model, stored in ChromaDB.

Usage:
  # Build embeddings from all extracted terms
  python tools/data/dicobat_embeddings.py build

  # Rebuild a specific theme
  python tools/data/dicobat_embeddings.py build --theme sols-infrastructures

  # Show stats
  python tools/data/dicobat_embeddings.py stats

Dependencies:
  pip install sentence-transformers chromadb
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install sentence-transformers chromadb")
    sys.exit(1)


# --- Configuration ---

# Knowledge lives in standalone construction-knowledge repo
KNOWLEDGE_ROOT = Path.home() / "CLAUDE" / "construction-knowledge"
PROJECT_ROOT = KNOWLEDGE_ROOT if KNOWLEDGE_ROOT.exists() else Path(__file__).resolve().parents[2]
SOURCE_DIR = PROJECT_ROOT / "source" / "dicobat"
VECTORDB_DIR = PROJECT_ROOT / "vectordb"
COLLECTION_NAME = "dicobat"

# Multilingual model — handles French well
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


# --- Chunking ---


def parse_frontmatter(text):
    """Extract YAML-like frontmatter from markdown."""
    metadata = {}
    match = re.match(r"^#\s+(.+)\n\n---\n(.+?)\n---", text, re.DOTALL)
    if match:
        metadata["title"] = match.group(1).strip()
        for line in match.group(2).strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                metadata[key.strip()] = val.strip()
    return metadata


def chunk_term_markdown(filepath):
    """Split a term markdown file into semantic chunks for embedding.

    Returns list of dicts: {text, metadata, chunk_type}
    """
    text = filepath.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)

    term_name = metadata.get("title", filepath.stem)
    theme = metadata.get("theme", filepath.parent.name)
    subcategory = metadata.get("subcategory", "")
    term_id = metadata.get("id", "")
    source_url = metadata.get("source", "")

    base_meta = {
        "term": term_name,
        "term_id": term_id,
        "theme": theme,
        "subcategory": subcategory,
        "source_url": source_url,
        "file": str(filepath.relative_to(PROJECT_ROOT)),
    }

    chunks = []

    # Split by ## sections
    sections = re.split(r"\n## ", text)

    for section in sections:
        if not section.strip():
            continue

        # Determine section type
        first_line = section.split("\n")[0].strip()
        section_body = "\n".join(section.split("\n")[1:]).strip()

        if first_line.startswith("#"):
            # This is the title / frontmatter section
            # Create a summary chunk with the title + metadata
            chunk_text = f"{term_name}: {subcategory} ({theme})"
            if section_body:
                # Add first paragraph if present
                first_para = section_body.split("\n\n")[0][:500]
                chunk_text += f"\n{first_para}"
            chunks.append({
                "text": chunk_text,
                "metadata": {**base_meta, "chunk_type": "summary"},
                "chunk_type": "summary",
            })
            continue

        section_type = "definition"  # default
        if "Translation" in first_line or "Traduction" in first_line:
            section_type = "translations"
        elif "Technical" in first_line or "Specification" in first_line:
            section_type = "specs"
        elif "Related" in first_line or "Voir aussi" in first_line:
            section_type = "cross_references"
        elif "Classification" in first_line:
            section_type = "classification"

        if not section_body:
            continue

        # For long sections, split into sub-chunks (~500 chars each)
        if len(section_body) > 800:
            paragraphs = section_body.split("\n\n")
            current_chunk = []
            current_len = 0

            for para in paragraphs:
                if current_len + len(para) > 600 and current_chunk:
                    chunk_text = f"{term_name} — {first_line}\n\n" + "\n\n".join(current_chunk)
                    chunks.append({
                        "text": chunk_text,
                        "metadata": {**base_meta, "chunk_type": section_type},
                        "chunk_type": section_type,
                    })
                    current_chunk = []
                    current_len = 0

                current_chunk.append(para)
                current_len += len(para)

            if current_chunk:
                chunk_text = f"{term_name} — {first_line}\n\n" + "\n\n".join(current_chunk)
                chunks.append({
                    "text": chunk_text,
                    "metadata": {**base_meta, "chunk_type": section_type},
                    "chunk_type": section_type,
                })
        else:
            chunk_text = f"{term_name} — {first_line}\n\n{section_body}"
            chunks.append({
                "text": chunk_text,
                "metadata": {**base_meta, "chunk_type": section_type},
                "chunk_type": section_type,
            })

    return chunks


# --- Embedding pipeline ---


def build_embeddings(theme_filter=None):
    """Process all extracted terms and store embeddings in ChromaDB."""
    if not SOURCE_DIR.exists():
        print(f"ERROR: No extracted terms found at {SOURCE_DIR}")
        print("Run the scraper first: python tools/data/dicobat_scraper.py extract")
        sys.exit(1)

    # Find all markdown files
    if theme_filter:
        md_files = sorted(SOURCE_DIR.glob(f"{theme_filter}/*.md"))
    else:
        md_files = sorted(SOURCE_DIR.rglob("*.md"))

    if not md_files:
        print("No markdown files found to process.")
        return

    print(f"\n{'='*60}")
    print("DICOBAT EMBEDDING PIPELINE")
    print(f"{'='*60}\n")
    print(f"Source:    {SOURCE_DIR}")
    print(f"Files:     {len(md_files)}")
    print(f"Model:     {MODEL_NAME}")
    print(f"VectorDB:  {VECTORDB_DIR}")
    print()

    # Load model
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print("Model loaded.\n")

    # Initialize ChromaDB
    VECTORDB_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTORDB_DIR))

    # Delete existing collection if rebuilding
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Dicobat construction dictionary embeddings"},
    )

    # Process files
    all_chunks = []
    for i, filepath in enumerate(md_files):
        chunks = chunk_term_markdown(filepath)
        all_chunks.extend(chunks)
        if (i + 1) % 100 == 0:
            print(f"  Chunked {i+1}/{len(md_files)} files ({len(all_chunks)} chunks)")

    print(f"\nTotal chunks: {len(all_chunks)}")

    if not all_chunks:
        print("No chunks generated.")
        return

    # Generate embeddings in batches
    batch_size = 64
    total_batches = (len(all_chunks) + batch_size - 1) // batch_size

    print(f"Generating embeddings ({total_batches} batches)...")
    start_time = time.time()

    for batch_idx in range(0, len(all_chunks), batch_size):
        batch = all_chunks[batch_idx:batch_idx + batch_size]
        texts = [c["text"] for c in batch]
        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        ids = [f"chunk_{batch_idx + j}" for j in range(len(batch))]
        metadatas = [c["metadata"] for c in batch]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

        batch_num = batch_idx // batch_size + 1
        if batch_num % 10 == 0 or batch_num == total_batches:
            elapsed = time.time() - start_time
            print(f"  Batch {batch_num}/{total_batches} ({elapsed:.1f}s)")

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print("EMBEDDING COMPLETE")
    print(f"{'='*60}")
    print(f"Files processed: {len(md_files)}")
    print(f"Chunks embedded: {len(all_chunks)}")
    print(f"Time:            {elapsed:.1f}s")
    print(f"VectorDB:        {VECTORDB_DIR}")

    # Save stats
    stats = {
        "files_processed": len(md_files),
        "chunks_embedded": len(all_chunks),
        "model": MODEL_NAME,
        "build_time_s": round(elapsed, 1),
        "build_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "chunk_types": {},
    }
    for c in all_chunks:
        ct = c["chunk_type"]
        stats["chunk_types"][ct] = stats["chunk_types"].get(ct, 0) + 1

    stats_file = VECTORDB_DIR / "build_stats.json"
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"Stats:           {stats_file}")
    print()


def show_stats():
    """Show current embedding database stats."""
    stats_file = VECTORDB_DIR / "build_stats.json"
    if stats_file.exists():
        with open(stats_file) as f:
            stats = json.load(f)
        print("Dicobat Embedding Stats:")
        for k, v in stats.items():
            if k == "chunk_types":
                print(f"  Chunk types:")
                for ct, count in v.items():
                    print(f"    {ct}: {count}")
            else:
                print(f"  {k}: {v}")
    else:
        print("No embeddings built yet.")
        print("Run: python tools/data/dicobat_embeddings.py build")

    # Also check ChromaDB if it exists
    if VECTORDB_DIR.exists():
        try:
            client = chromadb.PersistentClient(path=str(VECTORDB_DIR))
            collection = client.get_collection(COLLECTION_NAME)
            print(f"\n  ChromaDB collection: {collection.count()} entries")
        except Exception:
            pass


# --- CLI ---


def main():
    parser = argparse.ArgumentParser(description="Dicobat Embeddings Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    build_parser = subparsers.add_parser("build", help="Build embeddings from extracted terms")
    build_parser.add_argument("--theme", type=str, default=None, help="Only process this theme slug")

    subparsers.add_parser("stats", help="Show embedding stats")

    args = parser.parse_args()

    if args.command == "build":
        build_embeddings(theme_filter=args.theme)
    elif args.command == "stats":
        show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
