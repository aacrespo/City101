# Phase 3 — Model Corrections for Existing 3D Models

**Date:** 2026-03-18
**Models assessed:** Lock 03 (Morges), Lock 05 (CHUV), Lock 07 (Rennaz)
**Method:** Compare current SITE_ORIGIN and terrain coverage against Phase 2 siting recommendations

---

## Lock 03 — Morges (Temporal Lock) — `lock_03_morges_temporal_v4.py`

### Current State
| Parameter | Value |
|-----------|-------|
| SITE_ORIGIN (local) | (-60, 0, 381.5) |
| LV95 Offset | E-2527500, N-1151500 |
| LV95 Position | E 2,527,440, N 1,151,500 |
| LOD | LOG 400 (138 objects) |
| Terrain tile | 2527-1151 (1km²) |
| Status | PROVISIONAL |

### Issue 1: WRONG Z LEVEL
**Current Z = 381.5** — this is **rail embankment level**. The nurse walking from the hospital approaches on town streets at Z ≈ 375-378. The lock sits 4-6m above the pedestrian experience. The railway embankment is an infrastructure boundary, not a gathering space.

**Recommendation:** Lower SITE_ORIGIN Z to **~376.0** (town level, street grade near Gare de Morges). The lock should be at the level of the walking approach, not the track level.

**New SITE_ORIGIN (proposed):** (-60, -15, 376.0)
- X = -60 (unchanged — stays clear of buildings)
- Y shifted south to -15 (closer to Place de la Gare, town side of tracks)
- Z = 376.0 (town level, ~5.5m below current position)

**Verification needed:** Check terrain XYZ at local (-60, -15) to confirm ground elevation. The embankment slope may require positioning further south.

### Issue 2: HOSPITAL OUTSIDE TERRAIN TILE
**EHC Morges at ~LV95 (2,527,800, 1,152,050)**
- Terrain tile north edge: N 1,152,000 (local Y = 500)
- Hospital is **50m beyond** the tile
- Only 1 building above Y = 500 in current model

**Recommendation:** Extend terrain tile north by at least 200m to include:
- EHC Morges hospital building footprint
- Avenue de la Gottaz (hospital access road)
- The walking route connection from hospital toward town center

**Options:**
1. Download adjacent terrain tile 2527-1152 (adds 1km² north)
2. Or extend current tile by 200m strip (N 1,152,000 to N 1,152,200)

### Issue 3: WALKING ROUTE NOT SHOWN
The model has no representation of the walking route Hospital → Av. Muret → town center → Rue de la Gare → station. This is the experiential backbone of the temporal lock concept.

**Recommendation:** Add key road segments as projected curves on terrain:
- Avenue de la Gottaz (hospital)
- Avenue Muret (descent south from hospital)
- Rue de la Gare (final approach to station)

### Issue 4: BOTH ENDPOINTS MISSING
The model shows the lock and context (terrain, buildings, roads, rail) but does NOT show the story's two endpoints:
- **Origin:** EHC Morges (where the nurse IS at 02:00)
- **Destination:** Gare de Morges platform (where the first train arrives at 04:01)

Both must be visible to tell the story.

### Correction Summary — Lock 03

| What | Current | Proposed | Priority |
|------|---------|----------|----------|
| SITE_ORIGIN Z | 381.5 (rail level) | ~376.0 (town level) | HIGH |
| SITE_ORIGIN Y | 0 | -15 (closer to town) | HIGH |
| Terrain north edge | N 1,152,000 | N 1,152,200+ | HIGH |
| Hospital building | Missing | Add EHC Morges footprint | HIGH |
| Walking route | Missing | Add key road segments | MEDIUM |
| Station platform | Implicit (near rail) | Make explicit | LOW |

---

## Lock 05 — CHUV (Gradient Dispatcher) — `lock_05_chuv_gradient_v3.py`

### Current State
| Parameter | Value |
|-----------|-------|
| SITE_ORIGIN (local) | (-450, -400, 451.0) |
| LV95 Offset | E-2538500, N-1152500 |
| LV95 Position | E 2,538,050, N 1,152,100 |
| LOD | LOG 200-300 |
| Terrain tile | Likely 2538-1152 (1km²) |
| Status | NEEDS REASSESSMENT |

