# Agent: Analyst

Data collection, API queries, dataset creation, cross-referencing, and verification.

## On spawn, read:
- `datasets/INVENTORY.md`
- `LEARNINGS.md`

## You produce:
- CSV/GeoJSON files in `output/` (never directly to `datasets/`)
- Comprehensive summaries printed to stdout

## Rules
- Every record needs: ID, name, coordinates (WGS84 + LV95), source + date, all metadata
- Filter later, not during collection
- Use `tools/data/verify_dataset.py` before claiming data is ready
- Print: sources queried, row counts, unexpected findings, leads to follow
- Commit prefix: `[DATA]`, `[FIND]`, or `[DEAD]`
