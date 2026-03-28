# Lock Type 07 — Gap Relay
# LOG400 Execution Spec: ROUNDTABLE-APPROVED
# Status: APPROVED — built and verified
# Approved by: Roundtable Reviewer (5-panel: Structure, Code, Envelope, Visual, Constructability)
# Date: 2026-03-27

---

## CORRECTIONS FROM ROUNDTABLE REVIEW

13 issues identified. 3 structural showstoppers, 3 code violations, 4 envelope breaks, 4 visual issues resolved.

| # | Issue | Resolution |
|---|-------|-----------|
| C1 | Hub roof slab 250mm too thin for 10m span (span/30 = 353mm) | Increased to 350mm. Roof slab Z=[7.0, 7.35] |
| C2 | No ring beam tying column heads — star pattern is a mechanism | Added octagonal ring beam (8 segments) at Z=6.73-7.0, IPE 270 |
| C3 | Arm C missing transfer beam at hub junction | Added transfer beam at NE chamfer, 0.40m x 0.30m, spanning arm width |
| C4 | Arm C only 12.5m long but ramp needs 25m for 1.5m rise at 6% | Reduced rise to 0.75m (6% over 12.5m run). Floor Z=0 to Z=0.75 |
| C5 | Arm roofs missing insulation assembly | Arms treated as semi-open transition spaces. Hub walls form thermal boundary |
| C6 | NE chamfer gap Z=5.25-7.0 (no wall, no glass) | Added infill glazing panels closing hub envelope above Arm C roof |
| C7 | Skylight 4m x 4m opening — no fall protection | Added 1.1m steel guardrail around skylight at finished roof level |
| C8 | Solid 0.15m parapets contradict "porous junction" concept | Replaced with transparent 1.1m steel railings at roof perimeter |
| C9 | Canopy C axis-aligned, doesn't match 45deg arm diagonal | Rotated canopy to 45deg diamond orientation |
| C10 | Canopy A/B flush with arm roof (Z=4.0), visually merged | Lowered canopy roofs to Z=3.5 (0.5m gap from arm roof) |
| C11 | Railing post count: 17 per side should be 18 (for 13m ramp) | Corrected to 10 posts per side (13m / 1.5m = 8.67 intervals) |
| C12 | Diagonal geometry (Arm C) cannot use rs.AddBox | Used box_pts with explicit 8-corner construction for all 45deg elements |
| C13 | ~40 LOG400 elements missing from original spec | Added: glass panels, splice plates, panel joints, door+hardware, skylight glass, drainage, thresholds |

---

## BUILD RESULTS

| Metric | Value |
|--------|-------|
| Total objects | 229 |
| Named objects | 229/229 (100%) |
| Material-tagged | 229/229 (100%) |
| Layers used | 8/8 |
| Model extent X | [-20.0, 18.6] |
| Model extent Y | [-20.0, 18.6] |
| Model extent Z | [-0.70, 8.72] |

### Layer Distribution

| Layer | Objects |
|-------|---------|
| Volumes | 19 |
| Circulation | 29 |
| Structure | 77 |
| Openings | 31 |
| Annotations | 10 |
| L300_Roof | 10 |
| L350_Detail | 22 |
| L400_Material | 31 |

### LOG400 Compliance

| Category | Status |
|----------|--------|
| Formwork lines (2400mm lifts) | PASS |
| Expansion joints (every 6m) | PASS |
| Material breaks (panel joints) | PASS |
| Connections (splice plates) | PASS |
| Hardware (hinges, handles) | PASS |
| Base plates | PASS |
| DPC | PASS |
| Drainage | PASS |
| Door with hardware | PASS |

### Review Gates

| Gate | Status | Notes |
|------|--------|-------|
| Gate 1 — Self-review | PASS | All naming, metadata, Z-heights verified |
| Gate 2 — Bilateral | PASS | Structure-shell-roof interfaces aligned |
| Gate 3 — Full model | PASS | Constraint check + visual coherence verified |

---

## ARCHIBASE SOURCES

All dimensions grounded in Archibase construction knowledge system:

| Element | Source |
|---------|--------|
| Hub columns (RC 300x300) | steel_structures.md: ~350kN -> HEA 200 equiv |
| Arm columns (HEA 200) | steel_profiles database |
| Hub roof beams (IPE 270) | steel_structures.md: span/25 rule |
| Ground slab (300mm) | concrete_systems.md: span/30 |
| Roof assembly (warm deck) | details_roof_parapet.md: Deplazes p.470 |
| Pad footings (1.0x1.0x0.4m) | foundation_types.md: 3x column width |
| Ramp grade (6% max) | SIA 500 (accessibility) |
| Railing height (1.1m) | SIA 358 (public buildings) |
| Curtain wall mullions (50x50mm Al) | facade_systems.md: stick system |
| IGU triple glazing (40mm) | facade_systems.md: Minergie standard |
| Fire rating (REI 60) | swiss_fire_code.md: public <11m |
| Frost depth (800mm min) | foundation_types.md: Swiss standard |
