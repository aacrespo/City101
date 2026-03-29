"""
Fast building extraction using geopandas bbox filter on zipped FileGDB.
Outputs buildings filtered by height > 8m with origin-offset coordinates.
"""
import json
import os
import time
import sys

BBOX = (2497000, 1110000, 2562000, 1155000)  # W, S, E, N
ORIGIN = (2497000, 1110000)
MIN_HEIGHT = 8
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    import geopandas as gpd
    import numpy as np
    from shapely.geometry import MultiPoint

    src = r"C:\Users\Henna Rafik\Desktop\Huang - Sentient\Swisstopo\swissbuildings3d_2_2024-05_2056_5728.gdb.zip"

    print("Reading buildings with bbox filter...")
    print(f"  Source: {src}")
    print(f"  Bbox: {BBOX}")
    t0 = time.time()

    # Use fiona to iterate with bbox filter (handles 3D WKB correctly)
    import fiona
    from shapely.geometry import MultiPoint, shape

    buildings = []
    skipped = 0
    total = 0

    with fiona.open(f"zip://{src}", layer="sB20", bbox=BBOX) as f:
        feature_count = len(f)
        print(f"  Features in collection: {feature_count:,}")
        print(f"  Iterating with bbox filter...")

        for feat in f:
            total += 1
            if total % 20000 == 0:
                print(f"    ...{total:,} read, {len(buildings):,} kept ({time.time()-t0:.1f}s)")
                sys.stdout.flush()

            geom = feat["geometry"]
            if geom is None:
                continue

            # Extract Z from raw coordinate tuples
            all_z = []
            all_xy = []
            for polygon_coords in geom["coordinates"]:
                for ring in polygon_coords:
                    for coord in ring:
                        if len(coord) >= 3:
                            all_z.append(coord[2])
                            all_xy.append((coord[0], coord[1]))

            if len(all_z) < 3:
                continue

            ground_z = min(all_z)
            roof_z = max(all_z)
            height = roof_z - ground_z

            if height <= MIN_HEIGHT:
                skipped += 1
                continue

            # Convex hull footprint
            mp = MultiPoint(all_xy)
            hull = mp.convex_hull
            if hull.geom_type != "Polygon":
                continue

            hull = hull.simplify(1.0)

            coords = [
                [round(x - ORIGIN[0], 2), round(y - ORIGIN[1], 2)]
                for x, y in hull.exterior.coords
            ]

            buildings.append({
                "footprint": coords,
                "ground_z": round(ground_z, 2),
                "roof_z": round(roof_z, 2)
            })

    print(f"  Processed in {time.time()-t1:.1f}s")
    print(f"  Total in bbox: {len(gdf):,}")
    print(f"  Skipped (height <= {MIN_HEIGHT}m): {skipped:,}")
    print(f"  Kept: {len(buildings):,}")

    # Height stats
    if buildings:
        heights = [b["roof_z"] - b["ground_z"] for b in buildings]
        print(f"  Height range: {min(heights):.1f} - {max(heights):.1f}m")
        print(f"  Median height: {sorted(heights)[len(heights)//2]:.1f}m")

    if len(buildings) > 50000:
        print(f"\n  WARNING: {len(buildings):,} buildings is heavy for Rhino.")
        print(f"  Consider raising MIN_HEIGHT to 12 or 15m.")

    # Save
    out_path = os.path.join(OUT_DIR, "buildings_filtered.json")
    with open(out_path, "w") as f:
        json.dump(buildings, f)

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"\n  Saved: {out_path} ({size_mb:.1f} MB)")
    print(f"  Total time: {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
