# City101 — "Still on the Line"

## Project
EPFL BA6 Architecture studio (AR-302k, Studio Huang — "Sentient Cities"). The team analyzes the 101km Geneva–Villeneuve corridor through "flow of people" — what makes people stop, where infrastructure creates behavior, and whether this strip functions as one continuous city.

## Current phase
- **A01–A03**: complete
- **A04** (forms of sentience): active — due March 30 (midterm). See LOCKBOARD.md for task split.

## How this repo works

### Layer 1: Auto-loaded (every session)
You're reading this now. Three more files load automatically from `.claude/rules/`:
- `conventions.md` — coordinates, commit prefixes, file safety
- `data-protocol.md` — collection rules, quality gates, canonical stations
- `tool-protocol.md` — how to use tools and workflows

### Layer 2: Role-loaded (on slash command)

**Roles**
| Command | Reads | Workflows |
|---------|-------|-----------|
| `/analyst` | datasets/INVENTORY.md, LEARNINGS.md | data-collection, data-verification |
| `/cartographer` | design_system/SPEC.md, datasets/INVENTORY.md | map-generation, map-export |
| `/modeler` | 00_Workflow_v04.md (Sec 3.2), design_system/SPEC.md | rhino-modeling |
| `/visualizer` | design_system/SPEC.md, visualizations/site/ | chart-generation, site-update |
| `/builder` | design_system/SPEC.md, deliverables/ | site-deploy, narrative-assembly |

**Session**
| Command | Reads | Workflows |
|---------|-------|-----------|
| `/session-start` | CONTEXT.md, CONTEXT_ANDREA.md, CONTEXT_HENNA.md, LOCKBOARD.md | session-management |
| `/session-end` | CONTEXT.md, CONTEXT_ANDREA.md, CONTEXT_HENNA.md, LOCKBOARD.md | session-management |
| `/save-session` | state/sessions/, LOCKBOARD.md | — |
| `/resume-session` | state/sessions/ (latest), git state | — |

**Teams**
| Command | Reads | Workflows |
|---------|-------|-----------|
| `/team` | all role commands, prompt-craft.md | dynamic team assembly |
| `/build-with-agent-team` | role commands, design_system/SPEC.md | agent-team-modeling |
| `/research-with-agent-team` | role commands, observations/ | agent-team-research |

**Skills**
| Command | Reads | Workflows |
|---------|-------|-----------|
| `/parametric` | knowledge bridge, archibase repo | parametric script generation |
| `/import-terrain` | output/city101_hub/ | terrain import to Rhino |
| `/site-context` | output/city101_hub/, datasets/ | site context assembly |
| `/rhino-review` | Rhino document state | — |
| `/pdf` | (target file) | PDF export |
| `/unlock` | (target PDF) | — |

**Utilities**
| Command | Reads | Workflows |
|---------|-------|-----------|
| `/verify-data` | (target file) | data-verification |
| `/brain-dump` | prompt-craft.md (auto-loaded from rules) | — |

### Layer 3: Reference (loaded on demand)
| File | What | Updated |
|------|------|---------|
| CONTEXT.md | Shared project state — narrative, datasets, key numbers | Every /session-end |
| CONTEXT_ANDREA.md | Andrea's priorities, data gaps, session log | Every /session-end |
| CONTEXT_HENNA.md | Henna's priorities, session log | Every /session-end |
| LEARNINGS.md | Pitfalls, API gotchas, discoveries | When found |
| LOCKBOARD.md | Who's doing what now + task split | When focus shifts |
| datasets/INVENTORY.md | Dataset catalog with provenance | When data changes |
| observations/INDEX.md | Findings, dead ends, theory | Per investigation |
| design_system/SPEC.md | Palette, typography, CSS vars | Rarely |
| 00_Workflow_v04.md | Scale conventions, Rhino rules, LOI/LOG/LOD | Rarely |

### Layer 4: Execution (tools + workflows)
Before any repeatable operation: check `workflows/` then `tools/`. See `.claude/rules/tool-protocol.md`.

