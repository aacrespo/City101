"""
Bridge to standalone archibase repo (construction knowledge system).
Import this instead of directly referencing the external repo.

Usage:
    from tools.data.knowledge_bridge import ConstructionDB, KNOWLEDGE_ROOT

    db = ConstructionDB()
    mat = db.get_material('earth_rammed')

    # Read Layer 2 markdown
    guideline = (KNOWLEDGE_ROOT / "source/knowledge/materials/rammed_earth.md").read_text()
"""

import sys
from pathlib import Path

# Path to standalone archibase repo
KNOWLEDGE_ROOT = Path.home() / "CLAUDE" / "archibase"

if not KNOWLEDGE_ROOT.exists():
    raise FileNotFoundError(
        f"Construction knowledge repo not found at {KNOWLEDGE_ROOT}. "
        "Clone or create it first."
    )

# Add to Python path for imports
if str(KNOWLEDGE_ROOT) not in sys.path:
    sys.path.insert(0, str(KNOWLEDGE_ROOT))

# Re-export the main classes
from tools.knowledge_db import ConstructionDB, DB_PATH
from tools.dicobat_query import DicobatRAG

__all__ = ["ConstructionDB", "DicobatRAG", "KNOWLEDGE_ROOT", "DB_PATH"]
