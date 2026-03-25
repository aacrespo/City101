# HANDOFF FOR LUMEN — Station Reviews + Data Fetching
**From**: Cairn (desktop app, Session 6)
**To**: Lumen (browser, claude.ai)
**Date**: 2026-03-01 late night
**Purpose**: Execute data fetching tasks while Cairn holds narrative context

---

## YOUR ROLE
You are the data fetcher. Cairn (desktop with QGIS MCP) holds the analysis context and will process your outputs. Your job: produce clean CSVs that Andrea drops into `~/CLAUDE/City101_ClaudeCode/output/`. Don't analyze — just fetch, clean, and output.

## CONTEXT (read these from project knowledge if needed)
- `TODO_4_POINTS.md` — the full task breakdown
- `CONTEXT.md` — project state
- The project studies the Geneva–Villeneuve corridor (City101), analyzing working continuity infrastructure

---

## TASK 1: EXPANDED STATION LIST + GOOGLE REVIEWS (PRIORITY)

### Step 1: Build the station list (~80-100 stations)

Start with these 49 existing train stations (already in our data):
Genève, Genève-Sécheron, Genève-Aéroport, Genève-Eaux-Vives, Genève-Champel, Lancy-Bachet, Lancy-Pont-Rouge, Genthod-Bellevue, Vernier, Versoix, Coppet, Tannay, Mies, Founex, Nyon, Prangins, Gland, Begnins, Rolle, Perroy, Allaman, Aubonne, Saint-Prex, Morges, Lonay-Préverenges, Denges-Echandens, Bussigny, Renens VD, Prilly-Malley, Lausanne, Lausanne-Flon, La Conversion, Bossière, Grandvaux, Cully, Épesses, Rivaz, Saint-Saphorin, Vevey, La Tour-de-Peilz, Burier, Clarens, Montreux, Territet, Villeneuve VD, Aigle, Bex, Palézieux, Puidoux

**ADD these missing stations** (use Google Places to find and verify each):

Missing train stations:
- Lutry (between La Conversion and Bossière — major gap!)
- Chexbres-Village
- Puidoux-Chexbres

Lausanne M2 metro (all stations):
- Ouchy-Olympique, Jordils, Délices, Grancy, Flon (already have Lausanne-Flon), Riponne-Maurice Béjart, Bessières, Ours, CHUV, Aulagnon (if exists), Sallaz, Fourmi, Vennes, EPFL (M1), UNIL-Mouline (M1), UNIL-Sorge (M1), Bourdonnette (M1), Malley (M1), Vigie (M1), Lausanne-Gare (M1)

Léman Express additions (not already in list):
- Chêne-Bourg, Annemasse (cross-border!), Bernex, Bachet-de-Pesay

CGN boat landings (main corridor ones):
- Genève-Jardin Anglais, Genève-Pâquis, Nyon CGN, Rolle CGN, Morges CGN, Saint-Sulpice CGN, Lausanne-Ouchy CGN, Lutry CGN, Cully CGN, Vevey CGN, La Tour-de-Peilz CGN, Montreux CGN, Territet CGN, Villeneuve CGN, Chillon CGN

### Step 2: For EACH station, use Google Places to find:
- Google Place ID
- Google rating (1-5 stars)
- Google review count
- Station type (train/metro/boat/bus_hub)
- Coordinates (lat/lon WGS84)

### Step 3: For stations with reviews, fetch up to 5 reviews each
Tag each review for these themes (boolean flags):
- shelter (mentions rain, wind, cold, exposed, covered)
- cleanliness (dirty, clean, graffiti, maintained)
- safety (unsafe, dark, empty, sketchy, secure)
- wayfinding (confusing, signs, lost, underground, maze)
- amenities (café, vending, toilet, kiosk, shop)
- accessibility (elevator, stairs, wheelchair, stroller)
- crowding (full, packed, sardine, empty, spacious)
- beauty (lake view, nice, pleasant, architecture)
- work_friendly (laptop, wifi, work, quiet, plug, outlet)

Also tag sentiment: positive / negative / neutral

### Output files

**File 1: `city101_station_ratings.csv`**
Columns: station_name, station_type, lat_wgs84, lon_wgs84, google_place_id, google_rating, google_review_count, transport_mode

**File 2: `city101_station_REVIEWS.csv`**
Columns: station_name, station_type, google_place_id, review_text, shelter, cleanliness, safety, wayfinding, amenities, accessibility, crowding, beauty, work_friendly, sentiment

---

## TASK 2: FIRST/LAST TRAIN (IF TIME PERMITS)

For each of the ~52 train stations (not metro/boat), query:
- First departure (earliest train, any direction, weekday)
- Last departure (latest train, any direction, weekday)
- Dead window duration (hours between last and first)

This can potentially be done via web search of SBB timetables if the transport API isn't accessible from browser.

**Output: `city101_first_last_trains.csv`**
Columns: station_name, first_departure, last_departure, dead_window_hours, direction_first, direction_last

---

## TASK 3: TICKET PRICES (IF TIME PERMITS)

Research SBB pricing for key journeys:
- Geneva → Lausanne (point-to-point, demi-tarif, GA daily cost)
- Geneva → Villeneuve (same)
- Lausanne → Montreux (same)
- Nyon → Lausanne (same)
- Geneva → Nyon (same)

Also: Léman Pass prices, monthly/annual Abo costs for common segments.

**Output: `city101_ticket_prices.csv`**
Columns: from, to, distance_km, price_full, price_demitarif, price_ga_daily, price_abo_monthly

---

## IMPORTANT NOTES
- You have Google Places access (search, reviews, hours)
- Output CSVs as downloadable files — Andrea will move them to ~/CLAUDE/City101_ClaudeCode/output/
- Don't analyze the data — Cairn will do that with QGIS MCP
- If a station doesn't appear in Google Places, note it but move on
- Rate limit yourself — don't blast 100 Places queries at once
- Use the same review tagging methodology we used for EV charging reviews and remote work reviews (check project knowledge for those if needed)
- Coordinate system: WGS84 for lat/lon (Cairn will convert to LV95 for QGIS)

## WHEN DONE
Tell Andrea the files are ready for download. She'll drop them in the CLAUDE folder and Cairn picks them up from there.
