# Extract compas_wood Joint Parameters into Reference Tables

## Context

compas_wood is an open-source (MIT) timber joint generation library by Petras Vestartas / IBOIS (EPFL). The joint constraint values — tenon proportions, chamfer offsets, division ranges, interpolation formulas — are embedded across ~6400 lines of C++ geometry code rather than collected in a readable reference.

**Goal:** Read the source and produce structured reference tables that a design tool (or a human) can query without reading C++.

**Repo:** https://github.com/petrasvestartas/compas_wood
**Key file:** The C++ core lives in a submodule (`src/wood/`). Start at `cmake/src/wood/include/wood_joint_lib.cpp`.
**Also check:** `wood_globals.cpp`, `wood_globals.h`, `wood_joint.h`, `wood_joint.cpp`, `wood_cut.h`

## What to extract

### Table 1 — Joint Type Catalog
For each of the 42+ joint types (indices 0-69, 7 categories of 10):

| Field | Description |
|-------|-------------|
| `type_id` | Index (0-69) |
| `category` | Which of the 7 categories (ss_e_ip, ss_e_op, ts_e_p, cr_c_ip, tt_e_p, ss_e_r, b) |
| `name` | Human-readable name (e.g., "Vidy tenon-mortise", "Hilti butterfly") |
| `description` | What the joint does, in one sentence |
| `cut_type` | Fabrication method (edge_insertion, hole, drill, conic, etc.) |
| `source_reference` | If the joint is named after a real project (Vidy Chapel, Brussels Sports Tower), note it |

### Table 2 — Constraint Values per Joint
For each joint type, extract every numeric value that shapes the geometry:

| Field | Description |
|-------|-------------|
| `type_id` | Index |
| `parameter` | Name of the value (chamfer_offset, tenon_width_ratio, etc.) |
| `value` | The number |
| `unit` | mm, ratio, degrees, or unitless |
| `context` | What it controls — one sentence |
| `source_line` | File and approximate line number in the C++ source |

### Table 3 — Global Defaults
From `wood_globals.cpp`:

| Field | Description |
|-------|-------------|
| `parameter` | Name |
| `default_value` | The value |
| `unit` | Unit |
| `what_it_controls` | Plain language |
| `configurable` | Yes/No — can it be changed at runtime from Python? |

### Table 4 — Python API Surface
From the Python bindings, document what's actually controllable without recompiling:

| Field | Description |
|-------|-------------|
| `function` | Python function name |
| `parameter` | Parameter name |
| `type` | Data type |
| `default` | Default value |
| `what_it_controls` | Plain language |

## Output format

### Primary: SQLite tables for archibase (L1)

