# City101 — "Still on the Line"

## Project
EPFL BA6 Architecture studio (AR-302k, Studio Huang — "Sentient Cities"). Andrea analyzes the 101km Geneva–Villeneuve corridor through "flow of people" — what makes people stop, where infrastructure creates behavior, and whether this strip functions as one continuous city.

Teammate: Henna Rafik. Coordination via LOCKBOARD.md.

## Current phase
- **A01** (data collection): complete
- **A02** (data synchronicity): complete (submitted March 3)
- **A03** (field data): active — western field visit done, eastern visit March 13
- **A04** (forms of sentience): assigned March 10, due March 30 (midterm)

## How this repo works

### Layer 1: Auto-loaded (every session)
You're reading this now. Three more files load automatically from `.claude/rules/`:
- `conventions.md` — coordinates, commit prefixes, file safety
- `data-protocol.md` — collection rules, quality gates, canonical stations
- `tool-protocol.md` — how to use tools and workflows

### Layer 2: Role-loaded (on slash command)
| Command | Reads | Workflows |
|---------|-------|-----------|
| `/analyst` | datasets/INVENTORY.md, LEARNINGS.md | data-collection, data-verification |
| `/cartographer` | design_system/SPEC.md, datasets/INVENTORY.md | map-generation, map-export |
| `/modeler` | 00_Workflow_v04.md (Sec 3.2), design_system/SPEC.md | rhino-modeling |
| `/visualizer` | design_system/SPEC.md, visualizations/site/ | chart-generation, site-update |
| `/builder` | design_system/SPEC.md, deliverables/ | site-deploy, narrative-assembly |
| `/session-start` | CONTEXT.md, CONTEXT_ANDREA.md, CONTEXT_HENNA.md, LOCKBOARD.md | session-management |
| `/session-end` | CONTEXT.md, CONTEXT_ANDREA.md, CONTEXT_HENNA.md, LOCKBOARD.md | session-management |
| `/verify-data` | (target file) | data-verification |

### Layer 3: Reference (loaded on demand)
| File | What | Updated |
|------|------|---------|
| CONTEXT.md | Shared project state, narrative, datasets, key numbers | Every /session-end |
| CONTEXT_ANDREA.md | Andrea's priorities, data gaps, session log | Every /session-end |
| CONTEXT_HENNA.md | Henna's priorities, session log | Every /session-end |
| LEARNINGS.md | Pitfalls, API gotchas, discoveries | When found |
| LOCKBOARD.md | Who's doing what now | When focus shifts |
| datasets/INVENTORY.md | Dataset catalog with provenance | When data changes |
| observations/INDEX.md | Findings, dead ends, theory | Per investigation |
| design_system/SPEC.md | Palette, typography, CSS vars | Rarely |
| 00_Workflow_v04.md | Scale conventions, Rhino rules, LOI/LOG/LOD | Rarely |

### Layer 4: Execution (tools + workflows)
| Directory | What |
|-----------|------|
| `tools/` | Deterministic scripts — one operation each, defined inputs/outputs |
| `workflows/` | Markdown SOPs — step-by-step procedures referencing tools |

Before any repeatable operation: check workflows/ then tools/. See `.claude/rules/tool-protocol.md`.

## Repo structure
```
city101/
├── CLAUDE.md                  ← YOU ARE HERE (router)
├── CONTEXT.md                 ← living project state
├── LEARNINGS.md               ← accumulated pitfalls
├── LOCKBOARD.md               ← who's doing what
├── 00_Workflow_v04.md         ← scale conventions, Rhino rules
├── datasets/                  ← verified production data (INVENTORY.md inside)
├── source/                    ← frozen inputs (classmate data, raw files)
├── tools/                     ← reusable scripts (data/, maps/, git/, util/)
├── workflows/                 ← step-by-step SOPs
├── visualizations/site/       ← scrollytelling site + standalone viz
├── scripts/                   ← ad-hoc processing (not tools)
├── design_system/             ← SPEC.md — visual identity
├── observations/              ← INDEX.md — findings, dead ends
├── output/                    ← staging for agent team work
├── deliverables/              ← narrative drafts, submissions
├── .claude/commands/          ← slash commands (roles + utilities)
├── .claude/rules/             ← auto-loaded conventions
└── .claude/agents/            ← subagent definitions
```

## Key rules (details in .claude/rules/)
- **Coordinates**: Swiss LV95 / EPSG:2056. Web maps use WGS84.
- **File safety**: Never modify originals. Never delete. Ask before writing.
- **Data**: Nothing goes to datasets/ unverified. Agent output → output/ first.
- **Tools**: Check tools/ before building. Ask before creating/modifying tools or workflows.
- **Commits**: Use prefixes — [DATA] [FIND] [DEAD] [MAP] [VIZ] [MODEL] [BUILD] [SYNC]

## Team
| Person | Role |
|--------|------|
| Andrea | Lead — narrative, data, intervention sites |
| Henna | Teammate — thermal, ridership, cultural layers |

Claude accounts: Cairn (Andrea Max), Cairn Code (Claude Code), Lumen (Andrea school), Meridian (Henna school), Cadence (Henna personal).

## API notes
- transport.opendata.ch: 0.35s min between calls
- Google Places: standard limits, works on both accounts
- data.geo.admin.ch: WMS + REST, reasonable delays
- sharedmobility.ch: REST API
- Overpass (OSM): use terminal, not browser
