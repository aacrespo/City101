# Topology Decisions Log

Append-only. Each entry records a topology choice and why.

---

## 2026-03-26 — IBOIS Knowledge Extraction

**Decision:** Flat parallel for Phase 1 (no coordinator), sequential for Phase 2.

**Why:** Unlike Rhino modeling where agents share geometry and need coordination, these 4 repos are completely independent. No shared state, no interface conflicts, no need for a lead. Each agent clones its own repo, reads code, writes to its own output directory. Adding a coordinator would just burn tokens watching agents that don't need supervision.

Phase 2 is sequential because the integration agent needs all Phase 1 outputs before it can merge databases and write cross-tool scripts.

**Alternative considered:** Hierarchical with coordinator. Rejected — overhead not justified when agents have zero interaction.

**Decision:** Merged RhinoCommon + IBOIS into one plan instead of separate projects.

**Why:** They feed each other. RhinoCommon knowledge makes L3 translations correct (agents know which methods actually exist). IBOIS translations are practice that builds RhinoCommon fluency (translating real C++ into RhinoPython). Separating them means the IBOIS agent guesses at RhinoCommon methods, and the RhinoCommon scrape has no real use case to validate against. Together, Phase 2 scripts can be verified: "does this method exist in the L1 API table?"

**Decision:** Phase 0 and Phase 1 run simultaneously (8 agents total, at team cap).

**Why:** Zero dependencies between RhinoCommon scraping and IBOIS repo extraction. Different sources, different outputs, no shared state. Running sequentially would double wall time for no benefit. If budget is tight, drop forum scrape agent (H) to stay at 7.

**Decision:** Multi-base architecture — archibase (construction), rhinobase (Rhino modeling), iboisbase (timber craft). Not one merged database.

**Why:** Andrea noticed that mixing RhinoCommon API docs with SIA norms felt wrong. Different domains, different reasons to query. The 4-layer pattern (L1 SQLite / L2 Markdown / L3 Code / L4 Vector DB) is domain-agnostic — each base applies it to different knowledge. L3 scripts in city101 bridge the bases.

**Scalability rule:** Promote to a base only when LEARNINGS.md for that domain gets too long. Currently justified: rhinobase (used every modeling session), iboisbase (IBOIS collaboration). Future candidates (blenderbase, geobase) — only when needed. Don't build the richest library nobody opens.

**Decision:** Nice-to-have priority, not blocking midterm.

**Why:** Weekly limit at 60% with 4 days to midterm. Presentation slides, models, and animations are higher priority. But if there's budget headroom after Friday's screen test, Phase 1 (compas_wood alone) would be high-impact for slide 6 (Archibase). The IBOIS meeting brief is the immediate deliverable; the extraction is the follow-through.
