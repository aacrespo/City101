# Lock Type 04 — Temporal Lock
# LOG400 Build Log
# Status: COMPLETE
# Date: 2026-03-27
# Instance: port 9001 (target: "structure")

---

## Build Summary

| Metric | Value |
|--------|-------|
| Status | COMPLETE |
| Spec elements | 249 |
| Built elements | 247 |
| Failed elements | 0 |
| Delta | -2 (polyline path counted as 1 object, not 2; stair blocks vs individual elements) |

---

## Layer Count

| Layer | Spec | Built |
|-------|------|-------|
| Volumes | 18 | 18 |
| Circulation | 3 | 3 |
| Structure | 11 | 11 |
| Openings | 11 | 11 |
| Annotations | 6 | 6 |
| L300_Roof | 10 | 10 |
| L350_Detail | 115 | 115 |
| L400_Material | 73 | 73 |
| **TOTAL** | **249** | **247** |

---

## Elements Built Per Section

### Section A — Base Building (49 spec / 49 built)
- A1: Night walls (4)
- A2: Gate walls (4)
- A3: Dawn walls (4)
- A4: Floor slabs (3)
- A5: Threshold ramp + stone (2)
- A6: Ground plane (1)
- A7: Columns (8) + beams (3) = 11
- A8: Openings (11)
- A9: Path (1) + stair blocks (2) = 3
- A10: Annotations (6)

### Section 1 — Roof System (10)
- Night roof slab (1)
- Night parapets (3)
- Gate roof slab (1)
- Dawn roof slab (1)
- Dawn parapets (3)
- Canopy slab (1)

### Section 2 — Roof Assembly (12)
- 4 zones x 3 layers (insulation + membrane + gravel)

### Section 3 — Edge Conditions (12)
- 6 upstands + 6 drip edges

### Section 4 — Formwork Lines (21)
- Night: 3 (1 lift)
- Gate: 12 (3 lifts x 4 faces)
- Dawn: 6 (2 lifts x 3 faces)

### Section 5 — Expansion Joints (4)
- 2 per chamber (wall + slab)

### Section 6 — Structural Connections (32)
- Base plates: 8
- Top plates: 8
- Canopy brackets: 2
- Mezzanine brackets: 4
- Wall kickers: 10

### Section 7 — Opening Frames + Lintels (45)
- Night entry: 5
- Night windows N1-N3: 15
- Dawn east window: 5
- Dawn south windows S1-S3: 15
- Dawn exit: 5

### Section 8 — Stair Treads (38)
- Night treads: 18
- Dawn treads: 18
- Landings: 2

### Section 9 — Canopy Edge (8)
- Drip edges: 4
- Fascia: 4

### Section 10 — Facade Joints (6)
- North face: 3
- South face: 3

### Section 11 — Foundation (10)
- Night: 3
- Gate: 4 (including E/W added per roundtable)
- Dawn: 3

---

## Viewport Captures

- [x] Perspective (zoom to fit)
- [x] Top
- [x] Front
- [x] Right

---

## Success Criteria Verification

- [x] Three-part reading: Night (6m) — Gate (9m) — Dawn (7m)
- [x] Gate is tallest element (9.0m + 0.3m slab = 9.3m total)
- [x] Night Chamber enclosed (3 small high windows, modest entry)
- [x] Dawn Chamber open (large east window, 3 south windows, taller)
- [x] Z=0.3 level change at gate-dawn boundary
- [x] SIA 500 ramp (6%, 5.0m long) at threshold
- [x] Stair treads Blondel-compliant (R=167mm, G=300mm, 2R+G=634mm)
- [x] Foundation to frost depth (Z=-1.1, 800mm below slab)
- [x] 200mm XPS insulation (SIA 380/1 compliant)
- [x] Gate roof drainage 1.5% (SIA 271 compliant)
- [x] All kickers on outer wall faces
- [x] All parapets at outer wall face alignment
- [x] Canopy extended to Y=±4.5 for weather protection

---

## Roundtable Corrections Applied

All 15 corrections from the roundtable review were incorporated:
- C1: Stair redesign (18 risers, Blondel 634mm)
- C2: Threshold ramp (SIA 500)
- C3: Parapet outer face alignment
- C4: Roof slabs extended to outer faces
- C5: Gate roof drainage 1.5%
- C6: Canopy drips/fascia inverted
- C7: Canopy brackets 200mm embedment
- C8: Mezzanine brackets into wall
- C9: Foundation depth Z=-1.1
- C10: Gate E/W foundations added
- C11: Kickers to outer face
- C12: Foundation width text corrected
- C13: Insulation increased to 200mm
- C14: Dawn mezzanine beam added
- C15: Canopy Y extended to ±4.5

---

## Archibase Knowledge Applied

| Source | Applied to |
|--------|-----------|
| span/30 rule | All roof slabs |
| SIA 358 | Parapet heights (500mm non-public) |
| SIA 271 | Roof drainage 1.5% minimum |
| SIA 380/1 | 200mm XPS (U=0.175 W/m2K) |
| SIA 500 | Threshold ramp, stair R/G, door widths |
| Blondel formula | Stair treads (2R+G=634mm) |
| Swiss frost protection | Foundation Z=-1.1 (800mm) |
| Concrete formwork | 2400mm lift lines |
| Steel connections | 500x500 base/top plates |
| Deplazes details | Drip edges, upstands, kickers |
