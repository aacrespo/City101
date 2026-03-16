# LOG Level Checklist — 3D Model Review

Element checklist per LOG level. Used by the review panel and modeler to verify completeness.

## LOG 300 — Defined

All of these must be present:
- [ ] Façade divisions on all faces (opaque vs glazed zones)
- [ ] Structural elements: columns, beams, slabs with correct cross-sections
- [ ] All openings: doors (≥900mm clear), windows, voids with exact positions
- [ ] Floor plates at all levels
- [ ] Roof defined (not just a top face)
- [ ] Correct overall dimensions matching spatial plan

## LOG 350 — Coordinated

Everything from LOG 300, plus:
- [ ] Mullion grids on glazed façades (module from concept)
- [ ] Railings: height 1100mm, post spacing ≤1500mm
- [ ] Stairs: runs + landings, rise 170mm / run 290mm
- [ ] Key architectural details from the lock concept
- [ ] Connections between elements shown (column-to-beam, wall-to-slab)

## LOG 400 — Detailed

Everything from LOG 350, plus:
- [ ] Material breaks: concrete panel joints, timber stud lines, steel splice plates
- [ ] Connections: column-beam joints, wall-slab interfaces, foundation edges
- [ ] Hardware: hinges, handles, gate mechanisms (from concept)
- [ ] Panel joints on curtain walls at module grid
- [ ] Formwork lines on concrete (2400mm lifts)
- [ ] Expansion joints where required (every 6m on long elements)

## Material-Span Reference

| Material | Max simple span | Typical slab depth | Notes |
|----------|----------------|--------------------|-------|
| Timber | ≤8m | span/20 | Stud spacing 600mm OC |
| Steel | ≤15m | span/25 | Splice plates at connections |
| Concrete | ≤12m | span/30 | Formwork lines at 2400mm lifts |

## Accessibility Minimums (SIA 500)

| Element | Requirement |
|---------|-------------|
| Ramp grade | ≤6% (landing every 6m of run) |
| Ramp width | ≥1200mm |
| Door clear width | ≥900mm |
| Threshold height | ≤25mm |
| Turning radius | ≥1500mm at direction changes and in front of doors |
| Handrails | Both sides of ramps/stairs, 850–900mm height |
| Elevator car | Min 1100×1400mm clear, 900mm door |
| Controls | 900–1200mm height |
| Tactile guidance | Path from entry to key destinations |

## Layer Convention

```
Lock_XX::L200_Volumes
Lock_XX::L300_Structure
Lock_XX::L350_Detail
Lock_XX::L400_Material
Site_XX::Terrain
Site_XX::Buildings
Site_XX::Rail
Site_XX::Roads
```

## Material Colors (layer colors for visual distinction)

| Material | RGB |
|----------|-----|
| Concrete | (180, 180, 175) |
| Steel | (140, 150, 160) |
| Glass | (200, 220, 240) |
| Timber | (200, 170, 130) |
| Aluminum | (190, 195, 200) |

## Review Panel Trigger Points

Run the full 5-lens review panel after completing each LOG stage:
1. After reaching LOG 300 → review
2. After reaching LOG 350 → review
3. After reaching LOG 400 → review

**Iteration rules:**
- All 5 PASS → advance to next LOG stage
- Any FAIL → modeler fixes, re-run only failed lenses
- Max 3 iterations per LOG stage → escalate to human
- Only critical fixes block advancement; suggested improvements are optional
