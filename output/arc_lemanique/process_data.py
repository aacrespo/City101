"""
Arc Lemanique lightweight 3D model — data processing
Reads swisstopo terrain, buildings, lake → JSON files for Rhino import
"""
import json
import os
import sys
import time

# ── Config ──────────────────────────────────────────────────────────────
BBOX = (2497000, 1110000, 2562000, 1155000)  # W, S, E, N in EPSG:2056
ORIGIN = (BBOX[0], BBOX[1])  # SW corner — subtracted from all coords
TERRAIN_RES = 50  # meters
MIN_BUILDING_HEIGHT = 8  # meters
LAKE_ELEVATION = 372.0  # meters

TERRAIN_VRT = r"C:\Users\Henna Rafik\Desktop\Huang - Sentient\Swisstopo\ch.swisstopo.swissalti3d-combined_2026-03-25_011944.vrt"
BUILDINGS_GDB = r"C:\Users\Henna Rafik\Desktop\Huang - Sentient\Swisstopo\swissbuildings3d_2_2024-05_2056_5728.gdb.zip"
LAKE_GPKG = r"C:\Users\Henna Rafik\Desktop\Huang - Sentient\WORK\City101_LakeLeman.gpkg"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Step 1: Terrain ─────────────────────────────────────────────────────
def process_terrain():
    import rasterio
    from rasterio.windows import from_bounds
    from rasterio.enums import Resampling
    import numpy as np

    print("\n=== TERRAIN ===")
    t0 = time.time()

    with rasterio.open(TERRAIN_VRT) as src:
        # Get the pixel window for our bbox
        window = from_bounds(BBOX[0], BBOX[1], BBOX[2], BBOX[3], src.transform)
        print(f"  Source window: {window}")
        print(f"  Source pixels: {int(window.width)} x {int(window.height)}")

        # Calculate output dimensions at target resolution
        out_cols = int((BBOX[2] - BBOX[0]) / TERRAIN_RES)
        out_rows = int((BBOX[3] - BBOX[1]) / TERRAIN_RES)
        print(f"  Output grid: {out_cols} x {out_rows} = {out_cols * out_rows:,} vertices")

        # Read and resample in one step
        data = src.read(
            1,
            window=window,
            out_shape=(out_rows, out_cols),
            resampling=Resampling.bilinear
        )

    # Replace nodata with lake level
    nodata_mask = (data < -9000) | np.isnan(data)
    nodata_count = nodata_mask.sum()
    data[nodata_mask] = LAKE_ELEVATION
    print(f"  Replaced {nodata_count} nodata cells with {LAKE_ELEVATION}m")

    # Elevation stats
    print(f"  Elevation range: {data.min():.1f} – {data.max():.1f} m")

    # Apply origin offset: origin is top-left corner of grid in model space
    # Grid row 0 = North edge, row -1 = South edge
    # In model coords: y=0 is South (BBOX[1]), y=max is North (BBOX[3])
    # So origin_x = 0 (BBOX[0] - BBOX[0]), origin_y = North - South
    origin_x = 0.0
    origin_y = float(BBOX[3] - BBOX[1])  # top-left Y in model space

    # Flatten to list for JSON (row-major, north to south)
    elevations = [round(float(v), 2) for v in data.flatten()]

    result = {
        "origin_x": origin_x,
        "origin_y": origin_y,
        "resolution": TERRAIN_RES,
        "rows": out_rows,
        "cols": out_cols,
        "elevations": elevations
    }

    out_path = os.path.join(OUT_DIR, "terrain_50m.json")
    with open(out_path, "w") as f:
        json.dump(result, f)

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"  Saved: {out_path} ({size_mb:.1f} MB)")
    print(f"  Time: {time.time() - t0:.1f}s")
    return out_cols, out_rows


