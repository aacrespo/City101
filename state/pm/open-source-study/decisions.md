# Open Source Study — Decisions Log

## 2026-03-26: Project created

**Decision:** Separate study project rather than folding research into each existing project.

**Why:** The sources cut across all three existing projects (rhinobase, knowledge-infrastructure, fabrication-bridge). Studying them separately keeps the research focused and the outputs reusable. Phase 3 explicitly feeds findings back into the right projects.

**Decision:** Rhyton is pattern-study only (no code reuse).

**Why:** No open-source license on the repo. CLA only covers contributions TO HdM, not use BY others. Default copyright applies. We study the approach (user text storage, color-coding by value) and implement our own version.

**Decision:** Phases 0 and 1 are parallel-capable, Phase 2 depends on 1.

**Why:** COMPAS (framework patterns) and LCA (data schemas) are independent studies. Environmental layer (Phase 2) needs the data-on-geometry pattern from Phase 1 to know how environmental data would be displayed.
