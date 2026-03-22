# Stone Masonry Modeling Learnings

Techniques discovered while modeling coursed stone masonry walls. Updated by agents after each build round.

---

## 2026-03-22 — Structure Agent (cabin-v3 build)

1. **Molasse sandstone assembly for Swiss vernacular.** No archibase assembly exists — derived from `stone_masonry.md`: exterior lime render (2cm) + structural molasse (36cm) + interior lime plaster (2cm) = 40cm. Thermal performance is poor (U ~2.0 W/m²K) but acceptable for vernacular construction. The key requirement is envelope CONTINUITY, not thermal performance.

2. **Course height of 20cm works well for modeling.** Within the 15-25cm typical range for coursed stone. 13 courses x 20cm = 260cm gives a clean wall height. Real coursed masonry has slight variation per course, but for modeling purposes uniform height is appropriate.

3. **Stone walls generate many objects.** 13 courses x 4 walls x 3 layers (render/stone/plaster) = 156 objects for solid courses. With door and window splits, total reached 222 objects for stone walls alone. This is fine — each object has clear naming and metadata for downstream agents.

4. **Opening voids are just gaps in the course pattern.** For courses with openings, split the wall segment into pieces around the void. E.g., west wall with window at y=200-300: model y=36-200 segment + y=300-564 segment, leaving the void. Much more reliable than boolean subtraction, and the Openings agent can easily identify and fill the voids with frames/lintels.

5. **Render and plaster layers must also be split at openings.** Don't forget that the finish layers need the same void pattern as the structural stone. Every stone segment gets matching render (exterior) and plaster (interior) segments.

6. **Dressed quoins (pierre de taille) are a detail level choice.** At this LOD, the corner overlap convention (S/N full length, E/W between inner faces) represents the quoin pattern implicitly. At higher LOD, individual quoin blocks could be modeled as separate objects with `material: pierre_de_taille_molasse`.

7. **Wall plate spans the full perimeter.** The sabliere (10x15cm oak) must be continuous for load distribution. Model S/N plates full length, E/W between them — same convention as the stone courses. The plate is centered on the 36cm structural stone, not on the full 40cm assembly width.
