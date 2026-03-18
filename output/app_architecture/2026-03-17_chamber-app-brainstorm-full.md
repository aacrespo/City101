# Handoff: Chamber App — Concept, Research & Architecture Plan (Full Version)

**From:** DIDI (Andy's assistant repo, `/Users/andreacrespo/CLAUDE/DIDI_2`)
**To:** City101 Claude (studio repo)
**Date:** 2026-03-17 23:14
**Session type:** Brainstorming → research → software architecture planning

---

## What happened this session

Andy brainstormed the evolved concept, app vision, and modeling plan for the studio project. DIDI helped with:

1. **Concept feedback** on the brain dump (3 parts: concept, interface, modeling)
2. **Competitive research** — web search + review of existing `from_codebase_to_corridor/` case studies
3. **Software architecture plan** — full system design for the Chamber App prototype
4. **Plan file created** at `/Users/andreacrespo/CLAUDE/DIDI_2/.claude/plans/distributed-leaping-wreath.md`

---

## The v2 paper is done

`/Users/andreacrespo/CLAUDE/city101/output/city101_vertical_transport_research_v2.md` — 742 lines. It defines:
- Taxonomy of vertical transport systems mapped to the corridor
- 9 nodes selected via quantitative scoring (24 candidates, 5 criteria)
- Chamber concepts for each node (lock type, vertical analogy, circulations, sketch prompts)
- 4 design principles
- Full reference list

**This is the foundation for everything that follows.** The app, the modeling, the midterm — all flow from this paper.

---

## Concept evolution (Andy's brain dump, validated)

### Core metaphor
Vertical elevator → Horizontal elevator. Communes = floors. The corridor = the building.

### Key move
The elevator is anti-architecture (Koolhaas). The horizontal elevator is anti-urban. What "breaks" a vertical elevator is a power outage. What breaks the horizontal elevator is the gap in the 24hr chain (1am-3am, no public transport).

### The chamber
NOT a backup generator. It's the missing link itself. Infrastructure that **holds the gap, not skips it**. The equalizer. The dwell time IS the architecture.

### Beyond healthcare
The typology applies to ANY community with breaks in the 24hr chain. Healthcare is the proof-of-concept. The app makes it repeatable.

---

## Competitive landscape — nobody is doing this

Full research done. Key finding: **no existing tool chains sociological research → temporal analysis → gap identification → typological response → 3D output.**

### Closest tools and their gaps

| Tool | What it does | Gap vs. Andy's concept |
|---|---|---|
| Autodesk Forma | Site-level generative design from physical constraints | Input is geometry, not community. No temporal analysis. |
| Sidewalk Labs Delve | ML-generated neighborhood options with priority sliders | Parameters are financial/geometric, not social. Discontinued May 2024. |
| MIT Senseable City Lab | Maps city dynamics over time with sensor data | Analytics only — no intervention proposal. No typological framework. |
| KPF Urban Interface | Urban data analytics + generative design | Still starts from site/geometry, not community operational chains. |
| UrbanistAI | Participatory AI planning (Helsinki/UNDP) | Preference-based ("what do people want"), not research-based ("what does the chain reveal"). |
| EvoMass (CAADRIA 2024) | Typology-based massing optimization | Form-based typologies, not programmatic. Doesn't derive type from community need. |
| Finch3D / TestFit / Archistar | Generative floor plans / site feasibility | Building-scale only. Assume architecture is the answer. |

### Three genuine innovations in Andy's concept

1. **Input is sociological, not geometric.** Community + region → AI researches operational chain → architecture follows. Every other tool starts from a site.
2. **The typology is new.** The relay-lock chamber doesn't exist in any catalog. "Infrastructure that holds a temporal gap in a community's 24hr chain" is a new category.
3. **The tool can say NO.** "Your region isn't the best spot — the chain breaks elsewhere." No existing generative design tool recommends not building.

### Academic lineage
- Ratti/Senseable City Lab — temporal urban analytics
- Koolhaas — elevator as anti-architecture
- Cedric Price — architecture as time-based intervention
- Rittel — wicked problems, tool helps define the problem

### Existing research in the repo
`/Users/andreacrespo/CLAUDE/City101_ClaudeCode/research/from_codebase_to_corridor/` has:
- `case_collection.md` — 20 detailed case studies (Foster+Partners, KPFui, Archistar, etc.)
- `agentic_workflows_for_architecture.md` — Academic paper on software→architecture pattern transfer
- `section4_expanded.md` — Architecture's unique capabilities beyond software
- These all support the same conclusion: the gap Andy is filling is real.

---

## Software architecture — the Chamber App

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
2. **Chain Explorer** — 24hr timeline, actors, flows, break points
3. **Node Map** — Scored candidates on territory, time slider (day→night)
4. **Chamber Designer** — Weight sliders, trade-off cards, 3D preview
5. **System View** — All nodes as network, coverage, export

### Tech stack
- **Frontend:** Vanilla JS + D3 + Leaflet/MapLibre (matches existing city101 viz stack)
- **Backend:** Python FastAPI
- **AI:** Claude API (Anthropic Python SDK)
- **3D browser:** MapLibre GL (terrain already proven in transport_pulse_v2)
- **3D detail:** Rhino via MCP (live connection for final presentation)
- **Data:** Existing CSVs → JSON. No database.
- **Auth:** None. Local prototype.

### Rhino MCP integration (for final)
App → Backend converts spec to Rhino Python → MCP sends to Rhino → Rhino builds geometry → `capture_viewport` returns render → displayed in browser. The MCP server and tools (`execute_rhinoscript_python_code`, `create_object`, `capture_viewport`, etc.) are already running and tested.

### Data model
Three JSON structures flow between layers:
- **Chain Analysis** (Step 1 output): community, corridor, actors, flows, temporal_breaks
- **Scored Nodes** (Step 2 output): candidates with 5-criteria scores, tiers, decision gate (YES/NO)
- **Chamber Specs** (Step 3 output): per-node lock type, circulations, program, lock sequence, trade-offs

### Build sequence

| Phase | When | Goal |
|---|---|---|
| **0: Foundation** | Next session (1-2 sessions) | Scaffold, design system, pre-load healthcare data, landing page, map with 49 stations |
| **1: Chain Explorer + Breaks** | Before midterm (March 30) | Views 2-3, time slider, node popups. + AI renders + corridor animation for midterm |
| **2: Typology Engine** | April 1-15 | Views 4-5, weight sliders, trade-offs, PDF export |
| **3: AI Research Engine** | April 15-30 | Claude API integration, any community + region, test with non-healthcare |
| **4: 3D + Rhino MCP** | May 1-15 | Browser 3D preview, live Rhino connection, cadastre, construction detail |
| **5: Video + Polish** | May 15-end | Blender/AI 24hr video, second community test, final presentation |

### For midterm (March 30)
- Views 1-3 of the app working (landing, chain explorer, node map with time slider)
- v2 paper presented
- 1 node fully modeled in Rhino (template script established)
- AI-rendered visuals of 2-3 chamber experiences
- Corridor animation (build on transport_pulse_v2 + AI renders)

---

## Key quotes from the session

- "The best defense against being scooped is shipping, not worrying." — on Andy's fear that someone else might build something similar first
- The pipeline Andy imagined independently matched the architecture DIDI designed — strongest signal that the design is inherent to the problem, not imposed on it
- "The v2 paper isn't just research — it's the spec document for the tool."

---

## Open questions

- Which node to model first for midterm? Recommended: Node 4 (Morges) or Node 6 (CHUV)
- Brand identity direction (tmux/command-line aesthetic, how elegant?)
- Which non-healthcare community for generalizability test?
- Blender MCP — not yet connected. Needed for Phase 5.
