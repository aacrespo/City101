# Utility: Verify Data

Run quality checks on a dataset. Follow `workflows/data-verification.md`.

## Usage
Specify the file to verify: `/verify-data path/to/file.csv`

## Checks to run
1. **Run `tools/data/verify_dataset.py`** on the target file
2. **Row count** — does it match expectations?
3. **Coordinate validation** — WGS84: lat 46.1–46.6, lon 6.0–7.1
4. **Required fields** — no nulls in ID, name, coordinates
5. **Source attribution** — source column present and populated
6. **Duplicates** — check for duplicate IDs
7. **Outliers** — flag any values that look impossible

## Output
Print a clear PASS/FAIL summary with details on any issues found.

If PASS and the file is in `output/`, recommend promoting to `datasets/` with the correct subfolder.
