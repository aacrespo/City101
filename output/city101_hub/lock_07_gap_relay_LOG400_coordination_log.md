# Coordination Log — Lock 07 Gap Relay

## Roundtable Corrections Applied

| # | Issue | Resolution |
|---|-------|-----------|
| C1 | Hub roof slab 250mm too thin for 10m span | Increased to 350mm. Roof slab Z=[7.0, 7.35] |
| C2 | No ring beam at column heads | Added octagonal ring beam at Z=6.73-7.0, IPE 270 |
| C3 | Arm C missing transfer beam | Added transfer beam at NE chamfer, 0.40m x 0.30m |
| C4 | Arm C ramp needs 25m but arm is only 12.5m | Reduced rise to 0.75m (6% over 12.5m). Floor Z=0 to Z=0.75 |
| C5 | Arm roofs missing insulation | Arms treated as semi-open transition spaces (no full insulation). Hub walls at arm openings form thermal boundary |
| C6 | NE chamfer gap Z=5.25-7.0 | Added infill glazing panels above Arm C roof to hub roof level |
| C7 | Skylight fall protection | Added 1.1m guardrail around skylight at roof level |
| C8 | Solid parapets -> transparent railings | Replaced 0.15m solid parapets with 1.1m steel railings |
| C9 | Canopy C axis-aligned | Rotated to 45deg diamond orientation |
| C10 | Canopy A/B flush with arm roof | Lowered to Z=3.5 (0.5m below arm roof) |
| C11 | Railing posts: 17 per side -> 18 per side | Fixed count |
| C12 | Diagonal geometry must use extrusion, not AddBox | Using rs.AddSrfPt + JoinSurfaces for all 45deg elements |
| C13 | Missing LOG400 elements | Added: glass panels at arm ends, splice plates, panel joints, door+hardware, skylight glass, drainage |

## Decisions (chronological)

- [BUILD START] All corrections from roundtable applied. Building with corrected dimensions.
- [DESIGN] Arms treated as unconditioned transition spaces. Thermal boundary at hub walls.
- [DESIGN] Arm C rise reduced from 1.5m to 0.75m to maintain 6% grade within 12.5m arm length.

## Round Summary

- Pre-build: Roundtable complete. 13 corrections applied. Proceeding to Phase 1.
