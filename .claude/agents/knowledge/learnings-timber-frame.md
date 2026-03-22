# Timber Frame Modeling Learnings

Techniques and decisions from Cabin v3 timber frame build. Updated by Timber Agent.

---

## 1. Stone-timber transition is a design problem, not just a construction detail

The transition from stone masonry to timber frame is the most important interface in a mixed-material building. Three problems must be solved simultaneously:
- **Capillary break**: Moisture wicks from stone into timber through direct contact. A bitumen membrane (3mm) between sablière top and timber structure prevents this. This is from timber_construction.md: "Capillary break between timber and concrete/stone — never direct contact."
- **Thermal seal**: The material change creates a potential thermal bridge. Compriband expanding foam tape (2cm) fills irregularities and seals the junction.
- **Width reconciliation**: Stone wall (40cm) is wider than timber frame (34cm). The 6cm difference must be resolved architecturally. In Swiss vernacular, the stone base projects slightly outward — this overhang sheds water away from the timber above.

## 2. Width reconciliation: center with 3cm projection each side

Decision: timber frame is inset 3cm from the stone exterior face on all sides. This gives:
- 3cm stone overhang on exterior — water protection for timber base
- 3cm offset on interior — becomes a natural shelf/service zone at the transition
- Clean facade reading: stone base projects slightly beyond timber upper floor (historically correct)

## 3. Floor assembly sits ON the transition, not directly on sablière

The intermediate floor gypsum ceiling (bottom layer) sits on top of the thermal seal strip (z=272.3), not directly on the sablière (z=270). The transition layers (capillary break + thermal seal = 2.3cm) shift the entire floor assembly up by 2.3cm from the sablière top. This is architecturally correct — timber should never touch stone directly.

## 4. Joist bearing and fire stops

Joists span N-S, bearing on the sablières (y=10.5 to y=589.5). Fire stops (mineral wool blocking) fill the gaps between joists at the perimeter where they pass over the wall. This prevents fire from traveling through the joist cavity into the wall assembly and blocks air movement that would compromise the thermal envelope.

## 5. Frame wall layer order matters for build logic

The 7-layer timber frame wall assembly (from archibase: wall_timber_frame_ext) must be built exterior-to-interior:
1. Timber cladding (2.2cm) — rainscreen, ventilated
2. Ventilated air gap (3.0cm) — pressure equalization, drainage
3. Wood fibre board (6.0cm) — wind barrier, additional insulation
4. Studs + mineral wool (16.0cm) — primary structure + insulation
5. OSB vapour barrier (1.5cm) — airtightness layer (CRITICAL for envelope)
6. Service cavity (4.0cm) — electrical/plumbing without penetrating OSB
7. Gypsum plasterboard (1.25cm) — interior finish, fire protection

Total: 33.95cm ≈ 34cm

## 6. Window voids must cut through ALL 7 layers

When building wall layers with window openings, every layer must have the same void cut. The approach used: split each layer into 5 pieces around each window (below, above, left, between, right). This is the same principle as Learning #5 in learnings-walls.md — render/plaster must account for openings, not just structural courses.

## 7. Upper wall plate centered on wall assembly, not on studs

The upper wall plate (150x100mm oak) sits on top of the entire frame wall, centered on the 34cm assembly width. This distributes roof loads through all wall layers, not just the studs. Centered position: 3cm + (34-15)/2 = 3 + 9.5 = 12.5cm from stone exterior face.

## 8. E/W walls butt into S/N walls at interior face

East and west frame walls span between the interior faces of the south and north frame walls (y=37 to y=563). This creates a clean corner junction where the S/N walls are continuous (stronger for wind loads on the long faces) and E/W walls are infill. The S/N walls run the full 800cm building length.

## 9. Floor finish level determines wall base, not sablière top

Upper floor timber frame walls start at z=307.5 (floor finish level), not at z=272.3 (transition top) or z=270 (sablière top). The floor assembly occupies 35.2cm between the transition and the wall base. This means the clear ground floor height is z=0 to z=272.3 (gypsum ceiling of floor) = 272.3cm, and upper floor clear height is z=307.5 to z=557.5 = 250cm.

---

*Created: 2026-03-22 — Timber Agent, Cabin v3 build*
