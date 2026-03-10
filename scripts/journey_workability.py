#!/usr/bin/env python3
"""
City101 Journey-Level On-Train Workability Analysis
Geneva–Villeneuve corridor (+ Aigle)

Fetches real connections from transport.opendata.ch, classifies each journey
for on-train workability, and writes two CSVs:
  1. city101_journey_workability.csv       — one row per connection
  2. city101_journey_workability_summary.csv — one row per OD pair (aggregated)
"""

import csv
import json
import math
import sys
import time
import urllib.request
import urllib.parse
from collections import defaultdict
from datetime import datetime

# ──────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────

OUTPUT_DIR = "/Users/andreacrespo/CLAUDE/City101_ClaudeCode/output"
API_BASE = "https://transport.opendata.ch/v1/connections"
QUERY_DATE = "2026-03-03"
TIME_SLOTS = ["08:00", "12:00", "20:00"]
LIMIT_PER_QUERY = 6
RATE_LIMIT_SEC = 2.0  # generous spacing to avoid 429s
MAX_RETRIES = 4       # retry failed requests with backoff

MAJOR_NODES = [
    "Genève",
    "Genève-Aéroport",
    "Genève-Champel",
    "Genève-Eaux-Vives",
    "Lancy-Bachet",
    "Lancy-Pont-Rouge",
    "Genève-Sécheron",
    "Versoix",
    "Coppet",
    "Nyon",
    "Gland",
    "Rolle",
    "Allaman",
    "Morges",
    "Bussigny",
    "Renens VD",
    "Lausanne",
    "Puidoux",
    "Cully",
    "Vevey",
    "La Tour-de-Peilz",
    "Montreux",
    "Territet",
    "Villeneuve VD",
    "Aigle",
]

# ──────────────────────────────────────────────────────
# Build OD pairs
# ──────────────────────────────────────────────────────

def build_od_pairs():
    """Return deduplicated list of (from, to) pairs to query."""
    pairs = set()

    # 1. Every consecutive pair along the main line (24 pairs)
    for i in range(len(MAJOR_NODES) - 1):
        pairs.add((MAJOR_NODES[i], MAJOR_NODES[i + 1]))

    # 2. Hub-to-hub express pairs
    hub_pairs = [
        ("Genève", "Lausanne"),
        ("Lausanne", "Montreux"),
        ("Genève", "Nyon"),
        ("Lausanne", "Vevey"),
        ("Montreux", "Aigle"),
        ("Genève", "Morges"),
        ("Morges", "Lausanne"),
        ("Vevey", "Montreux"),
    ]
    for a, b in hub_pairs:
        pairs.add((a, b))

    # 3. Key commuter pairs (both directions)
    commuter_pairs = [
        ("Nyon", "Genève"),
        ("Morges", "Lausanne"),
        ("Vevey", "Lausanne"),
        ("Montreux", "Lausanne"),
    ]
    for a, b in commuter_pairs:
        pairs.add((a, b))

    return sorted(pairs)


# ──────────────────────────────────────────────────────
# API fetch
# ──────────────────────────────────────────────────────

def fetch_connections(from_station, to_station, time_slot):
    """Query the transport.opendata.ch API with retry + exponential backoff."""
    params = urllib.parse.urlencode({
        "from": from_station,
        "to": to_station,
        "date": QUERY_DATE,
        "time": time_slot,
        "limit": LIMIT_PER_QUERY,
    })
    url = f"{API_BASE}?{params}"

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "City101-Research/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                backoff = RATE_LIMIT_SEC * (2 ** (attempt + 1))  # 4s, 8s, 16s, 32s
                if attempt < MAX_RETRIES - 1:
                    print(f"    429 rate-limited, waiting {backoff:.0f}s (attempt {attempt+1}/{MAX_RETRIES})...")
                    time.sleep(backoff)
                else:
                    print(f"  FAILED after {MAX_RETRIES} retries: {from_station} → {to_station} @ {time_slot}")
                    return None
            else:
                print(f"  HTTP {e.code}: {from_station} → {to_station} @ {time_slot}")
                return None
        except Exception as e:
            print(f"  ERROR: {from_station} → {to_station} @ {time_slot}: {e}")
            return None
    return None


# ──────────────────────────────────────────────────────
# Parse helpers
# ──────────────────────────────────────────────────────

def parse_duration(dur_str):
    """Parse '00d00:33:00' → 33 (minutes). Returns float."""
    if not dur_str:
        return 0
    try:
        # Format: "00d00:33:00"
        parts = dur_str.split("d")
        days = int(parts[0]) if len(parts) > 1 else 0
        time_part = parts[1] if len(parts) > 1 else parts[0]
        h, m, s = time_part.split(":")
        return days * 1440 + int(h) * 60 + int(m) + int(s) / 60
    except Exception:
        return 0


