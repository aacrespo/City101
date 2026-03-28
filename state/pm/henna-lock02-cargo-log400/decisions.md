# Decisions Log — Lock 02 Cargo LOG400
*Append-only*

---

## 2026-03-27 — Project creation

**Decision**: Use sequential 3-phase topology (Design → Review → Execute) matching the lock_01 workflow.
**Why**: Lock_01 roundtable review caught 6 significant errors (C1–C6) before execution. This pattern prevents wasted Rhino build time on bad coordinates.
**How to apply**: Phase 2 MUST complete before Phase 3 starts. Do not skip review even if rushed.

**Decision**: Target port 9002, MCP target `lock_02`.
**Why**: Matches the established setup in prompts/[A04_ACTIVE]_lock_types_master.md — Batch 1 assigns 9002 to lock_02.

**Decision**: Roof is the primary gap. Start the spec design with roof system, then add structural connections, then formwork/detail.
**Why**: User confirmed "it has no roof." The base model has volumes, circulation, structure, and openings but no roof geometry.

**Decision**: v1 build used wrong MCP target (`lock_02` instead of `envelope`). Also built only detail layers (L300/L350/L400) without base building volumes — floating geometry in empty space.
**Why**: MCP config maps port 9002 → `"envelope"`, not `"lock_02"`. Must always check `.mcp.json` for correct target names.
**How to apply**: Always run `rhino_list_instances` or check `.mcp.json` before building. Target names are: structure(9001), envelope(9002), interior(9003).

**Decision**: v2 build — complete redo from scratch. Scene cleared, all 183 elements rebuilt with correct target `"envelope"`, complete building (base + LOG400 detail), archibase-informed structural sizing.

**Decision**: LOG400 definition = full assembly detail + materiality. Not LOG500 (as-built). Means: roof build-up layers (insulation/membrane/gravel), formwork lines, base plates, expansion joints, opening frames with lintels, facade panel joints. Does NOT mean: MEP, interior finishes, equipment.
