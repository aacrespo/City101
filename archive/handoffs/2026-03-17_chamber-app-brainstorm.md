# Handoff: Chamber App — Concept, Research & Architecture Plan

**Date:** 2026-03-17
**Session:** Concept brainstorm + competitive research + software architecture
**Team:** Andrea & Henna (concept development), Andrea (technical research & architecture)

---

## Summary

Following today's concept discussions between Andrea and Henna, a full software architecture plan was developed for the **Chamber App** — a tool that makes the relay-lock typology repeatable for any community in any region. Competitive research confirms no existing tool covers this pipeline. The plan is ready for implementation starting next session.

**Plan file:** `.claude/plans/distributed-leaping-wreath.md` (in DIDI_2 repo — copy relevant sections here as needed)

---

## Concept (evolved since March 10, discussed with Henna today)

### Core metaphor
Vertical elevator → Horizontal elevator. Communes = floors. The corridor = the building.

### Key move
The elevator is anti-architecture (Koolhaas). The horizontal elevator is anti-urban. What "breaks" a vertical elevator is a power outage. What breaks the horizontal elevator is the gap in the 24hr chain (01:00–03:00, no public transport).

### The chamber
Not a backup generator. It's the missing link itself. Infrastructure that **holds the gap, not skips it**. The equalizer. The dwell time IS the architecture.

### Beyond healthcare
The typology applies to any community with breaks in the 24hr chain. Healthcare is the proof-of-concept. The app makes it repeatable. Bakeries (early shifts, lab-to-shop transport) is one example discussed — many more exist.

### The interface vision
A tool where the typology can be applied to any community/region:
1. User input: "I want to solve [community]'s problem in [region]"
2. AI researches that community's full chain
3. Identifies breaking points along the corridor
4. AI is critical — can say "your region isn't the best spot, here's where the chain actually breaks"
5. Proposes solution with AI-generated 3D preview
6. User adjusts weights (visibility vs carbon, comfort vs footprint, etc.)
7. Shows compromises per proposition
8. Generates outputs: spec sheet, 3D model script, possibly 24hr usage video

---

## Competitive research — the gap is real

No existing tool chains **sociological research → temporal analysis → gap identification → typological response → 3D output.**

| Tool | What it does | Gap |
|---|---|---|
| Autodesk Forma | Site-level generative design | Input is geometry, not community. No temporal analysis. |
| Sidewalk Labs Delve | ML neighborhood options | Parameters financial/geometric, not social. Discontinued. |
| MIT Senseable City Lab | Maps city dynamics over time | Analytics only — no intervention proposal. |
| KPF Urban Interface | Urban data analytics + generative design | Starts from site, not community operational chains. |
| UrbanistAI (Helsinki/UNDP) | Participatory AI planning | Preference-based, not research-based. |
| EvoMass (CAADRIA 2024) | Typology-based massing optimization | Form-based, not programmatic. |
| Finch3D / TestFit / Archistar | Generative plans / site feasibility | Building-scale. Assume architecture is the answer. |

### Three innovations

1. **Input is sociological, not geometric.** Community + region → AI researches operational chain → architecture follows.
2. **The typology is new.** "Infrastructure that holds a temporal gap in a community's 24hr chain" is a new architectural category.
3. **The tool can say NO.** It evaluates whether architecture is the right answer. No existing generative tool does this.

### Academic lineage
- Ratti/Senseable City Lab — temporal urban analytics
- Koolhaas — elevator as anti-architecture
- Cedric Price — architecture as time-based intervention
- Rittel — wicked problems, tool helps define the problem

The `research/from_codebase_to_corridor/` folder in City101_ClaudeCode has 20 case studies and the agentic workflows paper — all support this positioning.

---

## Software architecture

### Three-layer pipeline

```
USER INTERFACE (browser)
  Community Input → Chain Explorer → Chamber Designer → Output Export
        │                │                │               │
TYPOLOGY ENGINE
  Break Scorer → Lock Matcher → Trade-off Calculator
        │
RESEARCH ENGINE
  Claude API → Data Fetchers (OSM, transit) → Territory Mapper
```