def comfort_score(category):
    """Return comfort score 1-4 based on train category."""
    cat = (category or "").upper()
    if cat in ("IC", "EC", "TGV", "ICE"):
        return 4
    if cat in ("IR",):
        return 3
    if cat in ("RE", "RER"):
        return 2
    # R, S, or unknown
    return 1


def classify_workability(duration_min, primary_cat, stops_per_10, has_xfer, xfer_wait):
    """Return workability class string."""
    cat = (primary_cat or "").upper()

    # BROKEN: transfer with >10 min wait
    if has_xfer and xfer_wait and xfer_wait > 10:
        return "BROKEN"

    # NOT_WORKABLE: too short
    if duration_min < 8:
        return "NOT_WORKABLE"

    # PRIME_WORK: >= 15 min, good train, low stop density, no transfer
    if (duration_min >= 15
            and cat in ("IC", "IR", "RE", "EC", "TGV", "ICE")
            and stops_per_10 < 1
            and not has_xfer):
        return "PRIME_WORK"

    # WORKABLE: >= 8 min, any long-distance type, stops_per_10 < 2
    if (duration_min >= 8
            and cat in ("IC", "IR", "RE", "EC", "TGV", "ICE")
            and stops_per_10 < 2):
        return "WORKABLE"

    # MARGINAL: >= 8 min but high stop density or regional only
    if duration_min >= 8:
        return "MARGINAL"

    return "NOT_WORKABLE"


# ──────────────────────────────────────────────────────
# Process one connection
# ──────────────────────────────────────────────────────

def process_connection(conn, from_station, to_station, time_slot):
    """Extract all fields from one connection object. Returns dict or None."""
    try:
        sections = conn.get("sections", [])
        if not sections:
            return None

        # Filter out walking sections (journey is null)
        ride_sections = [s for s in sections if s.get("journey")]
        if not ride_sections:
            return None

        # Overall departure/arrival
        dep_info = sections[0].get("departure", {})
        arr_info = sections[-1].get("arrival", {})
        departure_time = dep_info.get("departure", "")
        arrival_time = arr_info.get("arrival", "")

        # Duration
        duration_str = conn.get("duration", "")
        duration_min = round(parse_duration(duration_str), 1)

        # Number of sections (ride legs)
        num_sections = len(ride_sections)
        has_transfer = num_sections > 1

        # Find the longest leg → primary category + line name
        longest_leg = None
        longest_dur = -1
        for s in ride_sections:
            s_dep = s.get("departure", {}).get("departure", "")
            s_arr = s.get("arrival", {}).get("arrival", "")
            if s_dep and s_arr:
                try:
                    t0 = datetime.fromisoformat(s_dep)
                    t1 = datetime.fromisoformat(s_arr)
                    leg_dur = (t1 - t0).total_seconds()
                except Exception:
                    leg_dur = 0
            else:
                leg_dur = 0
            if leg_dur > longest_dur:
                longest_dur = leg_dur
                longest_leg = s

        journey_info = longest_leg.get("journey", {}) if longest_leg else {}
        primary_category = journey_info.get("category", "")
        line_name = journey_info.get("name", "")

        # Count intermediate stops (sum across all ride sections)
        total_intermediate = 0
        for s in ride_sections:
            j = s.get("journey", {})
            pass_list = j.get("passList", [])
            # passList includes departure and arrival, so intermediates = len - 2
            # But sometimes it's just intermediates. Let's count stops between
            # section departure and section arrival.
            if pass_list:
                # passList is all stops the train passes through (including endpoints of the section)
                # intermediates = total - 2 (first = departure, last = arrival of that section)
                inter = max(0, len(pass_list) - 2)
                total_intermediate += inter

        # Stop density
        if duration_min > 0:
            stops_per_10 = round(total_intermediate / (duration_min / 10), 2)
        else:
            stops_per_10 = 0

        # Transfer info
        transfer_station = ""
        transfer_wait_min = 0
        if has_transfer:
            # transfer happens between consecutive ride sections
            # but there may be walking sections in between
            for i in range(len(sections) - 1):
                s_curr = sections[i]
                s_next = sections[i + 1]
                # If current section ends and next one begins at different times → wait
                curr_arr = s_curr.get("arrival", {}).get("arrival", "")
                next_dep = s_next.get("departure", {}).get("departure", "")
                if curr_arr and next_dep:
                    try:
                        t_arr = datetime.fromisoformat(curr_arr)
                        t_dep = datetime.fromisoformat(next_dep)
                        wait = (t_dep - t_arr).total_seconds() / 60
                        if wait > transfer_wait_min:
                            transfer_wait_min = round(wait, 1)
                            transfer_station = s_curr.get("arrival", {}).get("station", {}).get("name", "")
                    except Exception:
                        pass

        # Comfort & workability
        cscore = comfort_score(primary_category)
        wclass = classify_workability(duration_min, primary_category, stops_per_10,
                                       has_transfer, transfer_wait_min)

        return {
            "from_station": from_station,
            "to_station": to_station,
            "time_slot": time_slot,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "duration_min": duration_min,
            "num_sections": num_sections,
            "primary_category": primary_category,
            "line_name": line_name,
            "intermediate_stops": total_intermediate,
            "stops_per_10min": stops_per_10,
            "has_transfer": has_transfer,
            "transfer_station": transfer_station,
            "transfer_wait_min": transfer_wait_min,
            "comfort_score": cscore,
            "workability_class": wclass,
        }
    except Exception as e:
        print(f"  WARNING: failed to parse connection: {e}")
        return None


