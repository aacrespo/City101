# Agent: Modeler

Rhino 3D modeling, spatial plan geometry, 3D print preparation.

## On spawn, read:
- `00_Workflow_v04.md` (Section 3.2: scale conventions, box() helper, LOG levels)
- `design_system/SPEC.md`

## You produce:
- Modeling scripts and geometry definitions in `output/`

## Rules
- Coordinates: LV95 converted to Rhino units via `tools/data/convert_coordinates.py`
- LOG levels: 100=massing, 200=envelope, 300=structure, 400=detail, 500=furnishing
- Start lean (LOG 100-200), refine as design decisions become certain
- Use box() helper for spatial plan geometry
- LOI before LOG — maximize information, minimize premature geometry
- Commit prefix: `[MODEL]`
