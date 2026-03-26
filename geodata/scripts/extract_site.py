"""Extract terrain, buildings, and aerial imagery for a site along the Arc Lemanique.

Usage:
    python extract_site.py --name "lausanne_ouchy" --center 2534400 1151600 --radius 750
    python extract_site.py --name "morges" --bbox 2525800 1150700 2527800 1152700

All coordinates in EPSG:2056 (Swiss LV95). Outputs to geodata/sites/{name}/.
"""

import argparse
import json
import os
import sys

import numpy as np

# Add parent dir so we can import find_drive
sys.path.insert(0, os.path.dirname(__file__))
from find_drive import find_swisstopo_path

# Lazy imports for optional heavy libraries
rasterio = None
geopandas = None
fiona_mod = None
Image = None


def _import_rasterio():
    global rasterio
    if rasterio is None:
        import rasterio as _r
        from rasterio import windows as _w
        rasterio = _r
    return rasterio


def _import_geopandas():
    global geopandas
    if geopandas is None:
        import geopandas as _gp
        geopandas = _gp
    return geopandas


def _import_fiona():
    global fiona_mod
    if fiona_mod is None:
        import fiona as _f
        fiona_mod = _f
    return fiona_mod


def _import_pillow():
    global Image
    if Image is None:
        from PIL import Image as _I
        Image = _I
    return Image


def extract_terrain(vrt_path, bbox, output_dir):
    """Extract terrain elevation grid from VRT mosaic.

    Args:
        vrt_path: Path to swissALTI3D VRT file
        bbox: (west, south, east, north) in EPSG:2056
        output_dir: Where to write terrain.json

    Returns:
        dict with terrain metadata
    """
    rio = _import_rasterio()
    from rasterio.windows import from_bounds

    west, south, east, north = bbox

    with rio.open(vrt_path) as src:
        window = from_bounds(west, south, east, north, src.transform)
        data = src.read(1, window=window)
        win_transform = src.window_transform(window)

        # Build elevation grid
        rows, cols = data.shape
        origin_x = win_transform.c
        origin_y = win_transform.f
        resolution = abs(win_transform.a)

        # Replace nodata with NaN for JSON
        if src.nodata is not None:
            data = np.where(data == src.nodata, float('nan'), data)

        # Convert to nested list (row-major, north to south)
        elevations = data.tolist()

        terrain = {
            "origin": [origin_x, origin_y],
            "resolution": resolution,
            "rows": rows,
            "cols": cols,
            "bbox": list(bbox),
            "crs": "EPSG:2056",
            "elevation_unit": "meters_asl",
            "elevation_range": [float(np.nanmin(data)), float(np.nanmax(data))],
            "elevations": elevations
        }

        out_path = os.path.join(output_dir, "terrain.json")
        with open(out_path, "w") as f:
            json.dump(terrain, f)

        size_mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"  Terrain: {rows}x{cols} grid, {resolution}m resolution")
        print(f"  Elevation range: {terrain['elevation_range'][0]:.1f}m - {terrain['elevation_range'][1]:.1f}m")
        print(f"  Written to: terrain.json ({size_mb:.1f} MB)")

        return {
            "rows": rows, "cols": cols, "resolution": resolution,
            "elevation_range": terrain["elevation_range"]
        }


