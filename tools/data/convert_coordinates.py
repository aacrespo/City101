#!/usr/bin/env python3
"""Convert coordinates between WGS84 and Swiss LV95 in a CSV file.

Usage:
    python tools/data/convert_coordinates.py input.csv --direction wgs84-to-lv95
    python tools/data/convert_coordinates.py input.csv --direction lv95-to-wgs84
    python tools/data/convert_coordinates.py input.csv --direction wgs84-to-lv95 --output output.csv

Requires: pip install pyproj
"""

import argparse
import csv
import sys
from pathlib import Path

try:
    from pyproj import Transformer
except ImportError:
    print("ERROR: pyproj is required. Install with: pip install pyproj")
    sys.exit(1)


# Transformers (cached)
WGS84_TO_LV95 = Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=True)
LV95_TO_WGS84 = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)


def find_col(headers, candidates):
    for col in candidates:
        if col in headers:
            return col
    return None


def convert(filepath, direction, output_path=None):
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: File not found: {filepath}")
        return False

    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or [])
        rows = list(reader)

    print(f"Input: {filepath} ({len(rows)} rows)")
    print(f"Direction: {direction}")

    if direction == "wgs84-to-lv95":
        lat_col = find_col(headers, {"lat", "latitude", "lat_wgs84", "Latitude"})
        lon_col = find_col(headers, {"lon", "longitude", "lon_wgs84", "Longitude", "lng"})
        if not lat_col or not lon_col:
            print(f"ERROR: Cannot find lat/lon columns. Found: {headers}")
            return False

        new_cols = ["lv95_e", "lv95_n"]
        for col in new_cols:
            if col not in headers:
                headers.append(col)

        converted = 0
        for row in rows:
            try:
                lat = float(row[lat_col])
                lon = float(row[lon_col])
                e, n = WGS84_TO_LV95.transform(lon, lat)
                row["lv95_e"] = f"{e:.2f}"
                row["lv95_n"] = f"{n:.2f}"
                converted += 1
            except (ValueError, TypeError):
                row["lv95_e"] = ""
                row["lv95_n"] = ""

    elif direction == "lv95-to-wgs84":
        e_col = find_col(headers, {"lv95_e", "E", "easting", "x"})
        n_col = find_col(headers, {"lv95_n", "N", "northing", "y"})
        if not e_col or not n_col:
            print(f"ERROR: Cannot find E/N columns. Found: {headers}")
            return False

        new_cols = ["lat_wgs84", "lon_wgs84"]
        for col in new_cols:
            if col not in headers:
                headers.append(col)

        converted = 0
        for row in rows:
            try:
                e = float(row[e_col])
                n = float(row[n_col])
                lon, lat = LV95_TO_WGS84.transform(e, n)
                row["lat_wgs84"] = f"{lat:.6f}"
                row["lon_wgs84"] = f"{lon:.6f}"
                converted += 1
            except (ValueError, TypeError):
                row["lat_wgs84"] = ""
                row["lon_wgs84"] = ""
    else:
        print(f"ERROR: Unknown direction '{direction}'. Use 'wgs84-to-lv95' or 'lv95-to-wgs84'.")
        return False

    # Write output (never overwrites input)
    if output_path is None:
        stem = path.stem
        suffix = "_lv95" if direction == "wgs84-to-lv95" else "_wgs84"
        output_path = path.parent / f"{stem}{suffix}.csv"
    else:
        output_path = Path(output_path)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Converted: {converted}/{len(rows)} rows")
    print(f"Output: {output_path}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert WGS84 ↔ LV95 coordinates in CSV")
    parser.add_argument("filepath", help="Input CSV path")
    parser.add_argument("--direction", required=True, choices=["wgs84-to-lv95", "lv95-to-wgs84"])
    parser.add_argument("--output", default=None, help="Output path (default: input_lv95.csv or input_wgs84.csv)")
    args = parser.parse_args()

    success = convert(args.filepath, args.direction, args.output)
    sys.exit(0 if success else 1)
