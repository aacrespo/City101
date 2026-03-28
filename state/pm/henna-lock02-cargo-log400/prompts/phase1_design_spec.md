# Phase 1 — Design: Lock 02 Cargo LOG400 Execution Spec
# PM Project: henna-lock02-cargo-log400
# Status: ACTIVE

---

## Your role

You are the architect agent for Lock Type 02 — Cargo Lock. Your job is to write a complete LOG400 execution specification for this building, ready for a structural reviewer to check and an executor to build in Rhino.

**Output file**: `output/city101_hub/lock_02_cargo_LOG400_execution_plan.md`

---

## Reference materials to read first

1. `prompts/[A04_ACTIVE]_lock_type_02_cargo.md` — the base concept (volumes, structure, openings, layers). This is your ground truth for the building's geometry.
2. `output/city101_hub/lock_01_border_LOG400_APPROVED.md` — the approved spec for Lock 01. Use this as your format template and engineering reference. Follow the same section structure, coordinate precision, and element naming conventions.
3. `00_Workflow_v04.md` section 2.4 — LOG400 definition: "Full assembly detail, materiality."

---

## Coordinate system — CRITICAL

Rhino document units: Centimeters.
Geometry is built in METER-SCALE values (e.g., X=-24 means 24 as a number, displayed as "24 cm" but conceptually 24m).

**ALL coordinates in this spec must be meter-scale. Use them exactly as written. Do NOT multiply by 100.**

X = corridor axis (negative = West/Entry, positive = East/Exit)
Y = lateral axis (positive = North, negative = South)
Z = vertical (0 = finished floor level)

---

## Base geometry recap (from concept prompt)

| Volume | X | Y | Z |
|--------|---|---|---|
| Logistics Hall | [-24, 24] | [-11, 11] | [0, 5] |
| Observation Corridor | [-20, 20] | [-4, 4] | [6, 10] |
| Entry Stair | [-24, -20] | [-4, 4] | [0, 6] |
| Exit Stair | [20, 24] | [-4, 4] | [0, 6] |
| Loading Dock Canopy | [-28, -24] | [-8, 8] | [3, 5.5] |

Structural columns (6 main): X=[-16, 0, +16] × Y=[+8, -8], 400mm × 400mm (0.4 × 0.4 units), Z=[0, 10]
Dock columns (4): X=[-28, -24] × Y=[+8, -8], 150mm × 150mm, Z=[0, 5.5]
Beams: longitudinal at Y=±4, Z=6, spanning X=[-20, 20]

Wall thicknesses: 300mm (0.3 units) for all enclosing walls.

---

## What LOG400 adds (your task)

The base model has: Volumes, Circulation, Structure, Openings, Annotations layers (LOG200–300).
You must specify the following LOG400 elements:

### 1. Roof System (L300_Roof layer)
- **Logistics Hall roof slab** — flat RC slab on top of Z=5 walls. Calculate appropriate thickness using span/30 rule. The 22m hall width is column-supported at Y=±8, giving 3m cantilevers + 16m primary span. Use appropriate structural logic (beam + slab? waffle? just note the system, model as flat box).
- **Logistics Hall parapets** — perimeter of logistics hall roof. Note: observation corridor sits at Z=6 on the inner portion. Parapet height ≥ 1070mm per SIA 358 where there is a drop > 1000mm.
- **Observation Corridor roof slab** — flat RC slab on top of Z=10 walls. Lightweight (public corridor, not heavy equipment). Span/30 for 8m width.
- **Observation Corridor parapets** — on N, S, E faces (West face abuts Entry Stair top).
- **Loading Dock Canopy roof** — the canopy volume (Z=[3, 5.5]) already exists as a volume. Add a thin roof slab on top (Z=5.5), with a 1.5% drainage fall to the south.

### 2. Roof Assembly Layers (L400_Material)
Three-layer build-up inside parapets for each roof zone:
- 120mm XPS insulation
- 5mm waterproofing membrane
- 50mm gravel ballast