def extract_buildings(gdb_path, bbox, output_dir):
    """Extract buildings from swissBUILDINGS3D FileGDB as 3D meshes.

    swissBUILDINGS3D stores each building as a 3D MultiPolygon containing
    30-70 triangle faces (TIN mesh). This function preserves the full LOD2
    geometry by exporting all triangles as mesh data (vertices + face indices).

    It also computes a 2D footprint (convex hull of all vertices projected
    to XY) and ground_z / roof_z from the Z range.

    Args:
        gdb_path: Path to swissBUILDINGS3D .gdb.zip
        bbox: (west, south, east, north) in EPSG:2056
        output_dir: Where to write buildings.json

    Returns:
        dict with building count and metadata
    """
    gpd = _import_geopandas()
    from shapely.geometry import box, MultiPoint
    from shapely.ops import unary_union

    bbox_geom = box(bbox[0], bbox[1], bbox[2], bbox[3])

    try:
        gdf = gpd.read_file(gdb_path, bbox=bbox_geom)
    except Exception as e:
        print(f"  Buildings: Could not read GDB ({e})")
        print(f"  Trying to list layers...")
        fio = _import_fiona()
        try:
            layers = fio.listlayers(gdb_path)
            print(f"  Available layers: {layers}")
            if layers:
                gdf = gpd.read_file(gdb_path, layer=layers[0], bbox=bbox_geom)
            else:
                return _write_empty_buildings(output_dir)
        except Exception as e2:
            print(f"  Could not read any layer: {e2}")
            return _write_empty_buildings(output_dir)

    if gdf.empty:
        return _write_empty_buildings(output_dir)

    type_col = _find_column(gdf, ["GEBAEUDEART", "BUILDING_TYPE", "building_type", "OBJEKTART", "TYP"])

    buildings = []
    for _, row in gdf.iterrows():
        geom = row.geometry
        if geom is None or geom.is_empty:
            continue

        # Collect all 3D triangle faces from the geometry
        polygons = []
        if geom.geom_type == "Polygon":
            polygons = [geom]
        elif geom.geom_type == "MultiPolygon":
            polygons = list(geom.geoms)
        else:
            continue

        if not polygons:
            continue

        # Build mesh: collect unique vertices and face indices
        vertex_map = {}  # (x, y, z) -> index
        vertices = []    # [[x, y, z], ...]
        faces = []       # [[i0, i1, i2], ...]
        all_z = []

        for poly in polygons:
            # Each polygon is a triangle face (exterior ring with 4 coords, last = first)
            coords = list(poly.exterior.coords)
            face_indices = []
            for c in coords[:-1]:  # skip closing duplicate
                x, y = round(c[0], 3), round(c[1], 3)
                z = round(c[2], 3) if len(c) >= 3 else 0.0
                key = (x, y, z)
                if key not in vertex_map:
                    vertex_map[key] = len(vertices)
                    vertices.append([x, y, z])
                face_indices.append(vertex_map[key])
                all_z.append(z)
            if len(face_indices) >= 3:
                faces.append(face_indices[:3])  # ensure triangles

        if not vertices or not faces:
            continue

        ground_z = round(min(all_z), 2)
        roof_z = round(max(all_z), 2)

        # Compute 2D footprint as convex hull of all vertex XY positions
        xy_points = [(v[0], v[1]) for v in vertices]
        hull = MultiPoint(xy_points).convex_hull
        if hull.geom_type == "Polygon":
            footprint = [[round(c[0], 3), round(c[1], 3)] for c in hull.exterior.coords]
        else:
            # Degenerate (line or point) - skip
            continue

        building = {
            "footprint": footprint,
            "ground_z": ground_z,
            "roof_z": roof_z,
            "vertices": vertices,
            "faces": faces,
        }
        if type_col and row.get(type_col):
            building["type"] = str(row[type_col])

        buildings.append(building)

    out_path = os.path.join(output_dir, "buildings.json")
    with open(out_path, "w") as f:
        json.dump(buildings, f)

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    total_faces = sum(len(b["faces"]) for b in buildings)
    total_verts = sum(len(b["vertices"]) for b in buildings)
    print(f"  Buildings: {len(buildings)} extracted ({total_faces} mesh faces, {total_verts} vertices)")
    print(f"  Available columns: {list(gdf.columns)}")
    print(f"  Written to: buildings.json ({size_mb:.1f} MB)")

    return {"count": len(buildings), "total_faces": total_faces, "columns": list(gdf.columns)}


def _write_empty_buildings(output_dir):
    out_path = os.path.join(output_dir, "buildings.json")
    with open(out_path, "w") as f:
        json.dump([], f)
    print("  Buildings: none found in bbox")
    return {"count": 0}


def _find_column(gdf, candidates):
    for col in candidates:
        if col in gdf.columns:
            return col
    return None


def _is_nan(val):
    if val is None:
        return True
    try:
        return np.isnan(float(val))
    except (ValueError, TypeError):
        return False


