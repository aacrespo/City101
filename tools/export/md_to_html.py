#!/usr/bin/env python3
"""Convert markdown to styled HTML with City101 design system.

Usage:
    python tools/export/md_to_html.py <input.md> [output.html]

If no output path is given, replaces .md with _print.html.
Opens in browser when done.

Requires: pip install markdown
"""

import sys
import re
import webbrowser
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Installing markdown...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
    import markdown


# ── City101 Design System Styles ──────────────────────────────────────────

SCREEN_CSS = """
body {
  background: #0a0a0f;
  color: #e8e6e1;
  font-family: 'Courier New', 'DM Mono', monospace;
  font-size: 14px;
  line-height: 1.75;
  margin: 0;
  padding: 0;
}
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 60px 40px;
}
h1 {
  color: #c9a84c;
  font-size: 28px;
  font-weight: 400;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border-bottom: 1px solid #333;
  padding-bottom: 12px;
  margin-top: 48px;
  margin-bottom: 24px;
}
h2 {
  color: #c9a84c;
  font-size: 20px;
  font-weight: 400;
  letter-spacing: 0.03em;
  margin-top: 40px;
  margin-bottom: 16px;
}
h3 {
  color: #d4c08a;
  font-size: 16px;
  font-weight: 600;
  margin-top: 32px;
  margin-bottom: 12px;
}
h4, h5, h6 {
  color: #8a8880;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 24px;
  margin-bottom: 8px;
}
p { margin: 0 0 16px 0; }
strong { color: #e8e6e1; font-weight: 700; }
em { font-style: italic; color: #c9a84c; }
a { color: #c9a84c; text-decoration: underline; text-underline-offset: 3px; }
ul, ol {
  margin: 0 0 16px 0;
  padding-left: 24px;
}
li { margin-bottom: 6px; }
li::marker { color: #8a8880; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
  font-size: 13px;
}
th {
  background: #1a1a22;
  color: #c9a84c;
  text-align: left;
  padding: 10px 14px;
  border-bottom: 2px solid #c9a84c;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-size: 11px;
}
td {
  padding: 8px 14px;
  border-bottom: 1px solid #1a1a22;
}
tr:nth-child(even) { background: #0f0f17; }
tr:hover { background: #1a1a25; }
code {
  background: #1a1a22;
  color: #d4c08a;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}
pre {
  background: #0f0f17;
  border: 1px solid #1a1a22;
  border-left: 3px solid #c9a84c;
  padding: 16px 20px;
  overflow-x: auto;
  margin: 20px 0;
  border-radius: 2px;
}
pre code {
  background: none;
  padding: 0;
  font-size: 13px;
  line-height: 1.6;
}
blockquote {
  border-left: 3px solid #c9a84c;
  margin: 20px 0;
  padding: 12px 20px;
  background: #0f0f17;
  color: #8a8880;
  font-style: italic;
}
blockquote p { margin-bottom: 8px; }
blockquote p:last-child { margin-bottom: 0; }
hr {
  border: none;
  border-top: 1px solid #333;
  margin: 40px 0;
}
img { max-width: 100%; height: auto; margin: 20px 0; }
.print-button-wrap {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}
.print-button-wrap button {
  background: #c9a84c;
  color: #0a0a0f;
  border: none;
  padding: 10px 24px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  cursor: pointer;
}
.print-button-wrap button:hover { background: #d4c08a; }
"""

PRINT_CSS = """
@media print {
  @page {
    size: A4;
    margin: 25mm 20mm 30mm 20mm;
  }
  body {
    background: #fff;
    color: #1a1a1a;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
  }
  .container {
    max-width: none;
    padding: 0;
    margin: 0;
  }
  .print-button-wrap { display: none; }
  h1 {
    color: #000;
    font-family: Georgia, serif;
    font-size: 22pt;
    text-transform: none;
    letter-spacing: 0;
    border-bottom: 2px solid #000;
    page-break-after: avoid;
  }
  h2 {
    color: #000;
    font-family: Georgia, serif;
    font-size: 16pt;
    page-break-after: avoid;
  }
  h3 {
    color: #333;
    font-size: 13pt;
    page-break-after: avoid;
  }
  h4, h5, h6 {
    color: #333;
    font-size: 11pt;
    page-break-after: avoid;
  }
  strong { color: #000; }
  em { color: #333; font-style: italic; }
  a { color: #000; text-decoration: none; }
  table {
    font-size: 9pt;
    page-break-inside: avoid;
  }
  th {
    background: #f0f0f0;
    color: #000;
    border-bottom: 2px solid #000;
    text-transform: none;
  }
  td { border-bottom: 1px solid #ccc; }
  tr:nth-child(even) { background: none; }
  tr:hover { background: none; }
  thead { display: table-header-group; }
  code {
    background: #f5f5f5;
    color: #333;
    border: 1px solid #ddd;
  }
  pre {
    background: #f8f8f8;
    border: 1px solid #ddd;
    border-left: 3px solid #333;
    font-size: 9pt;
    page-break-inside: avoid;
  }
  pre code { border: none; background: none; }
  blockquote {
    border-left: 3px solid #666;
    background: #f8f8f8;
    color: #333;
  }
  h1 { page-break-before: always; }
  h1:first-of-type { page-break-before: avoid; }
  p, li, blockquote {
    orphans: 3;
    widows: 3;
  }
  img {
    max-width: 100%;
    page-break-inside: avoid;
  }
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>{screen_css}{print_css}</style>
</head>
<body>
  <div class="container">
    <div class="print-button-wrap">
      <button onclick="window.print()">Print to PDF</button>
    </div>
    {content}
  </div>
</body>
</html>
"""


def extract_title(md_text: str, fallback: str) -> str:
    """Extract first h1 from markdown, or use filename as fallback."""
    match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def strip_frontmatter(md_text: str) -> str:
    """Remove YAML front matter if present."""
    if md_text.startswith('---'):
        end = md_text.find('---', 3)
        if end != -1:
            return md_text[end + 3:].lstrip()
    return md_text


def convert(input_path: str, output_path: str = None) -> str:
    """Convert markdown file to styled HTML. Returns output path."""
    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"File not found: {src}")

    if output_path:
        dst = Path(output_path)
    elif src.suffix == '.md':
        dst = src.with_name(src.stem + '_print.html')
    else:
        dst = src.with_name(src.name + '_print.html')

    md_text = src.read_text(encoding='utf-8')
    md_text = strip_frontmatter(md_text)
    title = extract_title(md_text, src.stem)

    html_content = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'nl2br'],
        output_format='html5'
    )

    full_html = HTML_TEMPLATE.format(
        title=title,
        screen_css=SCREEN_CSS,
        print_css=PRINT_CSS,
        content=html_content,
    )

    dst.write_text(full_html, encoding='utf-8')
    return str(dst)


def main():
    if len(sys.argv) < 2:
        print("Usage: python md_to_html.py <input.md> [output.html]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    result = convert(input_path, output_path)
    print(f"Created: {result}")
    print("Open in browser and Cmd+P / Ctrl+P to save as PDF.")

    try:
        webbrowser.open(f"file://{Path(result).resolve()}")
    except Exception:
        pass


if __name__ == '__main__':
    main()
