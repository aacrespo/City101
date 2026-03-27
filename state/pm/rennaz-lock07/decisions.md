# Decisions Log — Rennaz Lock 07

Append-only. Every design decision with rationale.

---

## 2026-03-27 — Phase 0 Spec Preparation

### D01: Material system = Timber
**Decision**: Glulam GL24h structure, CLT slabs, timber platform frame walls.
**Why**: Archibase has deepest knowledge in timber (Deplazes, Vittone, SIA 265). Aligns with IBOIS/thesis direction. Swiss precedent for timber pedestrian bridges. Negative GWP (-0.7 kgCO₂/kg).
**Rejected**: Steel (archibase has profiles but less assembly knowledge), concrete (heavier ecological footprint, doesn't align with thesis).

### D02: Deck elevation = +4.0m
**Decision**: Keep bridge deck at 4.0m above ground (from v2/v3 scripts).
**Why**: Needs to clear Route 9 cantonal highway infrastructure below. Creates the vertical separation that defines the lock as elevated connector.

### D03: Hospital ramp = switchback (SIA 500 compliant)
**Decision**: Replace v3's 26.7% grade ramp with 4-run switchback at 6% + elevator.
**Why**: v3 ramp violates SIA 500 (max 6%). For LOG 400 / LOD 400, code compliance is non-negotiable. The switchback becomes an architectural feature — the "equalization descent" where dwell time happens.
**Impact**: Hospital end footprint grows from 8×15m to 18×10m. Total model Y-range extends to ~48m (north side).

### D04: Wall assembly = Deplazes p.428 (timber platform frame, 276mm)
**Decision**: 7-layer assembly: 24mm larch + 40mm cavity + 18mm softboard + 120mm studs/insulation + 12mm plywood + 50mm service cavity + 12mm finish.
**Why**: Directly from archibase reference (Deplazes "Constructing Architecture"). Well-documented, buildable, Swiss standard. LOG 400 means modeling each layer as a separate solid.

### D05: Roof assembly = Deplazes p.475 (flat cold deck, 336mm)
**Decision**: Flat roof: bitumen felt + 21mm plywood + 300mm joists/insulation + 15mm plywood.
**Why**: Flat roof matches the linear/modern bridge aesthetic. Cold deck with ventilation cavity prevents condensation in timber construction. Simpler than pitched for this bridge typology.

### D06: Bay spacing = 6m
**Decision**: 11 structural bays at 6m centers along bridge span (Y=-30 to Y=30).
**Why**: GL24h 140×320mm can span 8m for pedestrian loads (5.0 kN/m² per SIA 261 category C4). 6m is comfortable, gives fine structural rhythm, matches v2/v3 proportions.

### D07: Team = 4 modelers + 1 lead = 5 total
**Decision**: Site, Structure, Envelope, Circulation agents + Lead coordinator.
**Why**: Below 8-agent cap (v3 workflow). Each agent has clear domain boundaries. Roof is handled by Envelope agent (horizontal assembly, same principles). Fewer agents = more robust for overnight autonomous operation.

### D08: Foundation = concrete pad footings + steel shoes
**Decision**: 600×600×400mm concrete pads under each column, 800mm below grade. Steel shoe connectors (Rothoblaas-type) with 30mm capillary break.
**Why**: Timber must never contact concrete directly (moisture). Steel shoes are standard Swiss practice. 800mm depth for frost protection (Swiss Plateau). Pad footings appropriate for flat terrain with good bearing soil (moraine/gravel at Rennaz, ~375m ASL near lake).

### D09: Elevator = hospital-grade stretcher-capable
**Decision**: 1100×2100mm cabin, 900mm door, serves +4.0m and 0.0m.
**Why**: Hospital context — must accommodate stretchers, wheelchairs, medical equipment. SIA 500 requires stretcher-capable elevator in healthcare-adjacent public buildings. Shaft at west end (X=-6 to -3.5) keeps it clear of ramp circulation.

### D10: Fire design = REI 60 via charring
**Decision**: Timber structure achieves REI 60 through charring design (39mm sacrificial layer per exposed face at 0.65mm/min).
**Why**: VKF/AEAI: low-rise (<11m) permits timber with REI 60. Charring is simpler than encapsulation for this building type. Sacrificial layer noted in metadata, not modeled as separate geometry (it's the outer 39mm of the structural member).
