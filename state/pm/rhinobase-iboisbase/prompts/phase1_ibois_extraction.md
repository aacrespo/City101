# Build iboisbase — IBOIS Timber Construction Knowledge

## Context

IBOIS (Laboratory for Timber Constructions, EPFL) has built a suite of open-source tools for computational timber design, fabrication, and quality control. The construction knowledge in these tools — joint constraints, assembly rules, machine limits, point cloud processing pipelines, quality tolerances — is embedded in code rather than collected as queryable reference.

**Goal:** Systematically extract knowledge from every accessible IBOIS tool into **iboisbase** — a standalone knowledge base for timber craft. Same 4-layer pattern as archibase (construction) and rhinobase (Rhino modeling), different domain.

**Architecture note:** iboisbase is NOT part of archibase. Archibase holds general construction knowledge (SIA codes, materials, structural rules). iboisbase holds IBOIS-specific timber craft knowledge (joint types, assembly sequences, fabrication constraints, quality tolerances). L3 scripts in city101 bridge them: read structural constraints from archibase, read joint parameters from iboisbase, execute via rhinobase.

## The tools

### Tool 1: compas_wood — Joint Generation
- **Repo:** https://github.com/petrasvestartas/compas_wood
- **License:** MIT
- **Language:** C++ core (submodule at `src/wood/`), Python bindings
- **Key files:** `wood_joint_lib.cpp` (~6400 lines), `wood_globals.cpp`, `wood_globals.h`, `wood_joint.h`, `wood_joint.cpp`, `wood_cut.h`
- **What to extract:**
  - 42+ joint types across 7 categories (finger, tenon-mortise, butterfly, cross-cutting, drilling, rotated, boundary)
  - Per-joint constraint values: chamfer offsets, tenon proportions, division ranges, interpolation formulas
  - Global defaults: proximity tolerances, angle thresholds, dihedral angle classification
  - Python API surface: what's controllable at runtime vs compile-time only
  - 3 configurable params per category: `division_length`, `shift`, `type_id`

### Tool 2: Manis — Assembly Constraint Solver
- **Repo:** https://github.com/ibois-epfl/Manis-timber-plate-joinery-solver
- **License:** MIT
- **What it does:** Creates joints between timber panels, generates CNC toolpaths and robot trajectories. Handles topology → joinery → fabrication → assembly as one pipeline.
- **What to extract:**
  - Topological constraints: how panel adjacency determines joint type
  - Assembly sequence rules: what order things get built and why
  - Joint-to-fabrication mapping: which joints need which CNC operations
  - Robot trajectory parameters: if externalized

### Tool 3: diffCheck — Quality Validation
- **Repo:** https://github.com/diffCheckOrg/diffCheck
- **License:** GPL-3.0 (can extract and reference values, but L3 scripts derived from this must stay GPL if they contain substantial GPL code — keep extraction to data/parameters, not reimplemented algorithms)
- **What it does:** Compares CAD models to point cloud scans of fabricated timber. Quantifies discrepancies.
- **What to extract:**
  - Tolerance thresholds: what counts as acceptable deviation between design and fabrication
  - Comparison metrics: which measurements it takes and their valid ranges
  - Quality classification: how it grades joint/assembly accuracy
  - Per-joint-type quality expectations: different tolerances for different joint types?

### Tool 4: Cockroach — Point Cloud Processing
- **Repo:** https://github.com/ibois-epfl/Cockroach
- **License:** LGPL-3.0
- **What it does:** Wraps Open3D, CGAL, PCL, Cilantro for point cloud and mesh operations in Grasshopper.
- **What to extract:**
  - Processing pipeline steps: what operations exist and in what order they're typically applied
  - Parameter defaults: voxel sizes, normal estimation radii, segmentation thresholds
  - Relevant for roundwood: which functions would you chain to go from raw tree scan → skeleton → properties

### Tool 5: Raccoon — CNC Fabrication (⚠️ NO LICENSE)
- **Repo:** https://github.com/ibois-epfl/Raccoon-ibois
- **License:** None (all rights reserved by default)
- **What it does:** G-code generation for 5-axis CNC and robot arms. Machine profiles, tool parameters, collision detection.
- **⚠️ DO NOT clone or extract from this repo.** No license means no permission. Instead:
  - Document what Raccoon *does* based on the README and published papers only (fair use)
  - Flag the `Tools.txt` machine profile format as something to ask IBOIS about
  - Note in L2 guide: "Raccoon knowledge pending — requires permission or license clarification from IBOIS"

### Tool 6: catalogue-explorer — Scanned Object Viewer (⚠️ NO LICENSE)
- **Repo:** https://github.com/ibois-epfl/catalogue-explorer
- **License:** None
- **Same rule as Raccoon:** document from README only, do not extract code.

## Output structure

