#!/usr/bin/env python3
"""Verify a CSV dataset against City101 quality gates.

Usage:
    python tools/data/verify_dataset.py path/to/file.csv
    python tools/data/verify_dataset.py path/to/file.csv --expected-rows 49
"""

import argparse
import csv
import sys
from pathlib import Path


# Corridor coordinate bounds (WGS84)
LAT_MIN, LAT_MAX = 46.1, 46.6
LON_MIN, LON_MAX = 6.0, 7.1

# Possible column names for required fields
ID_COLS = {"id", "ID", "unique_id", "station_id", "place_id"}
NAME_COLS = {"name", "Name", "label", "station", "station_name"}
LAT_COLS = {"lat", "latitude", "lat_wgs84", "Latitude"}
LON_COLS = {"lon", "longitude", "lon_wgs84", "Longitude", "lng"}
SOURCE_COLS = {"source", "Source", "data_source", "provenance"}


def find_col(headers, candidates):
    """Find the first matching column name from candidates."""
    for col in candidates:
        if col in headers:
            return col
    return None


def verify(filepath, expected_rows=None):
    path = Path(filepath)
    issues = []
    warnings = []

    # 1. File exists and is readable
    if not path.exists():
        print(f"FAIL: File not found: {filepath}")
        return False
    if not path.suffix.lower() == ".csv":
        warnings.append(f"File extension is '{path.suffix}', expected '.csv'")

    # 2. Read CSV
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
    except Exception as e:
        print(f"FAIL: Cannot read CSV: {e}")
        return False

    row_count = len(rows)
    print(f"File: {filepath}")
    print(f"Rows: {row_count}")
    print(f"Columns ({len(headers)}): {', '.join(headers)}")
    print()

    # 3. Row count check
    if expected_rows is not None:
        if row_count != expected_rows:
            warnings.append(f"Expected {expected_rows} rows, got {row_count}")
        else:
            print(f"Row count matches expected: {expected_rows}")
    if row_count == 0:
        issues.append("Dataset is empty (0 rows)")

    # 4. Required columns
    id_col = find_col(headers, ID_COLS)
    name_col = find_col(headers, NAME_COLS)
    lat_col = find_col(headers, LAT_COLS)
    lon_col = find_col(headers, LON_COLS)
    source_col = find_col(headers, SOURCE_COLS)

    if not id_col:
        warnings.append(f"No ID column found (looked for: {', '.join(ID_COLS)})")
    if not name_col:
        warnings.append(f"No name column found (looked for: {', '.join(NAME_COLS)})")
    if not lat_col:
        warnings.append(f"No latitude column found (looked for: {', '.join(LAT_COLS)})")
    if not lon_col:
        warnings.append(f"No longitude column found (looked for: {', '.join(LON_COLS)})")
    if not source_col:
        warnings.append(f"No source attribution column found (looked for: {', '.join(SOURCE_COLS)})")

    # 5. Null/empty checks on found required fields
    for col_name, col_label in [(id_col, "ID"), (name_col, "Name"), (lat_col, "Latitude"), (lon_col, "Longitude")]:
        if col_name:
            nulls = sum(1 for r in rows if not r.get(col_name, "").strip())
            if nulls > 0:
                issues.append(f"{nulls} empty values in '{col_name}' ({col_label})")

    # 6. Coordinate validation
    out_of_range = 0
    if lat_col and lon_col:
        for i, row in enumerate(rows):
            try:
                lat = float(row[lat_col])
                lon = float(row[lon_col])
                if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
                    out_of_range += 1
            except (ValueError, TypeError):
                pass  # Already caught by null check
        if out_of_range > 0:
            warnings.append(f"{out_of_range} rows with coordinates outside corridor bounds (lat {LAT_MIN}-{LAT_MAX}, lon {LON_MIN}-{LON_MAX})")

    # 7. Duplicate ID check
    if id_col:
        ids = [r.get(id_col, "").strip() for r in rows if r.get(id_col, "").strip()]
        dupes = len(ids) - len(set(ids))
        if dupes > 0:
            issues.append(f"{dupes} duplicate IDs in '{id_col}'")

    # 8. Summary
    print("=" * 50)
    if issues:
        print("RESULT: FAIL")
        print()
        print("Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("RESULT: PASS")

    if warnings:
        print()
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if not issues and not warnings:
        print("All checks passed with no warnings.")

    print("=" * 50)
    return len(issues) == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify a City101 dataset")
    parser.add_argument("filepath", help="Path to CSV file")
    parser.add_argument("--expected-rows", type=int, default=None, help="Expected row count")
    args = parser.parse_args()

    success = verify(args.filepath, args.expected_rows)
    sys.exit(0 if success else 1)
