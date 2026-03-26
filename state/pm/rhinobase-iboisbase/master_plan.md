# Master Plan: Knowledge Base Expansion (rhinobase + iboisbase)

**Goal:** Build two new knowledge bases alongside archibase: **rhinobase** (Rhino modeling fluency) and **iboisbase** (IBOIS timber craft). Same 4-layer pattern (SQLite/Markdown/Code/VectorDB), different domains. L3 scripts in city101 bridge all three.

**Created:** 2026-03-26
**Priority:** Nice-to-have for midterm (March 30). Core work is post-midterm.
**Status:** Planned, not started

**Scalability rule:** Promote a domain to its own base only when LEARNINGS.md for that domain gets too long to carry. Don't create bases speculatively. Currently justified: rhinobase (agents write Rhino scripts every session) and iboisbase (IBOIS collaboration). Future candidates: blenderbase, geobase — only when needed.

---

## Why

Two knowledge gaps, one plan:
1. **RhinoCommon fluency** — agents write RhinoPython through `rhino_execute_python_code` but pick methods by guessing from training data. A structured knowledge base (API classes, methods, patterns, forum idioms) makes every Rhino script more reliable.
2. **IBOIS timber knowledge** — 4 open-source tools with construction knowledge embedded in code. Extracting it proves the thesis and extends archibase to a new domain.

They feed each other: RhinoCommon knowledge makes the IBOIS L3 translations correct. The IBOIS translations are practice that builds RhinoCommon fluency. Separating them would be worse.

---

## Phase Overview

```
Phase 0: RhinoCommon Knowledge ────────────── ~2 hrs, runs in parallel with Phase 1
  ├── Agent F: API docs scrape → L1 (classes, methods, params, types)
  ├── Agent G: Developer guides → L2 (patterns, tutorials, how-tos)
  └── Agent H: Forum/discourse → L4 RAG (idiomatic solutions)

Phase 1: IBOIS Parallel Extraction ────────── ~2-3 hrs, runs in parallel with Phase 0
  ├── Agent A: compas_wood (MIT) ─── biggest, bottleneck
  ├── Agent B: Manis (MIT) ────────── medium
  ├── Agent C: diffCheck (GPL) ────── small, data only
  ├── Agent D: Cockroach (LGPL) ───── small
  └── Agent E: Raccoon + catalogue ── README-only docs, 15 min

Phase 2: Integration ──────────────────────── ~1-2 hrs (after Phase 0 + 1)
  ├── Merge all databases (RhinoCommon + IBOIS tools)
  ├── Write L3 RhinoPython scripts — grounded in both knowledge bases
  ├── Write cross-tool guides
  ├── Build higher-level MCP tools from L3 scripts
  └── Export CSVs for IBOIS sharing

Phase 3: Roundwood Loop ───────────────────── ~1 hr (after IBOIS meeting)
  └── Incorporate Damien's feedback + build cross-tool design loop script
```

**Total wall time: ~3-4 hrs** (Phase 0 and 1 run simultaneously)

---

## Phase 0: RhinoCommon Knowledge Base (parallel with Phase 1)

**Topology:** Flat parallel. 3 agents scraping different sources.

**Team:** 3 agents

| Agent | Source | Target layer | Output dir | Est. time |
|-------|--------|-------------|-----------|-----------|
| F: API scrape | developer.rhino3d.com/api/rhinocommon/ | L1 (SQLite) | output/rhinocommon_knowledge/api/ | 1-2 hrs |
| G: Guides | developer.rhino3d.com guides + Python scripting docs | L2 (Markdown) | output/rhinocommon_knowledge/guides/ | 1 hr |
| H: Forum | McNeel Discourse (RhinoPython/RhinoCommon threads) | L4 (RAG chunks) | output/rhinocommon_knowledge/forum/ | 1-2 hrs |

### Agent F — API Reference (L1)

Scrape the RhinoCommon API reference into SQLite:

