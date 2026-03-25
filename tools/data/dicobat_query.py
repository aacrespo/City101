#!/usr/bin/env python3
"""
Dicobat RAG Query Interface
============================
Retrieves relevant Dicobat construction terminology entries using semantic search.
Designed to be imported by other tools (e.g., the modeler workflow) or used standalone.

Usage (standalone):
  # Simple query
  python tools/data/dicobat_query.py "fondation semelle filante"

  # Query with more results
  python tools/data/dicobat_query.py "béton armé dalle" --top-k 10

  # Filter by theme
  python tools/data/dicobat_query.py "charpente assemblage" --theme charpente

  # Show full context (include source file content)
  python tools/data/dicobat_query.py "isolation thermique" --full

Usage (as module):
  from tools.data.dicobat_query import DicobatRAG

  rag = DicobatRAG()
  results = rag.query("fondation semelle filante", top_k=5)
  context = rag.query_for_context("plancher béton", top_k=3)
  # context is a formatted string ready to inject into a prompt

Dependencies:
  pip install sentence-transformers qdrant-client
"""

import argparse
import sys
from pathlib import Path

try:
    from qdrant_client import QdrantClient, models
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install sentence-transformers qdrant-client")
    sys.exit(1)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VECTORDB_DIR = PROJECT_ROOT / "vectordb" / "qdrant"
SOURCE_DIR = PROJECT_ROOT / "source" / "dicobat"
COLLECTION_NAME = "dicobat"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
VECTOR_DIM = 384


class DicobatRAG:
    """Dicobat RAG query interface. Lazy-loads model and DB on first query."""

    def __init__(self, vectordb_dir=None, model_name=None):
        self._vectordb_dir = vectordb_dir or VECTORDB_DIR
        self._model_name = model_name or MODEL_NAME
        self._model = None
        self._client = None

    def _ensure_loaded(self):
        if self._model is None:
            self._model = SentenceTransformer(self._model_name)
        if self._client is None:
            self._client = QdrantClient(path=str(self._vectordb_dir))

    def query(self, text, top_k=5, theme=None, chunk_type=None):
        """
        Semantic search against the Dicobat embeddings.

        Args:
            text: Search query (French or English)
            top_k: Number of results to return
            theme: Optional theme filter (e.g., "sols-infrastructures")
            chunk_type: Optional chunk type filter ("definition", "specs", "translations", etc.)

        Returns:
            List of dicts with keys: text, metadata, distance
        """
        self._ensure_loaded()

        query_embedding = self._model.encode([text]).tolist()[0]

        # Build Qdrant filter
        conditions = []
        if theme:
            conditions.append(
                models.FieldCondition(key="theme", match=models.MatchValue(value=theme))
            )
        if chunk_type:
            conditions.append(
                models.FieldCondition(key="chunk_type", match=models.MatchValue(value=chunk_type))
            )

        query_filter = None
        if conditions:
            query_filter = models.Filter(must=conditions)

        results = self._client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
        )

        output = []
        for point in results.points:
            payload = point.payload or {}
            output.append({
                "text": payload.get("document", ""),
                "metadata": {k: v for k, v in payload.items() if k != "document"},
                "distance": point.score,
            })

        return output

    def query_for_context(self, text, top_k=5, theme=None, include_source=False):
        """
        Query and format results as a context string for prompt injection.

        Returns a formatted string like:
        <dicobat-context>
        ## Term: fondation (Sols-infrastructures)
        [definition text...]

        ## Term: semelle filante (Sols-infrastructures)
        [definition text...]
        </dicobat-context>
        """
        results = self.query(text, top_k=top_k, theme=theme)

        if not results:
            return "<dicobat-context>\nNo matching terms found.\n</dicobat-context>"

        sections = []
        seen_terms = set()

        for r in results:
            meta = r["metadata"]
            term = meta.get("term", "unknown")
            theme_name = meta.get("theme", "")
            chunk_type = meta.get("chunk_type", "")

            # Deduplicate by term (keep first = most relevant)
            term_key = f"{term}_{chunk_type}"
            if term_key in seen_terms:
                continue
            seen_terms.add(term_key)

            header = f"## {term}"
            if theme_name:
                header += f" ({theme_name})"
            if chunk_type and chunk_type != "summary":
                header += f" [{chunk_type}]"

            section = f"{header}\n{r['text']}"

            # Optionally include full source file
            if include_source:
                source_file = PROJECT_ROOT / meta.get("file", "")
                if source_file.exists():
                    section += f"\n\n--- Full entry: {meta['file']} ---\n"
                    section += source_file.read_text(encoding="utf-8")

            sections.append(section)

        context = "\n\n".join(sections)
        return f"<dicobat-context>\n{context}\n</dicobat-context>"

    def list_themes(self):
        """List all themes in the database."""
        self._ensure_loaded()
        # Scroll through all points to get unique themes
        themes = set()
        offset = None
        while True:
            result = self._client.scroll(
                collection_name=COLLECTION_NAME,
                limit=1000,
                offset=offset,
                with_payload=["theme"],
            )
            points, next_offset = result
            for p in points:
                theme = (p.payload or {}).get("theme")
                if theme:
                    themes.add(theme)
            if next_offset is None:
                break
            offset = next_offset
        return sorted(themes)

    @property
    def count(self):
        """Number of chunks in the database."""
        self._ensure_loaded()
        return self._client.count(collection_name=COLLECTION_NAME).count


# --- CLI ---


def main():
    parser = argparse.ArgumentParser(description="Dicobat RAG Query")
    parser.add_argument("query", nargs="?", help="Search query (French or English)")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--theme", type=str, default=None, help="Filter by theme slug")
    parser.add_argument("--full", action="store_true", help="Show full source file content")
    parser.add_argument("--context", action="store_true", help="Output as prompt context block")
    parser.add_argument("--themes", action="store_true", help="List available themes")
    parser.add_argument("--stats", action="store_true", help="Show database stats")

    args = parser.parse_args()

    if not VECTORDB_DIR.exists():
        print("No vector database found. Build embeddings first:")
        print("  python tools/data/dicobat_embeddings.py build")
        sys.exit(1)

    rag = DicobatRAG()

    if args.themes:
        themes = rag.list_themes()
        print(f"Available themes ({len(themes)}):")
        for t in themes:
            print(f"  - {t}")
        return

    if args.stats:
        print(f"Database: {VECTORDB_DIR}")
        print(f"Chunks:   {rag.count}")
        themes = rag.list_themes()
        print(f"Themes:   {len(themes)}")
        return

    if not args.query:
        parser.print_help()
        return

    if args.context:
        ctx = rag.query_for_context(args.query, top_k=args.top_k, theme=args.theme, include_source=args.full)
        print(ctx)
    else:
        results = rag.query(args.query, top_k=args.top_k, theme=args.theme)
        print(f"\nResults for: \"{args.query}\"")
        print(f"{'='*60}\n")

        for i, r in enumerate(results):
            meta = r["metadata"]
            print(f"[{i+1}] {meta.get('term', '?')} — {meta.get('theme', '?')} ({meta.get('chunk_type', '?')})")
            print(f"    Score: {r['distance']:.4f}")
            print(f"    File: {meta.get('file', '?')}")
            print(f"    ---")
            # Show first 200 chars of text
            preview = r["text"][:200].replace("\n", " ")
            print(f"    {preview}...")
            print()

            if args.full:
                source_file = PROJECT_ROOT / meta.get("file", "")
                if source_file.exists():
                    print(f"    --- Full source ---")
                    print(source_file.read_text(encoding="utf-8"))
                    print()


if __name__ == "__main__":
    main()
