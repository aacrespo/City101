# PM: Lock Type 02 — Cargo Lock LOG400
**Project ID**: henna-lock02-cargo-log400
**Owner**: Henna
**Created**: 2026-03-27
**Deadline**: 2026-03-30 (midterm)
**Goal**: Upgrade Lock 02 Cargo from LOG200 base concept to full LOG400 — especially the missing roof system — and build it in Rhino on port 9002.

---

## Context

The base Lock 02 Cargo concept (LOG200–300) already defines:
- Logistics Hall: 48m × 22m × 5m
- Observation Corridor: 40m × 8m × 4m (Z=[6,10])
- Entry/Exit stairs
- Loading Dock Canopy
- 6 main columns + 4 dock columns
- Openings (truck bays, glazing, slot windows, floor viewing slots)

**Primary gap**: No roof exists. No structural connections, formwork, expansion joints, or facade detail.

LOG400 adds: roof slabs + parapets, roof assembly layers, structural connections (base/top plates, cantilever brackets), formwork lift lines, expansion joints, opening frames, facade panel joints, floor build-up at viewing slots.

---

## Phase Breakdown

### Phase 1 — Design Spec (1 session, ~45 min)
```
Goal: Produce complete LOG400 execution plan for Lock 02 Cargo
Topology: flat, narrow context — 1 architect agent working alone
Team: 1 agent (architect)
Reads: lock_02 base concept prompt, lock_01 APPROVED spec (reference format), 00_Workflow_v04.md LOG definitions
Produces: output/city101_hub/lock_02_cargo_LOG400_execution_plan.md
Dependencies: none
Success: spec covers all 7 sections (roof, formwork, joints, connections, hardware/frames, facade, floor); all coordinates consistent with base model; layer names follow Type_02_Cargo:: convention
```

### Phase 2 — Roundtable Review (1 session, ~30 min)
```
Goal: Catch structural/coordinate errors before execution
Topology: flat, narrow context — 1 reviewer reading Phase 1 output
Team: 1 agent (structural reviewer)
Reads: Phase 1 execution plan
Produces: output/city101_hub/lock_02_cargo_LOG400_APPROVED.md (corrected spec + decision log)
Dependencies: Phase 1 complete
Success: all flagged errors resolved; corrections documented; APPROVED status set
```

### Phase 3 — Execute (1–2 sessions, ~60 min)
```
Goal: Build all LOG400 geometry in Rhino port 9002
Topology: hierarchical — 1 executor (no coordinator needed, single Rhino instance)
Team: 1 agent (executor)
Reads: Phase 2 APPROVED spec
Produces: geometry in Rhino (100+ elements); viewport captures; session log
Dependencies: Phase 2 APPROVED
Success: all elements present in correct layers; viewport captures look correct; two-level reading clear (logistics below, observation above)
```

---

## Phase Sequence

```
[Phase 1: Design Spec] → [Phase 2: Review] → [Phase 3: Execute in Rhino]
     1 agent                  1 agent             1 agent
     ~45 min                  ~30 min             ~60 min
```

---

## Key Engineering Constraints

- Coordinate system: meter-scale in a centimeter-unit Rhino doc. Use numbers as-is. Do NOT multiply by 100.
- Origin: (0, 0, 0) — no site offset, no LV95
- Logistics Hall walls: 5m tall, 300mm thick → outer faces at Y=±11.3 and X=±24.3
- Observation Corridor: Z=[6,10], sits 1m above logistics hall roof (structural zone Z=[5,6])
- Main columns: X=[-16,0,16], Y=[±8], 400mm × 400mm, full height
- Dock columns: X=[-28,-24], Y=[±8], 150mm × 150mm, 5.5m tall
- Rhino target: `lock_02` — all MCP calls must include `target: "lock_02"`
- Port: 9002
