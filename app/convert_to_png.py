#!/usr/bin/env python3
"""
Convert SVG diagrams to PNG at 2x resolution (2400px wide).
Uses cairosvg for high-quality conversion.
"""

import os
import cairosvg
from pathlib import Path

OUTPUT_DIR = "/sessions/kind-tender-carson/mnt/app_architecture/diagrams"

# SVG dimensions -> PNG output widths
diagrams = [
    ("system_architecture.svg", 2400),
    ("ai_boundary.svg", 2400),
    ("scoring_funnel.svg", 2400),
    ("lock_decision_tree.svg", 2400),
    ("implementation_timeline.svg", 2400),
]

print("\n🎨 Converting SVGs to PNG (2x resolution)...\n")

for svg_file, output_width in diagrams:
    svg_path = os.path.join(OUTPUT_DIR, svg_file)
    png_file = svg_file.replace(".svg", ".png")
    png_path = os.path.join(OUTPUT_DIR, png_file)

    try:
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=output_width)
        # Get file size
        file_size = os.path.getsize(png_path) / 1024  # KB
        print(f"✓ {png_file:<40} ({file_size:.1f} KB)")
    except Exception as e:
        print(f"✗ {png_file:<40} ERROR: {e}")

print("\n✓ All conversions complete!\n")

# List all created files
print("📁 Created files:")
all_files = sorted(os.listdir(OUTPUT_DIR))
for f in all_files:
    if f.endswith(('.svg', '.png')):
        full_path = os.path.join(OUTPUT_DIR, f)
        size = os.path.getsize(full_path) / 1024
        print(f"   {f:<45} {size:>8.1f} KB")
