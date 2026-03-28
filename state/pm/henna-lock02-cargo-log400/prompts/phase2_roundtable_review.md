# Phase 2 — Roundtable Review: Lock 02 Cargo LOG400
# PM Project: henna-lock02-cargo-log400
# Status: ACTIVE (run after Phase 1 produces execution plan)

---

## Your role

You are the structural reviewer for Lock Type 02 — Cargo Lock. Your job is to read the draft execution spec, catch every error, resolve flagged issues, and produce the approved final spec that an executor will use without modification.

---

## Input

Read: `output/city101_hub/lock_02_cargo_LOG400_execution_plan.md`

---

## What to check

### 1. Coordinate consistency
- Do all element coordinates fit within the base model envelope?
- Do roofs bear on top of walls (not float in space, not penetrate them)?
- Do parapets extend the wall correctly (no gaps, no overlaps with other volumes)?
- Do structural connections land exactly on column centers?
- Are roof assembly layers correctly inset from parapet inner faces?

### 2. Engineering correctness
- Slab thicknesses: verify span/30 (or span/20 for two-way) is applied correctly for each span condition
- Parapet height: ≥ 1070mm per SIA 358 wherever there is a drop > 1000mm
- Cantilever brackets: does the projection and depth make structural sense for a 4m overhang?
- Formwork lift lines: 2400mm lifts — verify Z positions are correct for each wall height
- Expansion joints: are joint positions at correct X locations, continuous through walls AND slabs?

### 3. Layer assignments
- Every element assigned to correct layer (L300_, L350_, L400_)?
- Layer names follow `Type_02_Cargo::L300_Roof`, `Type_02_Cargo::L350_Detail`, `Type_02_Cargo::L400_Material`?

### 4. Flag resolution
- Resolve all `[FLAG N: ...]` items in the draft. State the verdict and rationale for each.

### 5. Conflict with observation corridor geometry
- The critical interface: Logistics Hall roof (Z≈5+) and Observation Corridor floor (Z=6). Check there is structural logic connecting them and no geometry conflict.
- Stair volumes (Z=[0,6]) — do their top faces interfere with any roof geometry?

### 6. Element naming
- All elements have unique, descriptive names matching the `L300_/L350_/L400_` prefix convention?
- Names match the layer they are assigned to?

---

## Output

Write: `output/city101_hub/lock_02_cargo_LOG400_APPROVED.md`

Structure:
1. **CORRECTIONS TABLE** — list every error found and how it was resolved:
   | # | Issue | Resolution |
2. **FLAG RESOLUTION TABLE** — each flag → verdict + rationale
3. **FULL CORRECTED SPEC** — complete element list with final coordinates (copy from draft, apply all corrections)
4. **EXECUTION SUMMARY** — element count table by section
5. **BUILD ORDER** — numbered sequence for the executor
6. **EXECUTOR NOTES** — critical reminders (coordinate system, target, port)
7. **DECISION LOG** — key architectural/structural decisions made

Set status: `APPROVED — ready for executor`

---

## If no errors found

Write a brief "No corrections needed" section and copy the full spec verbatim. Still write the DECISION LOG explaining the key choices made by the designer.

---

## Executor notes to always include

```
1. All coordinates are meter-scale in a centimeter-unit Rhino doc. Use numbers exactly as written.
2. Do NOT multiply by 100.
3. Use rhino_execute_python_code with Box() (BoundingBox from two corner points) for all elements.
4. Batch by section — formwork lines in one script, base plates in one script, etc.
5. If a boolean or complex operation fails, fall back to additive geometry only and note it.
6. After all geometry is placed: capture Perspective, Top, Front, and Section (Y=0 cut) viewports.
7. Target instance: lock_02 (port 9002). All MCP calls must include target: "lock_02".
```