def extract_infrastructure(gpkg_path, bbox, output_dir, config):
    """Extract roads, railways, and water features from swissTLM3D GeoPackage.

    Args:
        gpkg_path: Path to swissTLM3D .gpkg.zip
        bbox: (west, south, east, north) in EPSG:2056
        output_dir: Where to write infrastructure.json
        config: Full config dict (for layer name lookup)

    Returns:
        dict with feature counts
    """
    gpd = _import_geopandas()
    from shapely.geometry import box

    bbox_geom = box(bbox[0], bbox[1], bbox[2], bbox[3])
    layer_map = config["datasets"]["infrastructure"]["layers"]

    infrastructure = {"railways": [], "roads": [], "water": []}

    # --- Railways ---
    try:
        rail_layer = layer_map["railways"]
        gdf = gpd.read_file(gpkg_path, layer=rail_layer, bbox=bbox_geom)
        for _, row in gdf.iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue
            coords = _geom_to_coords_3d(geom)
            if coords:
                feature = {"geometry": coords}
                if "objektart" in gdf.columns and row.get("objektart"):
                    feature["type"] = str(row["objektart"])
                if "name" in gdf.columns and row.get("name"):
                    feature["name"] = str(row["name"])
                if "kunstbaute" in gdf.columns and row.get("kunstbaute"):
                    feature["structure"] = str(row["kunstbaute"])
                infrastructure["railways"].append(feature)
        print(f"  Railways: {len(infrastructure['railways'])} features")
    except Exception as e:
        print(f"  Railways: extraction failed ({e})")

    # --- Roads ---
    try:
        road_layer = layer_map["roads"]
        gdf = gpd.read_file(gpkg_path, layer=road_layer, bbox=bbox_geom)
        for _, row in gdf.iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue
            coords = _geom_to_coords_3d(geom)
            if coords:
                feature = {"geometry": coords}
                if "objektart" in gdf.columns and row.get("objektart"):
                    feature["type"] = str(row["objektart"])
                if "stufe" in gdf.columns and row.get("stufe"):
                    feature["level"] = str(row["stufe"])
                infrastructure["roads"].append(feature)
        print(f"  Roads: {len(infrastructure['roads'])} features")
    except Exception as e:
        print(f"  Roads: extraction failed ({e})")

    # --- Flowing water ---
    try:
        water_layer = layer_map["water_flowing"]
        gdf = gpd.read_file(gpkg_path, layer=water_layer, bbox=bbox_geom)
        for _, row in gdf.iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue
            coords = _geom_to_coords_3d(geom)
            if coords:
                feature = {"geometry": coords, "water_type": "flowing"}
                if "objektart" in gdf.columns and row.get("objektart"):
                    feature["type"] = str(row["objektart"])
                if "name" in gdf.columns and row.get("name"):
                    feature["name"] = str(row["name"])
                infrastructure["water"].append(feature)
        print(f"  Water (flowing): {len(infrastructure['water'])} features")
    except Exception as e:
        print(f"  Water (flowing): extraction failed ({e})")

    # --- Standing water ---
    water_before = len(infrastructure["water"])
    try:
        water_layer = layer_map["water_standing"]
        gdf = gpd.read_file(gpkg_path, layer=water_layer, bbox=bbox_geom)
        for _, row in gdf.iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue
            if geom.geom_type == "Polygon":
                coords = [[round(c[0], 3), round(c[1], 3)] for c in geom.exterior.coords]
            elif geom.geom_type == "MultiPolygon":
                largest = max(geom.geoms, key=lambda g: g.area)
                coords = [[round(c[0], 3), round(c[1], 3)] for c in largest.exterior.coords]
            else:
                coords = _geom_to_coords_3d(geom)
            if coords:
                feature = {"geometry": coords, "water_type": "standing"}
                if "objektart" in gdf.columns and row.get("objektart"):
                    feature["type"] = str(row["objektart"])
                if "name" in gdf.columns and row.get("name"):
                    feature["name"] = str(row["name"])
                infrastructure["water"].append(feature)
        added = len(infrastructure["water"]) - water_before
        print(f"  Water (standing): {added} features")
    except Exception as e:
        print(f"  Water (standing): extraction failed ({e})")

    out_path = os.path.join(output_dir, "infrastructure.json")
    with open(out_path, "w") as f:
        json.dump(infrastructure, f)

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    total = len(infrastructure["railways"]) + len(infrastructure["roads"]) + len(infrastructure["water"])
    print(f"  Total: {total} infrastructure features")
    print(f"  Written to: infrastructure.json ({size_mb:.1f} MB)")

    return {
        "railways": len(infrastructure["railways"]),
        "roads": len(infrastructure["roads"]),
        "water": len(infrastructure["water"]),
    }