Add to the archibase SQLite database (or create a new `compas_wood.db` in `output/compas_wood_reference/` if you can't access archibase directly). Tables:

```sql
-- The 42+ joint types
CREATE TABLE timber_joints (
    type_id INTEGER PRIMARY KEY,
    category TEXT,          -- ss_e_ip, ss_e_op, ts_e_p, cr_c_ip, tt_e_p, ss_e_r, b
    name TEXT,              -- human name: "Vidy tenon-mortise"
    description TEXT,       -- one sentence
    cut_type TEXT,          -- fabrication method: edge_insertion, hole, drill, conic
    source_reference TEXT,  -- real project if named after one
    source_file TEXT,       -- C++ file path
    source_line INTEGER     -- approximate line number
);

-- Every numeric constraint per joint
CREATE TABLE joint_constraints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER REFERENCES timber_joints(type_id),
    parameter TEXT,         -- chamfer_offset, tenon_width_ratio, division_min, etc.
    value REAL,
    unit TEXT,              -- mm, ratio, degrees, unitless
    context TEXT,           -- what it controls, plain language
    configurable INTEGER,   -- 1 = changeable from Python, 0 = C++ only
    source_file TEXT,
    source_line INTEGER
);

-- Global defaults from wood_globals.cpp
CREATE TABLE joint_globals (
    parameter TEXT PRIMARY KEY,
    default_value REAL,
    unit TEXT,
    description TEXT,
    configurable INTEGER    -- 1 = runtime, 0 = compile-time
);

-- Python API surface
CREATE TABLE joint_python_api (
    function_name TEXT,
    parameter TEXT,
    data_type TEXT,
    default_value TEXT,
    description TEXT,
    PRIMARY KEY (function_name, parameter)
);
```

This follows archibase L1 patterns — same approach as the KBOB, steel profiles, and SIA loads tables. An agent can query `SELECT * FROM joint_constraints WHERE type_id = 15 AND configurable = 1` the same way it already queries material properties.

### Secondary: Markdown guide for archibase (L2)

Write `output/compas_wood_reference/compas_wood_joint_system.md` — a knowledge guide following the format of existing guides in `$ARCHIBASE_PATH/source/knowledge/`. Should explain the joint system, the 7 categories, how type_id indexing works, and how constraints relate to fabrication. A human should be able to understand the system without opening C++.

### L3: RhinoPython execution scripts

The C++ joint generation functions are execution logic — they take parameters and produce geometry. Translate the most useful joint types into RhinoPython scripts that an agent can call directly in Rhino via MCP.

Write to `output/compas_wood_reference/scripts/`:

**For each of the main joint types (prioritize the ones with real-project references: Vidy, Hilti, Brussels):**

```python
# Example: scripts/joint_tenon_mortise_vidy.py
#
# Generates a Vidy tenon-mortise joint between two timber elements in Rhino.
# Parameters sourced from compas_wood type_id=14 (ss_e_op_4).
#
# Usage: agent calls this with two element GUIDs + optional overrides.
# Constraints from L1 are defaults — agent can query joint_constraints
# table to understand valid ranges before calling.

def create_vidy_tenon_mortise(element_a, element_b,
                               division_length=450,
                               shift=0.64,
                               chamfer_offset=-0.75):
    """
    L1 source: joint_constraints WHERE type_id = 14
    Valid ranges: division_length 100-1000mm, shift 0-1, chamfer_offset -1.0 to 0
    """
    # ... RhinoCommon geometry generation ...
```

**The pattern for each script:**
1. Header documents which L1 table rows it's based on (type_id, parameter names)
2. Function signature exposes all configurable parameters with L1 defaults
3. Docstring states valid ranges from L1
4. Body translates the C++ geometry logic into RhinoCommon calls
5. Returns Rhino GUIDs of created geometry

**Also create an index script** `scripts/joint_index.py` that maps joint names to script files — so an agent can do:
```python
from joint_index import get_joint_script
script = get_joint_script("tenon_mortise_vidy")  # returns path
```

**Priority order** (don't try all 42 — start with the most architecturally relevant):
1. Tenon-mortise variants (Vidy, standard) — most common structural joint
2. Finger joints (in-plane, out-of-plane) — plate construction
3. Cross-cutting joints — beam intersections
4. Butterfly/Hilti — special connections

The L1 ↔ L3 link is the key: the script *reads* L1 to know what's valid, then *executes* in Rhino. If someone later adds new constraint values to L1 (e.g., from Damien's roundwood research), the scripts automatically respect wider or narrower ranges.

### Also: CSV exports for sharing

Export the SQLite tables as CSVs too (`joint_catalog.csv`, `joint_constraints.csv`, `global_defaults.csv`, `python_api.csv`). These are for sharing with IBOIS — Damien isn't going to open a SQLite file, but he'll open a spreadsheet.

## Instructions

### Phase 1: Extract (L1 + L2)
1. Clone the repo (including submodules — the C++ core is a submodule)
2. Read the source files listed above systematically
3. For each joint type, trace the geometry generation function and extract every numeric literal, every ratio, every clamping range
4. Cross-reference with the Python bindings to determine what's runtime-configurable
5. Be precise about line numbers — these tables should be verifiable
6. If a value's purpose is unclear from the code alone, say so — don't guess
7. Write SQLite tables, markdown guide, and CSV exports

### Phase 2: Translate (L3)
8. For the priority joint types (Vidy tenon-mortise, finger joints, cross-cutting, butterfly), translate the C++ geometry generation into RhinoPython
9. Each script must reference its L1 source (type_id, parameter names) in the header
10. Default values in function signatures must match L1 exactly
11. Test that the scripts are syntactically valid Python with RhinoCommon imports (you can't run Rhino, but the code should be correct)
12. Create the index script that maps names to files

### Phase 3: Verify the loop
13. Write a short test scenario in the README: "An agent wants to join two beams with a tenon-mortise. It queries L1 for valid parameters, calls the L3 script with those parameters, geometry appears in Rhino." Walk through exactly which SQL queries and which function calls that involves. This proves the L1 ↔ L3 link works.

## Attribution

MIT license. Credit: "Extracted from compas_wood by Petras Vestartas, IBOIS/EPFL. https://github.com/petrasvestartas/compas_wood"

## Why this matters

This is step one toward making IBOIS's timber construction knowledge agent-readable. If we can turn 6400 lines of procedural C++ into queryable reference tables, that's a proof of concept for doing the same with Manis (assembly constraints), Raccoon (CNC profiles), and eventually the roundwood database. It's also a concrete deliverable we can show Damien after the meeting.
