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
A stone threshold at the door base (z=30-35, at plinth top) protects the wall base from water ingress at the opening. It projects 2cm beyond the wall face on each side for weather shedding. Easy to forget because it sits at the interface between foundation and wall — neither agent naturally "owns" it. Placed on `Team::Structure::Lintels` alongside the lintel since both are opening-edge elements.
