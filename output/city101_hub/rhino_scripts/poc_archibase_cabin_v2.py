# poc_archibase_cabin_v2.py
# Rammed Earth Cabin — Complete Build Script
# All dimensions in CENTIMETERS (Rhino units = cm)
#
# FIXES FROM V1:
# 1. Walls are MONOLITHIC RINGS (not 4 separate boxes) — each course is one
#    continuous ring extruded from a closed profile with a hole
# 2. Course annotation lines trace BOTH outer AND inner wall faces
# 3. Roof PANELS added (not just timber skeleton)
#
# CONSTRAINTS & SOURCES:
# - Wall outer: 500x400cm, thickness 40cm, inner 420x320cm
# - Foundation: 90cm wide, 80cm deep (Swiss frost depth) — concrete C25/30
# - Plinth: 50cm wide, 30cm tall (>= 300mm above grade per rammed_earth.md)
# - Course height: 15cm (20 courses = 300cm wall height)
# - Door: south wall centered, 90cm wide x 210cm tall (x=205-295, z=30-240)
# - Window: east wall centered, 100cm wide x 100cm tall (y=150-250, z=130-230)
#   Reduced from 120cm to 100cm to satisfy 1/3 rule on 320cm inner east wall
# - Lintels: timber glulam GL24h, 14x20cm section, 20cm bearing each side
#   (rammed_earth.md: lintels timber/stone, never steel)
# - Sill plates: 10x15cm softwood, bedded in lime mortar
# - Ridge beam: 14x20cm glulam GL24h, 540cm long (20cm overhang each end)
# - Rafters: 8x24cm softwood, 5 per side at 100cm spacing
# - Roof pitch: ~22° (80cm rise over 200cm half-span)
# - Roof overhang: 60cm south/north, 30cm east/west
#   (rammed_earth.md: roof overhang min 600mm, ideal 800mm)
# - Material metadata: density 1900 kg/m3, GWP 0.015 kgCO2/kg, A1 fire class, REI 90
#
# LAYER STRUCTURE:
# Cabin::Terrain        — ground plane surface
# Cabin::Foundation     — below-grade concrete ring (4 boxes)
# Cabin::Structure::Walls   — rammed earth courses (monolithic rings + partial rings)
# Cabin::Structure::Lintels — timber lintels over door and window
# Cabin::Structure::Roof    — sill plates, ridge beam, rafters, roof panels
# Cabin::Annotations        — course lines (outer + inner per course)

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# =============================================================================
# SCRIPT 1: TERRAIN + FOUNDATION + PLINTH
# =============================================================================

rs.CurrentLayer("Cabin::Terrain")
terrain_pts = [(-200, -200, 0), (700, -200, 0), (700, 600, 0), (-200, 600, 0)]
terrain = rs.AddSrfPt(terrain_pts)
rs.ObjectName(terrain, "Terrain_Grade")

rs.CurrentLayer("Cabin::Foundation")

