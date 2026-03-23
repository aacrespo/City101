---
Compaction at: 2026-03-20 15:09
Branch: andrea/prototypology-v2

## Lockboard snapshot
# Lockboard
**Updated**: 2026-03-18

## Both — Review app architecture docs

**Read and discuss together before next Claude Code session:**
- `output/app_architecture/` — 7 files (v1: 6 engine docs + v2: tool/presentation strategy)
- Key docs: `architecture_overview.md` (system diagram), `open_questions.md` (decisions needed), `v2_tool_and_presentation.md` (two-tab structure + midterm show)
- Come back with comments, disagreements, decisions on the open questions (especially Q1.1 chamber schema, Q1.2 transport vs place, Q3.3 story vs tool)

---

## Andrea — A04 midterm

### Active now
- **App architecture**: v1 engine docs + v2 tool/presentation strategy complete. Waiting on joint review before implementation.
- **Repo cleanup + context updates**: restructure files, update CLAUDE.md/CONTEXT.md, organize research for Henna's access.
- **Finalize project concept**: lock down the narrative so Henna can prompt slides from it.

### Next
- **LOG 400 modeling upgrades**: training round / first iterations on the scaffolding. Testing the review pipeline, integrating learnings back into app/software dev steps. Goal = template scripts for prototypology scalability.
- **Check other repo** (`~/CLAUDE/???`) for useful commands, automations, hooks to import.
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

## Blocked
- (nothing currently)

## Recent git
e39e1b1 [SYNC] Save session: Extended Architect theory converged, outline + prompts
78686eb [SYNC] Save session: Extended Architect draft complete — 8 sections, ~8,500 words
896eca8 [SYNC] Save session: Agent Teams test + modeling workflow
51a1398 [MODEL] Re-site Lock 03 Morges: ground level at (-60, 0, 381.5)
ce9b5d7 [MODEL] Wave 4 — LOG 400 upgrade for Morges Temporal Lock

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M output/city101_hub/site_modeling/wave4_upgrade_log.md
 M state/session-log.md
?? .obsidian/
?? Untitled.canvas
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/"
?? output/app_architecture/ARCHITECTURE_DESIGN_DOC.docx
?? output/app_architecture/ARCHITECTURE_DESIGN_DOC.md
?? output/app_architecture/architecture_diagram.html
?? output/app_architecture/build_docx.py
?? output/app_architecture/configurator_prototype.html
?? output/app_architecture/convert_to_png.py
?? output/app_architecture/create_diagrams.py
?? output/app_architecture/diagrams/
?? output/city101_hub/site_modeling/analyze_walking_route.py
?? output/lock_siting_audit/
?? output/research_app_tooling_landscape.md
?? output/research_ibois_comp_design.md
?? prompts/PROMPT_lock_siting_audit.md
?? prompts/PROMPT_wave4_log400_upgrade.md
?? state/pre-compact-snapshot.md
---
Compaction at: 2026-03-21 11:07
Branch: andrea/prototypology-v2

## Lockboard snapshot
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

## Blocked
- (nothing currently)

## Recent git
5457add Add /parametric skill for knowledge-grounded script generation
d9b3aee Add knowledge bridge to standalone construction-knowledge repo
fe792f3 [SYNC] Save session: v2 workflow design — output paths + coordinator guide
892385b [MODEL] Agent team modeling workflow v2 — output strategy + coordinator guide
29a0b8c [MODEL] Lock 05 CHUV: facade base reveal + canopy drip edge (agent free improvement)

## Uncommitted
 M .claude/settings.local.json
 M state/session-log.md
?? .obsidian/
?? Untitled.canvas
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? output/app_architecture/ARCHITECTURE_DESIGN_DOC.docx
?? output/app_architecture/ARCHITECTURE_DESIGN_DOC.md
?? output/app_architecture/architecture_diagram.html
?? output/app_architecture/build_docx.py
?? output/app_architecture/configurator_prototype.html
?? output/app_architecture/convert_to_png.py
?? output/app_architecture/create_diagrams.py
?? output/app_architecture/diagrams/
?? output/city101_hub/site_modeling/analyze_walking_route.py
?? output/dicobat/
?? output/research_app_tooling_landscape.md
?? output/research_ibois_comp_design.md
?? prompts/PROMPT_wave4_log400_upgrade.md
?? state/pre-compact-snapshot.md
---
Compaction at: 2026-03-21 23:45
Branch: main