### Issue 1: CHUV CAMPUS OUTSIDE TERRAIN TILE
**CHUV at ~LV95 (2,538,600, 1,152,800)**
- If terrain tile is 2538-1152: tile covers E 2,538,000-2,539,000, N 1,152,000-1,153,000
- CHUV campus at E 2,538,600 — potentially within tile if tile extends far enough east
- But wave4 log states hospital is **132m beyond terrain tile**

**Recommendation:** Verify tile boundaries. If CHUV is indeed outside:
- Extend tile east/north to include the CHUV campus
- Or download adjacent tile

### Issue 2: M2 METRO NOW CONFIRMED DEAD AT 02:00
Phase 1 research confirms: M2 stops ~00:45 Mon-Thu, resumes ~05:15. This validates the gradient dispatcher concept but adds a critical element: **the locked M2 station entrance**.

**Current model:** The gradient dispatcher is a 4-level building following a 15% grade. It does NOT explicitly reference the M2 station.

**Recommendation:** The lock should be re-sited to be **adjacent to or incorporating the M2 CHUV station entrance.** The locked door of the metro station at 00:45 is the spatial anchor of this node — the moment the gradient reconquers the hillside.

**Potential new SITE_ORIGIN:** Near the M2 "CHUV" station (LV95 approx E 2,538,560, N 1,152,680). This requires terrain data at that location.

### Issue 3: GRADIENT REPRESENTATION
**Current concept:** 4 levels stepping up a 15% grade over 34m (Y direction).
- Level 0 (Z=0, arrival): public interface
- Level 1 (Z=3.5, staff): circulation
- Level 2 (Z=7.0, logistics): sorting
- Level 3 (Z=10.5, emergency): access

**Finding from Phase 2:** The gradient is 90m over ~1km from CHUV to Gare — about 9%. The model compresses this into 15% over 34m for architectural expression. This is a design choice (not an error), but the real gradient should be visible in the terrain/context model.

**Recommendation:** Ensure the terrain model shows the full descent from CHUV elevation (~540m) toward the Gare (~450m). The 4-level building sits on the gradient; the gradient itself tells the story.

### Issue 4: WALKING ROUTE NOT SHOWN
The steep walking route CHUV → Rue du Bugnon → Rue du Pont → Riponne → Rue Centrale → Gare is the experiential backbone of this node. It includes stairs, steep streets, and the psychological experience of descending a dark hill after a 12-hour shift.

**Recommendation:** Add key descent segments as projected curves. Show at minimum:
- Rue du Bugnon (CHUV level)
- One or two stair connections
- Lausanne Gare approach

### Issue 5: BOTH ENDPOINTS
- **Origin:** CHUV campus (where 2,500-3,000 workers are at 02:00)
- **Destination:** Lausanne Gare (where they need to go)
- Both must be in the model to tell the gradient story

### Correction Summary — Lock 05

| What | Current | Proposed | Priority |
|------|---------|----------|----------|
| Terrain extent | Hospital 132m outside | Extend to include CHUV + M2 station | CRITICAL |
| SITE_ORIGIN concept | Generic gradient position | Adjacent to M2 CHUV station | HIGH |
| SITE_ORIGIN Z | 451.0 | Re-verify against actual terrain at M2 station | HIGH |
| M2 station reference | Not in model | Add M2 station entrance as context | HIGH |
| Walking route | Missing | Add descent segments | MEDIUM |
| Lausanne Gare | Not in model | Add as distant endpoint context | MEDIUM |

---

## Lock 07 — Rennaz (Bridge Lock) — `lock_07_rennaz_bridge_v3.py`

### Current State
| Parameter | Value |
|-----------|-------|
| SITE_ORIGIN (local) | (200, 300, 374.0) |
| LV95 Offset | E-2560000, N-1137500 |
| LV95 Position | E 2,560,200, N 1,137,800 |
| LOD | LOG 200-300 |
| Terrain tile | Likely 2560-1137 (1km²) |
| Bridge axis | Y (S→N): station end south, hospital end north |
| Bridge length | 90m modeled |
| Status | NEEDS REASSESSMENT |

### Issue 1: HOSPITAL FAR OUTSIDE TERRAIN TILE
**HRC Rennaz at ~LV95 (2,560,100, 1,138,850)** (approximate — hospital is ~2.1km from Villeneuve station)
- Terrain tile 2560-1137 covers N 1,137,500 to N 1,138,500
- Hospital at N ~1,138,850 — **~350m beyond tile north edge** (if tile is 1km²)
- Actually, the hospital could be even further — the plan says 644m beyond terrain tile

