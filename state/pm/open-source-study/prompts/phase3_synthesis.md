# Phase 3: Synthesis + Integration

**Project:** open-source-study
**Status:** ACTIVE
**Estimated:** ~30 min
**Dependencies:** Phases 0, 1A, 1B, 2 all complete

---

<context>
All research phases are done. You now have:
- `output/open-source-study/compas_patterns.md` — COMPAS architecture, adopt/skip/adapt decisions
- `output/open-source-study/lca_schema_comparison.md` — HdM Calc schema, field mapping, proposed assembly table
- `output/open-source-study/data_on_geometry_pattern.md` — our data-on-geometry design for rhinobase
- `output/open-source-study/environmental_layer.md` — Ladybug survey, integration recommendation

Existing projects to update:
- `state/pm/rhinobase-iboisbase/master_plan.md` — knowledge base expansion
- `state/pm/knowledge-infrastructure/` — feedback loop with case_notes
- `state/pm/fabrication-bridge/` — note: this one only has a framework doc, not a full master plan yet

The goal: pull everything together and update the existing projects with concrete learnings. No vague items — everything is either adopted (with spec), rejected (with reason), or deferred (with trigger condition).
</context>

<instructions>

## Tasks

### 1. Read all phase outputs
Read all four documents from output/open-source-study/. Note the key decisions from each.

### 2. Update rhinobase-iboisbase
Based on COMPAS patterns (Phase 0) and data-on-geometry design (Phase 1B):
- Should rhinobase adopt COMPAS datastructures or build its own?
- Does the data-on-geometry design change the rhinobase phase plan?
- Update the master plan with specific additions/changes. Mark what came from this study.

### 3. Update knowledge-infrastructure
Based on environmental layer recommendation (Phase 2):
- Does environmental data feed into the feedback loop?
- Any new case_notes categories needed?
- Update the project plan if applicable.

### 4. Update fabrication-bridge
Based on LCA schema (Phase 1A):
- Proposed assembly table → does it go into archibase L1?
- KBOB field mapping → any schema changes needed?
- Per-lock supply chain comparison → does the HdM snapshot format help?

### 5. Write synthesis

## Deliverable

Write `output/open-source-study/synthesis.md`:

```markdown
# Open Source Study — Synthesis

## What we studied
[One-paragraph summary of the four phases]

## Key decisions
| Decision | Source | Feeds into | Status |
|----------|--------|-----------|--------|
| ... | Phase N | project-id | Adopted / Rejected / Deferred |

## What changes in each project

### rhinobase-iboisbase
[Bullet list of concrete changes to the master plan]

### knowledge-infrastructure
[Bullet list of concrete changes]

### fabrication-bridge
[Bullet list of concrete changes]

## What we're NOT doing (and why)
[Rejected options with reasoning — important for future reference]

## Deferred items
| Item | Trigger to revisit | From |
|------|-------------------|------|
| ... | ... | Phase N |

## Surprise findings
[Anything unexpected that doesn't fit the existing projects]
```

Also append a summary to `state/pm/topology_history.md`.

</instructions>

<verification>
- [ ] Every Phase 0-2 output is referenced
- [ ] Each existing project has at least one concrete update (not just "consider X")
- [ ] Rejected items have specific reasons
- [ ] Deferred items have trigger conditions (not "someday")
- [ ] No open-ended "we should look into" items remain
</verification>
