#!/usr/bin/env python3
"""City101 design system reference for web maps.

Prints the standard configuration for Leaflet/Folium maps.
Use as a reference when building maps — copy the relevant snippets.

Usage:
    python tools/maps/apply_design_system.py
    python tools/maps/apply_design_system.py --css    # CSS variables only
    python tools/maps/apply_design_system.py --tiles   # Tile URL only
"""

import argparse

DESIGN = {
    "tiles": {
        "url": "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        "attribution": '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
        "name": "CartoDB Dark Matter",
    },
    "colors": {
        "background": "#0a0a0f",
        "accent": "#c9a84c",
        "text_primary": "#e8e6e1",
        "text_muted": "#8a8880",
        "data_layer": "#ffffff",
    },
    "fonts": {
        "display": "'Instrument Serif', serif",
        "body": "'DM Sans', sans-serif",
        "mono": "'DM Mono', monospace",
    },
    "css_variables": """
:root {
  --chrome-bg: #0a0a0f;
  --chrome-text: #e8e6e1;
  --chrome-accent: #c9a84c;
  --chrome-muted: #8a8880;
  --font-display: 'Instrument Serif', serif;
  --font-body: 'DM Sans', sans-serif;
  --font-mono: 'DM Mono', monospace;
}
""".strip(),
    "google_fonts_import": "@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400&family=DM+Sans:wght@400;500;700&family=Instrument+Serif&display=swap');",
}


def main():
    parser = argparse.ArgumentParser(description="City101 design system reference")
    parser.add_argument("--css", action="store_true", help="Print CSS variables only")
    parser.add_argument("--tiles", action="store_true", help="Print tile URL only")
    args = parser.parse_args()

    if args.css:
        print(DESIGN["css_variables"])
        return

    if args.tiles:
        print(DESIGN["tiles"]["url"])
        return

    print("City101 Design System — Web Maps")
    print("=" * 50)
    print()
    print(f"Basemap: {DESIGN['tiles']['name']}")
    print(f"  URL: {DESIGN['tiles']['url']}")
    print()
    print("Colors:")
    for name, hex_val in DESIGN["colors"].items():
        print(f"  {name}: {hex_val}")
    print()
    print("Fonts:")
    for role, font in DESIGN["fonts"].items():
        print(f"  {role}: {font}")
    print()
    print("Google Fonts import:")
    print(f"  {DESIGN['google_fonts_import']}")
    print()
    print("CSS Variables:")
    print(DESIGN["css_variables"])


if __name__ == "__main__":
    main()
