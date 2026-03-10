#!/usr/bin/env python3
"""TEMPLATE: Fetch SBB timetable data from transport.opendata.ch.

Usage:
    python tools/data/fetch_sbb_timetable.py "Lausanne" --limit 50
    python tools/data/fetch_sbb_timetable.py "Genève" --date 2026-03-10

STATUS: Template — needs testing with live API.
Rate limit: 0.35s minimum between calls.
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime

API_BASE = "http://transport.opendata.ch/v1"
MIN_DELAY = 0.35  # seconds between API calls
_last_call = 0


def rate_limited_fetch(url):
    """Fetch URL with rate limiting."""
    global _last_call
    elapsed = time.time() - _last_call
    if elapsed < MIN_DELAY:
        time.sleep(MIN_DELAY - elapsed)

    print(f"  Fetching: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "City101-Research/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        _last_call = time.time()
        return data
    except Exception as e:
        print(f"  ERROR: {e}")
        _last_call = time.time()
        return None


def fetch_stationboard(station, limit=50, date=None):
    """Fetch departures for a station."""
    params = {"station": station, "limit": limit}
    if date:
        params["date"] = date
    url = f"{API_BASE}/stationboard?{urllib.parse.urlencode(params)}"
    return rate_limited_fetch(url)


def main():
    parser = argparse.ArgumentParser(description="Fetch SBB timetable from transport.opendata.ch")
    parser.add_argument("station", help="Station name (e.g., 'Lausanne')")
    parser.add_argument("--limit", type=int, default=50, help="Max departures (default: 50). WARNING: low limits can mask real frequency.")
    parser.add_argument("--date", default=None, help="Date in YYYY-MM-DD format (default: today)")
    args = parser.parse_args()

    print(f"Station: {args.station}")
    print(f"Limit: {args.limit}")
    print(f"Date: {args.date or 'today'}")
    print()

    data = fetch_stationboard(args.station, args.limit, args.date)

    if data is None:
        print("FAIL: No data returned from API")
        sys.exit(1)

    station_info = data.get("station", {})
    print(f"Station found: {station_info.get('name', 'unknown')}")
    print(f"  ID: {station_info.get('id', 'unknown')}")
    coord = station_info.get("coordinate", {})
    print(f"  Coordinates: {coord.get('x', '?')}, {coord.get('y', '?')}")

    entries = data.get("stationboard", [])
    print(f"  Departures returned: {len(entries)}")

    if entries:
        print()
        print("First 5 departures:")
        for entry in entries[:5]:
            dep_time = entry.get("stop", {}).get("departure", "?")
            category = entry.get("category", "?")
            number = entry.get("number", "?")
            to = entry.get("to", "?")
            print(f"  {dep_time} — {category}{number} → {to}")

    print()
    print("Summary:")
    print(f"  Station: {station_info.get('name')}")
    print(f"  Departures: {len(entries)}")
    print(f"  API: {API_BASE}/stationboard")
    print(f"  NOTE: If limit was hit, real frequency may be higher. Remove limit cap to see true distribution.")


if __name__ == "__main__":
    main()