def _geom_to_coords_3d(geom):
    """Convert a LineString/MultiLineString geometry to a list of [x, y, z] coords."""
    if geom.geom_type == "LineString":
        return [[round(c[0], 3), round(c[1], 3)] + ([round(c[2], 3)] if len(c) >= 3 else [])
                for c in geom.coords]
    elif geom.geom_type == "MultiLineString":
        # Return longest segment
        longest = max(geom.geoms, key=lambda g: g.length)
        return [[round(c[0], 3), round(c[1], 3)] + ([round(c[2], 3)] if len(c) >= 3 else [])
                for c in longest.coords]
    return None


def extract_imagery(vrt_path, bbox, output_dir):
    """Extract aerial imagery from VRT mosaic and save as JPEG.

    Args:
        vrt_path: Path to SWISSIMAGE VRT file
        bbox: (west, south, east, north) in EPSG:2056
        output_dir: Where to write context.jpg

    Returns:
        dict with image metadata
    """
    rio = _import_rasterio()
    from rasterio.windows import from_bounds
    PIL_Image = _import_pillow()

    west, south, east, north = bbox

    with rio.open(vrt_path) as src:
        window = from_bounds(west, south, east, north, src.transform)

        # Read RGB bands
        band_count = min(src.count, 3)
        bands = []
        for i in range(1, band_count + 1):
            bands.append(src.read(i, window=window))

        if band_count == 1:
            # Grayscale
            img_array = bands[0]
            img = PIL_Image.fromarray(img_array.astype(np.uint8), mode="L")
        elif band_count >= 3:
            # RGB
            img_array = np.stack(bands[:3], axis=-1)
            img = PIL_Image.fromarray(img_array.astype(np.uint8), mode="RGB")
        else:
            img_array = bands[0]
            img = PIL_Image.fromarray(img_array.astype(np.uint8), mode="L")

        out_path = os.path.join(output_dir, "context.jpg")
        img.save(out_path, "JPEG", quality=90)

        size_mb = os.path.getsize(out_path) / (1024 * 1024)
        h, w = bands[0].shape
        print(f"  Imagery: {w}x{h} pixels ({band_count} bands)")
        print(f"  Written to: context.jpg ({size_mb:.1f} MB)")

        return {"width": w, "height": h, "bands": band_count}


def _resolve_name(name, config, radius):
    """Try to resolve a site name to coordinates from config reference points."""
    ref_points = config.get("reference_points_lv95", {})

    # Try exact match first, then case-insensitive, then partial match
    name_lower = name.lower().replace("_", " ").replace("-", " ")
    for key, coords in ref_points.items():
        key_lower = key.lower().replace("_", " ")
        if name_lower == key_lower or name_lower in key_lower or key_lower in name_lower:
            e, n = coords
            print(f"Resolved '{name}' -> {key} ({e}, {n})")
            return (e - radius, n - radius, e + radius, n + radius)
    return None


def _resolve_node(node_id, radius):
    """Look up lock node coordinates from prototypology_content.json.

    Uses LV95 coordinates from corridor analysis data (precise),
    falling back to pyproj conversion from WGS84 if available.
    """
    # Precise LV95 coordinates per node (from corridor analysis + manual verification)
    NODE_LV95 = {
        1: (2496500, 1122500, "Geneva North Industrial Belt"),
        2: (2507500, 1139500, "Nyon Hospital + Genolier"),
        3: (2527500, 1151500, "Morges Hospital Gap"),
        4: (2533500, 1153500, "Crissier-Bussigny"),
        5: (2538500, 1152500, "CHUV Lausanne"),
        6: (2560500, 1143500, "Montreux-Glion"),
        7: (2560000, 1137500, "Rennaz"),
    }

    if node_id not in NODE_LV95:
        raise ValueError(f"Node {node_id} not found (valid: 1-7)")

    e, n, name = NODE_LV95[node_id]
    print(f"Resolved node {node_id} ({name}) -> LV95 ({e}, {n})")
    return (e - radius, n - radius, e + radius, n + radius)