Follow the same offset-from-parapet logic as lock_01 APPROVED sections 1.6–1.8.

### 3. Parapet Edge Conditions (L400_Material)
- 20mm × 150mm waterproofing upstand at inner parapet face
- 30mm × 20mm drip edge at outer parapet top corner

### 4. Structural Connections (L350_Detail)
- **Column base plates** — 500mm × 500mm × 25mm steel plate, top flush with Z=0, centered on each of the 6 main columns and 4 dock columns = 10 elements total.
- **Column top bearing plates** — 500mm × 500mm × 20mm, at column top (logistics hall columns: Z=5.0; observation corridor columns run full height to Z=10.0).
- **Cantilever brackets** — at each main column, supporting the observation corridor overhang. The corridor spans X=[-20,20] but columns are at X=[-16,0,16]. The 4m overhang (from column to corridor end at X=±20) needs brackets. Design: 300mm wide × 200mm deep × 400mm projection from column face, at Z=5.8 (below corridor floor slab).

### 5. Formwork Lines (L400_Material)
- 20mm wide × 20mm tall boxes proud of wall face by 20mm
- Cast in 2400mm (2.4 unit) lifts
- Logistics Hall walls (5m tall): lift at Z=2.4 only
- Observation Corridor walls (4m tall, Z=[6,10]): lift at Z=8.4 only
- Exposed outer faces only (not interior interfaces between volumes)

### 6. Expansion Joints (L400_Material)
- Logistics Hall is 48m long. Place joints at X=-8 and X=+8 (dividing hall into three ~16m bays matching sorting bay separators).
- 20mm-wide colored solid boxes, continuous through walls and roof slab.

### 7. Opening Frames (L350_Detail)
- West truck bay (X=-24): steel hollow section 100×100mm frame + RC lintel
- East dispatch (X=+24): matching frame + lintel
- Observation south glazing wall (Y=-4): aluminum curtain wall frame — model as thin (50mm) frame boxes at perimeter of glazed zone
- North slot windows (5×): individual frames
- Floor viewing slots (3×, at X=[-8,0,8]): steel edge frame 80mm × 80mm running perimeter of each 4m × 4m slot

### 8. Facade Panel Joints (L400_Material)
- Logistics Hall north and south outer faces: vertical panel joints at X = -16, -8, 0, +8, +16
- 5mm wide × 20mm deep incised boxes, full wall height Z=[0, 5]

---

## New layers to create

```
Type_02_Cargo::L300_Roof    — RGB(200, 155, 100)  — roof slabs, parapets
Type_02_Cargo::L350_Detail  — RGB(160, 115, 70)   — connections, frames, brackets
Type_02_Cargo::L400_Material — RGB(120, 85, 50)   — formwork, joints, hardware, edge conditions
```

Do NOT rename or alter existing layers:
- `Type_02_Cargo::Volumes`
- `Type_02_Cargo::Circulation`
- `Type_02_Cargo::Structure`
- `Type_02_Cargo::Openings`
- `Type_02_Cargo::Annotations`

---

## Output format requirements

Follow the exact same structure as `output/city101_hub/lock_01_border_LOG400_APPROVED.md`:
- Section for each system
- Named elements with `L300_`, `L350_`, `L400_` prefixes
- Corner A / Corner B coordinates for each box
- Rationale for structural decisions
- Execution Summary table (element counts)
- Build order list
- Executor Notes section

Mark this file as: `Status: DRAFT FOR ROUNDTABLE REVIEW — do NOT execute until approved`

---

## Flags to raise if uncertain

If any coordinate or structural decision is ambiguous, insert a `[FLAG N: description]` comment in the spec. The reviewer will resolve it. Do not silently guess — flag it.

Examples of good flags:
- `[FLAG 1: Observation corridor roof at Z=10 — do parapets conflict with stair volume top at Z=6?]`
- `[FLAG 2: Cantilever bracket orientation — attach to column face or logistics roof slab?]`