# ──────────────────────────────────────────────────────
# Aggregation (summary per OD pair)
# ──────────────────────────────────────────────────────

def compute_summary(rows):
    """Aggregate rows by (from_station, to_station) → summary dict."""
    groups = defaultdict(list)
    for r in rows:
        key = (r["from_station"], r["to_station"])
        groups[key].append(r)

    summaries = []
    for (fr, to), conns in sorted(groups.items()):
        durations = [c["duration_min"] for c in conns]
        cats = [c["primary_category"] for c in conns if c["primary_category"]]
        spd = [c["stops_per_10min"] for c in conns]
        wclasses = [c["workability_class"] for c in conns]
        transfers = [c["has_transfer"] for c in conns]

        n = len(conns)
        avg_dur = round(sum(durations) / n, 1) if n else 0
        avg_spd = round(sum(spd) / n, 2) if n else 0

        # Best/worst category by comfort
        cat_order = {"IC": 6, "EC": 6, "TGV": 6, "ICE": 6, "IR": 5, "RE": 4, "RER": 4, "R": 3, "S": 2}
        if cats:
            best_cat = max(cats, key=lambda c: cat_order.get(c.upper(), 1))
            worst_cat = min(cats, key=lambda c: cat_order.get(c.upper(), 1))
        else:
            best_cat = worst_cat = ""

        # Workability percentages
        pct = lambda cls: round(100 * sum(1 for w in wclasses if w == cls) / n, 1) if n else 0
        pct_prime = pct("PRIME_WORK")
        pct_workable = pct("WORKABLE")
        pct_not_workable = pct("NOT_WORKABLE")
        xfer_pct = round(100 * sum(1 for t in transfers if t) / n, 1) if n else 0

        # Overall classification
        if pct_prime >= 50:
            overall = "PRIME_WORK"
        elif pct_prime + pct_workable >= 50:
            overall = "WORKABLE"
        elif pct_not_workable >= 50:
            overall = "NOT_WORKABLE"
        elif any(w == "BROKEN" for w in wclasses) and sum(1 for w in wclasses if w == "BROKEN") / n >= 0.3:
            overall = "BROKEN"
        else:
            overall = "MARGINAL"

        summaries.append({
            "from_station": fr,
            "to_station": to,
            "num_connections": n,
            "avg_duration_min": avg_dur,
            "best_category": best_cat,
            "worst_category": worst_cat,
            "avg_stops_per_10min": avg_spd,
            "pct_prime_work": pct_prime,
            "pct_workable": pct_workable,
            "pct_not_workable": pct_not_workable,
            "requires_transfer_pct": xfer_pct,
            "overall_workability": overall,
        })

    return summaries


