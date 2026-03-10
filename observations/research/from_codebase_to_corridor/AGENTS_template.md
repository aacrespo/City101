# AGENTS.md — Multi-Agent Governance for Architectural Projects

<!--
  HOW TO USE THIS TEMPLATE

  1. Fork this file into your project root as AGENTS.md
  2. Replace all [bracketed placeholders] with your project specifics
  3. Delete the HTML comments once you understand each section
  4. Share this file with every agent and team member — it is the single
     source of truth for how work gets divided, verified, and promoted.

  Estimated setup time: 15–30 minutes for a new project.

  Origin: Abstracted from City101 (EPFL Studio Huang, 2026), a 4-agent +
  2-human system for urban corridor analysis. The patterns generalize to
  any design project with spatial data, multiple contributors, and AI agents.
-->

---

## 1. Team Roster

<!--
  PURPOSE: Define who (human or agent) does what, and what tools each has access to.
  Without this, agents duplicate work, write to each other's files, or attempt
  operations they can't perform (e.g., an agent without MCP trying to control QGIS).
-->

### Humans

| Person | Role | Current focus | Tools / access |
|--------|------|---------------|----------------|
| [Lead Designer] | Design authority, final sign-off | [Current task] | [Software stack: Rhino, QGIS, etc.] |
| [Domain Expert / Teammate] | [Specialty] | [Current task] | [Their tools] |

### Persistent Agents

<!--
  "Persistent" = long-running conversation threads that accumulate context across sessions.
  Each gets a name so handoffs can reference them unambiguously.
-->

| Name | Role | Capabilities | Limitations |
|------|------|-------------|-------------|
| [Name 1] | Primary analytical agent | Desktop MCP (filesystem, [CAD tool], browser), API access | [Rate limits, no GPU, etc.] |
| [Name 2] | Code / orchestrator agent | Terminal, can spawn subagents, filesystem access | Cannot modify [CAD tool] directly |
| [Name 3] | Overflow / parallel tasks | Browser-only, project knowledge files | No MCP, no filesystem, lower context limits |
| [Name 4] | [Teammate]'s analytical agent | [Their setup] | [Their limits] |

### Ephemeral Agents (Subagents)

<!--
  Spawned by an orchestrator for specific tasks. They read AGENTS.md at start,
  do their job, write to staging, print a summary, and exit.
-->

Subagents follow these rules:
- Read this AGENTS.md at start (shared context)
- Do their assigned task only
- Write output to **`[staging-path]/`** — NEVER to production paths
- Print a structured summary to stdout (format in Section 5)
- Exit when done

Common subagent roles for architectural projects:

| Role | What it does | Typical output |
|------|-------------|----------------|
| Data collector | Fetches from APIs, scrapes, converts formats | CSVs, GeoJSON |
| Spatial validator | Checks coordinates, bounding boxes, CRS consistency | Validation reports |
| Cross-referencing agent | Joins datasets, computes derived metrics | Enriched CSVs |
| Design generator | Produces geometry from parameters | [Model files, DXF, etc.] |
| Reviewer / QA | Verifies outputs against contracts | Pass/fail reports |
| Narrative agent | Writes analysis text from data | Markdown drafts |

### Coordination Rules

1. **Whoever has the most current context coordinates.** Any agent can allocate tasks.
2. **Read the latest handoff** at conversation start.
3. **Respect task allocations** — don't duplicate work assigned to another agent.
4. **Flag cross-team impacts** — "this changes something [Teammate] needs to know."
5. **Keep handoffs lean.**
6. **Use names** — always say [Agent Name] so the trail is clear.

---

## 2. Data Contracts

<!--
  PURPOSE: Without shared conventions, agents produce data that can't be joined.
  One agent writes "Lausanne Gare", another writes "Lausanne CFF" — no downstream
  analysis works. Data contracts prevent this.
-->

### 2a. Canonical Entity List

