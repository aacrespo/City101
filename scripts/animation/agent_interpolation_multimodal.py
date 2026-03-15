#!/usr/bin/env python3
"""
Agent Interpolation: Multimodal Per-Minute Positions

Transforms stop_times into per-minute animated positions for all transport modes.
Rail/metro/funicular/tram/ferry: 1-minute resolution
Bus: 2-minute resolution (halves data volume)

Input:  output/transport_pulse_v2/gtfs_multimodal_corridor.csv
Output: output/transport_pulse_v2/gtfs_multimodal_interpolated.csv
"""
import pandas as pd
import numpy as np
import os, sys

BASE = "/Users/andreacrespo/CLAUDE/city101"
INPUT = os.path.join(BASE, "output/transport_pulse_v2/gtfs_multimodal_corridor.csv")
OUTPUT = os.path.join(BASE, "output/transport_pulse_v2/gtfs_multimodal_interpolated.csv")

# Resolution by mode (minutes between samples)
MODE_RESOLUTION = {
    'rail': 1, 'metro': 1, 'funicular': 1, 'tram': 1, 'ferry': 1,
    'bus': 2,
}


def time_to_minutes(tstr):
    """Parse HH:MM:SS to minutes since midnight. Handles >24:00:00."""
    parts = str(tstr).strip().split(':')
    h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
    return h * 60 + m + s / 60.0


def interpolate_trip(trip_rows, resolution=1):
    """Generate positions at given resolution for a single trip."""
    rows = trip_rows.sort_values('stop_sequence').reset_index(drop=True)
    if len(rows) < 2:
        return []

    arrivals = rows['arrival_time'].apply(time_to_minutes).values
    departures = rows['departure_time'].apply(time_to_minutes).values
    lats = rows['lat_wgs84'].values
    lons = rows['lon_wgs84'].values

    trip_start = int(np.floor(departures[0]))
    trip_end = int(np.ceil(arrivals[-1]))

    results = []

    minute = trip_start
    while minute <= trip_end:
        display_minute = min(minute, 1439)

        dwelling = False
        for i in range(len(rows)):
            arr_m = arrivals[i]
            dep_m = departures[i]
            if arr_m <= minute <= dep_m:
                results.append((display_minute, round(lats[i], 4), round(lons[i], 4)))
                dwelling = True
                break

        if not dwelling:
            for i in range(len(rows) - 1):
                dep_m = departures[i]
                arr_m = arrivals[i + 1]
                if dep_m < minute < arr_m:
                    travel_time = arr_m - dep_m
                    if travel_time <= 0:
                        results.append((display_minute, round(lats[i + 1], 4), round(lons[i + 1], 4)))
                    else:
                        frac = (minute - dep_m) / travel_time
                        lat = lats[i] + frac * (lats[i + 1] - lats[i])
                        lon = lons[i] + frac * (lons[i + 1] - lons[i])
                        results.append((display_minute, round(lat, 4), round(lon, 4)))
                    break

        minute += resolution

    return results


def main():
    print("=" * 80)
    print("MULTIMODAL INTERPOLATION — Transport Pulse v2")
    print("=" * 80)

    print(f"\nReading {INPUT}...")
    df = pd.read_csv(INPUT)
    n_trips = df['trip_id'].nunique()
    print(f"  {len(df)} stop_time rows, {n_trips} unique trips")
    print(f"  Modes: {sorted(df['mode_label'].unique())}")
    print(f"  Symbol codes: {sorted(df['symbol_code'].unique())}")

    print(f"\nInterpolating {n_trips} trips...")
    all_rows = []
    trip_count = 0
    skipped = 0

    for trip_id, group in df.groupby('trip_id'):
        mode_label = group['mode_label'].iloc[0]
        route_name = group['route_name'].iloc[0]
        symbol_code = group['symbol_code'].iloc[0]
        direction = group['direction'].iloc[0]

        resolution = MODE_RESOLUTION.get(mode_label, 1)
        positions = interpolate_trip(group, resolution)

        if not positions:
            skipped += 1
            continue

        for minute, lat, lon in positions:
            all_rows.append({
                'trip_id': trip_id,
                'route_name': route_name,
                'mode_label': mode_label,
                'symbol_code': symbol_code,
                'direction': direction,
                'minute_of_day': int(minute),
                'lat': lat,
                'lon': lon,
            })

        trip_count += 1
        if trip_count % 500 == 0:
            print(f"    {trip_count}/{n_trips} trips processed...")

    result = pd.DataFrame(all_rows)
    print(f"\n  Total interpolated rows: {len(result)}")
    print(f"  Trips processed: {trip_count}, skipped: {skipped}")

    # Stats by mode
    print(f"\n  Rows by mode_label:")
    for ml, count in result.groupby('mode_label').size().sort_values(ascending=False).items():
        n_t = result[result['mode_label'] == ml]['trip_id'].nunique()
        print(f"    {ml:<15} {count:>8} rows  ({n_t} trips)")

    print(f"\n  Rows by symbol_code:")
    for sc, count in result.groupby('symbol_code').size().sort_values(ascending=False).items():
        n_t = result[result['symbol_code'] == sc]['trip_id'].nunique()
        print(f"    {sc:<15} {count:>8} rows  ({n_t} trips)")

    # Validation
    print(f"\n--- VALIDATION ---")

    input_trips = set(df['trip_id'].unique())
    output_trips = set(result['trip_id'].unique())
    missing = input_trips - output_trips
    if missing:
        print(f"  WARNING: {len(missing)} trips missing from output")
    else:
        print(f"  PASS: All {len(input_trips)} input trips present")

    # Coordinate bounds (wider for buses)
    lat_range = (result['lat'].min(), result['lat'].max())
    lon_range = (result['lon'].min(), result['lon'].max())
    lat_ok = lat_range[0] >= 46.0 and lat_range[1] <= 46.7
    lon_ok = lon_range[0] >= 5.8 and lon_range[1] <= 7.3
    print(f"  Lat range: [{lat_range[0]:.4f}, {lat_range[1]:.4f}] — {'PASS' if lat_ok else 'WARN'}")
    print(f"  Lon range: [{lon_range[0]:.4f}, {lon_range[1]:.4f}] — {'PASS' if lon_ok else 'WARN'}")

    # Minute range
    print(f"  Minute range: {result['minute_of_day'].min()}–{result['minute_of_day'].max()}")

    # File size estimate
    est_size_mb = len(result) * 80 / 1024 / 1024  # ~80 bytes per row
    print(f"  Estimated CSV size: {est_size_mb:.1f} MB")
    if est_size_mb > 30:
        print(f"  *** WARNING: Exceeds 30MB threshold — flag for lead session ***")

    # Write output
    print(f"\nWriting {OUTPUT}...")
    result.to_csv(OUTPUT, index=False)
    actual_size = os.path.getsize(OUTPUT) / 1024 / 1024
    print(f"  {actual_size:.1f} MB, {len(result)} rows")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Input: {INPUT}")
    print(f"Output: {OUTPUT} ({actual_size:.1f} MB)")
    print(f"Trips: {trip_count} processed, {skipped} skipped")
    print(f"Rows: {len(result)}")
    print(f"Resolution: rail/metro/funicular/tram/ferry=1min, bus=2min")
    print(f"Coordinates rounded to 4 decimal places (~11m)")
    print("Done.")


if __name__ == '__main__':
    main()
