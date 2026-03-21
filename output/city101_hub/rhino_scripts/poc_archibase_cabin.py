"""
POC Archibase Cabin — Rammed Earth Cabin in Rhino
==================================================
All dimensions in centimeters. Rhino units = cm.

Material constraints sourced from archibase ConstructionDB:
  - Rammed earth: 400mm min load-bearing, H:T <= 8:1, density 1900 kg/m3
  - Plinth: >= 300mm above grade (capillary moisture protection)
  - Foundation: 800mm depth (Swiss frost depth), wider than wall
  - Lintels: GL24h glulam, 20cm bearing beyond opening
  - Fire: REI 60 required (habitation/low-rise), rammed earth provides REI 90

Cabin spec:
  Plan: 500 x 400 cm exterior (5m x 4m)
  Wall thickness: 40 cm (400mm, min for load-bearing)
  Interior: 420 x 320 cm
  Wall height: 300 cm (H:T = 7.5, within <= 8 limit)
  Foundation depth: 80 cm below grade
  Plinth height: 30 cm above grade
  Door: south wall, centered, 90 x 210 cm
  Window: east wall, centered, 120 x 100 cm
  Roof: gable, timber glulam ridge + softwood rafters
"""

import rhinoscriptsyntax as rs
import math


# =====================================================================
# LAYERS
# =====================================================================
layers = [
    ['Cabin::Terrain', [120, 160, 80]],
    ['Cabin::Foundation', [160, 160, 160]],
    ['Cabin::Structure::Walls', [180, 130, 70]],
    ['Cabin::Structure::Lintels', [200, 170, 100]],
    ['Cabin::Structure::Roof', [140, 100, 60]],
    ['Cabin::Annotations', [100, 100, 100]],
]

for item in layers:
    name = item[0]
    color = item[1]
    if not rs.IsLayer(name):
        rs.AddLayer(name, color)


# =====================================================================
# 1. TERRAIN
# =====================================================================
rs.CurrentLayer("Cabin::Terrain")
corners = [[-200, -200, 0], [700, -200, 0], [700, 600, 0], [-200, 600, 0]]
terrain = rs.AddSrfPt(corners)
rs.ObjectName(terrain, "Terrain_Grade")
rs.SetUserText(terrain, "type", "reference_plane")
rs.SetUserText(terrain, "elevation_cm", "0")


# =====================================================================
# 2. FOUNDATION STRIP
# =====================================================================
rs.CurrentLayer("Cabin::Foundation")

# 90cm wide, centered on 40cm wall centerline (45cm each side)
# Outer: (-25,-25) to (525,425). Inner: (65,65) to (435,335). z=-80 to 0

foundation_boxes = [
    ["Foundation_South", [[-25, -25, -80], [525, -25, -80], [525, 65, -80], [-25, 65, -80],
                          [-25, -25, 0], [525, -25, 0], [525, 65, 0], [-25, 65, 0]]],
    ["Foundation_North", [[-25, 335, -80], [525, 335, -80], [525, 425, -80], [-25, 425, -80],
                          [-25, 335, 0], [525, 335, 0], [525, 425, 0], [-25, 425, 0]]],
    ["Foundation_West", [[-25, 65, -80], [65, 65, -80], [65, 335, -80], [-25, 335, -80],
                         [-25, 65, 0], [65, 65, 0], [65, 335, 0], [-25, 335, 0]]],
    ["Foundation_East", [[435, 65, -80], [525, 65, -80], [525, 335, -80], [435, 335, -80],
                         [435, 65, 0], [525, 65, 0], [525, 335, 0], [435, 335, 0]]],
]

for item in foundation_boxes:
    obj = rs.AddBox(item[1])
    rs.ObjectName(obj, item[0])
    rs.SetUserText(obj, "material", "concrete_c25_30")
    rs.SetUserText(obj, "depth_cm", "80")
    rs.SetUserText(obj, "width_cm", "90")
    rs.SetUserText(obj, "frost_protection", "Swiss_standard_800mm")
    rs.SetUserText(obj, "source", "ConstructionDB")