### Five views
1. **Landing** — "I want to solve [community]'s problem in [region]"
2. **Chain Explorer** — 24hr timeline, actors, flows, break points highlighted
3. **Node Map** — Scored candidates on territory, time slider (day→night)
4. **Chamber Designer** — Weight sliders, trade-off cards, 3D preview
5. **System View** — All nodes as network, coverage analysis, export

### Tech stack
| Component | Choice | Rationale |
|---|---|---|
| Frontend | Vanilla JS + D3 + Leaflet/MapLibre | Matches existing city101 viz stack |
| Backend | Python FastAPI | Matches existing pipeline scripts |
| AI | Claude API (Anthropic Python SDK) | v2 paper IS the prompt engineering prototype |
| 3D browser | MapLibre GL | Terrain already proven in transport_pulse_v2 |
| 3D detail | Rhino via MCP | Live connection for final presentation |
| Data | Existing CSVs → JSON | No database needed |

### Rhino MCP integration (for final)
```
APP (browser) → BACKEND (FastAPI) → MCP → RHINO (local)
                                         → builds geometry
                                         → capture_viewport
                                    ← render image returned
              ← displayed in browser
```
Backend translates JSON chamber specs into Rhino Python commands. MCP tools already running: `execute_rhinoscript_python_code`, `create_object`, `capture_viewport`, `create_layer`, etc.

### Data model (3 JSON structures between layers)
- **Chain Analysis**: community, corridor, actors, flows, temporal_breaks
- **Scored Nodes**: candidates with 5-criteria scores, tiers, YES/NO decision gate
- **Chamber Specs**: per-node lock type, circulations, program, lock sequence, trade-offs

---

## Build sequence

| Phase | When | Goal |
|---|---|---|
| **0: Foundation** | Next build session | Scaffold at `city101/app/`, design system, pre-load healthcare data, map with 49 stations |
| **1: Chain Explorer + Breaks** | Before midterm (March 30) | Views 2-3, time slider, node popups + AI renders + corridor animation |
| **2: Typology Engine** | April 1-15 | Views 4-5, weight sliders, trade-offs, PDF export |
| **3: AI Research Engine** | April 15-30 | Claude API, any community + region, test non-healthcare |
| **4: 3D + Rhino MCP** | May 1-15 | Browser 3D, live Rhino, cadastre, construction detail (1 node) |
| **5: Video + Polish** | May 15-end | Blender/AI 24hr video, second community, final presentation |

### Midterm deliverables (March 30)
- Views 1-3 of the app working
- v2 paper presented
- 1 node fully modeled in Rhino (template script)
- AI-rendered visuals of 2-3 chamber experiences
- Corridor animation (transport_pulse_v2 + AI renders)

### Final deliverables (end of May)
- Full 5-view app with live Claude API
- Live Rhino MCP connection (adjust weights → chamber updates)
- 24hr usage video (Blender/AI, 4 circulations)
- Cadastre integration + construction detail
- Second community test (generalizability proof)

---

## Building blocks already in this repo

- **9 D3/Leaflet visualizations** (`visualizations/`)
- **MapLibre 3D terrain animation** (`output/transport_pulse_v2/`)
- **Design system** (`design_system/SPEC.md`) — evolving toward tmux/terminal aesthetic
- **Map module** (`visualizations/site/city101_maps.js`, `city101_geodata.js`)
- **All datasets** (`datasets/` — CSV, GeoJSON, ready to convert to JSON)
- **Python pipeline** (`scripts/` — modular, agent-based)
- **v2 paper** (`output/city101_vertical_transport_research_v2.md`) — defines all 9 nodes

Phase 0 ports these into the app scaffold at `city101/app/`.

---

## Open questions

- Which node to model first? Recommendation: Node 4 (Morges) or Node 6 (CHUV) — richest concepts
- Brand identity refinement — tmux-inspired, how far toward elegant?
- Which non-healthcare community for generalizability? (bakeries, logistics, education?)
- Blender MCP — not yet connected, needed for Phase 5 video
