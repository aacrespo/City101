# openings Modeling Learnings

Techniques discovered while modeling. Updated by agents after each build round.

---

## 2026-03-21: Rammed Earth Cabin Lintels + Sill

### 1. Orientation matters for lintels on perpendicular walls
The door lintel (south wall) runs along x with width along y, while the window lintel (east wall) runs along y with width along x. When using `AddBox`, the L/W/H parameters must be swapped to match the wall orientation. Easy to mix up x and y dimensions — always sketch the bounding box corners first.

### 2. Window sill projection for drip detail
The sill extends 2cm beyond the outer wall face (x=500 outer face, sill goes to x=502). This projection is a drip detail — water runs off the sill edge instead of tracking back along the wall face, which would erode rammed earth. The 5cm overhang on each side of the window opening (110cm sill for 100cm window) provides a visual frame and additional weather protection.

### 3. Lintel bearing interface with rammed earth courses
The 20cm bearing length on each side means the lintel sits on top of a rammed earth course. If courses are 10-15cm tall, the bearing zone spans roughly 1.5-2 courses vertically. The timber-to-earth interface should have a DPC (damp-proof course) or mortar bed to prevent moisture wicking from the earth into the glulam. This detail is not modeled here but should be addressed by the walls or detail agent.


### 4. Door thresholds are easily missed but critical for rammed earth
A stone threshold at the door base (z=30-35, at plinth top) protects the wall base from water ingress at the opening. It projects 2cm beyond the wall face on each side for weather shedding. Easy to forget because it sits at the interface between foundation and wall — neither agent naturally "owns" it. Placed on `Cabin::Openings::Threshold` layer.

---

## 2026-03-21: Cabin v2 — Multi-agent build observations

### 5. Lintel height vs course height causes cross-course collisions
The door lintel is 20cm tall but courses are 15cm. If the lintel bottom aligns with a course bottom (z=240), the lintel top (z=260) protrudes 5cm into the NEXT course above. The walls agent must void not just the course the lintel sits in, but also any course the lintel protrudes into. Always communicate the exact z-extents of lintels to the walls agent, not just "lintel at door head."

### 6. Render/plaster around openings must account for lintel depth
Render and plaster layers split around openings (left, right, above) must start at the lintel TOP, not the lintel BOTTOM. The lintel replaces the wall material at the opening head — render should not cover the lintel face. In this build, render above door initially started at z=240 (lintel bottom) instead of z=260 (lintel top), creating a 20cm overlap.

### 7. Bounding boxes are misleading for hollow/voided geometry
During review, courses with boolean voids (door/window cutouts) still report full-perimeter bounding boxes. A course with a door void on the south wall still shows bbox min=(0,0,...) because the west/north/east walls extend to those coordinates. Volume checks are the reliable way to verify voids exist — compare actual volume to theoretical full-ring volume (perimeter_area * course_height).

### 8. Threshold-plinth x-overlap is intentional, not a collision
The threshold extends 2cm past the door opening on each side (x=203-297 vs door at 205-295), overlapping the plinth in x. But since the threshold sits ON TOP of the plinth (z=30-35 vs plinth z=0-30), there's no z-collision. The x-overhang is a deliberate weather detail — stone covers the plinth-to-wall joint at the door edge.

### 9. Reveal/jamb finish is a LOD question
At the opening edges, cut rammed earth faces are exposed. In reality these get a 2cm lime render return wrapping into the opening. At cabin LOD this is omitted — but at detail LOD (1:20 or closer) these returns should be modeled as thin boxes at the jamb faces. Same applies to lintel soffits if visible.

### 10. Sill slope is a future LOD refinement
The window sill is modeled as a flat 5cm box. A real sill slopes 5-10 degrees outward for drainage. At this LOD a flat box is acceptable. To add slope later: use 8-point AddBox with the outer edge (x=502) z-coords 1-2cm lower than the inner edge (x=460).

### 11. Cross-agent review protocol that works
The observation-then-propose cycle caught issues no single agent would find in isolation:
- Openings agent found wall course gaps (courses 07-14 incomplete) and lintel collisions
- Structure agent found bearing length concerns (resolved by measurement)
- Walls agent self-corrected during build but missed Course 16 void
Volume verification scripts are essential — visual/bbox inspection is not sufficient for hollow geometry.

---

## 2026-03-22: Cabin v3 — Stone masonry openings (GF)

### 12. Stone lintels vs timber lintels: material choice matters for vernacular
For Swiss Alpine vernacular with molasse stone walls, stone lintels are more authentic than timber. Timber lintels (glulam) were used in cabin v2 (rammed earth) because earth walls need gentler materials. Stone masonry can take stone lintels — the compressive strength of molasse (20-60 MPa) is more than sufficient for 90-100cm spans at residential scale. Reserve timber lintels for rammed earth or very wide spans.

### 13. Frame positioning within deep stone reveals
With 36cm stone walls, the window/door frame position within the reveal is an architectural decision. Setting frames 4cm from the exterior face creates a deep interior reveal (useful as shelf/display in vernacular buildings) and keeps the glass closer to the weather plane. The 36cm reveal depth is a feature of stone construction — it provides thermal buffer and visual character.

### 14. Threshold vs sill naming and layer placement
The door threshold and window sills serve the same weather-shedding function but at different heights. Both go on the Sills layer (not a separate Threshold layer) because they're the same building element type — a horizontal stone piece protecting the opening base. The threshold sits at z=0 (ground level), window sills at z=75-80 (opening bottom). Both project 2cm beyond the exterior wall face.

### 15. Reveal soffit geometry overlaps with lintel z-range
The reveal soffit (lime render on lintel underside) sits at z=200-202, which overlaps vertically with the lintel at z=200-220. This is correct — the soffit render is applied to the BOTTOM face of the lintel, so it occupies the same z-start. The 2cm render is thin enough to not cause visual issues, but at higher LOD this interface needs careful detailing (the render is applied TO the stone, not floating below it).

### 16. Two completely different opening systems: stone vs timber frame
Stone openings (GF) and timber frame openings (UF) are architecturally different systems:
- **Stone**: monolithic lintel (stone/timber), deep 36cm reveals finished with lime render, stone sills with drip projection. The stone mass IS the thermal envelope.
- **Timber frame**: doubled header beams in stud zone, mineral wool reveal insulation around the full opening perimeter, window frame must connect to OSB vapour barrier. The insulated assembly IS the envelope — every layer must be completed at the penetration.
Don't copy techniques between systems. Stone reveals get lime render; timber reveals get insulation.

### 17. Reading timber agent coordination data from Rhino objects
When the timber agent has already built the frame walls with split layers (left/mid/right segments), the gap between segments reveals the window void positions. Object naming conventions (e.g., `East_gypsum_left`, `East_gypsum_mid1`) encode the split pattern. The bounding boxes of these segments define the void extents precisely — no separate coordination message needed if you can read the geometry.

### 18. Window frame position in timber wall assembly
The frame sits at the wind barrier inner face (the boundary between insulated stud zone and the ventilated rainscreen). This puts the glass close to the weather plane while keeping the frame within the structural zone. The reveal insulation then fills the gap between the frame and the interior layers (OSB, service cavity, gypsum), completing the thermal envelope at the penetration.
