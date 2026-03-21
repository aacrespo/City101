# PDF Export

Convert a markdown file to a print-ready HTML with screen and print styles.

## Arguments
$ARGUMENTS — path to the markdown file to convert

## Instructions

You are converting a markdown file to a standalone, beautifully styled HTML file optimized for both screen viewing and PDF printing.

### Step 1: Read the source file

Read the markdown file at the path provided in $ARGUMENTS. If the path is relative, resolve it from the repository root. Confirm the file exists and has content before proceeding.

### Step 2: Determine the output path

Replace the `.md` extension with `_print.html`. Example: `output/research.md` becomes `output/research_print.html`. If the file doesn't end in `.md`, append `_print.html` to the full filename.

### Step 3: Parse and convert the markdown

Convert the full markdown content to HTML, handling all of these elements:

- **Headings** (h1–h6): proper hierarchy, spacing, and styling
- **Paragraphs**: with comfortable line-height
- **Bold and italic**: `**bold**`, `*italic*`, `***bold italic***`
- **Lists**: ordered and unordered, including nested lists
- **Tables**: full support with headers, alignment, alternating row colors
- **Code blocks**: fenced (```) with language class if specified, and inline `code`
- **Blockquotes**: with left border accent
- **Horizontal rules**: as section dividers
- **Links**: styled but functional
- **Images**: if referenced, include with max-width constraints

### Step 4: Generate the HTML file

Write a single standalone HTML file with all CSS embedded (no external dependencies). The file must include:

#### Document structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[extracted from first h1, or filename]</title>
  <style>/* all styles here */</style>
</head>
<body>
  <div class="container">
    <div class="print-button-wrap">
      <button onclick="window.print()">Print to PDF</button>
    </div>
    <!-- converted content -->
  </div>
</body>
</html>
```

#### Screen styles (default)

Use the City101 design system aesthetic:

```css
/* Base */
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

/* Headings */
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

/* Text */
p { margin: 0 0 16px 0; }

strong { color: #e8e6e1; font-weight: 700; }
em { font-style: italic; color: #c9a84c; }

a { color: #c9a84c; text-decoration: underline; text-underline-offset: 3px; }

/* Lists */
ul, ol {
  margin: 0 0 16px 0;
  padding-left: 24px;
}
li { margin-bottom: 6px; }
li::marker { color: #8a8880; }

/* Tables */
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

/* Code */
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

/* Blockquotes */
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

/* Horizontal rule */
hr {
  border: none;
  border-top: 1px solid #333;
  margin: 40px 0;
}

/* Images */
img { max-width: 100%; height: auto; margin: 20px 0; }

/* Print button */
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
```

#### Print styles (@media print)

These override screen styles for clean PDF output:

```css
@media print {
  @page {
    size: A4;
    margin: 25mm 20mm 30mm 20mm;

    @bottom-center {
      content: counter(page);
      font-family: Georgia, serif;
      font-size: 10px;
      color: #666;
    }
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

  /* Hide print button */
  .print-button-wrap { display: none; }

  /* Headings */
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

  /* Text */
  strong { color: #000; }
  em { color: #333; font-style: italic; }
  a { color: #000; text-decoration: none; }

  /* Tables */
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
  td {
    border-bottom: 1px solid #ccc;
  }
  tr:nth-child(even) { background: none; }
  tr:hover { background: none; }
  thead { display: table-header-group; }

  /* Code */
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

  /* Blockquotes */
  blockquote {
    border-left: 3px solid #666;
    background: #f8f8f8;
    color: #333;
  }

  /* Page breaks */
  h1 { page-break-before: always; }
  h1:first-of-type { page-break-before: avoid; }

  /* Prevent orphans and widows */
  p, li, blockquote {
    orphans: 3;
    widows: 3;
  }

  /* Images */
  img {
    max-width: 100%;
    page-break-inside: avoid;
  }
}
```

### Step 5: Verify and report

After writing the file:
1. Confirm the output file was created and state its path
2. Report a brief summary: number of headings, tables, code blocks found
3. Remind the user they can open the HTML in a browser and click "Print to PDF" or use Cmd+P / Ctrl+P to export

### Important notes

- Do NOT use any external CDN, JavaScript library, or CSS framework. Everything must be embedded.
- Do NOT modify the source markdown file.
- Escape any HTML special characters (`<`, `>`, `&`) that appear in the markdown content as literal text (not as tags).
- Preserve the document's structure faithfully — do not reorder, summarize, or omit content.
- If the markdown contains front matter (YAML between `---`), skip it and do not render it.