# =====================================================================
# 3. PLINTH
# =====================================================================
# 50cm wide (5cm overhang each side), z=0 to 30
# Door opening in south wall: x=205 to x=295

plinth_boxes = [
    ["Plinth_South_Left", [[-5, -5, 0], [205, -5, 0], [205, 45, 0], [-5, 45, 0],
                           [-5, -5, 30], [205, -5, 30], [205, 45, 30], [-5, 45, 30]]],
    ["Plinth_South_Right", [[295, -5, 0], [505, -5, 0], [505, 45, 0], [295, 45, 0],
                            [295, -5, 30], [505, -5, 30], [505, 45, 30], [295, 45, 30]]],
    ["Plinth_North", [[-5, 355, 0], [505, 355, 0], [505, 405, 0], [-5, 405, 0],
                      [-5, 355, 30], [505, 355, 30], [505, 405, 30], [-5, 405, 30]]],
    ["Plinth_West", [[-5, 45, 0], [45, 45, 0], [45, 355, 0], [-5, 355, 0],
                     [-5, 45, 30], [45, 45, 30], [45, 355, 30], [-5, 355, 30]]],
    ["Plinth_East", [[455, 45, 0], [505, 45, 0], [505, 355, 0], [455, 355, 0],
                     [455, 45, 30], [505, 45, 30], [505, 355, 30], [455, 355, 30]]],
]

for item in plinth_boxes:
    obj = rs.AddBox(item[1])
    rs.ObjectName(obj, item[0])
    rs.SetUserText(obj, "material", "concrete_c25_30")
    rs.SetUserText(obj, "height_cm", "30")
    rs.SetUserText(obj, "width_cm", "50")
    rs.SetUserText(obj, "purpose", "capillary_moisture_barrier")
    rs.SetUserText(obj, "source", "ConstructionDB+rammed_earth.md")


# =====================================================================
# 4. RAMMED EARTH WALLS
# =====================================================================
rs.CurrentLayer("Cabin::Structure::Walls")

wall_meta = {
    "material": "earth_rammed",
    "density_kg_m3": "1900",
    "gwp_kgco2_per_kg": "0.015",
    "fire_class": "A1",
    "fire_rating": "REI 90",
    "thickness_cm": "40",
    "compressive_strength_mpa": "2.0",
    "thermal_conductivity": "0.7",
    "ht_ratio": "7.5",
    "source": "ConstructionDB+rammed_earth.md",
}

wall_boxes = [
    # South wall with door opening (door x=205-295, z=30-240)
    ["Wall_South_Left", [[0, 0, 30], [205, 0, 30], [205, 40, 30], [0, 40, 30],
                         [0, 0, 330], [205, 0, 330], [205, 40, 330], [0, 40, 330]]],
    ["Wall_South_Right", [[295, 0, 30], [500, 0, 30], [500, 40, 30], [295, 40, 30],
                          [295, 0, 330], [500, 0, 330], [500, 40, 330], [295, 40, 330]]],
    ["Wall_South_AboveDoor", [[205, 0, 240], [295, 0, 240], [295, 40, 240], [205, 40, 240],
                              [205, 0, 330], [295, 0, 330], [295, 40, 330], [205, 40, 330]]],
    # North wall (solid)
    ["Wall_North", [[0, 360, 30], [500, 360, 30], [500, 400, 30], [0, 400, 30],
                    [0, 360, 330], [500, 360, 330], [500, 400, 330], [0, 400, 330]]],
    # East wall with window (window y=140-260, z=130-230)
    ["Wall_East_BelowWindow", [[460, 40, 30], [500, 40, 30], [500, 360, 30], [460, 360, 30],
                               [460, 40, 130], [500, 40, 130], [500, 360, 130], [460, 360, 130]]],
    ["Wall_East_AboveWindow", [[460, 40, 230], [500, 40, 230], [500, 360, 230], [460, 360, 230],
                               [460, 40, 330], [500, 40, 330], [500, 360, 330], [460, 360, 330]]],
    ["Wall_East_LeftOfWindow", [[460, 40, 130], [500, 40, 130], [500, 140, 130], [460, 140, 130],
                                [460, 40, 230], [500, 40, 230], [500, 140, 230], [460, 140, 230]]],
    ["Wall_East_RightOfWindow", [[460, 260, 130], [500, 260, 130], [500, 360, 130], [460, 360, 130],
                                 [460, 260, 230], [500, 260, 230], [500, 360, 230], [460, 360, 230]]],
    # West wall (solid)
    ["Wall_West", [[0, 40, 30], [40, 40, 30], [40, 360, 30], [0, 360, 30],
                   [0, 40, 330], [40, 40, 330], [40, 360, 330], [0, 360, 330]]],
]

