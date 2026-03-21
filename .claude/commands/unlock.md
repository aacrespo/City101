# /unlock — Remove PDF restrictions

Run this when a PDF is locked (Vectorworks Educational Version, print restrictions, etc.).

## Usage
`/unlock /path/to/file.pdf`

## Steps

1. Check if `pikepdf` is installed: `python3 -c "import pikepdf"`. If not, install: `pip3 install pikepdf`.

2. Run:
```bash
python3 -c "
import pikepdf, sys
pdf = pikepdf.open(sys.argv[1])
out = sys.argv[1].replace('.pdf', '_unlocked.pdf')
pdf.save(out)
pdf.close()
print(f'Saved to: {out}')
" "$input_path"
```

3. Output path: same directory, append `_unlocked` before `.pdf`.

4. Report the output path.

## Notes
- This removes permission restrictions (print/edit locks), NOT password encryption.
- If the PDF has a user password, it can't be unlocked without the password.
