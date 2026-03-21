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
