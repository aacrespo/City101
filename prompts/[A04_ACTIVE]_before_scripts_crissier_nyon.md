# Before Scripts — Crissier-Bussigny + Nyon-Genolier

## What this is for

This prompt generates **"before" Rhino modeling scripts** for two lock nodes. These represent how the team would have modeled typologies BEFORE the knowledge system (archibase, playbook, agent teams, reviewer) existed. The contrast with the current workflow is a key slide in the midterm presentation (March 30).

The "before" is last Tuesday. A student reads a typology paper, opens Rhino, writes a Python script with hardcoded guesses. No construction database, no fire codes, no layer buildups, no multi-agent coordination. Just boxes.

## Output

Two separate Rhino Python scripts (rhinoscriptsyntax):

1. `before_lock05_crissier_bussigny.py` — Logistics Engine
2. `before_lock03_nyon_genolier.py` — Altitude Lock

Save both to `output/city101_hub/rhino_scripts/`.

## Node descriptions

### Lock 05 — Crissier-Bussigny — Logistics Engine (km 58-62)

The gap is spatial, not temporal. Distribution centers built for trucks, not people. 2.5km from Bussigny station through hostile industrial landscape. Yusuf, 38, forklift operator at Feldschlosschen — always drives because buses stop at 23:46 and the zone has no pedestrian infrastructure.

**What the "before" script should model:**
- A simple rectangular logistics interface building at the edge of an industrial zone
- Ground floor: open warehouse bay (truck-scale openings on one side)
- Upper floor: worker break/waiting space with views toward Bussigny station
- Maybe a covered walkway or canopy extending toward the road
- Overall: ~30m x 15m footprint, 2 stories (~8m total height)
- Industrial character: large spans, minimal columns, flat roof

### Lock 03 — Nyon-Genolier — Altitude Lock (km 25)

8 hours of altitude severance. Sophie, 26, junior nurse at Clinique de Genolier — no car, NStCM last train at 21:29, clinic is on a hilltop at 550m altitude, 200m above Nyon, 6km of dark winding road. On night shifts she stays at the clinic because there is literally no way down.

**What the "before" script should model:**
- A small transit shelter/waiting pavilion at the NStCM Genolier station
- Single story with a mezzanine or loft (waiting area above, dispatch below)
- Sloped roof responding to hillside context
- Overall: ~20m x 10m footprint, ~6m to ridge
- A simple ramp or stair connection suggesting the altitude change
- Mountain/rural character: compact, sheltering

## Instructions for the modeling Claude

You are writing naive Rhino Python scripts. This means:

### DO
- Use `import rhinoscriptsyntax as rs` only
- Hardcode ALL dimensions (meters, as floats)
- Use simple geometric operations: `rs.AddBox`, `rs.AddSrfPt`, `rs.ExtrudeCurveStraight`, `rs.AddLine`, `rs.AddPolyline`
- Create basic layers (just a few: "Walls", "Slabs", "Roof", "Columns" — flat hierarchy)
- Add a docstring at the top saying what you're modeling and where dimensions came from ("estimated from paper" / "guessed based on program")
- Make it actually run in Rhino 8 — valid Python, valid rs calls
- Keep each script under 150 lines
- Use a simple origin at (0,0,0)

### DO NOT
- Import or reference `knowledge_bridge`, `ConstructionDB`, `DicobatRAG`, or anything from archibase
- Use any construction specs (no mm-level dimensions, no layer buildups, no U-values, no fire ratings)
- Reference SIA norms, KBOB data, Eurocode, or any building code
- Include a reviewer step, a verification step, or any QA process
- Use agent team patterns (no role tags, no handoffs, no multi-file coordination)
- Include material properties, structural calculations, or assembly details
- Create elaborate layer hierarchies (no `Lock05::Structure::Columns::Interior`)
- Add annotations with technical specs
- Write more than one script per node

### Tone of the code
Think of a student who knows Rhino Python basics, has read about the site, and is trying to get something 3D on screen quickly. The dimensions are round numbers. Wall thickness is "30cm because that seems right." Slab thickness is "20cm." Column size is "30x30cm." No justification, no source. The script works but the output is a collection of extruded rectangles that communicates spatial layout without any construction intelligence.

### Contrast points (for the presentation)
The audience will see these scripts side-by-side with the current workflow output. Key differences to make visible:

| Before (these scripts) | After (current workflow) |
|---|---|
| Hardcoded guesses | Database-sourced dimensions |
| Flat layers ("Walls") | Hierarchical (`Lock::Structure::Walls::Exterior`) |
| No material logic | Material constraints from KBOB/archibase |
| Single monolithic script | Multi-agent team (architect, structure, envelope, reviewer) |
| No verification | Playbook reviewer checks fire, structure, accessibility |
| ~100-150 lines | ~500-800 lines across agents |
| Walls are boxes | Walls have layers (insulation, structure, finish) |
| "30cm seems right" | "400mm per SIA 266 for rammed earth, H:T ratio 7.5:1" |

The "before" scripts don't need to be bad — they need to be honest about what modeling without a knowledge system looks like.