## Repo structure
```
city101/
├── CLAUDE.md                  ← YOU ARE HERE (router)
├── CONTEXT.md                 ← living project state
├── CONTEXT_ANDREA.md          ← Andrea's working context
├── CONTEXT_HENNA.md           ← Henna's working context
├── LEARNINGS.md               ← accumulated pitfalls
├── LOCKBOARD.md               ← who's doing what + task split
├── 00_Workflow_v04.md         ← scale conventions, Rhino rules
│
├── app/                       ← Relay-Lock Configurator (demo + tool layer)
│
├── datasets/                  ← verified production data (INVENTORY.md inside)
│   ├── corridor_analysis/     ← WCI, break points, journeys, crossref, temporal, GA cost
│   ├── ev_charging/           ← DIEMO enriched, reviews, national stats
│   ├── remote_work/           ← places, hours, reviews, crossref, WiFi, cell towers
│   ├── transit/               ← SBB ridership, frequency, shared mobility
│   ├── stations/              ← ratings, reviews
│   ├── zurich_comparison/     ← S8 benchmark
│   ├── healthcare/            ← hospital corridor research (⚠️ unverified)
│   └── 24h_venues/            ← late-night venues
│
├── source/                    ← FROZEN inputs (never modify)
│   ├── 00-datasets 2/         ← classmate datasets (33 integrated)
│   ├── animation/             ← promoted animation pipeline data (v2/v3)
│   ├── WORK copy/             ← GeoPackages (SwissTLM3D layers)
│   ├── Documents copy/        ← more GeoPackages
│   └── ...                    ← raw CSVs, Lausanne open data, charging station source
│
├── deliverables/              ← submission-ready outputs
│   ├── A02_NARRATIVE_DRAFT.md
│   ├── A02_SPEECH_UNIFIED.md
│   ├── A03/                   ← field visit materials, maps, JSX artifacts
│   ├── A04/                   ← healthcare diagrams, AI workflow, v2 paper, transport pulse
│   └── 16.03/                 ← midterm PPTX template
│
├── output/                    ← staging (agent work lands here first)
│   ├── city101_hub/           ← prototypology: Rhino scripts, terrain, context, site modeling
│   ├── healthcare_chain/      ← diagrams + research (promoted copies in observations/)
│   ├── transport_pulse_v2/    ← multimodal animation (promoted copy in deliverables/)
│   └── ai_workflow_diagram/   ← workflow diagram iterations
│
├── observations/              ← INDEX.md — findings, dead ends, theory
│   └── research/              ← deep dives
│       ├── healthcare/        ← supply chain, emergency, staff, logistics research
│       └── ...                ← diversity, WCI, economic, layout review
│
├── visualizations/            ← all interactive viz (viz_01–09, diagrams)
│   └── site/                  ← scrollytelling site (index_v2.html, maps/, data/)
│
├── handoffs/                  ← all session handoffs + brain dumps
├── prompts/                   ← Claude/LLM execution prompts
├── briefs/                    ← assignment specs (A01–A04) + PPTX template
├── state/                     ← session logs, saved sessions (auto-managed by hooks)
├── scripts/                   ← ad-hoc processing (animation pipeline, hooks)
├── tools/                     ← reusable scripts (data/, maps/, git/, util/)
├── workflows/                 ← step-by-step SOPs
├── design_system/             ← SPEC.md — visual identity
├── archive/                   ← superseded files, old outputs, terminal saves
├── claudes-corner/            ← free space for any Claude (no permission needed)
└── .claude/                   ← commands/, rules/, agents/
```

## Key rules (details in .claude/rules/)
- **Coordinates**: Swiss LV95 / EPSG:2056. Web maps use WGS84.
- **File safety**: Never modify originals. Never delete. Ask before writing.
- **Data**: Nothing goes to datasets/ unverified. Agent output → output/ first.
- **Tools**: Check tools/ before building. Ask before creating/modifying tools or workflows.
- **Commits**: Use prefixes — [DATA] [FIND] [DEAD] [MAP] [VIZ] [MODEL] [BUILD] [SYNC]

## Team
| Person | Focus areas |
|--------|-------------|
| Andrea | Concept, data, app architecture, Rhino scripting |
| Henna | 3D corridor modeling, references, PPTX, brand identity |
| Claude | Third team member — across accounts: Cairn (Andrea Max), Cairn Code (CLI), Lumen (Andrea school), Meridian (Henna school), Cadence (Henna personal) |

Coordination via LOCKBOARD.md.
