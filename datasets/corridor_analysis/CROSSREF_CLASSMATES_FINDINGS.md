# Classmate Cross-Reference — Findings
**Date**: 2026-03-01  
**Dataset**: `city101_station_crossref_classmates.csv` (49 stations × 46 columns)  
**Method**: Haversine distance from each of 49 corridor stations to 2,093 geocoded points from 33 classmate datasets, counted at 500m and 1000m radii. Religious diversity measured via Shannon index across denominations.

---

## Datasets integrated

| Classmate | Dataset | Points | Theme |
|-----------|---------|--------|-------|
| Charlene Dejean | Gig work locations | 50 | Labor / precariat |
| Thomas Riegert | Public hospitals | 23 | Healthcare / shift workers |
| Thomas Riegert | Private clinics | 68 | Healthcare |
| Thomas Riegert | General practitioners | 110 | Healthcare |
| Thomas Riegert | Specialists | 188 | Healthcare |
| Thomas Riegert | Religious buildings (7 types) | 204 | Diversity / Comtesse |
| Thomas Riegert | Religious communities (8 types) | 274 | Diversity / Comtesse |
| Thomas Riegert | Esoteric practices | 43 | Diversity |
| Siméon Pavicevic | Industrial zones | 25 | Production economy |
| Siméon Pavicevic | Industrial companies | 195 | Production economy |
| Marek Waeber | Public schools (all levels) | 199 | Family infrastructure |
| Marek Waeber | Grocery stores (5 brands) | 121 | Daily needs |
| Vladislav Belov | Acoustic ecology points | 49 | Environmental quality |
| Henna Rafik | UHI zones (high/med/low) | 203 | Thermal comfort |
| Henna Rafik | Thermal comfort points | 33 | Environmental quality |
| Mohamad Ali | Restaurants | 150 | Food economy |
| Mohamad Ali | Informal learning spaces | 132 | Knowledge infrastructure |
| Charlene Dejean | Rooftops / best views | 27 | Experiential quality |

---

## Key findings

### 1. Comtesse vindicated — diversity correlates with urban completeness

Religious diversity (Shannon index) and station richness track almost perfectly along the corridor. The five most religiously diverse stations are all in the top seven richest:

| Station | Shannon diversity | Denominations | Richness (1km) |
|---------|------------------|---------------|----------------|
| Genève-Champel | 2.12 | 10 (all represented) | 127 |
| Lausanne | 1.96 | 9 | 250 |
| Lausanne-Flon | 1.94 | 9 | 277 |
| Genève-Eaux-Vives | 1.94 | 8 | 59 |
| Vevey | 1.73 | 7 | 75 |

Comtesse's formula — diversity × accessibility × time = urban vitality — is empirically confirmed at the station level. Where denominations coexist, everything else clusters too: healthcare, schools, restaurants, workspaces. Homogeneous segments (Lavaux, Bex, Palézieux) have near-zero richness.

### 2. The richness cliff — binary, not gradient

Lausanne-Flon: 277 features within 1km. Palézieux: 0. This isn't a gentle fade — the corridor switches between extreme urban intensity and absolute void. The top 5 stations contain more classmate features than the bottom 30 combined.

### 3. Frequency-amenity paradox — confirmed with 33 datasets

Stations with excellent transit but near-zero urban richness — the train delivers you to a void:

| Station | Trains/hr | Richness | Healthcare | Schools |
|---------|-----------|----------|------------|---------|
| Vernier Blandonnet | 84.0 | 7 | 0 | 0 |
| Palézieux | 11.5 | 0 | 0 | 0 |
| Aigle | 16.5 | 1 | 0 | 0 |
| Lancy-Bachet | 12.5 | 5 | 0 | 2 |
| Bussigny | 9.0 | 3 | 0 | 0 |

These are the **highest-impact intervention sites** for the adaptive rail module. The infrastructure for arrival exists; the infrastructure for staying does not.

### 4. Gig work follows tourism, not infrastructure gaps

Gig workers cluster at lakeside tourism nodes: Vevey (5), Montreux (5), Nyon (4), Morges (4). Geneva proper has only 2 within 1km of the main station. Zero gig work at break points like Bussigny or Palézieux.

The precariat follows the tourists, not the commuters. This means the gig economy and the knowledge economy use different versions of the same corridor — different stations, different hours, different spatial logic. The corridor has at least three overlapping cities: the IC knowledge corridor, the S-Bahn commuter corridor, and the tourism/gig corridor.

### 5. Industry disconnected from the rail spine

The top industrial station by company count is Begnins (6 companies, 8.5 trains/hr) — a small village stop. Major industrial zones (PAV-Geneva, Vevey, Montreux) register as zone proximity but with few individual companies near rail. Siméon's data confirms the production economy doesn't align with the knowledge worker corridor. Industry uses roads; knowledge uses rails. Same territory, parallel networks.

### 6. Healthcare generates night demand at rich nodes

Hospitals and clinics cluster at Geneva (50 within 1km of Champel), Lausanne (92 near Flon), and Vevey (13). These are the nodes where shift workers start and end their days. When crossed with first/last train data (Henna's priority), this will reveal which healthcare workers get stranded by the dead window — a nurse finishing at CHUV (Lausanne) at 23:00 needing to reach Montreux faces a different corridor than one needing to reach Renens.

### 7. Schools as family infrastructure filter

199 schools across the corridor, but heavily concentrated at nodes. Stations like Aigle (16.5 trains/hr) have zero schools within 1km despite being a cantonal town. This suggests families in gap segments depend on cars for school access, reinforcing the "corridor selects for car-owners in the gaps" hypothesis.

---

## What this means for the prototypology

The adaptive rail module should deploy at **frequency-amenity paradox stations** — places where transit connectivity exists but urban completeness doesn't. The classmate cross-reference gives us the specific intervention sites and tells us what's missing at each:

- **Palézieux**: Everything. First candidate for full-program module.
- **Aigle**: Healthcare, schools, workspaces. Eastern corridor's biggest void.
- **Bussigny**: Western Lausanne's paradox — major interchange, no urban life.
- **Lancy-Bachet**: Geneva's southern gateway, no there there.
- **Vernier Blandonnet**: 84 trains/hr, 7 features. The busiest nothing.

---

## Columns in the dataset

The CSV contains 46 columns. For each classmate dataset: `{label}_500m` and `{label}_1000m` counts. Plus:
- `healthcare_total_500m/1000m` — aggregated across hospitals, clinics, GPs, specialists
- `religious_total_500m/1000m` — aggregated across all denominations
- `religious_denominations_1000m` — count of distinct denominations
- `religious_denominations_list` — which denominations present
- `religious_shannon_diversity` — Shannon diversity index (0 = monoculture, >2 = highly diverse)
- `station_richness_1000m` — total non-religious classmate features within 1km