# ── Step 2: Lake ────────────────────────────────────────────────────────
def process_lake():
    import geopandas as gpd
    from shapely.geometry import box
    from pyproj import Transformer

    print("\n=== LAKE ===")
    t0 = time.time()

    gdf = gpd.read_file(LAKE_GPKG)
    print(f"  Source CRS: {gdf.crs}")
    print(f"  Features: {len(gdf)}")

    # Reproject to LV95
    gdf_lv95 = gdf.to_crs("EPSG:2056")

    # Clip to bbox
    clip_box = box(BBOX[0], BBOX[1], BBOX[2], BBOX[3])
    clipped = gdf_lv95.geometry.iloc[0].intersection(clip_box)
    print(f"  Clipped geometry type: {clipped.geom_type}")

    # Extract exterior ring, apply origin offset
    if clipped.geom_type == "Polygon":
        coords = list(clipped.exterior.coords)
    elif clipped.geom_type == "MultiPolygon":
        # Take the largest polygon
        largest = max(clipped.geoms, key=lambda g: g.area)
        coords = list(largest.exterior.coords)
    else:
        print(f"  ERROR: unexpected geometry type {clipped.geom_type}")
        return

    # Apply origin offset and round
    offset_coords = [
        [round(x - ORIGIN[0], 2), round(y - ORIGIN[1], 2)]
        for x, y in coords
    ]

    result = {
        "elevation": LAKE_ELEVATION,
        "coords": offset_coords,
        "num_points": len(offset_coords)
    }

    out_path = os.path.join(OUT_DIR, "lake.json")
    with open(out_path, "w") as f:
        json.dump(result, f)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"  Points: {len(offset_coords)}")
    print(f"  Saved: {out_path} ({size_kb:.1f} KB)")
    print(f"  Time: {time.time() - t0:.1f}s")


# ── Step 3: Buildings ───────────────────────────────────────────────────
def process_buildings():
    import fiona
    from shapely.geometry import shape, MultiPoint

    print("\n=== BUILDINGS ===")
    t0 = time.time()

    src_path = "zip://" + BUILDINGS_GDB
    buildings = []
    total_read = 0
    skipped_low = 0
    skipped_tiny = 0

    with fiona.open(src_path, layer="sB20", bbox=BBOX) as src:
        print(f"  Features in bbox: scanning...")

        for feat in src:
            total_read += 1
            if total_read % 10000 == 0:
                print(f"    ...read {total_read:,} features, kept {len(buildings):,}")

            geom = feat["geometry"]
            if geom is None:
                continue

            # Extract all Z values from 3D MultiPolygon
            all_z = []
            all_xy = []
            for polygon_coords in geom["coordinates"]:
                for ring in polygon_coords:
                    for coord in ring:
                        if len(coord) >= 3:
                            all_z.append(coord[2])
                            all_xy.append((coord[0], coord[1]))

            if not all_z:
                continue

            ground_z = min(all_z)
            roof_z = max(all_z)
            height = roof_z - ground_z

            # Height filter
            if height <= MIN_BUILDING_HEIGHT:
                skipped_low += 1
                continue

            # Compute 2D footprint as convex hull
            if len(all_xy) < 3:
                skipped_tiny += 1
                continue

            mp = MultiPoint(all_xy)
            hull = mp.convex_hull

            if hull.geom_type == "Point" or hull.geom_type == "LineString":
                skipped_tiny += 1
                continue

            # Extract hull coordinates, apply origin offset
            hull_coords = [
                [round(x - ORIGIN[0], 2), round(y - ORIGIN[1], 2)]
                for x, y in hull.exterior.coords
            ]

            buildings.append({
                "footprint": hull_coords,
                "ground_z": round(ground_z, 2),
                "roof_z": round(roof_z, 2)
            })

    print(f"  Total read: {total_read:,}")
    print(f"  Skipped (height <= {MIN_BUILDING_HEIGHT}m): {skipped_low:,}")
    print(f"  Skipped (degenerate): {skipped_tiny:,}")
    print(f"  Kept: {len(buildings):,}")

    if len(buildings) > 50000:
        print(f"  WARNING: {len(buildings)} buildings is a lot. Consider increasing height filter.")

    out_path = os.path.join(OUT_DIR, "buildings.json")
    with open(out_path, "w") as f:
        json.dump(buildings, f)

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"  Saved: {out_path} ({size_mb:.1f} MB)")
    print(f"  Time: {time.time() - t0:.1f}s")
    return len(buildings)


# ── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("Arc Lemanique — Data Processing")
    print(f"Bbox: {BBOX}")
    print(f"Origin offset: {ORIGIN}")
    print(f"Terrain resolution: {TERRAIN_RES}m")
    print(f"Building height filter: > {MIN_BUILDING_HEIGHT}m")
    print("=" * 60)

    cols, rows = process_terrain()
    process_lake()
    num_buildings = process_buildings()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"  Terrain: {cols} x {rows} = {cols * rows:,} vertices")
    print(f"  Buildings: {num_buildings:,}")
    print(f"  Output dir: {OUT_DIR}")
    print("=" * 60)