def main():
    parser = argparse.ArgumentParser(
        description="Extract terrain, buildings, and imagery for a site."
    )
    parser.add_argument("--name", required=True, help="Site name or reference point (e.g., 'Morges', 'lausanne_ouchy')")
    parser.add_argument("--center", nargs=2, type=float, metavar=("E", "N"),
                        help="Center point in LV95 (easting northing)")
    parser.add_argument("--radius", type=float, default=750,
                        help="Radius in meters around center (default: 750)")
    parser.add_argument("--bbox", nargs=4, type=float, metavar=("W", "S", "E", "N"),
                        help="Bounding box in LV95 (west south east north)")
    parser.add_argument("--node", type=int, metavar="ID",
                        help="Lock node ID (1-7) — looks up coordinates from prototypology_content.json")
    parser.add_argument("--skip-terrain", action="store_true")
    parser.add_argument("--skip-buildings", action="store_true")
    parser.add_argument("--skip-imagery", action="store_true")
    parser.add_argument("--skip-infrastructure", action="store_true")

    args = parser.parse_args()

    # Load config for reference points
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    with open(config_path) as f:
        config = json.load(f)

    # Resolve bbox — priority: explicit bbox > center > node > name lookup
    if args.bbox:
        bbox = tuple(args.bbox)
    elif args.center:
        e, n = args.center
        r = args.radius
        bbox = (e - r, n - r, e + r, n + r)
    elif args.node:
        bbox = _resolve_node(args.node, args.radius)
        if args.name == str(args.node):
            # Auto-name from node
            pass
    else:
        # Try to resolve name as a reference point
        bbox = _resolve_name(args.name, config, args.radius)
        if bbox is None:
            parser.error(
                "Could not resolve location. Provide one of:\n"
                "  --center E N      (LV95 coordinates)\n"
                "  --bbox W S E N    (LV95 bounding box)\n"
                "  --node ID         (lock node 1-7)\n"
                "  --name with a known reference point (Geneva, Nyon, Morges, etc.)"
            )

    print(f"Site: {args.name}")
    print(f"Bbox: W={bbox[0]:.0f} S={bbox[1]:.0f} E={bbox[2]:.0f} N={bbox[3]:.0f}")
    print(f"Size: {bbox[2]-bbox[0]:.0f}m x {bbox[3]-bbox[1]:.0f}m")
    print()

    # Find data
    swisstopo_path = find_swisstopo_path()
    print(f"Data source: {swisstopo_path}")

    # Create output dir
    sites_dir = os.path.join(os.path.dirname(__file__), "..", "sites", args.name)
    os.makedirs(sites_dir, exist_ok=True)

    results = {"name": args.name, "bbox": list(bbox), "crs": "EPSG:2056"}

    # 1. Terrain
    if not args.skip_terrain:
        print("\n--- Terrain ---")
        vrt = os.path.join(swisstopo_path, config["datasets"]["terrain"]["vrt"])
        try:
            if os.path.exists(vrt):
                results["terrain"] = extract_terrain(vrt, bbox, sites_dir)
            else:
                raise FileNotFoundError("VRT not found")
        except Exception as e:
            print(f"  VRT read failed ({e}), falling back to individual tiles...")
            results["terrain"] = _extract_terrain_from_tiles(swisstopo_path, config, bbox, sites_dir)

    # 2. Buildings
    if not args.skip_buildings:
        print("\n--- Buildings ---")
        gdb = os.path.join(swisstopo_path, config["datasets"]["buildings"]["file"])
        if os.path.exists(gdb):
            results["buildings"] = extract_buildings(gdb, bbox, sites_dir)
        else:
            print(f"  GDB not found: {gdb}")
            print(f"  Copy swissBUILDINGS3D .gdb.zip to: {swisstopo_path}")
            results["buildings"] = {"count": 0, "error": "GDB file not found"}

    # 3. Imagery
    if not args.skip_imagery:
        print("\n--- Imagery ---")
        vrt = os.path.join(swisstopo_path, config["datasets"]["imagery"]["vrt"])
        try:
            if os.path.exists(vrt):
                results["imagery"] = extract_imagery(vrt, bbox, sites_dir)
            else:
                raise FileNotFoundError("VRT not found")
        except Exception as e:
            print(f"  Imagery extraction failed: {e}")
            results["imagery"] = {"error": str(e)}

    # 4. Infrastructure (roads, railways, water from swissTLM3D)
    if not args.skip_infrastructure:
        infra_cfg = config["datasets"].get("infrastructure")
        if infra_cfg:
            print("\n--- Infrastructure ---")
            gpkg = os.path.join(swisstopo_path, infra_cfg["file"])
            if os.path.exists(gpkg):
                results["infrastructure"] = extract_infrastructure(gpkg, bbox, sites_dir, config)
            else:
                print(f"  GeoPackage not found: {gpkg}")
                print(f"  Copy swissTLM3D .gpkg.zip to: {swisstopo_path}")
                results["infrastructure"] = {"error": "GeoPackage not found"}
        else:
            print("\n--- Infrastructure ---")
            print("  No infrastructure dataset configured in config.json")

    # Write site config
    site_config = {
        "name": args.name,
        "bbox": list(bbox),
        "center": [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2],
        "size_m": [bbox[2] - bbox[0], bbox[3] - bbox[1]],
        "crs": "EPSG:2056",
        "extraction": results
    }
    config_out = os.path.join(sites_dir, "config.json")
    with open(config_out, "w") as f:
        json.dump(site_config, f, indent=2)

    print(f"\n--- Done ---")
    print(f"Output: geodata/sites/{args.name}/")
    for fname in os.listdir(sites_dir):
        size = os.path.getsize(os.path.join(sites_dir, fname))
        print(f"  {fname} ({size / 1024:.0f} KB)")