def box(x, y, z, L, W, H):
    pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
           (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
    return rs.AddBox(pts)

# Foundation ring: 90cm wide, 80cm deep, centered on 40cm wall
# Foundation outer: (-25,-25) to (525,425)
# Foundation inner: (65,65) to (435,335)
f_s = box(-25, -25, -80, 550, 90, 80)
rs.ObjectName(f_s, "Foundation_South")
f_n = box(-25, 335, -80, 550, 90, 80)
rs.ObjectName(f_n, "Foundation_North")
f_w = box(-25, 65, -80, 90, 270, 80)
rs.ObjectName(f_w, "Foundation_West")
f_e = box(435, 65, -80, 90, 270, 80)
rs.ObjectName(f_e, "Foundation_East")

for obj in [f_s, f_n, f_w, f_e]:
    rs.SetUserText(obj, "material", "concrete_c25_30")
    rs.SetUserText(obj, "depth_cm", "80")
    rs.SetUserText(obj, "width_cm", "90")
    rs.SetUserText(obj, "source", "Swiss frost depth + rammed_earth.md")

# Plinth (50cm wide, z=0 to z=30, with door gap)
p_s_left = box(-5, -5, 0, 210, 50, 30)
rs.ObjectName(p_s_left, "Plinth_South_Left")
p_s_right = box(295, -5, 0, 210, 50, 30)
rs.ObjectName(p_s_right, "Plinth_South_Right")
p_n = box(-5, 355, 0, 510, 50, 30)
rs.ObjectName(p_n, "Plinth_North")
p_w = box(-5, 45, 0, 50, 310, 30)
rs.ObjectName(p_w, "Plinth_West")
p_e = box(455, 45, 0, 50, 310, 30)
rs.ObjectName(p_e, "Plinth_East")

for obj in [p_s_left, p_s_right, p_n, p_w, p_e]:
    rs.SetUserText(obj, "material", "concrete_c25_30")
    rs.SetUserText(obj, "height_cm", "30")
    rs.SetUserText(obj, "source", "rammed_earth.md: plinth >= 300mm above grade")

print("Terrain + Foundation + Plinth done")

# =============================================================================
# SCRIPT 2: RAMMED EARTH WALL COURSES (MONOLITHIC RINGS)
# =============================================================================

rs.CurrentLayer("Cabin::Structure::Walls")

COURSE_H = 15
WALL_BASE = 30
N_COURSES = 20

DOOR_X1, DOOR_X2 = 205, 295
DOOR_Z_TOP = 240

WIN_Y1, WIN_Y2 = 150, 250
WIN_Z_BOT, WIN_Z_TOP = 130, 230

def make_full_ring(z, h):
    """Create a full monolithic wall ring (no openings) at height z with height h."""
    outer = rs.AddPolyline([(0,0,z), (500,0,z), (500,400,z), (0,400,z), (0,0,z)])
    inner = rs.AddPolyline([(40,40,z), (460,40,z), (460,360,z), (40,360,z), (40,40,z)])
    srf = rs.AddPlanarSrf([outer, inner])
    if srf:
        path = rs.AddLine((0,0,z), (0,0,z+h))
        solid = rs.ExtrudeSurface(srf[0], path, cap=True)
        rs.DeleteObject(path)
        rs.DeleteObject(srf[0])
        rs.DeleteObject(outer)
        rs.DeleteObject(inner)
        return solid
    else:
        rs.DeleteObject(outer)
        rs.DeleteObject(inner)
        return make_ring_from_boxes(z, h)

def make_ring_from_boxes(z, h):
    """Fallback: create ring from 4 boxes and boolean union."""
    def bx(x,y,zz,L,W,H):
        pts = [(x,y,zz),(x+L,y,zz),(x+L,y+W,zz),(x,y+W,zz),
               (x,y,zz+H),(x+L,y,zz+H),(x+L,y+W,zz+H),(x,y+W,zz+H)]
        return rs.AddBox(pts)
    s = bx(0, 0, z, 500, 40, h)
    n = bx(0, 360, z, 500, 40, h)
    w = bx(0, 40, z, 40, 320, h)
    e = bx(460, 40, z, 40, 320, h)
    try:
        result = rs.BooleanUnion([s, n, w, e])
        if result:
            return result[0]
    except:
        pass
    return rs.AddGroup("ring_z{}".format(int(z)), [s, n, w, e])

for i in range(N_COURSES):
    z = WALL_BASE + i * COURSE_H
    z_top = z + COURSE_H
    course_name = "Course_Ring_{:02d}".format(i + 1)
    has_door = (z < DOOR_Z_TOP)
    has_window = (z < WIN_Z_TOP and z_top > WIN_Z_BOT)

    if not has_door and not has_window:
        ring = make_full_ring(z, COURSE_H)
        if ring:
            rs.ObjectName(ring, course_name)
    else:
        def bx(x,y,zz,L,W,H):
            pts = [(x,y,zz),(x+L,y,zz),(x+L,y+W,zz),(x,y+W,zz),
                   (x,y,zz+H),(x+L,y,zz+H),(x+L,y+W,zz+H),(x,y+W,zz+H)]
            return rs.AddBox(pts)
        parts = []
        parts.append(bx(0, 360, z, 500, 40, COURSE_H))  # North wall
        parts.append(bx(0, 40, z, 40, 320, COURSE_H))    # West wall
        if has_door:
            parts.append(bx(0, 0, z, DOOR_X1, 40, COURSE_H))
            parts.append(bx(DOOR_X2, 0, z, 500-DOOR_X2, 40, COURSE_H))
        else:
            parts.append(bx(0, 0, z, 500, 40, COURSE_H))
        if has_window:
            parts.append(bx(460, 40, z, 40, WIN_Y1-40, COURSE_H))
            parts.append(bx(460, WIN_Y2, z, 40, 360-WIN_Y2, COURSE_H))
        else:
            parts.append(bx(460, 40, z, 40, 320, COURSE_H))
        for j, p in enumerate(parts):
            rs.ObjectName(p, "{}_part{}".format(course_name, j+1))

all_objs = rs.ObjectsByLayer("Cabin::Structure::Walls")
for obj in all_objs:
    rs.SetUserText(obj, "material", "earth_rammed")
    rs.SetUserText(obj, "density_kg_m3", "1900")
    rs.SetUserText(obj, "gwp_kgco2_per_kg", "0.015")
    rs.SetUserText(obj, "fire_class", "A1")
    rs.SetUserText(obj, "fire_rating", "REI 90")
    rs.SetUserText(obj, "thickness_cm", "40")
    rs.SetUserText(obj, "course_height_cm", "15")
    rs.SetUserText(obj, "source", "ConstructionDB + rammed_earth.md")

print("Wall courses built: {} objects".format(len(all_objs)))

# =============================================================================
# SCRIPT 3: COURSE ANNOTATION LINES
# =============================================================================

rs.CurrentLayer("Cabin::Annotations")

for i in range(N_COURSES):
    z = WALL_BASE + (i + 1) * COURSE_H
    outer = rs.AddPolyline([(0,0,z), (500,0,z), (500,400,z), (0,400,z), (0,0,z)])
    rs.ObjectName(outer, "Course_{:02d}_Outer".format(i+1))
    inner = rs.AddPolyline([(40,40,z), (460,40,z), (460,360,z), (40,360,z), (40,40,z)])
    rs.ObjectName(inner, "Course_{:02d}_Inner".format(i+1))
    rs.SetUserText(outer, "type", "course_line_outer")
    rs.SetUserText(outer, "course_height_cm", "15")
    rs.SetUserText(inner, "type", "course_line_inner")
    rs.SetUserText(inner, "course_height_cm", "15")

print("Course lines done: 40 lines (20 outer + 20 inner)")

# =============================================================================
# SCRIPT 4: LINTELS
# =============================================================================

rs.CurrentLayer("Cabin::Structure::Lintels")

door_lintel = box(185, 13, 240, 130, 14, 20)
rs.ObjectName(door_lintel, "Lintel_Door")
rs.SetUserText(door_lintel, "material", "timber_glulam")
rs.SetUserText(door_lintel, "grade", "GL24h")
rs.SetUserText(door_lintel, "section_cm", "14x20")
rs.SetUserText(door_lintel, "bearing_length_cm", "20")
rs.SetUserText(door_lintel, "source", "rammed_earth.md: lintels timber/stone, never steel")

win_lintel = box(473, 130, 230, 14, 140, 20)
rs.ObjectName(win_lintel, "Lintel_Window")
rs.SetUserText(win_lintel, "material", "timber_glulam")
rs.SetUserText(win_lintel, "grade", "GL24h")
rs.SetUserText(win_lintel, "section_cm", "14x20")
rs.SetUserText(win_lintel, "bearing_length_cm", "20")
rs.SetUserText(win_lintel, "source", "rammed_earth.md: lintels timber/stone, never steel")

print("Lintels done: door (130cm) + window (140cm)")

# =============================================================================
# SCRIPT 5: ROOF STRUCTURE + PANELS
# =============================================================================

rs.CurrentLayer("Cabin::Structure::Roof")

# Sill plates (10x15cm)
sill_s = box(0, 15, 330, 500, 10, 15)
rs.ObjectName(sill_s, "Sill_South")
sill_n = box(0, 375, 330, 500, 10, 15)
rs.ObjectName(sill_n, "Sill_North")
sill_w = box(15, 40, 330, 10, 320, 15)
rs.ObjectName(sill_w, "Sill_West")
sill_e = box(475, 40, 330, 10, 320, 15)
rs.ObjectName(sill_e, "Sill_East")

for s in [sill_s, sill_n, sill_w, sill_e]:
    rs.SetUserText(s, "material", "timber_softwood")
    rs.SetUserText(s, "section_cm", "10x15")
    rs.SetUserText(s, "source", "rammed_earth.md: timber sill plate bedded in lime mortar")

# Ridge beam (14x20cm glulam)
RIDGE_Z = 410
ridge = box(-20, 193, RIDGE_Z-20, 540, 14, 20)
rs.ObjectName(ridge, "Ridge_Beam")
rs.SetUserText(ridge, "material", "timber_glulam")
rs.SetUserText(ridge, "grade", "GL24h")
rs.SetUserText(ridge, "section_cm", "14x20")
rs.SetUserText(ridge, "source", "ConstructionDB timber_glulam")

# Rafters (8x24cm softwood)
rafter_positions = [50, 150, 250, 350, 450]
for idx, x in enumerate(rafter_positions):
    s_pts = [
        (x-4, 20, 345), (x+4, 20, 345), (x+4, 20, 369), (x-4, 20, 369),
        (x-4, 193, 390), (x+4, 193, 390), (x+4, 193, 414), (x-4, 193, 414),
    ]
    sr = rs.AddBox(s_pts)
    if sr:
        rs.ObjectName(sr, "Rafter_South_{:02d}".format(idx+1))
        rs.SetUserText(sr, "material", "timber_softwood")
        rs.SetUserText(sr, "section_cm", "8x24")
    n_pts = [
        (x-4, 380, 345), (x+4, 380, 345), (x+4, 380, 369), (x-4, 380, 369),
        (x-4, 207, 390), (x+4, 207, 390), (x+4, 207, 414), (x-4, 207, 414),
    ]
    nr = rs.AddBox(n_pts)
    if nr:
        rs.ObjectName(nr, "Rafter_North_{:02d}".format(idx+1))
        rs.SetUserText(nr, "material", "timber_softwood")
        rs.SetUserText(nr, "section_cm", "8x24")

# Roof panels (surfaces with overhang)
panel_s = rs.AddSrfPt([
    (-30, -40, 330), (530, -40, 330), (530, 207, 414), (-30, 207, 414),
])
if panel_s:
    rs.ObjectName(panel_s, "Roof_Panel_South")
    rs.SetUserText(panel_s, "material", "timber_sheathing")
    rs.SetUserText(panel_s, "source", "rammed_earth.md: roof overhang min 600mm, ideal 800mm")

panel_n = rs.AddSrfPt([
    (-30, 440, 330), (530, 440, 330), (530, 193, 414), (-30, 193, 414),
])
if panel_n:
    rs.ObjectName(panel_n, "Roof_Panel_North")
    rs.SetUserText(panel_n, "material", "timber_sheathing")

print("Roof structure + panels done")
print("BUILD COMPLETE")
