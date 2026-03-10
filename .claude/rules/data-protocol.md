# Data Protocol

## Collection requirements
Before any API query or dataset creation, each record must have:
1. Unique ID
2. Name / label
3. Coordinates (both WGS84 and LV95)
4. Source + fetch date
5. All available metadata from the API

**Filter later for export, not during collection.**

## Corridor reference
- 49 stations: Geneva (Genève) → Villeneuve
- Valid WGS84 ranges: lat 46.1–46.6, lon 6.0–7.1
- Valid LV95 ranges: E 2'496'000–2'565'000, N 1'130'000–1'155'000

## Data operations approach
For large operations (API fetches, processing big files): write a **single self-contained script** that runs end-to-end.

Pattern: fetch → filter → process → match → write output → **print comprehensive summary**.

The summary must list:
- Every dataset or source queried
- Row counts and key statistics
- Anything unexpected or worth investigating
- Download URLs for data not fetched

## Quality gates
Before promoting any data from `output/` to `datasets/`:
- Row counts match expectations
- Coordinates valid (ranges above)
- No null/empty required fields (ID, name, coordinates)
- Source attribution present
- No absurd outliers or duplicates

Use `tools/data/verify_dataset.py` to check. See `workflows/data-verification.md`.

## Data flow
```
API / source → output/ (staging) → verify → datasets/ (production)
```
Agent output ALWAYS goes to `output/` first. Nothing reaches `datasets/` unverified.
