# Wave 4 — LOG 400 Upgrade Log

## Lock 03: Temporal Lock (Morges, km 48)
**Date:** 2026-03-18
**File:** `city101_wave3_Morges_site_context.3dm`
**Script:** `lock_03_morges_temporal_v4.py`

### Upgrade Summary
LOG 200-300 → LOG 400 ("full assembly detail, materiality")

| Category | v3 (LOG 200-300) | v4 (LOG 400) | Change |
|----------|-------------------|--------------|--------|
| Walls | 3 solid envelopes | 33 wall panels (0.3m thick, split at openings) | Volumes → articulated walls |
| Facade | 10 opening boxes | 33 frame elements (0.15m depth reveals) | Boxes → recessed surrounds |
| Circulation | 2 solid stair blocks | 22 elements (10 treads + landing per stair) | Blocks → individual treads |
| Ground | — | 6 elements (foundation strip, ramp, plinth) | NEW |
| Roof | — | 10 elements (8 parapets + 2 canopy extensions) | NEW |
| FloorPlates | 6 slabs | 6 slabs | Unchanged |
| Structure | 20 columns | 28 elements (20 columns + 8 edge beams) | Added beams |
| **Total** | **41** | **138** | **+97 objects** |

### Spatial Plan (unchanged)
- Night Chamber: x [-17, -2], 15m wide, 6m tall
- Gate Threshold: x [-2, 2], 4m wide, 8m tall
- Dawn Chamber: x [2, 17], 15m wide, 6m tall
- Y range: [-5, 5] (10m depth)
- SITE_ORIGIN: (-60, 0, 381.5) — re-sited from (0, 15, 392.0)

### Siting Fix
Original v3 placement at (0, 15, 392) landed the lock on top of buildings near the
terrain text dot. Re-sited to (-60, 0, 381.5):
- **15m north of rail tracks** — on the hospital-approach side (uphill)
- **Terrain Z=381.5** — ground level, 1.4m elevation range across footprint
- **Clear of all buildings** — verified no overlap within 2m margin
- **On the path** between EHC Morges hospital (uphill/north) and the station (at tracks)
- LV95: E 2,527,440, N 1,151,500

### Layer Hierarchy (v4)
```
Lock_03::
  Walls        (180, 200, 220)  — 33 wall panels
  Structure    (100, 100, 110)  — 20 columns + 8 beams
  FloorPlates  (220, 220, 210)  — 6 slabs (unchanged)
  Facade       (255, 220, 120)  — 33 frame elements
  Circulation  (200, 160, 160)  — 20 treads + 2 landings
  Ground       (140, 130, 120)  — 4 foundation + ramp + plinth
  Roof         (200, 210, 220)  — 8 parapets + 2 canopy
```

### Key Decisions
1. **Walls split at openings** rather than boolean subtraction — cleaner geometry, no tolerance issues
2. **Stair tread run = 0.18m** (not 0.20m) to leave 0.2m for landing platform at top
3. **Gate N/S open** — no walls on north/south gate faces (passage openings), only threshold strips on Facade layer
4. **Foundation strip simplified** to 4 perimeter segments (0.5m wide × 0.4m deep)
5. **Canopy extends 1.5m** beyond gate envelope on N and S sides
6. **Parapets at 0.15m** height on top of chamber roof slabs (z=6.3)
7. **Edge beams sit below slab** (z=2.7 to 3.0) at column lines

### Deleted v3 Layers
- `Lock_03::Volumes` → replaced by `Lock_03::Walls`
- `Lock_03::Openings` → replaced by `Lock_03::Facade`

### Verification
- Total objects: 138 (target was 120-130, slightly over due to wall segmentation)
- All geometry at correct Z (SITE_ORIGIN Z=381.5, ground level)
- Wall thickness: 0.3m
- Stair treads individually visible (0.18m run × 0.05m thick)
- Facade frames create depth in perspective view
- Model responsive — 138 breps added to ~2,700-object file (now ~2,800 total)

---

## Lock 03: Re-siting Audit (2026-03-18, session 2)

### What we tried
Planned to re-site Lock 03 along the actual hospital→station walking route, with roads projected onto terrain for visual verification. Wrote analysis scripts, traced the road network through GeoJSON data with real Z values.

### What we found

**1. Avenue de Marcelin is NOT on the walking route.**
The original plan assumed Av. de Marcelin as the descent from hospital to station. Google Maps shows the actual route goes: Hospital → Av. Muret (south) → west through town center → Rue de la Gare → station. Completely different corridor.

**2. Rail sits on an embankment.**
Rail tracks are at Z~381-382 on a raised embankment. The town and walking route are 6m BELOW at Z~375-378. Pont de la Gare is a bridge OVER the tracks at Z~386. The current lock at Z=381.5 sits on the embankment — at rail level, not at street/walking level.

**3. The hospital is outside the 3D model.**
Terrain tile stops at N=1152000 (local Y=500). EHC Morges is at ~N=1152050 (local Y=550) — 50m beyond the northern edge. Only 1 building exists above Y=500. The model cannot tell the story of the hospital-to-station connection.

### The fundamental problem (Andrea's insight)

**The siting approach was wrong.** Tracing a geometric walking route and optimizing for terrain flatness misses the point entirely. The lock is waiting infrastructure for a nurse finishing at 2am:

- A 30-minute walk alone at night is not safe or realistic
- The nurse is AT THE HOSPITAL when the gap hits — not on the road
- Is there a shuttle? A night bus? Or nothing?
- You can't solve a connection problem by only looking at one endpoint
- Both the hospital AND the station must be in the model to tell the story

This applies to ALL 9 nodes, not just Morges. See `prompts/PROMPT_lock_siting_audit.md` for the full audit prompt.

### Decision: HALT placement, research first

**Do NOT re-site until:**
1. Actual night transit to/from EHC Morges is researched (MBC network, Noctambus)
2. The experiential gap is understood (where does the nurse wait? how do they get to the station?)
3. Terrain tile is extended north to include the hospital
4. Both endpoints are in the 3D model
5. The same audit is applied to CHUV (Lock 05) and Rennaz (Lock 07)

### Current state
- Lock 03 remains at SITE_ORIGIN (-60, 0, 381.5) — LOG 400, 138 objects
- Position is PROVISIONAL pending re-siting audit
- Analysis scripts preserved at `output/city101_hub/site_modeling/analyze_walking_route.py`
- Documented in LEARNINGS.md under "Lock siting: start from the person, not the geometry"
