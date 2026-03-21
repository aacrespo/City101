# POC: Archibase → Agent Team → Rhino Geometry
# Rammed earth wall segment — all dimensions from archibase knowledge base
#
# Sources:
#   Thickness 400mm — rammed_earth.md (min load-bearing)
#   Density 1900 kg/m³ — ConstructionDB.get_material('earth_rammed')
#   Fire class A1 — ConstructionDB.get_material('earth_rammed')
#   REI 60 required — ConstructionDB.get_fire_requirement('habitation','low','mur_porteur')
#   Course height 150mm — rammed_earth.md (range 100-150mm)
#   Plinth 300mm — rammed_earth.md (min above grade)
#   KBOB 02.007.01 — ConstructionDB.get_kbob('terre')
#
# Units: Millimeters (Rhino document units)
# Layers: POC::Structure, POC::Annotations

import rhinoscriptsyntax as rs
import Rhino

# --- Create layers ---
if not rs.IsLayer("POC"):
    rs.AddLayer("POC", [200, 200, 200])
if not rs.IsLayer("POC::Structure"):
    rs.AddLayer("POC::Structure", [180, 120, 60], parent="POC")
if not rs.IsLayer("POC::Annotations"):
    rs.AddLayer("POC::Annotations", [100, 100, 100], parent="POC")

# --- Helper: create box from corner + dimensions ---
def make_box(x, y, z, length, width, height):
    """Create box from corner point + L/W/H. Returns GUID."""
    pts = [
        (x, y, z),
        (x + length, y, z),
        (x + length, y + width, z),
        (x, y + width, z),
        (x, y, z + height),
        (x + length, y, z + height),
        (x + length, y + width, z + height),
        (x, y + width, z + height),
    ]
    return rs.AddBox(pts)

# --- Wall body on POC::Structure ---
rs.CurrentLayer("POC::Structure")

wall = make_box(0, 0, 300, 3000, 400, 3000)
rs.ObjectName(wall, "Wall_L0_RE_Main")

# Set metadata on wall
rs.SetUserText(wall, "material", "earth_rammed")
rs.SetUserText(wall, "material_name", "Pisé (terre battue)")
rs.SetUserText(wall, "density_kg_m3", "1900")
rs.SetUserText(wall, "gwp_kgco2_per_kg", "0.015")
rs.SetUserText(wall, "compressive_strength_mpa", "2.0")
rs.SetUserText(wall, "fire_class", "A1")
rs.SetUserText(wall, "rei_achieved", "REI 90+ (code minimum REI 60)")
rs.SetUserText(wall, "thickness_mm", "400")
rs.SetUserText(wall, "thickness_source", "rammed_earth.md: min 400mm load-bearing")
rs.SetUserText(wall, "height_thickness_ratio", "7.5 (max 8.0)")
rs.SetUserText(wall, "course_height_mm", "150")
rs.SetUserText(wall, "kbob_id", "02.007.01")

# --- Plinth on POC::Structure ---
plinth = make_box(-50, -50, 0, 3100, 500, 300)
rs.ObjectName(plinth, "Plinth_L0_Concrete")

# --- Course lines on POC::Annotations ---
rs.CurrentLayer("POC::Annotations")
for i in range(20):
    z = 300 + (i + 1) * 150  # 450, 600, 750, ..., 3300
    line = rs.AddLine((0, 0, z), (3000, 0, z))
    rs.ObjectName(line, "Course_{:02d}".format(i + 1))

print("BUILD COMPLETE")
print("  Wall: 3000x400x3000mm at z=300")
print("  Plinth: 3100x500x300mm at z=0")
print("  Courses: 20 lines from z=450 to z=3300")
