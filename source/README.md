# Source Data — City101 Geneva-Villeneuve Corridor

This folder contains **raw source data** used to produce the clean analysis datasets in `../datasets/`.
Do not edit files here for analysis — use `../datasets/` instead.

---

## Folder Structure

### `WORK copy/` — Active Base Map Layers (23 GeoPackages, ~391 MB)
**Loaded in QGIS project.** Core geometric layers for the corridor.

| Layer | Description |
|-------|-------------|
| City101_Buildings.gpkg | Building footprints (145 MB) |
| City101_Streets.gpkg | Street network (66 MB) |
| City101_SingleTreesBush.gpkg | Vegetation (96 MB) |
| City101_TrainLines.gpkg | Rail infrastructure (30 MB) |
| City101_Road_NODES.gpkg | Road network nodes (24 MB) |
| City101_Flowing_Waters.gpkg | Rivers & streams |
| City101_VillageNames.gpkg | Place names |
| City101_Communes.gpkg | Municipal boundaries |
| City101_Communes_SURFACE.gpkg | Municipal boundary surfaces |
| City101_CantonalBoundaries.gpkg | Cantonal borders |
| City101_LakeLeman.gpkg | Lake Geneva |
| City101_StandingWater.gpkg | Ponds & lakes |
| City101_SpecialUse_Area.gpkg | Land use categories |
| City101_TrafficZonesParkings.gpkg | Parking & traffic zones |
| City101_Traffic_Structures.gpkg | Traffic features |
| City101_Transit_Stops.gpkg | Train & transit stations |
| City101_Transit_Buildings_AirportETC.gpkg | Airport & transit buildings |
| City101_Sports_Fields.gpkg | Sports infrastructure |
| City101_Highway_EntryExits.gpkg | Highway access points |
| City101_FieldNames.gpkg | Agricultural field names |
| City101_PeakNames.gpkg | Mountain peaks |
| City101_Walls.gpkg | Walls & fences |
| City101_GroundCover.gpkg | Ground cover (180 KB, lean version) |

### `Documents copy/` — Secondary Base Layers (3 GeoPackages, ~33 MB)
Also loaded in QGIS. Includes an earlier, larger version of GroundCover.

| Layer | Description |
|-------|-------------|
| City101_GroundCover.gpkg | Ground cover (27 MB — earlier/larger version) |
| City101_SmallBuildings.gpkg | Small building subset (5.1 MB) |
| City101_LeisureArea.gpkg | Leisure & recreation zones (544 KB) |

### `00-datasets 2/` — Classmate Submissions (18 students, ~2 GB)
Raw datasets contributed by BA6 studio classmates. Each student's folder uses the `studentname-filename` prefix convention.

| Student | Topic | Formats |
|---------|-------|---------|
| **aimericmarin** | Cultural spaces, libraries, museums, sailboats, theaters | GPX, PNG |
| **alexeipotapushin** | Coop/Migros retail, e-commerce, delivery tiers A/B/C | CSV, GeoJSON, PDF |
| **andreacrespo** | EV charging, remote work, wifi, cell towers | CSV, GPKG, PDF, PY |
| **charlenedejean** | Gig work, rooftops | CSV |
| **cristinamartinez** | Intergenerational exchange, social segregation | QGZ, PDF |
| **danielgo** | Electronics repair, e-waste, secondhand stores | CSV, PDF |
| **dimitriroulet** | Waste: hazardous, incineration, composting, landfill, sorting, wastewater | CSV |
| **hennarafik** | UHI heat islands, cold air drainage, psycho-comfort, cultural circuits, local traditions, thermal comfort | CSV, GPKG, PDF, QGZ |
| **jeppeoppegaard** | Secondhand shops, wastewater treatment, lake villages | CSV |
| **juliefavre** | Apple farms, commercial hubs, farm-to-market flows, pollinator hubs | CSV, GeoJSON, PDF |
| **lhiamrossier** | Water quality (CIPEL), microbial flows, STEP, marshlands, soil, amphibian zones + TLM3D base (1.5 GB) | CSV, GeoJSON, GPKG |
| **marekwaeber** | Public schools (all levels), supermarkets (Migros/Coop/Aldi/Lidl/Denner) | CSV, PDF |
| **mohamadalielmawla** | Food systems/restaurants, informal learning | CSV, QGZ, PDF |
| **noebrun** | Churches, ephemeral events, ports | CSV |
| **simeonpavicevic** | Energy consumption/production, industrial sectors/zones | CSV, GeoJSON |
| **stellaguicciardi** | Birdhouses (Geneva + Lausanne), temporary structures | CSV, PDF |
| **thomasriegert** | Religious communities (8 faiths), health (GPs, hospitals, clinics, specialists) | CSV, QGZ |
| **vladislavbelov** | Acoustic ecology, local materials, noise rasters, tranquility | CSV, GPKG, PDF, TIF |

### `Charging station csv copy/` — EV Charging Working Copy
Copies of EV charging CSVs and the enrichment script. Canonical versions are in `../datasets/ev_charging/`.

### `invisible flows copy/` — Remote Work / Connectivity Working Copy
Working copies of wifi, cell towers, remote work data and enrichment scripts. Canonical versions are in `../datasets/remote_work/`.

### `lausanne/` — Lausanne Open Data (Shapefiles)
Official Ville de Lausanne open data exports:
- **Horodateur/** — Parking meters
- **Mobilier-urbain/** — Urban furniture (benches)
- **Stationnement/** — Parking: tariff codes, macaron zones, parking lots, parking points

### `zurich/` — Zurich Comparison Data
- `Greater_Zurich_StatPop_Version.gpkg` (588 MB) — Zurich S8 lakeside corridor benchmark

### Root-level files (scripts & working CSVs)
Fetch scripts and intermediate CSVs used during data collection. Canonical versions of these CSVs are in `../datasets/`.

---

## Coordinate System Conventions

All CSVs have been standardized to use these column names:

| Column | Coordinate System | Example Values |
|--------|-------------------|----------------|
| `lat_wgs84` | WGS84 latitude | 46.2044 |
| `lon_wgs84` | WGS84 longitude | 6.1432 |
| `E_LV95` | Swiss LV95 easting | 2,500,000+ |
| `N_LV95` | Swiss LV95 northing | 1,100,000+ |
| `E_CH1903` | Old Swiss CH1903 easting (lhiamrossier only) | ~500,000 |
| `N_CH1903` | Old Swiss CH1903 northing (lhiamrossier only) | ~150,000 |

---

## What Goes Where

| If you need... | Go to... |
|----------------|----------|
| Clean analysis-ready CSVs | `../datasets/` |
| QGIS base map layers | `source/WORK copy/` + `source/Documents copy/` |
| Raw classmate submissions | `source/00-datasets 2/{studentname}/` |
| Zurich S8 comparison | `source/zurich/` |
| Lausanne parking/urban furniture | `source/lausanne/` |
| Data collection scripts | `source/*.py` or `source/Charging station csv copy/` |
| Superseded/old versions | `../archive/superseded/` |
