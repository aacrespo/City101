# PDF Export

Convert a markdown file to a print-ready HTML with City101 design system styles (screen + print).

## Arguments
$ARGUMENTS — path to the markdown file to convert

## Instructions

1. Resolve the file path from $ARGUMENTS (relative paths resolve from repo root). Confirm it exists.
2. Run the conversion tool:
   ```
   python tools/export/md_to_html.py <input_path> [optional_output_path]
   ```
   The tool handles markdown parsing, City101 styling, and print CSS. Output defaults to `<name>_print.html`.
3. Report: output file path, brief content summary (headings/tables/code blocks found).
4. Remind the user: open in browser → Cmd+P / Ctrl+P → Save as PDF.

## Important
- Do NOT modify the source markdown file.
- If the tool isn't installed (`markdown` module missing), run: `pip install markdown`
- The tool's styles match `design_system/SPEC.md` (dark screen, clean print). If you need to customize styles, edit `tools/export/md_to_html.py`.
