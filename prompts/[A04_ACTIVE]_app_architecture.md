# Prompt: App Architecture — "Still on the Line" Typology Interface

## Role
You are a systems architect designing the architecture for an interactive interface that applies an architectural typology ("the chamber" / "relay-lock") to different communities and regions along a 101km corridor (Geneva–Villeneuve, Switzerland).

## Context
Read these files first:
1. `output/braindump_2026-03-17_three-things.md` — Section 2 (The Interface / App Vision) is the primary input
2. `output/city101_vertical_transport_research_v2.md` — the research paper defining the typology, 9 nodes, and scoring framework
3. `CONTEXT.md` — current project state, the 9-node table, defined vs open questions

## What the interface does (user story)

A user comes to the interface and says: "I want to apply the Still on the Line typology to solve [community]'s problem in [region]."

The system then:
1. **Researches** the community's 24hr chain (work patterns, transport needs, breaking points)
2. **Maps breaking points** along the corridor for that community
3. **Evaluates** whether the user's chosen region matches the actual breaking points — pushes back if not
4. **Proposes solutions** — best compromise considering typology values, with visual preview
5. **Lets user adjust weights** — parameter panel for criteria (visibility, carbon footprint, comfort, etc.)
6. **Generates outputs**: spec sheet, 3D preview, Rhino script, possibly 24hr usage video

## What you need to design

Create a Mermaid diagram (or set of diagrams) covering:

### 1. System architecture
- What are the modules/services?
- What data flows between them?
- What's the AI layer vs the deterministic layer?
- Where does Rhino/MCP fit? (local tool vs server-side?)

### 2. Data model
- What inputs does the system need? (corridor data, cadastre, transport schedules, community-specific research)
- What does the typology "know"? (the defined variables from the v2 paper — lock types, scoring criteria, four circulations, threshold sequence)
- What's computed vs what's configured?

### 3. Decision logic
- How does the system select which lock type fits a community?
- How does the scoring framework (5 criteria from v2 paper) apply to new communities?
- How do user weight adjustments modify the proposition?
- What are the fixed constraints vs flexible parameters?

### 4. Output pipeline
- Spec sheet generation
- 3D preview (web-based, likely Three.js or OSM 3D)
- Rhino script generation (.py for RhinoCommon)
- How these connect — same data model feeding different renderers?

### 5. Phasing
- **Midterm (March 30)**: What's the minimum viable demo? (Healthcare only, hardcoded, show the logic)
- **Post-midterm**: What unlocks the "any community" expansion?
- **Stretch**: What makes it work for any Swiss city?

## Constraints
- This is an architecture student project, not a startup. The interface is a design tool and a demonstration of the typology's applicability.
- Healthcare is the only fully researched community. All others would need AI-driven research at runtime.
- Existing assets: 3 Rhino scripts (LOG 200-300), an HTML prototypology explorer, 9-node scoring framework, extensive corridor data (see `datasets/INVENTORY.md`).
- Mermaid.js for diagrams. Output as `.md` files with embedded Mermaid blocks.
- Frame as human-AI collaboration / skill environment, NOT "agentic workflow."

## Output
Write to `output/app_architecture/`:
1. `architecture_overview.md` — system diagram + module descriptions
2. `data_flow.md` — what data moves where, what format
3. `decision_logic.md` — how the typology selection works
4. `output_pipeline.md` — how outputs get generated
5. `phasing.md` — what to build when
6. `open_questions.md` — things that need Andrea + Henna input before implementation

Use Mermaid blocks for all diagrams. Keep prose minimal — diagrams first, explanations second.