for item in wall_boxes:
    obj = rs.AddBox(item[1])
    rs.ObjectName(obj, item[0])
    for key in wall_meta:
        rs.SetUserText(obj, key, wall_meta[key])


# =====================================================================
# 5. COURSE LINES
# =====================================================================
rs.CurrentLayer("Cabin::Annotations")

course_num = 0
z = 45
while z <= 330:
    course_num = course_num + 1
    pts = [[0, 0, z], [500, 0, z], [500, 400, z], [0, 400, z], [0, 0, z]]
    crv = rs.AddPolyline(pts)
    name = "Course_%02d" % course_num
    rs.ObjectName(crv, name)
    rs.SetUserText(crv, "type", "construction_annotation")
    rs.SetUserText(crv, "course_height_cm", "15")
    rs.SetUserText(crv, "source", "rammed_earth.md")
    z = z + 15


# =====================================================================
# 6. LINTELS
# =====================================================================
rs.CurrentLayer("Cabin::Structure::Lintels")

lintel_meta = {
    "material": "timber_glulam",
    "grade": "GL24h",
    "section_cm": "14x20",
    "bearing_length_cm": "20",
    "compressive_strength_mpa": "24.0",
    "density_kg_m3": "480",
    "gwp_kgco2_per_kg": "-0.7",
    "fire_class": "D",
    "source": "ConstructionDB+timber_construction.md",
}

# Door lintel
lintel_d = rs.AddBox([[185, 13, 240], [315, 13, 240], [315, 27, 240], [185, 27, 240],
                      [185, 13, 260], [315, 13, 260], [315, 27, 260], [185, 27, 260]])
rs.ObjectName(lintel_d, "Lintel_Door")
for key in lintel_meta:
    rs.SetUserText(lintel_d, key, lintel_meta[key])

# Window lintel
lintel_w = rs.AddBox([[473, 120, 230], [487, 120, 230], [487, 280, 230], [473, 280, 230],
                      [473, 120, 250], [487, 120, 250], [487, 280, 250], [473, 280, 250]])
rs.ObjectName(lintel_w, "Lintel_Window")
for key in lintel_meta:
    rs.SetUserText(lintel_w, key, lintel_meta[key])


# =====================================================================
# 7. ROOF STRUCTURE
# =====================================================================
rs.CurrentLayer("Cabin::Structure::Roof")

# Sill plates (wall-width x 15cm height)
sill_boxes = [
    ["Sill_South", [[0, 0, 330], [500, 0, 330], [500, 40, 330], [0, 40, 330],
                    [0, 0, 345], [500, 0, 345], [500, 40, 345], [0, 40, 345]]],
    ["Sill_North", [[0, 360, 330], [500, 360, 330], [500, 400, 330], [0, 400, 330],
                    [0, 360, 345], [500, 360, 345], [500, 400, 345], [0, 400, 345]]],
    ["Sill_West", [[0, 40, 330], [40, 40, 330], [40, 360, 330], [0, 360, 330],
                   [0, 40, 345], [40, 40, 345], [40, 360, 345], [0, 360, 345]]],
    ["Sill_East", [[460, 40, 330], [500, 40, 330], [500, 360, 330], [460, 360, 330],
                   [460, 40, 345], [500, 40, 345], [500, 360, 345], [460, 360, 345]]],
]