```sql
CREATE TABLE rhinocommon_namespaces (
    namespace TEXT PRIMARY KEY,      -- Rhino.Geometry, Rhino.DocObjects, etc.
    description TEXT,
    class_count INTEGER
);

CREATE TABLE rhinocommon_classes (
    class_name TEXT PRIMARY KEY,     -- Brep, NurbsSurface, Curve, Point3d
    namespace TEXT REFERENCES rhinocommon_namespaces(namespace),
    description TEXT,
    base_class TEXT,
    is_struct INTEGER               -- 1 for structs like Point3d, Vector3d
);

CREATE TABLE rhinocommon_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT REFERENCES rhinocommon_classes(class_name),
    method_name TEXT,
    is_static INTEGER,
    return_type TEXT,
    parameters TEXT,                -- JSON: [{name, type, description, default}]
    description TEXT,
    example_code TEXT               -- if available on the docs page
);

CREATE TABLE rhinocommon_properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT REFERENCES rhinocommon_classes(class_name),
    property_name TEXT,
    type TEXT,
    readable INTEGER,
    writable INTEGER,
    description TEXT
);
```

**Priority namespaces** (most used in architectural scripting):
1. `Rhino.Geometry` — Brep, Curve, Surface, Mesh, Point3d, Vector3d, Plane, Transform
2. `Rhino.DocObjects` — ObjectAttributes, Layer, adding objects to document
3. `Rhino.RhinoDoc` — document access, object tables
4. `Rhino.Commands` — Result enum
5. `Rhino.Input` — getting user input (less relevant for MCP, but good to know)

### Agent G — Developer Guides (L2)

Scrape and organize the McNeel developer guides into archibase-format markdown:
- RhinoPython 101 (getting started, syntax, Rhino specifics)
- Common geometry operations (creating, transforming, boolean, splitting)
- Working with Breps (the hard one — surfaces vs polysurfaces vs solids)
- Layers, attributes, document management
- Coordinate systems and transformations
- Performance patterns (when to use Mesh vs Brep, batch operations)

Each guide: what the pattern is, when to use it, working code example, common pitfalls.

### Agent H — Forum Idioms (L4 RAG)

Scrape high-value McNeel Discourse threads into RAG chunks:
- Search for: "RhinoPython", "RhinoCommon", "scriptcontext", common geometry operations
- Focus on answered questions with working code
- Each chunk: question + accepted answer + code
- Tag with topic (boolean, surface, mesh, transform, etc.)

**Dependencies:** None between F/G/H. All run simultaneously.

**Success criteria:**
- L1 database covers the priority namespaces with method signatures
- L2 guides cover the 6 core patterns listed above
- L4 has 500+ idiomatic code chunks from the forum
- An agent can query: "how do I loft curves into a surface?" and get the right class, method, parameters, and a working example

---

## Phase 1: IBOIS Parallel Extraction (parallel with Phase 0)

**Topology:** Flat parallel. No coordinator — agents work on independent repos.

**Team:** 5 agents (4 extractors + 1 doc agent)

| Agent | Repo | License | Output dir | Est. time |
|-------|------|---------|-----------|-----------|
| A: compas_wood | petrasvestartas/compas_wood | MIT | output/iboisbase/compas_wood/ | 2-3 hrs |
| B: Manis | ibois-epfl/Manis-timber-plate-joinery-solver | MIT | output/iboisbase/manis/ | 1-2 hrs |
| C: diffCheck | diffCheckOrg/diffCheck | GPL-3.0 | output/iboisbase/diffcheck/ | 30-60 min |
| D: Cockroach | ibois-epfl/Cockroach | LGPL-3.0 | output/iboisbase/cockroach/ | 30-60 min |
| E: Docs-only | Raccoon + catalogue-explorer | No license | output/iboisbase/docs_only/ | 15 min |

**Each extractor produces:**
- `[tool].db` — SQLite with tool-specific tables
- `[tool]_guide.md` — L2 markdown guide
- `[tool]_summary.md` — what was found, what was unclear, line references

**Dependencies:** None between agents. All run simultaneously.

