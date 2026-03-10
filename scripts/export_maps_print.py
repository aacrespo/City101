"""
City101 — Re-export Print Maps (PNGs + PDFs)
=============================================
Run this script inside QGIS Python console, OR via the QGIS MCP plugin.

It exports all 7 A02_MAP layouts as:
  - PNG at 150 DPI → visualizations/site/maps/
  - PDF at 300 DPI → visualizations/site/maps/print/

Prerequisites:
  - CITY101_WORKING.qgz must be open (page backgrounds already set to #0a0a0f)
"""

import os
from qgis.core import (
    QgsProject, QgsLayoutExporter
)

project = QgsProject.instance()
manager = project.layoutManager()

# Output directories
base_dir = os.path.dirname(project.fileName())
png_dir = os.path.join(base_dir, 'visualizations', 'site', 'maps')
pdf_dir = os.path.join(base_dir, 'visualizations', 'site', 'maps', 'print')
os.makedirs(png_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)

# Layout name → filename mapping
layout_map = {
    'A02_MAP1_Working_Continuity_Index': 'map1_wci',
    'A02_MAP2_Remote_Work_Infrastructure': 'map2_remote_work',
    'A02_MAP3_Lavaux_Fracture': 'map3_lavaux',
    'A02_MAP4_Geneva_Pole': 'map4_geneva',
    'A02_MAP5_Lausanne_Pole': 'map5_lausanne',
    'A02_MAP6_Transit_Backbone': 'map6_transit',
    'A02_MAP7_Data_Synchronicity': 'map7_synchronicity',
}

results = []

for layout_name, filename in layout_map.items():
    layout = manager.layoutByName(layout_name)
    if layout is None:
        results.append(f"SKIP {layout_name}: not found")
        continue

    exporter = QgsLayoutExporter(layout)

    # PNG export (150 DPI)
    png_path = os.path.join(png_dir, f'{filename}.png')
    png_settings = QgsLayoutExporter.ImageExportSettings()
    png_settings.dpi = 150
    res = exporter.exportToImage(png_path, png_settings)
    if res == QgsLayoutExporter.Success:
        size_mb = os.path.getsize(png_path) / (1024 * 1024)
        results.append(f"OK  PNG {filename}.png ({size_mb:.1f} MB)")
    else:
        results.append(f"ERR PNG {filename}.png (code {res})")

    # PDF export (300 DPI)
    pdf_path = os.path.join(pdf_dir, f'{filename}.pdf')
    pdf_settings = QgsLayoutExporter.PdfExportSettings()
    pdf_settings.dpi = 300
    res = exporter.exportToPdf(pdf_path, pdf_settings)
    if res == QgsLayoutExporter.Success:
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        results.append(f"OK  PDF {filename}.pdf ({size_mb:.1f} MB)")
    else:
        results.append(f"ERR PDF {filename}.pdf (code {res})")

print("\n=== Export Results ===")
for r in results:
    print(r)
print(f"\nPNG dir: {png_dir}")
print(f"PDF dir: {pdf_dir}")
