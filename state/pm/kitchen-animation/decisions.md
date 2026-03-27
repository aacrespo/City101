# Kitchen Animation — Decisions Log
*Append-only. Newest at bottom.*

---

**2026-03-27 — Scrap Blender kitchen environments**
kitchen_v2, kitchen_v3 Blender files were built autonomously without Andrea's feedback. Layouts are wrong. HTML/CSS handles all environments instead. Blender produces character sprites ONLY.
*Decided by: Andrea*

**2026-03-27 — HTML as animation medium, not Blender**
After considering Blender animation, AI video generation, and HTML: HTML wins for precision (exact design system colors, exact narrative control), iteration speed (edit CSS, refresh), and deadline feasibility. Blender characters composite on top as sprite sheets.
*Decided by: Andrea + Cairn Code*

**2026-03-27 — Keep specialist accessories subtle**
At 64-128px sprite scale, subtle differences won't read. Only bold differences (color, hat, obvious tool) should differentiate specialists. Don't over-detail accessories that disappear at scale.
*Decided by: Andrea*

**2026-03-27 — CAG vs RAG analogy corrected**
CAG = big books pre-loaded on workstation, heavy backpack, fast access. RAG = index card box, light backpack, fetch on demand from pantry. Every tool/reference grabbed → backpack grows (context consumed).
*Decided by: Andrea*

**2026-03-27 — Andrea signs off characters first (Phase 0)**
Character models need emotes v2 arm movements finished before any batch rendering. Andrea does this manually in Blender, confirms what's ready, THEN Claude renders sprites. No autonomous rendering without sign-off.
*Decided by: Andrea*
