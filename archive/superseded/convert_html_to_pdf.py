#!/usr/bin/env python3
from xhtml2pdf import pisa
import sys

# Read HTML file
with open('handoffs/HANDOFF_08-03_S1.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Convert to PDF
with open('handoffs/HANDOFF_08-03_S1.pdf', 'w+b') as f:
    pisa.CreatePDF(html_content, dest=f)

print("PDF created successfully: handoffs/HANDOFF_08-03_S1.pdf")