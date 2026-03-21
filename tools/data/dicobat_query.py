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
  pip install sentence-transformers chromadb
"""

import argparse
import sys
from pathlib import Path

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install sentence-transformers chromadb")
    sys.exit(1)


# Knowledge lives in standalone construction-knowledge repo
KNOWLEDGE_ROOT = Path.home() / "CLAUDE" / "construction-knowledge"
PROJECT_ROOT = KNOWLEDGE_ROOT if KNOWLEDGE_ROOT.exists() else Path(__file__).resolve().parents[2]
VECTORDB_DIR = PROJECT_ROOT / "vectordb"
SOURCE_DIR = PROJECT_ROOT / "source" / "dicobat"
COLLECTION_NAME = "dicobat"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class DicobatRAG:
    """Dicobat RAG query interface. Lazy-loads model and DB on first query."""

    def __init__(self, vectordb_dir=None, model_name=None):
        self._vectordb_dir = vectordb_dir or VECTORDB_DIR
        self._model_name = model_name or MODEL_NAME
        self._model = None
        self._collection = None

    def _ensure_loaded(self):
        if self._model is None:
            self._model = SentenceTransformer(self._model_name)
        if self._collection is None:
            client = chromadb.PersistentClient(path=str(self._vectordb_dir))
            self._collection = client.get_collection(COLLECTION_NAME)

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

        query_embedding = self._model.encode([text]).tolist()

        where_filter = None
        conditions = []
        if theme:
            conditions.append({"theme": {"$eq": theme}})
        if chunk_type:
            conditions.append({"chunk_type": {"$eq": chunk_type}})

        if len(conditions) == 1:
            where_filter = conditions[0]
        elif len(conditions) > 1:
            where_filter = {"$and": conditions}

        results = self._collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
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
        # Get a sample to extract unique themes
        results = self._collection.get(limit=10000, include=["metadatas"])
        themes = set()
        for meta in results["metadatas"]:
            if "theme" in meta:
                themes.add(meta["theme"])
        return sorted(themes)

    @property
    def count(self):
        """Number of chunks in the database."""
        self._ensure_loaded()
        return self._collection.count()


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
            print(f"    Distance: {r['distance']:.4f}")
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
