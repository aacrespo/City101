"""Bundle city101_breathing.html into a standalone file with all data embedded.

Compresses buildings_polygons.geojson with gzip and embeds as base64.
Small files (meta, population, communes) are embedded as inline JSON.
Uses pako.js CDN for client-side decompression.

Output: city101_breathing_standalone.html (~8 MB)
"""
import gzip
import base64
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
HTML_IN = os.path.join(BASE, "city101_breathing.html")
HTML_OUT = os.path.join(BASE, "city101_breathing_standalone.html")

def main():
    print("=== Bundling standalone HTML ===")

    # Read source HTML
    with open(HTML_IN, "r", encoding="utf-8") as f:
        html = f.read()

    # Read small data files as JSON
    print("Reading small data files...")
    with open(os.path.join(DATA, "building_meta.json"), "r", encoding="utf-8") as f:
        meta_json = f.read().strip()
    with open(os.path.join(DATA, "population_24h.json"), "r", encoding="utf-8") as f:
        pop_json = f.read().strip()
    with open(os.path.join(DATA, "communes.geojson"), "r", encoding="utf-8") as f:
        communes_json = f.read().strip()

    # Compress large GeoJSON
    print("Compressing buildings_polygons.geojson...")
    with open(os.path.join(DATA, "buildings_polygons.geojson"), "rb") as f:
        raw = f.read()
    compressed = gzip.compress(raw, compresslevel=9)
    b64 = base64.b64encode(compressed).decode("ascii")
    print(f"  Raw: {len(raw)/1024/1024:.1f} MB -> Base64(gzip): {len(b64)/1024/1024:.1f} MB")

    # Add pako.js CDN to <head>
    html = html.replace(
        '<script src="https://unpkg.com/maplibre-gl@4.5.0/dist/maplibre-gl.js"></script>',
        '<script src="https://unpkg.com/maplibre-gl@4.5.0/dist/maplibre-gl.js"></script>\n'
        '<script src="https://unpkg.com/pako@2.1.0/dist/pako.min.js"></script>'
    )

    # Build embedded data block
    embedded_data = f"""
// ─── EMBEDDED DATA (standalone mode) ───
const __EMBEDDED_META = {meta_json};
const __EMBEDDED_POP = {pop_json};
const __EMBEDDED_COMMUNES = {communes_json};
const __EMBEDDED_BUILDINGS_B64GZ = "{b64}";

function __decompressB64Gz(b64str) {{
  const bin = atob(b64str);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  const decompressed = pako.inflate(bytes, {{ to: 'string' }});
  return JSON.parse(decompressed);
}}
"""

    # Replace the loadAll function to use embedded data
    new_load_all = """async function loadAll(){
  document.getElementById('loadMsg').textContent = 'Decompressing building data...';
  // Small data is already inline
  buildingMeta = __EMBEDDED_META;
  pop24h = __EMBEDDED_POP;
  curvesArray = buildingMeta.curve_keys.map(k => buildingMeta.curves[k]);

  // Decompress buildings GeoJSON from embedded gzipped base64
  await new Promise(r => setTimeout(r, 50)); // Let UI update
  buildingsGeoJSON = __decompressB64Gz(__EMBEDDED_BUILDINGS_B64GZ);
  document.getElementById('loadMsg').textContent = 'Rendering ' + buildingsGeoJSON.features.length.toLocaleString() + ' buildings...';
  await new Promise(r => setTimeout(r, 50));
}"""

    # Replace the loadAll function in the HTML
    # Match from "async function loadAll(){" to the closing "}"
    html = re.sub(
        r'async function loadAll\(\)\{.*?\n\}',
        new_load_all,
        html,
        flags=re.DOTALL
    )

    # Replace commune data source from file to inline
    html = html.replace(
        "map.addSource('communes', {type: 'geojson', data: 'data/communes.geojson'});",
        "map.addSource('communes', {type: 'geojson', data: __EMBEDDED_COMMUNES});"
    )

    # Inject embedded data block right after 'use strict';
    html = html.replace(
        "'use strict';",
        "'use strict';\n" + embedded_data
    )

    # Write output
    print(f"Writing standalone HTML...")
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html)

    fsize = os.path.getsize(HTML_OUT)
    print(f"\nDone! {HTML_OUT}")
    print(f"File size: {fsize/1024/1024:.1f} MB")
    print("Open directly in browser — no server needed.")

if __name__ == "__main__":
    main()