**Success criteria:**
- Each SQLite database has populated tables with source_file and source_line references
- Each L2 guide is readable by a human with no code access
- compas_wood has all 42+ joint types cataloged

---

## Phase 2: Integration (after Phase 0 + Phase 1)

**Topology:** Small team, sequential tasks with one parallel split.

**Depends on:** Both Phase 0 and Phase 1 complete.

**Team:** 3 agents

| Agent | Task | Reads | Produces |
|-------|------|-------|----------|
| I: DB merger | Merge all SQLite databases | All Phase 0+1 .db files | `iboisbase.db`, `rhinocommon.db` (or unified) |
| J: L3 scripter | Write RhinoPython joint scripts | compas_wood L1 + RhinoCommon L1/L2 | `scripts/joints/*.py`, `scripts/joint_index.py` |
| K: Guide writer | Cross-tool overview + CSVs | All L2 guides + merged DB | `ibois_tools_overview.md`, CSV exports |

Agent I runs first (merge), then J and K run in parallel (both read from merged DB).

**L3 script quality gate:** Each script must:
1. Reference L1 source (type_id, parameter names) in header
2. Use only RhinoCommon methods confirmed to exist in the L1 API database
3. Default values match IBOIS L1 exactly
4. Include a docstring with valid parameter ranges

**MCP tool wrapping:** For the highest-value L3 scripts, wrap them as new Rhino MCP tools. Pattern:
```
L3 script (standalone .py) → thin MCP wrapper → new tool: rhino_create_timber_joint
```
This makes the knowledge directly callable without agents writing code each time.

**Success criteria:**
- Cross-tool query works: "for joint type X, what are constraints + fabrication needs + tolerances?"
- L3 scripts use verified RhinoCommon methods (not guessed)
- At least 2 new MCP tools wrapping common joint operations
- CSVs are clean and shareable with IBOIS

---

## Phase 3: Roundwood Loop (after IBOIS meeting, March 27+)

**Topology:** Single agent, exploratory.

**Depends on:** Phase 2 + meeting with Damien.

**Tasks:**
1. Incorporate whatever Damien shares (roundwood database format, query capabilities, property extraction status)
2. If point cloud data is accessible: build the Cockroach pipeline (scan → skeleton → properties)
3. Complete `roundwood_design_loop.py`: query available trees → match structural need → select joint → generate → validate
4. If Raccoon gets a license: extract machine profiles

**Success criteria:**
- End-to-end script: real tree data → structural matching → joint generation → quality check

---

## Prompt files

- `state/pm/rhinobase-iboisbase/prompts/phase0_rhinocommon.md` — Phase 0: rhinobase ✅
- `state/pm/rhinobase-iboisbase/prompts/phase1_ibois_extraction.md` — Phase 1-3: iboisbase ✅

---

## Risk / Notes

- **Phase 0 + 1 run simultaneously = 8 agents.** That's at the team cap (v3 workflow says max 8). If budget is tight, Phase 0 can be 2 agents (skip forum scrape, do it later).
- **compas_wood is the bottleneck.** 6400 lines of C++, most complex extraction. If time is very short, do compas_wood + RhinoCommon API only — that's the minimum viable extraction.
- **GPL caution on diffCheck.** Extract data/thresholds only. Don't reimplement algorithms in L3 scripts.
- **Raccoon is locked.** No license. Meeting with Damien may unlock it.
- **Forum scraping (Agent H) may hit rate limits.** McNeel Discourse might require pagination/auth. Fallback: curate manually from top threads.
- **Weekly limit at 60%.** If running before midterm, the minimum high-impact subset is: RhinoCommon API (Agent F) + compas_wood (Agent A) + integration for 2-3 L3 scripts. That's 3 agents, ~3 hrs, and gives you something concrete for slide 6.
- **Midterm value:** "We built a knowledge base that knows Swiss construction codes AND RhinoCommon AND IBOIS timber joints — and the agents use all three when they model." That's the story.
- **Post-midterm value:** The full extraction becomes the foundation for thesis-level prototypology work. Every lock can use real timber construction knowledge.
