# The Extended Architect

**Working title** — The document that unifies six months of practice into one framework.

**Thesis**: The architect's integrative capacity — holding multiple domain constraints simultaneously — can be extended by AI agents carrying domain knowledge. This collapses the cost of early multidisciplinary integration, turning the organigram from an administrative constraint into a design instrument. Consequence: buildings shaped by constraints that traditional practice encounters too late.

**Key insight**: It's not about optimizing toward a known narrative. The brief is the brief. What changes is *who is listening from the start*. AI makes it economically viable to have the builder, the structural engineer, the sustainability consultant all present as agents from Phase 0. The space "talks back" differently when more domains are listening.

---

## Source Documents

| # | Document | Location | Role |
|---|----------|----------|------|
| 1 | From Codebase to Corridor | `observations/research/from_codebase_to_corridor/agentic_workflows_for_architecture.md` | Foundation — software→architecture pattern transfer |
| 2 | Section 4 Expanded | `observations/research/from_codebase_to_corridor/section4_expanded.md` | Frontier — where architecture exceeds software |
| 3 | Organigram as Design Parameter | `experiments/organigram_design_parameter copy.docx` | Theory — Conway's Law, topology as tunable parameter |
| 4 | Multi-Agent CAD Research | `/Users/andreacrespo/CLAUDE/DIDI_2/state/multi-agent-cad-research.md` | Architecture — Router, knowledge layers, collision avoidance |
| 5 | Agent Team Modeling Workflow | `workflows/agent-team-modeling.md` | Operations — how to run a multi-agent build |
| 6 | Gemini Embeddings API | `https://ai.google.dev/gemini-api/docs/embeddings` | Technology — RAG/knowledge Layer 4 |

---

## Structure

### 0. Abstract
One paragraph. The thesis above. AI extends the architect's integrative capacity. The organigram becomes a design instrument. Buildings are shaped by constraints they would otherwise encounter too late.

### 1. The Problem: Who Is in the Room

Architecture is integrative. The architect holds structure, envelope, program, sustainability, circulation, buildability, experience simultaneously. Two limits constrain this:

- **Cognitive**: human working memory holds 5-7 active constraints. Rammed earth example — compaction reach OR thermal mass OR fire code, but not all three while also designing space.
- **Economic**: SIA model places specialists at the phase where their contribution is contractually justified. The builder arrives at execution. By then, design is shaped by their absence.

Not failures of skill or intention. EPFL trains interdisciplinary architects. The limits are structural: people cost money, time is finite, cognition has a ceiling.

*Sources: Doc 3 §1-2, Doc 1 §1*

### 2. What Changes: The Cost of Listening Collapses

AI agents cost tokens, not CHF/hr. Consequences:

- Structural agent present from first sketch, not first coordination meeting
- Buildability agent (craft knowledge — piseur's compaction reach, formwork sequence) constrains geometry at conception, not at tender
- Sustainability agent flags embodied carbon before material is committed

The architect still decides. But decisions are informed by constraints that traditional practice delivers too late — or never.

**From sequential consultation to parallel presence.** Not "design, then check" but "design while constraints are simultaneously active."

*Sources: Doc 4 §4, Doc 3 §5, Doc 2 §4.1*

### 3. The Organigram as Design Instrument

If you can choose who is in the room, when, with what knowledge — the organigram is a design decision with design consequences.

**3.1 — Three tunable dimensions:**
- Communication topology: hierarchical ↔ flat
- Context scope: full visibility ↔ minimal
- Task dependency: sequential ↔ parallel

**3.2 — Phase-adaptive reconfiguration:**
- Discovery (brief → analysis): flat, broad, parallel. Cross-domain surprises. The archipelago emerged from this — nobody tasked an agent with finding it.
- Production (design → documentation): hierarchical, scoped, sequential. Coherence and quality control.
- Mirrors SIA phases but makes transitions explicit and rapid.

**3.3 — Conway's Law, inverted:**
Want integrated building → flat communication from Phase 0. Want modular building → scoped agents. The organigram shapes the building. Design the organigram.

*Sources: Doc 3 §3-5, Doc 1 §2, Doc 5*

### 4. The Architecture: How It Works

Four systems that make the extended architect operational.

**4.1 — Knowledge system** (what agents know):

| Layer | Content | Access |
|---|---|---|
| Structured DB (SQLite) | KBOB, SIA tables, spans | `knowledge_query(sql)` |
| File tree (Markdown) | Typology, precedents, craft | `knowledge_read(path)` |
| Parametric scripts (Python) | Executable constraints | `rhinoscript_execute(script, params)` |
| RAG (Gemini → ChromaDB) | Dicobat, SIA norms, atlases | `knowledge_search(query)` |

Scripts = where knowledge becomes enforcement. ConstraintViolation, not suggestion.
Gemini Embedding 2 = multimodal. Construction detail images become queryable alongside text.

**4.2 — Geometric coordination** (how agents share space):
- Skill (prompt-level): layer discipline. Baseline always.
- Tool (MCP-level): spatial mutex — claim_zone/release_zone.
- Agent (coordinator): read-all, write-none. Clash detection + semantic resolution.

**4.3 — Execution infrastructure:**
- Local: single Rhino, layer separation (demonstrated: 7 agents, 709 objects)
- Router: multi-instance dispatch
- Cloud: Azure VMs for true parallelism

**4.4 — The blackboard:**
Shared spatial model all agents read/write. Not API contracts — composition. USD (Omniverse), iTwin, BIM. The Rhino file with layer groups is a working version.

*Sources: Doc 4 §3-7, Doc 6, Doc 2 §4.2-4.3, Doc 5*

### 5. Proof: City101 and the Locks

**5.1 — City101 corridor analysis** (6 months, 25+ sessions):
- 49 stations, 20+ datasets, 4 Claude accounts, 2 humans
- Six emergent patterns (multi-account coordination, monolithic scripts, staged promotion, living state, canonical entities, LOI/LOG/LOD)
- Flat topology → cross-domain correlations (diversity × frequency × workspace = urban completeness, r = 0.63-0.71)
- Archipelago: space talked back because enough domains were listening

**5.2 — Lock 05 CHUV** (1 session):
- 7 agents, 709 objects, 4 rounds, 1 Rhino file
- First demonstrated parallel multi-agent coordination in live CAD
- What worked / what didn't

**5.3 — Prototypology pipeline** (ongoing):
- Site → terrain → context → architecture, with knowledge + coordination systems from §4
- Locks carry imprint of early integration

*Sources: Doc 1 §2, Doc 4 §3, Doc 5*

### 6. The Frontier

**6.1 — Spatial experience reasoning.** Agents that judge "19.3km breaks continuity" — not just compute distance. Gehl, Space Syntax, "time makes space."

**6.2 — Computational narrative.** Design argument as structured data. IBIS, D-Agree. CONTEXT.md as prototype. Unsolved: connecting independent findings into argument computationally.

**6.3 — Craft knowledge formalization.** The piseur problem. Scripts enforce but can't explain. Formalization that preserves the builder's judgment.

*Sources: Doc 2 §4.1, 4.4, 4.6, Doc 4 §8.3*

### 7. Implications

**Practice:** Architect elevates from coordinator to system designer. Direction générale as design act.

**Education:** Organizational topology as design discipline, not admin skill.

**Profession:** Cost collapse of early integration changes what buildings are possible. Constraint is generative, not decorative.

---

## Status

- [x] Thesis converged (2026-03-19)
- [x] Outline structured
- [ ] Section drafting
- [ ] Internal review / fine-tuning
- [ ] Integration with process booklet / presentation
