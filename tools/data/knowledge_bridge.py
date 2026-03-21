"""
Bridge to standalone archibase repo (construction knowledge system).
Import this instead of directly referencing the external repo.

Set ARCHIBASE_PATH env var to override the default location.
Default: ~/CLAUDE/archibase

Usage:
    from tools.data.knowledge_bridge import ConstructionDB, KNOWLEDGE_ROOT

    db = ConstructionDB()
    mat = db.get_material('earth_rammed')

    # Read Layer 2 markdown
    guideline = (KNOWLEDGE_ROOT / "source/knowledge/materials/rammed_earth.md").read_text()
"""

import os
import sys
from pathlib import Path

# Path to standalone archibase repo — override with ARCHIBASE_PATH env var
KNOWLEDGE_ROOT = Path(os.environ.get("ARCHIBASE_PATH", Path.home() / "CLAUDE" / "archibase"))

if not KNOWLEDGE_ROOT.exists():
    raise FileNotFoundError(
        f"Archibase not found at {KNOWLEDGE_ROOT}. "
        "Either copy it there or set ARCHIBASE_PATH to its location."
    )

# Add to Python path for imports
if str(KNOWLEDGE_ROOT) not in sys.path:
    sys.path.insert(0, str(KNOWLEDGE_ROOT))

# Re-export the main classes
from tools.knowledge_db import ConstructionDB, DB_PATH
from tools.dicobat_query import DicobatRAG

__all__ = ["ConstructionDB", "DicobatRAG", "KNOWLEDGE_ROOT", "DB_PATH"]