## Lockboard snapshot
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

## Blocked
- (nothing currently)

## Recent git
4f71238 [MODEL] POC archibase → agent team → Rhino: wall, cabin, team build
d1facce [SYNC] Make archibase path configurable — ARCHIBASE_PATH env var
7b2d30f [SYNC] Switch to router MCP config, add Rhino MCP rule
f24c9e3 Merge branch 'main' of https://github.com/aacrespo/City101
fcfbdb5 Merge andrea/prototypology-v2: repo hygiene, app promotion, archibase rename

## Uncommitted
 M .claude/agents/knowledge/learnings-walls.md
 M .claude/agents/knowledge/rhino-playbook.md
 M .claude/settings.local.json
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
---
Compaction at: 2026-03-22 01:30
Branch: main

## Lockboard snapshot
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

## Blocked
- (nothing currently)

## Recent git
d393813 [SYNC] Cabin v3 session save: 825 objects, workflow v2.2, all learnings
8e1621a [SYNC] Session log break marker + snapshot update
3bf263f [SYNC] Cabin v2 learnings: playbook, workflow v2.1, session save
4f71238 [MODEL] POC archibase → agent team → Rhino: wall, cabin, team build
d1facce [SYNC] Make archibase path configurable — ARCHIBASE_PATH env var

## Uncommitted
 M .claude/settings.local.json
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .claude/agents/knowledge/learnings-circulation.md
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
---
Compaction at: 2026-03-22 01:33
Branch: main

## Lockboard snapshot
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

## Blocked
- (nothing currently)

## Recent git
d393813 [SYNC] Cabin v3 session save: 825 objects, workflow v2.2, all learnings
8e1621a [SYNC] Session log break marker + snapshot update
3bf263f [SYNC] Cabin v2 learnings: playbook, workflow v2.1, session save
4f71238 [MODEL] POC archibase → agent team → Rhino: wall, cabin, team build
d1facce [SYNC] Make archibase path configurable — ARCHIBASE_PATH env var

## Uncommitted
 M .claude/agents/knowledge/learnings-review.md
 M .claude/settings.local.json
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .claude/agents/knowledge/learnings-circulation.md
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
---
Compaction at: 2026-03-22 10:56
Branch: main

## Lockboard snapshot
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

## Blocked
- (nothing currently)

## Recent git
92d74ce [SYNC] Session save: training curriculum + LOG + legal framework
ce72302 [SYNC] Agent training curriculum: 10 exercises + furniture library + session prompt
6cf6bc9 [SYNC] Workflow: add per-element LOG definitions (Section 2.5)
5488906 [SYNC] Save session: repo hygiene complete, archibase wired, PoC ready
9eab144 [SYNC] Session save: playbook v3 + legal knowledge framework

## Uncommitted
 M .claude/agents/knowledge/rhino-playbook.md
 M .claude/settings.local.json
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/furniture/
---
Compaction at: 2026-03-22 19:18
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:21
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:22
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:23
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:24
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:26
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:33
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:33
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:43
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:43
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:43
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
---
Compaction at: 2026-03-22 19:48
Branch: main

## Lockboard snapshot
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

## Recent git
112d79d [SYNC] Session end: knowledge pipeline complete, DB migration queued
610d854 [SYNC] Save session: YouTube embedding pipeline, 11/32 videos processed
58a642e henna presentation
1b339d6 new brand identity
97c846c Merge branch 'main' of https://github.com/aacrespo/City101

## Uncommitted
 M .claude/settings.local.json
 M LEARNINGS.md
 M state/pre-compact-snapshot.md
 M state/session-log.md
?? .env.example
?? "experiments/organigram_design_parameter copy.docx"
?? "experiments/rhino mcp server.zip"
?? "experiments/rhino mcp server/TEST_PROMPTS_WINDOWS.md"
?? output/agent_training/DISTILLED_LEARNINGS.md
?? output/agent_training/FULL_CURRICULUM.md
?? output/agent_training/learnings/
?? output/agent_training/log_modeler-1.md
?? output/agent_training/log_modeler-2.md
?? output/agent_training/log_modeler-3.md
?? output/agent_training/log_modeler-4.md
?? output/agent_training/log_reviewer-constraints.md
?? output/agent_training/log_reviewer-visual.md
?? output/agent_training/visual_review/
?? prompts/[A04_ACTIVE]_full_training_curriculum_execution.md