# ──────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("City101 Journey-Level On-Train Workability Analysis")
    print(f"Corridor: Genève → Villeneuve → Aigle  |  Date: {QUERY_DATE}")
    print("=" * 70)

    od_pairs = build_od_pairs()
    print(f"\nOD pairs to query: {len(od_pairs)}")
    print(f"Time slots: {TIME_SLOTS}")
    total_queries = len(od_pairs) * len(TIME_SLOTS)
    print(f"Total API calls: {total_queries}")
    print(f"Estimated time: ~{total_queries * RATE_LIMIT_SEC:.0f}s\n")

    all_rows = []
    query_count = 0
    errors = 0

    for od_idx, (fr, to) in enumerate(od_pairs):
        for ts in TIME_SLOTS:
            query_count += 1
            if query_count % 10 == 0 or query_count == 1:
                print(f"  [{query_count}/{total_queries}] {fr} → {to} @ {ts}")

            data = fetch_connections(fr, to, ts)
            time.sleep(RATE_LIMIT_SEC)

            if not data or "connections" not in data:
                errors += 1
                continue

            for conn in data["connections"]:
                row = process_connection(conn, fr, to, ts)
                if row:
                    all_rows.append(row)

    print(f"\nFetch complete: {query_count} queries, {errors} errors, {len(all_rows)} connections parsed.\n")

    # ── Write CSV 1: per-connection ──
    csv1_path = f"{OUTPUT_DIR}/city101_journey_workability.csv"
    fieldnames_1 = [
        "from_station", "to_station", "time_slot", "departure_time", "arrival_time",
        "duration_min", "num_sections", "primary_category", "line_name",
        "intermediate_stops", "stops_per_10min", "has_transfer", "transfer_station",
        "transfer_wait_min", "comfort_score", "workability_class",
    ]
    with open(csv1_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_1)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Written: {csv1_path}  ({len(all_rows)} rows)")

    # ── Write CSV 2: summary per OD pair ──
    summaries = compute_summary(all_rows)
    csv2_path = f"{OUTPUT_DIR}/city101_journey_workability_summary.csv"
    fieldnames_2 = [
        "from_station", "to_station", "num_connections", "avg_duration_min",
        "best_category", "worst_category", "avg_stops_per_10min",
        "pct_prime_work", "pct_workable", "pct_not_workable",
        "requires_transfer_pct", "overall_workability",
    ]
    with open(csv2_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_2)
        writer.writeheader()
        writer.writerows(summaries)
    print(f"Written: {csv2_path}  ({len(summaries)} rows)")

    # ── Summary stats ──
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    # Workability distribution
    wc_counts = defaultdict(int)
    for r in all_rows:
        wc_counts[r["workability_class"]] += 1
    print("\nWorkability distribution (all connections):")
    for cls in ["PRIME_WORK", "WORKABLE", "MARGINAL", "NOT_WORKABLE", "BROKEN"]:
        n = wc_counts.get(cls, 0)
        pct = 100 * n / len(all_rows) if all_rows else 0
        bar = "#" * int(pct / 2)
        print(f"  {cls:15s}  {n:4d}  ({pct:5.1f}%)  {bar}")

    # Train type distribution
    print("\nTrain type distribution:")
    cat_counts = defaultdict(int)
    for r in all_rows:
        cat_counts[r["primary_category"] or "?"] += 1
    for cat, n in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:6s}  {n:4d}")

    # Top PRIME_WORK routes
    print("\nTop PRIME_WORK routes (by connection count):")
    prime_routes = defaultdict(int)
    for r in all_rows:
        if r["workability_class"] == "PRIME_WORK":
            prime_routes[(r["from_station"], r["to_station"])] += 1
    for (fr, to), n in sorted(prime_routes.items(), key=lambda x: -x[1])[:10]:
        print(f"  {fr:25s} → {to:25s}  {n} connections")

    # NOT_WORKABLE routes
    print("\nRoutes classified NOT_WORKABLE (too short / too many stops):")
    nw_routes = defaultdict(int)
    for r in all_rows:
        if r["workability_class"] == "NOT_WORKABLE":
            nw_routes[(r["from_station"], r["to_station"])] += 1
    for (fr, to), n in sorted(nw_routes.items(), key=lambda x: -x[1])[:10]:
        print(f"  {fr:25s} → {to:25s}  {n} connections")

    # Summary-level overall workability
    print("\nOD Pair Overall Workability Summary:")
    ow_counts = defaultdict(int)
    for s in summaries:
        ow_counts[s["overall_workability"]] += 1
    for cls in ["PRIME_WORK", "WORKABLE", "MARGINAL", "NOT_WORKABLE", "BROKEN"]:
        print(f"  {cls:15s}  {ow_counts.get(cls, 0)} OD pairs")

    # Average durations by category
    print("\nAverage duration by train category (minutes):")
    cat_durs = defaultdict(list)
    for r in all_rows:
        if r["primary_category"]:
            cat_durs[r["primary_category"]].append(r["duration_min"])
    for cat in sorted(cat_durs.keys()):
        vals = cat_durs[cat]
        print(f"  {cat:6s}  avg={sum(vals)/len(vals):5.1f}  min={min(vals):5.1f}  max={max(vals):5.1f}  n={len(vals)}")

    print("\n" + "=" * 70)
    print("Done.")


if __name__ == "__main__":
    main()
