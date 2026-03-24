# Lockboard
**Updated**: 2026-03-20

## Both — Review app architecture docs

**Read and discuss together before next Claude Code session:**
- `output/app_architecture/` — 7 files (v1: 6 engine docs + v2: tool/presentation strategy)
- Key docs: `architecture_overview.md` (system diagram), `open_questions.md` (decisions needed), `v2_tool_and_presentation.md` (two-tab structure + midterm show)
- Come back with comments, disagreements, decisions on the open questions (especially Q1.1 chamber schema, Q1.2 transport vs place, Q3.3 story vs tool)

---

## Andrea — A04 midterm

### Active now
- **Agent team prototypology**: Router + workflow proven (7 agents, 709 objects on Lock 05). Ready to scale to remaining nodes.
- **App architecture**: v1 engine docs + v2 tool/presentation strategy complete. Waiting on joint review before implementation.
- **Finalize project concept**: lock down the narrative so Henna can prompt slides from it.

### Next
- **Scale to all 9 nodes** using `workflows/agent-team-modeling.md`
- **PR plugin port fix upstream** to `jingcheng-chen/rhinomcp`
- **Set up Henna** with modified plugin (docs in `experiments/rhino mcp server/SETUP.md`)
- **Implement scoring engine** once arch docs are reviewed and decisions made.

Branch: andrea/prototypology-v2
Since: 18 March 2026

---

## Henna — A04 midterm

### Active now
- **3D corridor modeling**: finish the full corridor with point cloud pipeline. Research already done lives in `observations/research/` and `output/city101_hub/`.
- **MCP investigation**: Blender + Rhino MCPs for the app visualization layer.
- **Architectural references**: Koolhaas, Jane Jacobs, other references from v2 paper (`deliverables/A04/city101_vertical_transport_research_v2.md`). Deepen concept grounding.
- **Rework PowerPoint**: redesign how we explain the AI workflow to architecture students who don't know what repos, git, .claude, CLAUDE.md, backend/frontend are. Make it legible to non-technical audience.
- **Brand identity**: find the balance between tmux terminal aesthetic and elegant architecture presentation. The aesthetic shifts per slide depending on the nature of the concept. Showcase how terminal displays, markdown files, VS Code visuals can be art in themselves.

Branch: main
Since: 18 March 2026

---

## Claude — Archibase knowledge pipeline

### Done (2026-03-22)
- Deplazes + Vittone PDFs extracted → 14 curated markdown files (layer buildups, dimensions)
- EPFL coursework scanned → INDEX written (50+ files identified)
- SQLite expanded → 99 rows (sizing rules, insulation, glazing, soil bearing)
- Vision embedder built → Gemini Embedding 2 via Vertex AI
- Deplazes (470p) + Vittone (1016p) embedded in ChromaDB (2,480 entries)
- Training Session 2 complete → 7 exercises, 105 objects, 13 learnings
- YouTube embedding plan written

### Next session
- **Migrate ChromaDB → Qdrant**: ChromaDB segfaults on large collections. Move 2,480 existing vision entries to Qdrant (local, free). Zero re-embedding cost if migration works.
- **Continue embedding**: SIA norms (21 PDFs), Bloomsbury (13 chapters), Dicobat Visuel — blocked by DB migration
- **YouTube tutorial embedding**: paused until DB stable. Plan + tool ready. Other session has videos downloaded.
- **Flash vs Pro comparison**: test Gemini Flash quality on construction details (free quota resets daily)
- **Exercise generation from book pages**: one Gemini call per page → exercise spec + assembly sequence + reference image

### Blocked
- ChromaDB instability — need DB migration before adding more content
- Gemini generation models not accessible on Vertex AI ($300 credits) — need to resolve auth or use AI Studio with billing
