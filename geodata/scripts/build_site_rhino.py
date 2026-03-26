"""Build a 3D site model in Rhino from extracted geodata.

This script is a reference for agents using Rhino MCP.
It reads from geodata/sites/{name}/ and creates:
  - Terrain mesh on TERRAIN layer
  - Building meshes (LOD2) on BUILDINGS_CONTEXT layer
  - Railway curves on RAILWAYS layer
  - Road curves on ROADS layer
  - Water curves on WATER layer
  - Empty design layers

Usage from Rhino Python console or via MCP execute_python_code:
  Adjust SITE_NAME and SITE_DIR, then run.
"""

import json
import os
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc

# --- Configuration ---
SITE_NAME = "morges"  # Change this
SITE_DIR = os.path.join(os.path.dirname(__file__), "..", "sites", SITE_NAME)


def build_terrain(site_dir):
    """Create terrain mesh from terrain.json."""
    terrain_path = os.path.join(site_dir, "terrain.json")
    if not os.path.exists(terrain_path):
        print("terrain.json not found, skipping terrain")
        return None

    with open(terrain_path) as f:
        terrain = json.load(f)

    origin_x, origin_y = terrain["origin"]
    res = terrain["resolution"]
    rows = terrain["rows"]
    cols = terrain["cols"]
    elevations = terrain["elevations"]

    mesh = rg.Mesh()

    for r in range(rows):
        for c in range(cols):
            x = origin_x + c * res
            y = origin_y - r * res  # Origin is top-left, Y decreases
            z = elevations[r][c]
            if z is None or z != z:  # NaN check
                z = 0
            mesh.Vertices.Add(x, y, z)

    for r in range(rows - 1):
        for c in range(cols - 1):
            i = r * cols + c
            mesh.Faces.AddFace(i, i + 1, i + cols + 1, i + cols)

    mesh.Normals.ComputeNormals()
    mesh.Compact()

    guid = sc.doc.Objects.AddMesh(mesh)
    if guid:
        rs.ObjectLayer(guid, "TERRAIN")
        rs.ObjectName(guid, "terrain_{}".format(SITE_NAME))
        print("Terrain: {}x{} grid, {} vertices".format(rows, cols, mesh.Vertices.Count))
    return guid


def build_buildings(site_dir):
    """Create building meshes from buildings.json (LOD2 TIN geometry)."""
    buildings_path = os.path.join(site_dir, "buildings.json")
    if not os.path.exists(buildings_path):
        print("buildings.json not found, skipping buildings")
        return []

    with open(buildings_path) as f:
        buildings = json.load(f)

    count = 0
    for bldg in buildings:
        verts = bldg.get("vertices", [])
        faces = bldg.get("faces", [])

        if not verts or not faces:
            # Fallback: extrude from footprint if no mesh data
            footprint = bldg.get("footprint", [])
            ground_z = bldg.get("ground_z", 0)
            roof_z = bldg.get("roof_z", ground_z + 10)
            if len(footprint) < 3:
                continue
            pts = [rg.Point3d(p[0], p[1], ground_z) for p in footprint]
            if pts[0].DistanceTo(pts[-1]) > 0.01:
                pts.append(pts[0])
            crv = rg.PolylineCurve([rg.Point3d(p.X, p.Y, p.Z) for p in pts])
            guid = sc.doc.Objects.AddCurve(crv)
            if guid:
                rs.ObjectLayer(guid, "BUILDINGS_CONTEXT")
                height = max(roof_z - ground_z, 1)
                srf = rs.ExtrudeCurveStraight(guid, (0, 0, 0), (0, 0, height))
                if srf:
                    rs.CapPlanarHoles(srf)
                    rs.ObjectLayer(srf, "BUILDINGS_CONTEXT")
                rs.DeleteObject(guid)
                count += 1
            continue

        # Build mesh from vertices + faces (preferred path)
        mesh = rg.Mesh()
        for v in verts:
            mesh.Vertices.Add(v[0], v[1], v[2])
        for face in faces:
            if len(face) >= 3:
                mesh.Faces.AddFace(face[0], face[1], face[2])

        mesh.Normals.ComputeNormals()
        mesh.Compact()

        if mesh.IsValid:
            guid = sc.doc.Objects.AddMesh(mesh)
            if guid:
                rs.ObjectLayer(guid, "BUILDINGS_CONTEXT")
                count += 1

    print("Buildings: {} created".format(count))
    return count


def build_infrastructure(site_dir):
    """Create infrastructure curves from infrastructure.json."""
    infra_path = os.path.join(site_dir, "infrastructure.json")
    if not os.path.exists(infra_path):
        print("infrastructure.json not found, skipping infrastructure")
        return

    with open(infra_path) as f:
        infra = json.load(f)

    layer_map = {
        "railways": "RAILWAYS",
        "roads": "ROADS",
        "water": "WATER",
    }

    for category, layer_name in layer_map.items():
        features = infra.get(category, [])
        count = 0
        for feat in features:
            coords = feat.get("geometry", [])
            if len(coords) < 2:
                continue
            points = []
            for c in coords:
                x, y = c[0], c[1]
                z = c[2] if len(c) >= 3 else 0
                points.append(rg.Point3d(x, y, z))
            if len(points) >= 2:
                crv = rg.PolylineCurve(points)
                guid = sc.doc.Objects.AddCurve(crv)
                if guid:
                    rs.ObjectLayer(guid, layer_name)
                    count += 1
        print("{}: {} curves".format(layer_name, count))


def setup_layers():
    """Create layer structure for the site model."""
    layers = {
        "TERRAIN": (160, 155, 140),
        "BUILDINGS_CONTEXT": (200, 195, 185),
        "RAILWAYS": (100, 100, 110),
        "ROADS": (170, 170, 165),
        "WATER": (100, 150, 200),
        "SITE_BOUNDARY": (255, 100, 100),
        "DESIGN": (100, 150, 255),
        "STRUCTURE": (180, 180, 175),
        "LANDSCAPE": (120, 170, 100),
    }

    for name, color in layers.items():
        if not rs.IsLayer(name):
            rs.AddLayer(name, rs.CreateColor(*color))


def main():
    print("Building site model: {}".format(SITE_NAME))
    print("Reading from: {}".format(SITE_DIR))

    if not os.path.isdir(SITE_DIR):
        print("Site directory not found: {}".format(SITE_DIR))
        print("Run extract_site.py first:")
        print("  python geodata/scripts/extract_site.py --name \"{}\" --node 3 --radius 750".format(SITE_NAME))
        return

    rs.UnitSystem(4)  # meters
    setup_layers()
    build_terrain(SITE_DIR)
    build_buildings(SITE_DIR)
    build_infrastructure(SITE_DIR)

    rs.Command("-_Zoom _Extents ", False)
    sc.doc.Views.Redraw()
    print("Done. Design layers ready for work.")


if __name__ == "__main__":
    main()