Everything goes to `output/iboisbase/` with this structure:

```
output/iboisbase/
├── iboisbase.db              ← unified SQLite database (L1)
├── README.md                    ← overview of what was extracted, how to use it
│
├── guides/                      ← L2 markdown guides (archibase format)
│   ├── compas_wood_joints.md
│   ├── manis_assembly.md
│   ├── diffcheck_quality.md
│   ├── cockroach_pointcloud.md
│   └── ibois_tools_overview.md  ← how the tools relate to each other
│
├── scripts/                     ← L3 RhinoPython execution scripts
│   ├── joints/                  ← from compas_wood
│   │   ├── joint_index.py
│   │   ├── tenon_mortise_vidy.py
│   │   ├── tenon_mortise_standard.py
│   │   ├── finger_inplane.py
│   │   ├── finger_outofplane.py
│   │   ├── cross_cutting_rect.py
│   │   └── butterfly_hilti.py
│   ├── assembly/                ← from Manis
│   │   ├── assembly_index.py
│   │   ├── panel_joint_selector.py    ← topology → joint type
│   │   └── assembly_sequence.py       ← ordering logic
│   ├── validation/              ← from diffCheck (data extraction only, respect GPL)
│   │   └── quality_checker.py         ← applies tolerance thresholds from L1
│   └── pointcloud/              ← from Cockroach
│       ├── pointcloud_index.py
│       ├── tree_skeleton_extractor.py ← scan → 11-point skeleton pipeline
│       └── tree_property_extractor.py ← skeleton → diameter, taper, curvature
│
└── csv/                         ← CSV exports for sharing with IBOIS
    ├── joint_catalog.csv
    ├── joint_constraints.csv
    ├── joint_globals.csv
    ├── assembly_rules.csv
    ├── quality_tolerances.csv
    └── pointcloud_defaults.csv
```

## L1 — SQLite schema

Single database `iboisbase.db` with tables across all tools:

```sql
-- ═══════════════════════════════════════
-- FROM compas_wood
-- ═══════════════════════════════════════

CREATE TABLE timber_joints (
    type_id INTEGER PRIMARY KEY,
    category TEXT,            -- ss_e_ip, ss_e_op, ts_e_p, cr_c_ip, tt_e_p, ss_e_r, b
    name TEXT,
    description TEXT,
    cut_type TEXT,            -- edge_insertion, hole, drill, conic
    source_reference TEXT,    -- real project if named after one
    source_repo TEXT DEFAULT 'compas_wood',
    source_file TEXT,
    source_line INTEGER
);

CREATE TABLE joint_constraints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER REFERENCES timber_joints(type_id),
    parameter TEXT,
    value REAL,
    unit TEXT,
    context TEXT,
    configurable INTEGER,     -- 1 = Python runtime, 0 = C++ only
    source_repo TEXT DEFAULT 'compas_wood',
    source_file TEXT,
    source_line INTEGER
);

CREATE TABLE joint_globals (
    parameter TEXT PRIMARY KEY,
    default_value REAL,
    unit TEXT,
    description TEXT,
    configurable INTEGER,
    source_repo TEXT DEFAULT 'compas_wood'
);

CREATE TABLE joint_python_api (
    function_name TEXT,
    parameter TEXT,
    data_type TEXT,
    default_value TEXT,
    description TEXT,
    source_repo TEXT DEFAULT 'compas_wood',
    PRIMARY KEY (function_name, parameter)
);

-- ═══════════════════════════════════════
-- FROM Manis
-- ═══════════════════════════════════════

CREATE TABLE assembly_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_type TEXT,            -- topology, sequence, fabrication_mapping
    condition TEXT,            -- when this rule applies
    action TEXT,               -- what happens
    parameters TEXT,           -- JSON of any numeric values
    source_repo TEXT DEFAULT 'manis',
    source_file TEXT,
    source_line INTEGER
);

CREATE TABLE fabrication_mappings (
    joint_type TEXT,
    cnc_operation TEXT,        -- drill, mill, cut, saw
    tool_requirements TEXT,    -- what tools needed
    constraints TEXT,          -- JSON: min/max values
    source_repo TEXT DEFAULT 'manis'
);

-- ═══════════════════════════════════════
-- FROM diffCheck
-- ═══════════════════════════════════════

CREATE TABLE quality_tolerances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    context TEXT,              -- joint_type, assembly, surface
    metric TEXT,               -- deviation_mm, angle_deg, gap_mm
    acceptable_min REAL,
    acceptable_max REAL,
    unit TEXT,
    description TEXT,
    source_repo TEXT DEFAULT 'diffcheck',
    source_file TEXT
);

-- ═══════════════════════════════════════
-- FROM Cockroach
-- ═══════════════════════════════════════

CREATE TABLE pointcloud_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT,            -- voxel_downsample, estimate_normals, segment, skeletonize
    default_params TEXT,       -- JSON of default parameter values
    typical_order INTEGER,     -- where in a pipeline this usually appears
    description TEXT,
    relevant_for TEXT,         -- roundwood, plate, general
    source_repo TEXT DEFAULT 'cockroach',
    source_file TEXT
);
```

