# Phase 0 — Interface Negotiation
# Lock 05 Visibility Lock — v2 Full Rebuild
# Execute with: /build-with-agent-team or manually spawn agents below

## Context

<context>
The Visibility Lock: a central opaque working core (16m×16m, Z=0-8) surrounded by an elevated viewing ring (Z=5-9). The public orbits the machine on a perimeter ramp that wraps 3/4 of the building. Two exit stairs (NW and SE). Roof at Z=10.

MCP target: `envelope` (port 9002)
Archibase: `H:\Shared drives\City 101\archibase`

This is a REBUILD. The v1 model failed because agents built independently and accumulated 33 corrections across 4 review rounds. This time: discuss first, agree on every interface, THEN build.
</context>

## Team Assembly

<team>
Spawn 4 agents. ALL agents receive this entire prompt. NO agent builds geometry — this phase is DISCUSSION ONLY.

### Agent 1: LEAD (coordinator)
Role: Facilitate discussion, resolve disputes, compile the shared spec. Does NOT propose geometry — only asks questions and forces agents to be specific. Uses authority hierarchy from v3 workflow.

### Agent 2: STRUCTURE
Role: Proposes column grid, beam layout, slab levels, foundation strategy.
Must query Archibase before proposing: `structural_grids.md`, `floor_systems.md`, `foundation_types.md`
Owns: columns, beams, slabs, foundations

### Agent 3: ENVELOPE
Role: Proposes wall splits (all 4 core faces), ring walls, stair enclosures, roof, thermal envelope.
Must query Archibase: `wall_systems.md`, `roof_systems.md`, `facade_systems.md`
Owns: walls, ring volumes, glazing, roof system, gap cladding

### Agent 4: CIRCULATION
Role: Proposes ramp geometry (TRUE SLOPES), stair flights, handrails (PIPES), parapets, landings, doors.
Must query Archibase: `accessibility_sia500.md`, `stair_railing_systems.md`, `swiss_fire_code.md`
Owns: ramps, stairs, handrails, parapets, doors, public path
</team>

## Discussion Protocol

<instructions>
### Round 1: Each agent proposes their system (sequential, 3 proposals)

STRUCTURE goes first:
- Propose the column grid (positions, sizes, Z ranges)
- Propose floor slabs (ground slab extent, mezzanine, ring floor, ring ceiling, roof slab)
- Propose beam layout (transfer beams core→outriggers, roof beams)
- State: "I need X at Z=Y" for every level datum

ENVELOPE goes second:
- Propose core walls (all 4 faces, split for openings — specify EVERY piece with coordinates)
- Propose ring outer walls (all 4 faces, split for slot windows)
- Propose ring inner glazing (curtain wall with mullions, transoms)
- Propose stair enclosure walls (NW and SE, with ceiling slabs for fire compartment)
- Propose roof assembly (slab + parapets + vapor/insulation/membrane/gravel)
- Propose gap cladding (Z=9 to Z=10 at ring perimeter)
- State: "My wall base is at Z=X, my wall top is at Z=Y, my opening is at Z=A to Z=B"

CIRCULATION goes third:
- Propose the perimeter ramp: EXACT slope calculation (total rise, total run, grade %)
- For each ramp run: start point (x,y,z), end point (x,y,z), width, slab thickness
- Propose ramp geometry method: `rs.AddSrfPt` for sloped quads — specify all 8 corners per slab
- Propose parapets that FOLLOW THE SLOPE (same method, 1.1m above walking surface at every point)
- Propose handrails as PIPES (`rs.AddPipe`, 40mm diameter, 0.875m above walking surface)
- Propose stair flights: rise, going, number of risers per flight, landing sizes
- Propose ALL doors: worker entry, cargo entry, ramp-to-ring entry, stair-to-ring doors, stair exits
- State: "I arrive at Z=X where your slab is" for every connection

### Round 2: Interface negotiation (all agents at the table)

LEAD asks each pair to resolve their boundaries:

1. **Structure ↔ Envelope**: Do wall bases match slab tops? Do columns fit inside walls or outside? Do beams interfere with wall openings?

2. **Structure ↔ Circulation**: Does the ramp arrive at the correct ring floor Z? Do stair flights land on real slabs? Are there ground slabs under all circulation elements?

3. **Envelope ↔ Circulation**: Where does the ramp enter the ring (which wall, what opening)? Where do stairs connect to the ring (which wall, what door)? Do parapets conflict with ring outer walls?

4. **All three**: Trace the public path from ground to ring — every element it touches, every Z transition, every door it passes through. Is it continuous? Is it SIA 500 compliant?

5. **All three**: Trace the fire escape from the farthest point on the ring to ground — every element, every door, every stair. Is it VKF compliant (≤35m)?

For EACH interface:
- Who owns the boundary element?
- What is the exact Z-height / coordinate?
- What happens if there's a conflict? (Use authority hierarchy)

