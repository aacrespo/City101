# Prompt: Fix & Complete the Transport Map

## Context
You're working on City101, analyzing the 101km Geneva–Villeneuve rail corridor. Read CONTEXT.md first.

The existing transport map is at `deliverables/A03/train_pulse_24h.html`. It's a 24h animated Leaflet map showing train movements along the corridor. It works but needs fixes and completion.

## What needs to change

### 1. Remove the sky color system
The background currently shifts color to represent time of day (dawn, midday, dusk, night). **Remove this entirely.** We already have a clock display showing the time — the color changes are redundant and distracting. Set a fixed dark background (`#0a0a0f` or the existing dark color) that doesn't change.

Look for the `SKY` array and `skyColor()` function — remove or bypass them. The `mapEl.style.backgroundColor = skyColor(mt)` line in the animation loop needs to use a fixed color instead.

### 2. Better symbols (not just dots)
Currently trains are shown as dots. Replace with symbols that differentiate transport types:
- **IC/IR trains**: → arrow or elongated shape (fast, long-distance)
- **S-Bahn/Regional**: ○ circle (local, frequent)
- **RE**: ◇ diamond (regional express, in between)

Keep the trail/wake effect if it exists, just change the dot shape.

### 3. Add missing transport types
The map currently only shows trains. Add ALL public transport operating along the corridor:

| Transport | Data source | Symbol suggestion |
|---|---|---|
| **Postal buses (CarPostal)** | GTFS data from opentransportdata.swiss | 🟩 small square, green tint |
| **Funiculars** | Lausanne M2, Glion-Rochers-de-Naye, others | △ triangle |
| **Metro** | M1 (TSOL), M2 (TL) in Lausanne | ■ filled square |
| **CGN boats** | Lake Geneva boat service | ◁ boat shape |
| **Noctambus** | Night bus services (Fri/Sat only) | Same as bus but with glow/highlight |
| **LEB, BAM, MOB** | Regional narrow-gauge railways | Same as regional but different color |
| **Léman Express** | Cross-border rail (CEVA) | Already in data? Verify. |

**Data:** Check if GTFS data for these exists in `source/` or `datasets/`. If not, you may need to download from opentransportdata.swiss or create simplified route data. For the scope of this task, even approximate routes with correct schedules would work.

### 4. Show the complete network
The goal is: anyone looking at this map should understand the FULL public transport picture along the corridor. Not just the main rail lines but the actual network that real people use.

Add a legend showing all transport types with their symbols.

### 5. Highlight the 01:00–05:00 gap
When the clock enters the dead window, make it visually obvious:
- Maybe a subtle red pulse on the clock
- Or a text overlay: "DEAD WINDOW — Limited service"
- The emptiness of the map during these hours should speak for itself, but help the viewer notice

## Technical notes
- The existing map uses Leaflet + Canvas overlay for train rendering
- Train data comes from `source/animation/gtfs_corridor_trains_interpolated.csv` (39,695 rows, 860 trips)
- Station data from `source/animation/gtfs_corridor_stops.csv` (49 stations)
- Rail geometry from `source/animation/corridor_rail_lines_v3.geojson`
- Read LEARNINGS.md for known pitfalls with this data

## Output
- Updated `deliverables/A03/train_pulse_24h.html` (or create v2 if safer)
- Commit with clear message

## Quality bar
This is a presentation piece. It should look polished and be immediately readable. The viewer should see it and think "oh, THAT's what the corridor's transport looks like — and THAT's the gap."