The `source_repo` column on every table lets an agent trace any value back to its origin. An agent can query across tools: "for a Vidy tenon-mortise, what are the joint constraints (compas_wood), the CNC requirements (Manis), and the acceptable quality tolerances (diffCheck)?"

## L2 — Markdown guides

Each guide follows archibase format (see `$ARCHIBASE_PATH/source/knowledge/` for examples). Key guide:

**`ibois_tools_overview.md`** — the one that ties everything together:
- How the tools relate: compas_wood (design) → Manis (assembly planning) → Raccoon (fabrication) → diffCheck (validation)
- What connects them: joint types are the shared concept across all tools
- Where Cockroach fits: upstream (point cloud → geometry) and downstream (scan → validate)
- What's missing: no shared schema between tools (this is the gap we're filling)

## L3 — RhinoPython scripts

Same pattern as existing prototypology scripts. For each script:
1. Header documents L1 source (table, type_id, parameters)
2. Function signature uses L1 defaults
3. Docstring states valid ranges from L1
4. Body uses RhinoCommon calls
5. Returns Rhino GUIDs

**Priority order:**
1. compas_wood joints: Vidy tenon-mortise, standard tenon-mortise, finger (in-plane + out-of-plane), cross-cutting, butterfly
2. Cockroach pipeline: tree scan → skeleton → properties (this connects directly to Damien's PhD)
3. Manis: panel joint selection, assembly sequencing
4. diffCheck: tolerance checking (L1 data only — don't reimplement GPL algorithms, just apply the thresholds)

**The cross-tool script** — the real deliverable:
```python
# scripts/roundwood_design_loop.py
#
# Full loop: query available trees (L1) → match to structural need →
# select joint type (L1) → generate joint geometry (L3 joint script) →
# check against quality tolerances (L1 diffCheck) →
# report fabrication requirements (L1 Manis)
```

## Instructions

### Phase 1: compas_wood (deepest extraction)
1. Clone repo with submodules
2. Extract all joint types, constraints, globals, API surface
3. Write SQLite tables, markdown guide, priority L3 scripts
4. This is the most mature tool — spend the most time here

### Phase 2: Manis
5. Clone repo
6. Focus on: topology→joint mapping, assembly sequence logic, fabrication requirements
7. This is a Grasshopper plugin — look for C# or Python component code with the rules

### Phase 3: diffCheck
8. Clone repo
9. Extract tolerance thresholds and quality metrics only
10. Respect GPL: extract *data* (numbers, thresholds, classification rules), not *algorithms*
11. L3 scripts apply thresholds from L1, they don't reimplement diffCheck's comparison engine

### Phase 4: Cockroach
12. Clone repo
13. Map the processing pipeline: which operations, what order, what defaults
14. L3 focus: the tree-specific pipeline (scan → skeleton → properties) for roundwood

### Phase 5: Raccoon + catalogue-explorer (documentation only)
15. Do NOT clone these repos
16. Document capabilities from READMEs and published papers only
17. Note in L2 guides what knowledge is missing and why (no license)
18. Flag the `Tools.txt` machine profile format as a collaboration opportunity

### Phase 6: Integration
19. Write the cross-tool overview guide (L2)
20. Write the roundwood design loop script (L3)
21. Verify the full L1↔L3 loop: query → select → generate → validate
22. Export CSVs for sharing

## Attribution

Per-tool attribution in every file:
- compas_wood (MIT): "Extracted from compas_wood by Petras Vestartas, IBOIS/EPFL"
- Manis (MIT): "Extracted from Manis by IBOIS/EPFL"
- diffCheck (GPL-3.0): "Tolerance values referenced from diffCheck by Settimi, Gilliard, Skevaki, Kladeftira, IBOIS/EPFL & CRCL/EPFL"
- Cockroach (LGPL-3.0): "Pipeline documented from Cockroach by IBOIS/EPFL"

## Why this matters

IBOIS has built the most complete open-source timber construction toolchain in academia. But each tool is its own island — compas_wood doesn't talk to Manis, Manis doesn't talk to diffCheck. The knowledge is there, it's just not connected.

This extraction creates the connection layer: a single database where an agent can ask "for this joint type, what are the design constraints, the assembly rules, the fabrication requirements, and the acceptable tolerances?" — across four different tools, in one query.

That's what we'd show Damien: not "we want to use your tools" but "we already read all of them, here's how they fit together, and here's what's missing."
