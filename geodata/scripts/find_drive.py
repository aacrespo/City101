"""Auto-detect the shared drive path to swisstopo data.

Scans drive letters A:-Z: for 'Shared drives/City 101/Swisstopo'.
Falls back to SWISSTOPO_PATH environment variable if set.
"""

import os
import sys

SHARED_DRIVE_SUBPATH = os.path.join("Shared drives", "City 101", "Swisstopo")


def find_swisstopo_path():
    """Return the path to the swisstopo data folder.

    Resolution order:
    1. SWISSTOPO_PATH environment variable (explicit override)
    2. Auto-detect: scan drive letters for 'Shared drives/City 101/Swisstopo'
    """
    env_path = os.environ.get("SWISSTOPO_PATH")
    if env_path and os.path.isdir(env_path):
        return env_path

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        path = os.path.join(f"{letter}:\\", SHARED_DRIVE_SUBPATH)
        if os.path.isdir(path):
            return path

    raise FileNotFoundError(
        "Could not find swisstopo data.\n"
        "Options:\n"
        "  1. Mount Google Shared Drive 'City 101' (contains Swisstopo/ folder)\n"
        "  2. Set SWISSTOPO_PATH environment variable to your local copy\n"
        f"  Expected path: X:\\{SHARED_DRIVE_SUBPATH}"
    )


if __name__ == "__main__":
    try:
        path = find_swisstopo_path()
        print(f"Found swisstopo data at: {path}")
        # List key files
        files = os.listdir(path)
        tif_count = sum(1 for f in files if f.startswith("swissalti3d") and f.endswith(".tif"))
        img_count = sum(1 for f in files if f.startswith("swissimage") and f.endswith(".tif"))
        vrt_count = sum(1 for f in files if f.endswith(".vrt"))
        gdb_count = sum(1 for f in files if f.endswith(".gdb.zip"))
        print(f"  Terrain tiles (swissALTI3D): {tif_count}")
        print(f"  Imagery tiles (SWISSIMAGE):  {img_count}")
        print(f"  VRT mosaics:                 {vrt_count}")
        print(f"  Building databases (GDB):    {gdb_count}")
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