<!--
  The single definitive list of entities (sites, stations, zones, buildings —
  whatever your project's "atoms" are). Every agent references this list exactly.
-->

**Primary entity type:** [e.g., stations, parcels, building footprints]
**Canonical list file:** `[path/to/canonical_entities.csv]`
**Join key column:** `[entity_name]` or `[entity_id]`
**Count:** [N] entities

Every output CSV must include a `[join_key]` column using EXACTLY the names in the canonical list. If a source uses different names, map them to the canonical name. Include the source's original name in a `source_name` column.

<!--
  If your project has secondary entity types (e.g., communes, districts),
  define a canonical list for each.
-->

### 2b. Coordinate System

**Project CRS:** [EPSG code, e.g., EPSG:2056 Swiss LV95]
**Web/visualization CRS:** [EPSG:4326 WGS84]
**Conversion library:** [e.g., pyproj, proj4js]

All output files must include BOTH coordinate systems:
- `lat_wgs84`, `lon_wgs84` — WGS84
- `[E_local]`, `[N_local]` — project CRS

**Validation bounding box:**
- WGS84 lat: [min_lat] to [max_lat]
- WGS84 lon: [min_lon] to [max_lon]
- Any row outside these ranges is flagged as suspect

### 2c. Output Schema Convention

Every dataset must include these columns:

| Column | Type | Required | Purpose |
|--------|------|----------|---------|
| `[join_key]` | string | Yes | Links to canonical entity list |
| `lat_wgs84` | float | Yes | WGS84 latitude |
| `lon_wgs84` | float | Yes | WGS84 longitude |
| `[E_local]` | float | Yes* | Local CRS easting (*if project uses local CRS) |
| `[N_local]` | float | Yes* | Local CRS northing |
| `source` | string | Yes | URL or dataset name |
| `fetch_date` | ISO date | Yes | When data was retrieved |
| `id` | string | Yes | Unique row identifier |

**Column naming convention:**
- `snake_case`, lowercase
- Prefix with domain if ambiguous: `transit_frequency`, `demo_population`
- Booleans: `is_` or `has_` prefix
- Percentages: `pct_` prefix
- Counts: `n_` or `count_` suffix

### 2d. File Naming

All project-generated files: `[project_prefix]_[domain]_[descriptor].csv`

Example: `city101_transit_ridership.csv`, `city101_ev_charging_ENRICHED_v3.csv`

Versioning: append `_v2`, `_v3` for manual versions. If using git, versions are commits — no suffix needed.

---

## 3. File Governance

<!--
  PURPOSE: Prevent agents from overwriting each other's work, contaminating
  production data, or touching files they shouldn't. This is the single most
  important safety mechanism.
-->

### Directory Roles

```
[project_root]/
├── AGENTS.md                 <- THIS FILE (every agent reads first)
├── CONTEXT.md                <- living project state (Section 4)
├── LEARNINGS.md              <- accumulated pitfalls (Section 4)
│
├── [datasets/]               <- PRODUCTION data (verified only)
│   ├── [domain_1/]           (e.g., corridor_analysis/)
│   ├── [domain_2/]           (e.g., transit/)
│   └── [domain_3/]           (e.g., geometry/)
│
├── [source/]                 <- FROZEN inputs (never modified)
│   ├── [raw_data/]           (original downloads, classmate submissions)
│   └── [reference/]          (base geometry, cadastral, etc.)
│
├── [output/]                 <- STAGING (agents write here)
│   └── [agent outputs land here, reviewed before promotion]
│
├── [handoffs/]               <- session handoffs
├── [scripts/]                <- processing scripts
├── [visualizations/]         <- maps, web, diagrams
├── [deliverables/]           <- final submissions
└── [archive/]                <- superseded files (never delete, move here)
```

### Write Permissions

| Path | Who can write | Notes |
|------|--------------|-------|
| `[source/]` | **Nobody** | Frozen inputs. Never modify. |
| `[datasets/]` | **Lead agent or human only** | Production. Only after verification. |
| `[output/]` | **Any agent** | Staging area. All agent output goes here first. |
| `[handoffs/]` | **Any agent** | Session summaries |
| `[scripts/]` | **Any agent** | Processing code |
| `[visualizations/]` | **Designated agent only** | To prevent conflicts |
| `CONTEXT.md` | **Lead agent** | Updated at session end |
| `LEARNINGS.md` | **Any agent** | Append-only |
| `[CAD project file]` | **Human only** | Agents never modify directly |

### File Safety Rules

- **NEVER modify or overwrite original files.** Always write to a new path.
- **NEVER delete any file or directory.** Move to `[archive/]` instead.
- **Ask before ANY filesystem write** — state the exact path and what will be written.
- **Never read files outside the project** — no `~/.ssh`, `~/.config`, credentials, browser data.
- **Write outputs to `[staging-path]/`** until verified and promoted.

### Promotion Workflow

```
Agent produces file → writes to output/ → prints summary
                                              ↓
Lead agent or human reviews → runs verification checks (Section 3, below)
                                              ↓
                              Pass? → Move to datasets/[domain]/
                              Fail? → Re-spawn agent with specific fix instructions
```

### Verification Gates

Before any file moves from `[output/]` to `[datasets/]`, verify:

- [ ] Row counts match expectations
- [ ] Coordinates within validation bounding box
- [ ] No null/empty values in required columns (join key, coordinates, source)
- [ ] Join key matches canonical entity list (no orphans, no missing)
- [ ] Source attribution present for every row
- [ ] No absurd outliers, duplicates, or impossible values
- [ ] File loads without encoding errors or ragged rows

Verification script pattern:
```python
import pandas as pd

df = pd.read_csv('[output/file.csv]')

# Coordinate ranges
assert df['lat_wgs84'].between([MIN_LAT], [MAX_LAT]).all(), "Lat out of range"
assert df['lon_wgs84'].between([MIN_LON], [MAX_LON]).all(), "Lon out of range"

# Join integrity
canonical = set([CANONICAL_NAMES])
output_names = set(df['[join_key]'].unique())
orphans = output_names - canonical
missing = canonical - output_names
assert not orphans, f"Orphan names: {orphans}"
print(f"Coverage: {len(output_names)}/{len(canonical)} entities")

# Required columns
required = ['[join_key]', 'lat_wgs84', 'lon_wgs84', 'source', 'fetch_date']
for col in required:
    nulls = df[col].isna().sum()
    assert nulls == 0, f"{col} has {nulls} null values"
```

---

## 4. Living State Files

<!--
  PURPOSE: Agents are ephemeral. Context is not. These files bridge sessions
  so a new agent (or the same agent in a new conversation) can pick up where
  the last one left off without re-deriving everything.
-->

### CONTEXT.md — Current Project State

**Location:** `[project_root]/CONTEXT.md`
**Updated by:** Lead agent, at the end of each work session
**Read by:** Every agent at session start

Contents:
- **Project phase** — what stage are we in, what's due when
- **Active questions** — what the team is currently investigating
- **Recent decisions** — what was decided and why (not the full history, just recent)
- **Dataset inventory** — what exists, row counts, last updated dates
- **Blockers** — anything stalled and why
- **Observations** — patterns noticed but not yet confirmed (mark as remarks, not conclusions)

Template:
```markdown
# Project Context — [Project Name]
Last updated: [date] by [agent/person name]

## Current phase
[What phase, what's due, what's active]

## Active questions
- [Question 1 — who's investigating]
- [Question 2 — status]

## Recent decisions
- [Date]: [Decision and brief rationale]

## Dataset status
| Dataset | Rows | Last updated | Status |
|---------|------|-------------|--------|
| [name] | [n] | [date] | [complete / in progress / needs verification] |

## Blockers
- [Blocker] — [why, who can unblock]

## Observations (remarks, not conclusions)
- [Pattern noticed — needs verification]
```

### LEARNINGS.md — Accumulated Pitfalls

**Location:** `[project_root]/LEARNINGS.md`
**Updated by:** Any agent that encounters a pitfall
**Format:** Append-only (never delete entries, they save future agents time)

Contents:
- API quirks (rate limits, parameter gotchas, broken endpoints)
- Data quality issues (known gaps, encoding problems, format traps)
- Tool-specific workarounds (QGIS rendering bugs, library version conflicts)
- Methodology notes (what analysis approach worked, what didn't)

Template:
```markdown
# Learnings — [Project Name]

## API pitfalls
- **[API name]**: [Pitfall description]. Workaround: [solution]. (Added [date])

## Data quality
- **[Dataset]**: [Issue]. (Added [date])

## Tool workarounds
- **[Tool]**: [Problem and fix]. (Added [date])

## Methodology
- **[Approach]**: [What worked / didn't work and why]. (Added [date])
```

---

## 5. Handoff Protocol

<!--
  PURPOSE: When one agent ends a session and another picks up, the handoff
  prevents lost context. A bad handoff means the next session wastes 30 minutes
  re-deriving what was already known. A good handoff gets them productive in 2 minutes.
-->

### When to Write a Handoff

- End of any work session
- Before switching between agents
- When a human is passing work to an agent (or vice versa)

### Handoff Format

**File:** `[handoffs/]HANDOFF_[DD-MM]_S[session_number].md`

```markdown
# Handoff — [Date], Session [N]
**Agent:** [Name]
**Duration:** [approximate]

## What was done
- [Concrete deliverable 1 — file path if applicable]
- [Concrete deliverable 2]

## Decisions made
- [Decision and rationale — these are binding unless explicitly revisited]

## Data produced
| File | Rows | Status |
|------|------|--------|
| [path] | [n] | [verified / staging / needs review] |

## Open questions
- [Question that needs answering before the next step]

## Blockers
- [What's stuck and why]

## Suggested next steps
- [What the next session should do first]

## For [Teammate name] specifically
- [Anything that affects their work]
```

### Agent Summary Format (for subagents)

When a subagent completes its task, it prints this to stdout:

```markdown
## Agent Summary: [agent name]

### Files produced
- `[path/to/file.csv]` — [rows] rows, [cols] columns. [one-line description]

### Data sources used
- [Source name] ([URL]) — [what was extracted, quality notes]

### Data sources searched but not used
- [Source name] ([URL]) — [why: no relevant data, paywalled, wrong format]

### Data sources discovered (not in original plan)
- [Source name] ([URL]) — [what it contains, potential use]

### Quality notes
- [Missing entities, suspicious values, coverage gaps]

### What I could not find
- [Anything the task asked for that does not exist or is not public]

### Suggestions for the lead
- [Direction changes, unexpected findings, recommended next steps]
```

---

## 6. Safety Rules

<!--
  PURPOSE: Agents have real filesystem access, can call APIs with real quotas,
  and can modify project files. These rules prevent expensive mistakes.
-->

### Filesystem

- **NEVER modify or overwrite original/source files**
- **NEVER delete any file or directory** (move to archive instead)
- **Ask before any filesystem write** — state exact path and content description
- **Never read files outside the project tree** — no home directory configs, credentials, SSH keys, browser data
- **All agent output goes to staging** — never directly to production

### API Rate Limits

| API | Rate limit | Minimum delay between calls |
|-----|-----------|----------------------------|
| [API 1] | [limit] | [delay, e.g., 0.35s] |
| [API 2] | [limit] | [delay] |
| [API 3] | [limit] | [delay] |

If multiple agents share an API, assign them different endpoints or stagger calls. Never let two agents hammer the same endpoint simultaneously.

### Actions Requiring Human Approval

These operations are **never** performed autonomously:

- [ ] Modifying the [CAD/BIM project file] (e.g., `.qgz`, `.3dm`, `.rvt`)
- [ ] Pushing to a remote repository
- [ ] Deleting or archiving files
- [ ] Making API calls that cost money (paid geocoding, cloud compute, etc.)
- [ ] Running scripts that modify geometry in production models
- [ ] Publishing or sharing deliverables externally
- [ ] Changing project CRS or canonical entity list
- [ ] Promoting data from staging to production (unless explicitly delegated)

### Data Integrity

- **Never fabricate or estimate data** unless explicitly instructed. If data does not exist, report the gap.
- **Never silently drop rows** during processing. Log dropped rows and reasons.
- **Never overwrite a dataset** — write a new version with a suffix or new path.
- **Always preserve source attribution** — every row traces back to its origin.

---

## 7. Design-Specific Governance

<!--
  PURPOSE: Architectural projects have geometric data, model files, and
  design-phase-dependent levels of detail. Generic data governance doesn't
  cover these. This section does.
-->

### LOI / LOG / LOD Framework

<!--
  Adapt these definitions to your studio's conventions. The point is:
  don't model what isn't decided, don't collect less data than you'll need.
-->

| Concept | Definition | Rule |
|---------|-----------|------|
| **LOI** (Level of Information) | Richness of metadata per entity | Work rich, export lean. Collect all available attributes. Filter at export time, not during collection. |
| **LOG** (Level of Geometry) | Geometric detail of models | Start lean, refine progressively. Detail follows design certainty. |
| **LOD** (Level of Development) | Overall completeness | Increases as the project progresses. Don't model what isn't decided. |

### Phase-Dependent Permissions

| Phase | Agents can | Agents cannot |
|-------|-----------|---------------|
| Research / data collection | Fetch data, create CSVs/GeoJSON, produce analysis | Generate design geometry, modify site models |
| Analysis / synthesis | Cross-reference, compute metrics, produce visualizations | Lock design decisions, modify canonical entities |
| Design development | Generate parametric geometry to staging | Write to production model without review |
| Documentation | Produce drawings, schedules, specs | Change design geometry |

### Geometric Modifications

- **Model file** (Rhino, Revit, SketchUp, etc.): `[path/to/model]`
- **Agents never modify the model directly.** They produce geometry files (DXF, OBJ, GeoJSON, 3DM) to staging. The human imports and positions.
- **Exception:** If MCP bridge exists (e.g., Rhino-to-agent via Grasshopper), the agent may create geometry in a **dedicated agent layer** that is clearly separated from human work.

### Model Versioning

<!--
  Choose your approach. Options:
  - Manual: _v1, _v2 suffixes (simple, works without infrastructure)
  - Git LFS: for binary model files
  - Speckle: branch-based, good for collaborative BIM
  - Other: whatever your studio uses
-->

**Approach:** [Manual versioning / Git LFS / Speckle branches / other]

Rules:
- Every version is tied to a **design decision**, not a date. Name it: `[model]_[decision-tag]_v[N].[ext]`
- Never overwrite a version. The previous version stays in place (or moves to archive).
- If using Speckle: one branch per agent, merge to main only with human review.
- **Backup before any automated operation:** `[model].backup_before_[operation]`

### Clash / Consistency Detection

<!--
  If your project involves multiple geometric layers that must align
  (structure + facade + MEP, or urban fabric + transit + landscape),
  define what consistency means and when to check.
-->

**When to run consistency checks:**
- [ ] After importing agent-generated geometry
- [ ] After merging branches or model versions
- [ ] Before any deliverable export
- [ ] [Other project-specific triggers]

**What to check:**
- Spatial extents match across layers
- No geometry outside the site boundary
- [Domain-specific: e.g., floor levels align, setbacks respected, transit routes connect]

### Print / Export Conventions

| Output | Format | Resolution | CRS |
|--------|--------|-----------|-----|
| Screen maps | PNG | 150 DPI | [Project CRS] |
| Print maps | PDF | 300 DPI | [Project CRS] |
| Web maps | GeoJSON / tiles | N/A | WGS84 |
| Architectural drawings | [DWG/PDF/...] | [per studio conventions] | [Project CRS] |
| 3D exports | [OBJ/FBX/GLB/...] | N/A | [Project CRS, Z-up] |

---

## 8. Naming Conventions

<!--
  PURPOSE: Consistent naming means files are findable, layers are readable
  in QGIS/Rhino, and git diffs are meaningful. Every name should tell you
  what something is without opening it.
-->

### Files

**Pattern:** `[project_prefix]_[domain]_[descriptor]_[version].[ext]`

| Component | Convention | Example |
|-----------|-----------|---------|
| Project prefix | Short, unique per project | `city101`, `alpine03`, `zhport` |
| Domain | Thematic group | `transit`, `geometry`, `energy`, `landscape` |
| Descriptor | What the file contains | `ridership`, `catchment_areas`, `facade_panels` |
| Version | Only for manual versioning | `_v2`, `_v3`, `_ENRICHED` |
| Extension | Standard | `.csv`, `.geojson`, `.3dm`, `.pdf` |

Qualifiers (append before extension when needed):
- `_RAW` — unprocessed source data
- `_ENRICHED` — processed / joined / augmented
- `_CROSSREF` — cross-referenced against canonical entities
- `_REVIEWS` — qualitative data (ratings, comments)
- `_MERGED` — combined from multiple sources

### Layers (QGIS / Rhino / CAD)

**Pattern:** `[NN]_[domain]_[descriptor]`

| Component | Convention | Example |
|-----------|-----------|---------|
| NN | Two-digit ordering number | `01`, `15`, `42` |
| Domain | Same as file domains | `transit`, `topo`, `design` |
| Descriptor | Same as file descriptors | `stations`, `contours_5m`, `intervention_A` |

Group layers by domain. Keep ordering numbers spaced (01, 05, 10, 15...) so new layers slot in without renumbering everything.

### Datasets (Column Names)

| Convention | Example |
|-----------|---------|
| `snake_case`, lowercase | `station_name`, `lat_wgs84` |
| Prefix with domain if ambiguous | `transit_freq`, `demo_pop` |
| Booleans: `is_` or `has_` | `is_accessible`, `has_wifi` |
| Percentages: `pct_` | `pct_commuter` |
| Counts: `n_` or `_count` | `n_departures`, `review_count` |
| Indices/scores: `_index` or `_score` | `wci_index`, `diversity_score` |
| Shannon diversity: `shannon_` | `shannon_cuisine`, `shannon_modal` |

### Branches (if using Git)

**Pattern:** `[type]/[brief-description]`

| Type | When | Example |
|------|------|---------|
| `data/` | Adding or processing datasets | `data/ridership-sbb` |
| `analysis/` | New analysis or metric | `analysis/temporal-wci` |
| `viz/` | Visualization work | `viz/scrollytelling-site` |
| `design/` | Geometry / intervention work | `design/station-intervention-A` |
| `fix/` | Correcting errors | `fix/coordinate-crs-mismatch` |

### Handoffs

**Pattern:** `HANDOFF_[DD-MM]_S[N].md` where N is the session number for that day.

### Versions

**Tie versions to decisions, not dates:**
- Good: `city101_facade_after-setback-decision_v3.3dm`
- Bad: `city101_facade_march5.3dm`

When the version reflects a specific design move, the filename becomes documentation.

---

## Quick Start Checklist

When setting up a new project with this template:

- [ ] Replace all `[bracketed placeholders]` with project-specific values
- [ ] Delete the HTML comments (they are setup instructions, not runtime docs)
- [ ] Create the canonical entity list CSV
- [ ] Set up the folder structure (datasets, source, output, handoffs, etc.)
- [ ] Write the initial CONTEXT.md (even if brief — "Project just started")
- [ ] Create an empty LEARNINGS.md (it will fill up fast)
- [ ] Define your coordinate bounding box
- [ ] List your APIs and their rate limits
- [ ] Decide on version control approach (git vs manual)
- [ ] Share this file with all team members and agents

---

## Adaptation Notes

This template assumes:
- **Spatial data** is central to the project (coordinates, CRS, bounding boxes). If your project is not spatial, simplify Section 2 accordingly.
- **Multiple AI agents** are working in parallel. If you have one agent, Sections 1 and 5 simplify but don't disappear — you still need handoffs between sessions.
- **A staging/production split** for data quality. If your project is small enough that one person verifies everything in real time, you can collapse `output/` and `datasets/` — but keep the verification checklist.
- **Design tools** produce binary files that agents cannot directly modify. If your pipeline is fully code-based (e.g., OpenSCAD, Grasshopper scripting), adjust Section 7 to reflect that agents CAN generate geometry directly.

The governance overhead should be proportional to the project. A 2-week charrette needs less formality than a 6-month thesis. Scale down by removing sections, but keep: data contracts (Section 2), file safety (Section 6), and naming (Section 8). Those three prevent the mistakes that actually cost time.