for item in sill_boxes:
    obj = rs.AddBox(item[1])
    rs.ObjectName(obj, item[0])
    rs.SetUserText(obj, "material", "timber_softwood")
    rs.SetUserText(obj, "density_kg_m3", "450")
    rs.SetUserText(obj, "gwp_kgco2_per_kg", "-0.7")
    rs.SetUserText(obj, "source", "ConstructionDB")

# Ridge beam: 14x20cm glulam at y=200, z=400-420
ridge = rs.AddBox([[-20, 193, 400], [520, 193, 400], [520, 207, 400], [-20, 207, 400],
                   [-20, 193, 420], [520, 193, 420], [520, 207, 420], [-20, 207, 420]])
rs.ObjectName(ridge, "Ridge_Beam")
rs.SetUserText(ridge, "material", "timber_glulam")
rs.SetUserText(ridge, "grade", "GL24h")
rs.SetUserText(ridge, "section_cm", "14x20")
rs.SetUserText(ridge, "density_kg_m3", "480")
rs.SetUserText(ridge, "gwp_kgco2_per_kg", "-0.7")
rs.SetUserText(ridge, "source", "ConstructionDB")

# Rafters: 8x24cm softwood
rise = 55.0  # z: 345 to 400
run_s = 180.0  # y: 20 to 200 (wall center to ridge)
slope_len = math.sqrt(rise * rise + run_s * run_s)
sin_a = rise / slope_len
cos_a = run_s / slope_len
dy_depth = 24.0 * sin_a
dz_depth = 24.0 * cos_a

x_positions = [62.5, 187.5, 312.5, 437.5]

for i in range(len(x_positions)):
    x = x_positions[i]
    hw = 4.0

    # South side
    b1 = [x - hw, 20, 345]
    b2 = [x + hw, 20, 345]
    b3 = [x + hw, 200, 400]
    b4 = [x - hw, 200, 400]
    t1 = [x - hw, 20 - dy_depth, 345 + dz_depth]
    t2 = [x + hw, 20 - dy_depth, 345 + dz_depth]
    t3 = [x + hw, 200 - dy_depth, 400 + dz_depth]
    t4 = [x - hw, 200 - dy_depth, 400 + dz_depth]
    rafter_s = rs.AddBox([b1, b2, b3, b4, t1, t2, t3, t4])
    rs.ObjectName(rafter_s, "Rafter_South_%02d" % (i + 1))
    rs.SetUserText(rafter_s, "material", "timber_softwood")
    rs.SetUserText(rafter_s, "section_cm", "8x24")
    rs.SetUserText(rafter_s, "density_kg_m3", "450")
    rs.SetUserText(rafter_s, "source", "ConstructionDB")

    # North side
    b1n = [x - hw, 380, 345]
    b2n = [x + hw, 380, 345]
    b3n = [x + hw, 200, 400]
    b4n = [x - hw, 200, 400]
    t1n = [x - hw, 380 + dy_depth, 345 + dz_depth]
    t2n = [x + hw, 380 + dy_depth, 345 + dz_depth]
    t3n = [x + hw, 200 + dy_depth, 400 + dz_depth]
    t4n = [x - hw, 200 + dy_depth, 400 + dz_depth]
    rafter_n = rs.AddBox([b1n, b2n, b3n, b4n, t1n, t2n, t3n, t4n])
    rs.ObjectName(rafter_n, "Rafter_North_%02d" % (i + 1))
    rs.SetUserText(rafter_n, "material", "timber_softwood")
    rs.SetUserText(rafter_n, "section_cm", "8x24")
    rs.SetUserText(rafter_n, "density_kg_m3", "450")
    rs.SetUserText(rafter_n, "source", "ConstructionDB")


print("POC Archibase Cabin complete")
print("Objects: 1 terrain + 4 foundation + 5 plinth + 9 walls + 20 courses + 2 lintels + 4 sills + 1 ridge + 8 rafters = 54 total")
