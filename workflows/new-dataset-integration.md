# Workflow: New Dataset Integration

## Objective
Integrate a new classmate dataset into the project.

## When to use
When incorporating data from `source/00-datasets 2/` (classmate submissions) or any external dataset.

## Required inputs
- Source file path (in `source/`)
- Classmate name and dataset description
- Expected coordinate system

## Steps
1. **Identify source file** in `source/00-datasets 2/` or other location
2. **Check coordinate system**:
   - WGS84 (lat/lon) → ready for web, needs LV95 for QGIS
   - LV95 (E/N) → ready for QGIS, needs WGS84 for web
   - GPX → needs conversion to CSV first
   - If conversion needed: use `tools/data/convert_coordinates.py`
3. **Check for overlaps** with existing data:
   - Religious buildings: compare with Thomas Riegert's data
   - Stores/grocery: compare with Marek Waeber's data (known incomplete)
   - Cultural: compare with Henna's data
   - Use duplicate detection in `tools/util/merge_datasets.py` if available
4. **Validate** using `workflows/data-verification.md`:
   - Row counts, coordinate ranges, required fields, source attribution
5. **Add station-level data to crossref** if applicable:
   - Match points to nearest of 49 corridor stations
   - Add columns to `datasets/corridor_analysis/city101_station_crossref_classmates.csv`
6. **Update `datasets/INVENTORY.md`** with new entry:
   - Dataset name, file path, row count, key columns, source, date
7. **Commit with `[DATA]` prefix**

## Expected output
- Verified dataset in `datasets/[subfolder]/`
- Updated INVENTORY.md
- Updated crossref if station-level

## Edge cases
- GPX format (Aimeric Marin): convert to CSV with lat/lon extraction first
- Image-only data (PNG maps): cannot be automated — manual extraction needed, flag for human
- QGIS project format (Cristina Martinez): needs QGIS MCP to extract layers
- Overlapping data: don't discard either — merge with source tracking so both origins are preserved

## History
- 10 March 2026: Created (v7 repo setup)