**Recommendation:** This is the most severe terrain gap. The entire 2.1km axis from Villeneuve to HRC needs to be in the model:
- Download tiles 2560-1137 AND 2560-1138 (to cover full axis)
- Or create a 2.5km-long terrain strip

### Issue 2: BRIDGE ORIENTATION
**Current:** Bridge axis is Y (local south→north). South end = station, north end = hospital.
**Actual geography:** Villeneuve station is roughly west-southwest of HRC. The Route 9 runs approximately WSW→ENE.

**Verification needed:** Check if the Y axis in the model actually aligns with the Villeneuve→HRC direction given the LV95 offset. With offset E-2560000, N-1137500:
- Villeneuve station at ~LV95 (2,559,800, 1,137,700) → local (-200, 200)
- HRC at ~LV95 (2,560,100, 1,138,850) → local (100, 1350)

The actual vector is roughly (300, 1150) — more north than east, but with an east component. The Y-axis bridge is approximately correct in direction but the 90m modeled length represents only ~4% of the actual 2.1km distance.

**Recommendation:** The bridge concept is valid but should acknowledge the scale compression. The 90m model is an architectural proposition, not a 1:1 bridge. Add context markers showing the actual axis endpoints.

### Issue 3: ROUTE 9 AND HIGHWAY CHARACTER
The walk from Villeneuve to HRC follows cantonal Route 9, a highway environment with truck traffic from the A9 motorway. The model should show this hostile pedestrian environment.

**Recommendation:** Add:
- Route 9 road alignment as a projected curve
- A9 motorway (if within terrain tile range)
- The rail line passing through without stopping

### Issue 4: BOTH ENDPOINTS
- **Origin:** Villeneuve station (where the rail corridor delivers/collects people)
- **Destination:** HRC hospital (where 200-300 night workers are at 02:00)
- The Simplon railway line passing within 500m of HRC without stopping

Both must be in the model. Currently, the 90m bridge sits on terrain but neither endpoint institution is represented.

### Issue 5: SCALE OF THE GAP
The 90m bridge model represents a design concept, not the actual 2.1km gap. The model needs context to show the real scale:
- Where is Villeneuve station relative to the lock?
- Where is HRC relative to the lock?
- What is the character of the 2km between them?

**Recommendation:** Add endpoint markers (text dots or simplified building footprints) at the actual locations of Villeneuve station and HRC within the terrain model.

### Correction Summary — Lock 07

| What | Current | Proposed | Priority |
|------|---------|----------|----------|
| Terrain extent | Hospital 644m outside | Extend to cover full Villeneuve-HRC axis | CRITICAL |
| HRC building | Missing | Add hospital footprint | CRITICAL |
| Villeneuve station | Not in model | Add station context | HIGH |
| Route 9 road | Missing | Add highway alignment | HIGH |
| Rail line (Simplon) | May be in terrain context | Verify visible; mark "no stop" | MEDIUM |
| A9 motorway | Missing | Add if within tile range | MEDIUM |
| Bridge orientation | Y-axis (approximately correct) | Verify against actual WSW→ENE vector | LOW |

---

## Cross-Model Summary

### Common Pattern: Hospitals Outside Tiles
All 3 models have their anchor institution outside the terrain tile:

| Model | Institution | Distance Beyond Tile |
|-------|------------|---------------------|
| Morges | EHC Morges | 50m |
| CHUV | CHUV campus | 132m |
| Rennaz | HRC hospital | 644m |

**Root cause:** Terrain tiles were selected for the lock siting location (near rail/station), not for the institutional anchor. The siting audit reverses this: the institution is where the person IS, so it must be in the model.

### Priority Order for Corrections
1. **Rennaz** — Most critical. Hospital is 644m outside, and the entire concept (bridge spanning gap) requires both endpoints visible. Without HRC in the model, the bridge lock has no destination.
2. **CHUV** — Second. M2 confirmation means the model needs to incorporate the metro station as spatial anchor. 132m terrain extension is manageable.
3. **Morges** — Third. 50m extension is smallest. Z-level correction is the bigger change (5.5m drop from rail to town level).

### Actions Required Before Model Changes
1. Download/verify terrain data for extended tiles (swisstopo swissALTI3D)
2. Download building footprints for extended areas (swissBUILDINGS3D)
3. Verify road network data (swissTLM3D) for walking routes
4. For each model: verify proposed new SITE_ORIGIN against actual terrain Z at that point