### Round 3: Compilation

LEAD compiles everything into THREE documents:

1. **element_catalog.md** — every element in the model:
```
| # | Name | Layer | Owner | Geometry | Coordinates | Notes |
```
Geometry types: BOX (for axis-aligned), SLAB_SLOPED (for ramp, 8 corners), PIPE (for handrails), TEXTDOT

2. **interface_registry.md** — every boundary:
```
| Interface | Owner | Ref agent | Z-height | Rule |
```

3. **coordination_spec.md** — the master build document combining both

### Round 4: Sign-off

Each agent reads the full element_catalog and verifies:
- Every element I own is listed with correct coordinates
- Every interface I share is listed with the agreed rule
- My system is structurally/code complete (no missing lintels, no missing handrails, no unsealed enclosures)

If ANY agent objects → resolve in discussion → update spec → re-verify.
Only after ALL agents sign off does Phase 1 begin.
</instructions>

## Geometry Standards

<standards>
### Sloped slab (ramp runs, sloped parapets)
```python
def sloped_slab(name, x1,y1,z1_start, x2,y2,z2_end, width, thickness, layer):
    """Create a slab that slopes from z1_start to z2_end."""
    # Top face (walking surface)
    t1 = (x1, y1, z1_start)
    t2 = (x2, y1, z2_end)
    t3 = (x2, y2, z2_end)
    t4 = (x1, y2, z1_start)
    # Bottom face (soffit)
    b1 = (x1, y1, z1_start - thickness)
    b2 = (x2, y1, z2_end - thickness)
    b3 = (x2, y2, z2_end - thickness)
    b4 = (x1, y2, z1_start - thickness)
    # Build 6 surfaces
    top = rs.AddSrfPt([t1,t2,t3,t4])
    bot = rs.AddSrfPt([b1,b2,b3,b4])
    s1 = rs.AddSrfPt([t1,t2,b2,b1])
    s2 = rs.AddSrfPt([t2,t3,b3,b2])
    s3 = rs.AddSrfPt([t3,t4,b4,b3])
    s4 = rs.AddSrfPt([t4,t1,b1,b4])
    brep = rs.JoinSurfaces([top,bot,s1,s2,s3,s4], delete_input=True)
    rs.ObjectName(brep, name)
    rs.ObjectLayer(brep, layer)
    return brep
```

### Pipe handrail
```python
def pipe_handrail(name, points, radius=0.02, layer=None):
    """Create a pipe handrail along a list of points."""
    crv = rs.AddPolyline(points)
    pipe = rs.AddPipe(crv, 0, radius)
    rs.DeleteObject(crv)
    rs.ObjectName(pipe, name)
    if layer: rs.ObjectLayer(pipe, layer)
    return pipe
```

### Axis-aligned box (walls, slabs, columns — only for FLAT elements)
```python
def box(name, p1, p2, layer=None):
    if layer: rs.CurrentLayer(layer)
    corners = rs.AddBox([
        (p1[0],p1[1],p1[2]), (p2[0],p1[1],p1[2]),
        (p2[0],p2[1],p1[2]), (p1[0],p2[1],p1[2]),
        (p1[0],p1[1],p2[2]), (p2[0],p1[1],p2[2]),
        (p2[0],p2[1],p2[2]), (p1[0],p2[1],p2[2])
    ])
    rs.ObjectName(corners, name)
    return corners
```

### Rule: NEVER use `rs.AddBox` for sloped geometry. If Z varies across the element, use `sloped_slab` or `rs.AddSrfPt`.
</standards>

## V1 Failures to Avoid

<lessons>
1. Ramp as stepped boxes → must be true slopes with `AddSrfPt`
2. Parapets as fixed-Z boxes → must follow ramp slope, constant 1.1m above surface
3. Handrails as 40mm boxes → must be `AddPipe` with 20mm radius
4. South wall left solid → must have viewing panel like N/E/W
5. East wall missing piers → all 4 faces must have identical framing pattern
6. No south lintel → all 4 faces must have lintels in L350
7. Diagonal columns at r=11 (inside core) → must be at r=14 (outside core, inside ring)
8. No ground slab under ring/stairs/ramp → full footprint foundation
9. No stair landings at Z=5 → stair must connect to ring floor
10. No stair ceiling slabs → fire compartment must be sealed (walls + floor + ceiling)
11. No corner landing parapets → every elevated edge needs fall protection
12. No ramp-to-ring entry door → primary public access must have an opening
13. No stair-to-ring doors → circulation must be continuous
14. Ring floor gaps at corners → complete ring without holes
</lessons>

## Output

This phase produces 3 files in `output/city101_hub/lock_05_v2/`:
- `coordination_spec.md`
- `interface_registry.md`
- `element_catalog.md`

These files are the ONLY input to Phase 1. If it's not in the catalog, it doesn't get built.
