# Prompt: Implementation Plan for "The Extended Architect" §4

## Context
You are building the implementation plan for a multi-agent architectural workflow system. The theory is written — this session is about **execution**. The goal: take the four-system architecture described in the outline and turn it into a concrete, buildable plan with steps, decisions, and dependencies.

Read first:
1. `experiments/extended_architect/OUTLINE.md` — §4 specifically (The Architecture: How It Works)
2. Then load sources as needed:
   - Knowledge system → `/Users/andreacrespo/CLAUDE/DIDI_2/state/multi-agent-cad-research.md` §6
   - Geometric coordination → same doc §5
   - Operational workflow → `workflows/agent-team-modeling.md`
   - Gemini Embeddings → `https://ai.google.dev/gemini-api/docs/embeddings`

## What already exists (don't rebuild these)
- **Rhino Router MCP**: built, working. Routes MCP commands to Rhino instances. Lives in a fork of rhinomcp (`aacrespo/rhinomcp`, branch `feature/configurable-port`).
- **Agent team workflow**: `workflows/agent-team-modeling.md` — tested on Lock 05 CHUV (7 agents, 709 objects). Operational but not connected to knowledge or enforcement systems.
- **City101 repo infrastructure**: CLAUDE.md routing, role commands, session management, staged promotion pipeline. All working.
- **Prototypology pipeline**: site selection → terrain → context → architecture. Working in Rhino via MCP.

## What needs to be built (the four systems from §4)

### System 1: Knowledge System
Four layers, built incrementally:

**Layer 1 — Structured DB (SQLite)**
- Import KBOB v8.02 (embodied energy, GWP, UBP — 608KB Excel, freely available)
- Import SIA reference tables (spans, sections, fire requirements) — summaries only, respect copyright
- Schema: materials table, properties table with source + version tracking, conflict_flag column
- Agent access: `knowledge_query(sql)` tool or equivalent

**Layer 2 — File tree (Markdown)**
- Directory structure proposed in research doc §6.2
- Each file: self-contained, <3K tokens, with README routing per directory
- Priority content: materials/bio-geo-sourced (rammed earth, timber, stone), codes/sia (summaries), typology
- Already partially exists in scattered form across city101 — needs consolidation

**Layer 3 — Parametric scripts (Python)**
- Rhino Python scripts with embedded constraints and validation
- First script: rammed earth wall (height/thickness ratio, compaction reach, thermal mass by climate zone)
- Pattern: validate constraints → generate geometry → annotate with layer/attributes/notes → return or raise ConstraintViolation
- Scripts consume Layer 1 (query DB for material properties) and Layer 2 (read guidelines)
- DO NOT build before Layer 1 exists — scripts that hardcode values they should query are tech debt

**Layer 4 — RAG (Gemini Embeddings → ChromaDB)**
- Target: Dicobat (dictionary-structured, natural chunk boundaries at entries)
- Pipeline: extract text (PyMuPDF) → chunk at entry boundaries → embed with Gemini (gemini-embedding-001 or gemini-embedding-2-preview for multimodal) → store in ChromaDB
- 768 dimensions, RETRIEVAL_DOCUMENT task type for indexing, RETRIEVAL_QUERY for search
- Agent access: `knowledge_search(query, source, top_k)` tool
- Gemini Embedding 2 can embed PDF pages and images directly — construction detail drawings become queryable
- Copyright: vector DB and source PDFs are local-only, .gitignored. Never committed.
- BUILD ONLY when a dense reference work is available (Dicobat PDF, SIA norms). If Andrea doesn't have the PDFs yet, this stays theoretical.

### System 2: Geometric Coordination
Three progressive levels:

**Level 1 — Skill (prompt-level)** — ALREADY EXISTS in agent-team-modeling workflow
- Each agent's prompt specifies layer scope
- No code to write, just prompt discipline

**Level 2 — Tool (MCP-level spatial mutex)** — NEEDS BUILDING
- New MCP tool or Rhino Python function: `claim_zone(agent_id, bbox, layer)` → granted/conflict
- Zone registry: who claimed what, when
- `release_zone(agent_id, zone_id)` when done
- Granularity decision needed: object-level (precise but slow) vs bounding-box (fast but coarse) vs layer-level (current implicit model)
- Implementation: could be a Python dict maintained in the Router, or a SQLite table, or a simple JSON file

**Level 3 — Agent (coordinator)** — FUTURE, not for initial implementation
- Read-all, write-none coordinator agent
- Clash detection after each build round
- Semantic conflict resolution (not just spatial overlap)
- Don't build until Level 2 is tested

### System 3: Execution Infrastructure
- **Local (current)**: single Rhino instance, layer separation. Working.
- **Router (built)**: needs testing with true multi-instance (Henna's Windows machine first, then Azure)
- **Cloud (future)**: Azure VM setup. Not priority for initial implementation.

### System 4: The Blackboard (shared model as coordination medium)
- Currently: Rhino .3dm file with layer groups. Working but not queryable.
- Next step: expose model state to agents in a structured way. The `rhino_get_objects` MCP tool already does this partially.
- Future: Speckle integration for object-level version control, or USD composition if Omniverse becomes relevant.

## Decisions Andrea needs to make
1. **Where does the knowledge system live?** In city101? In DIDI_2? In a new repo? The knowledge tree is project-agnostic (materials, codes, standards apply to any Swiss project). It probably shouldn't be inside a studio-specific repo.
2. **Do you have the Dicobat PDF?** If yes, Layer 4 is buildable now. If no, skip RAG for initial implementation.
3. **KBOB Excel — do you have it or need to download?** It's freely available from KBOB.admin.ch.
4. **Spatial mutex granularity**: start with layer-level (simplest, matches current practice) or go straight to bounding-box?
5. **First parametric script**: rammed earth wall? Or something from the current prototypology work (e.g., a LOG-400 wall script with SIA compliance)?

## Build order (suggested)
```
Phase 1: Knowledge foundation
  1a. Create knowledge/ directory structure (Layer 2 — file tree)
  1b. Import KBOB into SQLite (Layer 1 — structured DB)
  1c. Write first parametric script (Layer 3 — depends on 1a + 1b)

Phase 2: Coordination enforcement
  2a. Implement spatial mutex tool (Level 2 coordination)
  2b. Test with 2-agent parallel build on a simple Lock
  2c. Integrate with agent-team-modeling workflow

Phase 3: Dense reference (if source material available)
  3a. Build Gemini embedding pipeline
  3b. Index Dicobat (or first available reference work)
  3c. Add knowledge_search tool to agent workflow

Phase 4: Multi-instance (requires Windows)
  4a. Test Router with Henna's machine
  4b. Validate multi-instance coordination
  4c. Azure VM setup if needed
```

## Output expected from this session
A concrete implementation plan document with:
- Build order with dependencies
- File/directory structure for the knowledge system
- Schema for the SQLite database
- Interface definitions for new tools (knowledge_query, knowledge_search, claim_zone)
- Which existing files/workflows need modification
- What Andrea needs to provide (PDFs, data files, decisions)
- Estimated scope per phase (is this a session? a week? ongoing?)

## Framing (from the theory conversation)
This isn't infrastructure for its own sake. Every system serves the thesis: **making it economically viable to have more domain perspectives in the room from the start.** The knowledge system IS the domain perspectives. The coordination system lets them coexist. The execution infrastructure lets them run in parallel. Build toward that, not toward architectural elegance.
