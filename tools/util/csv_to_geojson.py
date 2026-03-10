#!/usr/bin/env python3
"""Convert a CSV with lat/lon columns to GeoJSON FeatureCollection.

Usage:
    python tools/util/csv_to_geojson.py input.csv output.geojson
    python tools/util/csv_to_geojson.py input.csv output.geojson --lat-col latitude --lon-col longitude
"""

import argparse
import csv
import json
import sys
from pathlib import Path

# Corridor bounds for validation (WGS84)
LAT_MIN, LAT_MAX = 46.1, 46.6
LON_MIN, LON_MAX = 6.0, 7.1


def find_col(headers, candidates):
    for col in candidates:
        if col in headers:
            return col
    return None


def convert(input_path, output_path, lat_col=None, lon_col=None):
    path = Path(input_path)
    if not path.exists():
        print(f"ERROR: File not found: {input_path}")
        return False

    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    # Find coordinate columns
    if lat_col is None:
        lat_col = find_col(headers, ["lat", "latitude", "lat_wgs84", "Latitude"])
    if lon_col is None:
        lon_col = find_col(headers, ["lon", "longitude", "lon_wgs84", "Longitude", "lng"])

    if not lat_col or lat_col not in headers:
        print(f"ERROR: Latitude column '{lat_col}' not found. Available: {headers}")
        return False
    if not lon_col or lon_col not in headers:
        print(f"ERROR: Longitude column '{lon_col}' not found. Available: {headers}")
        return False

    print(f"Input: {input_path} ({len(rows)} rows)")
    print(f"Lat column: {lat_col}")
    print(f"Lon column: {lon_col}")

    features = []
    skipped = 0
    out_of_range = 0

    for row in rows:
        try:
            lat = float(row[lat_col])
            lon = float(row[lon_col])
        except (ValueError, TypeError, KeyError):
            skipped += 1
            continue

        if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
            out_of_range += 1

        # All CSV columns become properties (except lat/lon)
        properties = {k: v for k, v in row.items() if k not in (lat_col, lon_col)}

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat],
            },
            "properties": properties,
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    out_path = Path(output_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"Output: {output_path}")
    print(f"Features: {len(features)}")
    if skipped:
        print(f"Skipped (bad coords): {skipped}")
    if out_of_range:
        print(f"Warning: {out_of_range} points outside corridor bounds")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV to GeoJSON")
    parser.add_argument("input", help="Input CSV path")
    parser.add_argument("output", help="Output GeoJSON path")
    parser.add_argument("--lat-col", default=None, help="Latitude column name")
    parser.add_argument("--lon-col", default=None, help="Longitude column name")
    args = parser.parse_args()

    success = convert(args.input, args.output, args.lat_col, args.lon_col)
    sys.exit(0 if success else 1)
