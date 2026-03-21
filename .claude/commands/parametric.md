# Skill: Parametric Script Generator

You generate parametric architecture scripts that produce Rhino geometry, grounded in the construction knowledge system.

## Knowledge system access

Before writing any script, load the knowledge bridge:

```python
import sys
sys.path.insert(0, '/Users/andreacrespo/CLAUDE/archibase')
from tools.knowledge_db import ConstructionDB
```

### Layer 1 — Query for numbers
```python
db = ConstructionDB()
db.get_material('earth_rammed')           # material properties
db.get_load('A1')                         # SIA 261 live loads
db.get_room_dimensions('bedroom_double')  # minimum room sizes
db.get_fire_requirement('habitation', 'medium', 'mur_porteur')  # REI
db.get_spans(material='timber_gl', load_type='residential')     # span tables
db.get_kbob('béton')                      # official Swiss LCA data
db.get_steel_profile('IPE 300')           # section properties
db.get_assembly('wall_timber_frame_ext')  # wall/floor/roof buildups
```

### Layer 2 — Read for guidelines
```
~/CLAUDE/archibase/source/knowledge/
├── materials/           → material behavior, constraints, compatibility
├── construction_systems/ → assembly logic, parametric design principles
├── typologies/          → spatial patterns, program requirements
└── norms_guidelines/    → Swiss codes, Minergie, accessibility, acoustic
```
Read the directory README first, then the specific file you need.

### Layer 4 — Search for deep knowledge
```python
from tools.dicobat_query import DicobatRAG
rag = DicobatRAG()
context = rag.query_for_context("assemblage tenon mortaise", top_k=5)
```

## Script generation workflow

1. **Understand the brief**: what building type, what site, what material strategy
2. **Read Layer 2** guidelines for the relevant materials and construction systems
3. **Query Layer 1** for exact values (spans, loads, dimensions, GWP)
4. **Write the script** following these rules:

### Script rules
- **Constraints are enforced in code**, not commented as suggestions
- **Every dimension has a source** — reference the SIA norm, Layer 1 table, or design decision
- **Query don't hardcode** — import ConstructionDB for material properties, spans, loads
- **Generate metadata** — every Rhino object gets attributes (material, function, assembly type)
- **Fail loudly** — raise errors on constraint violations, don't silently clip values
- **Structure as**: inputs → site logic → massing → structure → envelope → subdivision → output

### Script structure template
```python
"""
[Building type] parametric generator
=====================================
Generates [description] in Rhino via MCP.

Inputs:
  - site_boundary: curve (closed polyline)
  - program: dict of {use: area_m2}
  - material_strategy: str ('timber', 'concrete', 'hybrid', 'earth')

Knowledge sources:
  - L1: materials, spans, loads, fire requirements
  - L2: [relevant guideline files]
  - L4: [relevant RAG queries if used]
"""

import sys
sys.path.insert(0, '/Users/andreacrespo/CLAUDE/archibase')
from tools.knowledge_db import ConstructionDB

db = ConstructionDB()

# === PARAMETERS ===
# Site
# ...

# Program (from brief)
# ...

# Material strategy (from Layer 1 + Layer 2)
# ...

# Structural (from Layer 1 span tables)
# ...

# === SITE LOGIC ===
# ...

# === MASSING ===
# ...

# === STRUCTURE ===
# ...

# === ENVELOPE ===
# ...

# === OUTPUT ===
# Geometry + metadata summary
```

### Rhino/MCP conventions
- Use `mcp__rhino__execute_rhinoscript_python_code` for geometry generation
- Layer naming: `[LOG level]_[element]` (e.g., `200_walls`, `300_columns`)
- LOG levels: 100=massing, 200=envelope, 300=structure, 400=detail
- Coordinates in Rhino model units (meters, origin at site reference point)

## What this skill is NOT
- Not a Grasshopper definition generator (we work in scripted Rhino)
- Not a structural calculator (we use lookup tables, not FEA)
- Not a BIM modeler (we generate design geometry with metadata, not IFC)

## Commit prefix
`[MODEL]`
