# Wave 4: LOG 400 Upgrade — Detailed Lock Modeling

**Branch:** `andrea/prototypology-v2`
**Rhino needed:** YES — open Rhino with MCP addon before starting
**Depends on:** Wave 3 (3 locks placed on real terrain — complete)
**Commit prefix:** `[MODEL]`

---

## Where we are

Waves 1–3 are done. We have 3 site models in Rhino with:
- Terrain meshes (swissALTI3D, 125x125 subsampled)
- 3D buildings (swissBUILDINGS3D LOD2, culled to terrain extent)
- 2D context (roads, rail, moved to terrain Z)
- Lock geometry placed at real site positions (v3 scripts with SITE_ORIGIN)

The locks are currently at **LOG 200-300** — massing volumes, floor plates, columns, openings, circulation cores. Wave 4 upgrades them toward **LOG 400** (architectural detail).

---

## Before starting — read these

1. **LOG levels definition:** `00_Workflow_v04.md` Section 3.2 — what LOG 400 means
2. **Lock concepts:** `output/city101_hub/prototypology_content.json` — what each lock *is*
3. **Current scripts:** `output/city101_hub/rhino_scripts/lock_*_v3.py` — what's built so far
4. **Wave 3 log:** `output/city101_hub/site_modeling/wave3_integration_log.md` — QA findings, coordinate offsets, cross-site observations
5. **Script test log:** `output/city101_hub/script_test_log.md` — known issues from Wave 2
6. **Wave 3 prompt (for context on what was done):** `prompts/PROMPT_wave3_site_context_integration.md`

---

## The 3 locks to upgrade

| Lock | Site | Script | Key concept | Current state |
|------|------|--------|-------------|---------------|
| Lock 03 — Temporal Lock | Morges | `lock_03_morges_temporal_v3.py` | Night/Dawn/Gate chambers, temporal rhythm | 41 objects: 3 volumes, 6 floors, 20 columns, 10 openings, 2 stairs |
| Lock 05 — Gradient Dispatcher | CHUV | `lock_05_chuv_gradient_v3.py` | 4 stepping levels on hillside, gradient flow | 68 objects: 4 volumes, 8 floors, 52 columns, 10 openings, 6 circulation |
| Lock 07 — Bridge Lock | Rennaz | `lock_07_rennaz_bridge_v3.py` | 90m span, V-columns, station-to-hospital bridge | 118 objects: 8 volumes/floors, 110 structure/openings/circulation |

---

## What LOG 400 means (interpret from 00_Workflow_v04.md)

Read the workflow doc for the precise definition, but generally LOG 400 adds:
- **Facade articulation** — wall thickness, window openings as voids (not just surface marks)
- **Structural expression** — slab edges, beam depths, column profiles
- **Circulation detail** — stair geometry (treads/risers), ramp slopes, elevator shafts
- **Material zones** — different layers or colors for structure vs enclosure vs circulation
- **Threshold conditions** — how the lock meets ground, how entries work, edge details

---

## Approach

For each lock, working in the existing Rhino file:

1. **Open the site model** (e.g., `city101_wave3_CHUV_site_context.3dm`)
2. **Assess what's there** — get object info, understand current geometry
3. **Upgrade in place** — add detail to existing geometry, don't rebuild from scratch
4. **Maintain the SITE_ORIGIN pattern** — all new geometry uses the same offset
5. **Keep layer discipline** — use the Lock_XX sublayer hierarchy

### Priority order
Start with **Lock 05 CHUV** (most architecturally complex — gradient stepping, dense context). Then Morges, then Rennaz.

### What to add (suggested, adapt based on LOG 400 definition)
- Wall thickness (currently just planes/surfaces → extrude to ~0.3m walls)
- Window/door openings as boolean subtractions or recessed frames
- Slab edges with thickness (~0.3m floor plates)
- Stair geometry with actual treads
- Ground connection — how the lock meets terrain (foundations, grade beams, landscape interface)
- Roof/canopy elements if conceptually appropriate

---

## Key learnings from Wave 3 (don't repeat these mistakes)

From `wave3_integration_log.md`:
- **DXF coordinates are in kilometers** — if importing anything new, scale 1000x
- **2D context has no Z** — must move to terrain Z after import
- **Building tiles are 4km wide** — must cull to terrain extent
- **Coordinate offsets:** Morges E-2527500/N-1151500, CHUV E-2538500/N-1152500, Rennaz E-2560000/N-1137500
- **Can't hide active layer** — switch to another layer before toggling visibility for captures

---

## Deliverables

1. Updated Rhino files with LOG 400 geometry (save in place)
2. Updated scripts if modified → `rhino_scripts/lock_*_v4.py`
3. `output/city101_hub/site_modeling/wave4_upgrade_log.md` — what was added, decisions made
4. Viewport captures of each upgraded lock (perspective, section, detail)
5. Commit: `[MODEL] Wave 4 — LOG 400 upgrade for [site name]`

---

## Reference files
- `00_Workflow_v04.md` — LOG/LOD/LOI definitions
- `output/city101_hub/prototypology_content.json` — lock concepts
- `output/city101_hub/rhino_scripts/lock_*_v3.py` — current scripts
- `output/city101_hub/site_modeling/wave3_integration_log.md` — Wave 3 process + QA
- `output/city101_hub/site_modeling/HANDOFF.md` — data inventory + pipeline docs
- `workflows/rhino-modeling.md` — Rhino workflow SOP
- `design_system/SPEC.md` — palette/colors if needed for material zones