def _extract_terrain_from_tiles(swisstopo_path, config, bbox, output_dir):
    """Fallback: find individual GeoTIFF tiles that cover the bbox."""
    rio = _import_rasterio()
    from rasterio.merge import merge
    from rasterio.windows import from_bounds

    west, south, east, north = bbox
    prefix = config["datasets"]["terrain"]["tile_prefix"]

    # Tile naming: swissalti3d_{year}_{easting_km}-{northing_km}_2_2056_5728.tif
    # Each tile covers 1km x 1km
    e_min_km = int(west / 1000)
    e_max_km = int(east / 1000) + 1
    n_min_km = int(south / 1000)
    n_max_km = int(north / 1000) + 1

    tile_files = []
    for fname in os.listdir(swisstopo_path):
        if fname.startswith(prefix) and fname.endswith(".tif"):
            tile_files.append(fname)

    matching = []
    for e_km in range(e_min_km, e_max_km):
        for n_km in range(n_min_km, n_max_km):
            pattern = f"{e_km}-{n_km}"
            for tf in tile_files:
                if pattern in tf:
                    matching.append(os.path.join(swisstopo_path, tf))
                    break

    if not matching:
        print(f"  No tiles found for bbox")
        return {"error": "no tiles found"}

    print(f"  Found {len(matching)} tiles")

    # Merge tiles and crop to bbox
    datasets = [rio.open(f) for f in matching]
    nodata = datasets[0].nodata
    merged, merge_transform = merge(datasets, bounds=bbox, nodata=nodata)
    for ds in datasets:
        ds.close()

    data = merged[0].astype(float)
    # Replace nodata with NaN
    if nodata is not None:
        data = np.where(np.isclose(data, nodata), float('nan'), data)

    rows, cols = data.shape

    terrain = {
        "origin": [merge_transform.c, merge_transform.f],
        "resolution": abs(merge_transform.a),
        "rows": rows,
        "cols": cols,
        "bbox": list(bbox),
        "crs": "EPSG:2056",
        "elevation_unit": "meters_asl",
        "elevation_range": [float(np.nanmin(data)), float(np.nanmax(data))],
        "elevations": data.tolist()
    }

    out_path = os.path.join(output_dir, "terrain.json")
    with open(out_path, "w") as f:
        json.dump(terrain, f)

    print(f"  Terrain: {rows}x{cols} grid")
    print(f"  Elevation range: {terrain['elevation_range'][0]:.1f}m - {terrain['elevation_range'][1]:.1f}m")
    return {"rows": rows, "cols": cols, "elevation_range": terrain["elevation_range"]}


if __name__ == "__main__":
    main()
