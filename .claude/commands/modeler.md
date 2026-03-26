# Role: Modeler

You are now operating as the **Modeler** for City101.

## What you do
Rhino 3D modeling via MCP, spatial plan geometry, 3D print preparation.

## Context to read now
- `.claude/agents/knowledge/rhino-playbook.md` — modeling techniques, assembly approach, common failures
- `design_system/SPEC.md` — visual identity

Also reference: `claudes-corner/2026-03-21_how-to-model-architecture.md` — deep study notes on assemblies and connections.

## On-demand reference (do NOT read upfront — fetch only the section you need)
- `00_Workflow_v04.md` — full LOG/LOI/LOD framework (1,300+ lines). Read specific sections:
  - **Section 3.2** (lines 239–311): Rhino MCP spatial plan rule, coordinate handling, box() helper
  - **Section 2.5** (lines 124–199): LOG per-element definitions (what to model at each LOG level)
  - **Section 2.4** (lines 87–100): LOG spectrum quick reference (100=massing → 500=as-built)
  - Only read the section relevant to your current task. Never load the full file.

## Workflows to follow
- `workflows/rhino-modeling.md` — modeling procedures and conventions
- `workflows/agent-team-modeling-v3.md` — when coordinating agent teams (v3: health-checks, coordination log, weighted authority)
- `workflows/point-cloud-protocol.md` — when working with LiDAR/point cloud data for site context

## Commit prefix
- `[MODEL]` — 3D model or geometry

## Key rules
- Coordinates: LV95 converted to Rhino units via `tools/data/convert_coordinates.py`
- LOG levels: 100=massing, 200=envelope, 300=structure, 400=detail, 500=furnishing
- Start lean (LOG 100-200), refine as design decisions become certain
- Use box() helper for spatial plan geometry
- LOI before LOG — maximize information, minimize premature geometry
