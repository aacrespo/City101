#!/usr/bin/env python3
"""
Convert a folder of sequential PNG frames to an animated GIF.

Usage:
    python3 tools/export/png_to_gif.py <input_folder> [options]

Examples:
    python3 tools/export/png_to_gif.py output/kitchen_animation/renders/cairn/idle/
    python3 tools/export/png_to_gif.py output/kitchen_animation/renders/cairn/walk/ --fps 12 --scale 0.5
    python3 tools/export/png_to_gif.py output/kitchen_animation/renders/ --all --fps 10

Options:
    --fps N         Frames per second (default: 10)
    --scale F       Scale factor 0.0-1.0 (default: 1.0, no resize)
    --loop N        Loop count: 0=infinite (default: 0)
    --output PATH   Output GIF path (default: <input_folder>.gif)
    --all           Process all subfolders as separate animations
    --bounce        Ping-pong: play forward then reverse (good for idle, thinking)

Requires Pillow: pip install Pillow
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    print("  Or in a venv: python3 -m venv .venv && source .venv/bin/activate && pip install Pillow")
    sys.exit(1)


def frames_from_folder(folder: Path) -> list[Path]:
    """Get sorted PNG frames from a folder."""
    pngs = sorted(folder.glob("*.png"))
    if not pngs:
        pngs = sorted(folder.glob("frame_*.png"))
    return pngs


def make_gif(
    frame_paths: list[Path],
    output_path: Path,
    fps: int = 10,
    scale: float = 1.0,
    loop: int = 0,
    bounce: bool = False,
):
    """Create an animated GIF from a list of PNG frame paths."""
    if not frame_paths:
        print(f"  No frames found, skipping.")
        return False

    frames = []
    for p in frame_paths:
        img = Image.open(p).convert("RGBA")
        if scale != 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.Resampling.NEAREST)  # pixel art = nearest neighbor
        frames.append(img)

    if bounce and len(frames) > 2:
        frames = frames + frames[-2:0:-1]  # forward + reverse (skip first/last dupe)

    duration_ms = int(1000 / fps)

    # For transparent GIFs, we need to handle the alpha channel
    # Convert RGBA to P (palette) mode with transparency
    output_frames = []
    for frame in frames:
        # Create a new image with a transparent background
        bg = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        bg.paste(frame, (0, 0), frame)
        # Convert to P mode for GIF
        converted = bg.convert("P", palette=Image.Palette.ADAPTIVE, colors=255)
        # Set transparency for the most common background color
        output_frames.append(converted)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_frames[0].save(
        output_path,
        save_all=True,
        append_images=output_frames[1:],
        duration=duration_ms,
        loop=loop,
        transparency=0,
        disposal=2,  # restore to background between frames
    )

    size_kb = output_path.stat().st_size / 1024
    print(f"  ✓ {output_path.name}: {len(frame_paths)} frames → {len(output_frames)} frames (bounce={bounce}), {size_kb:.0f}KB")
    return True


def process_folder(folder: Path, args):
    """Process a single folder of frames."""
    frames = frames_from_folder(folder)
    if not frames:
        return False

    if args.output:
        out = Path(args.output)
    else:
        out = folder.parent / f"{folder.name}.gif"

    print(f"Processing: {folder.name} ({len(frames)} frames)")
    return make_gif(frames, out, fps=args.fps, scale=args.scale, loop=args.loop, bounce=args.bounce)


def process_all(root: Path, args):
    """Process all subfolders under root."""
    count = 0
    for subfolder in sorted(root.iterdir()):
        if subfolder.is_dir():
            frames = frames_from_folder(subfolder)
            if frames:
                out = root / f"{subfolder.name}.gif"
                print(f"Processing: {subfolder.name} ({len(frames)} frames)")
                if make_gif(frames, out, fps=args.fps, scale=args.scale, loop=args.loop, bounce=args.bounce):
                    count += 1
    print(f"\nDone: {count} GIFs created in {root}")


def main():
    parser = argparse.ArgumentParser(description="Convert PNG sequences to animated GIFs")
    parser.add_argument("input", help="Input folder with PNG frames (or parent folder with --all)")
    parser.add_argument("--fps", type=int, default=10, help="Frames per second (default: 10)")
    parser.add_argument("--scale", type=float, default=1.0, help="Scale factor (default: 1.0)")
    parser.add_argument("--loop", type=int, default=0, help="Loop count, 0=infinite (default: 0)")
    parser.add_argument("--output", "-o", help="Output GIF path")
    parser.add_argument("--all", action="store_true", help="Process all subfolders")
    parser.add_argument("--bounce", action="store_true", help="Ping-pong animation (forward+reverse)")
    args = parser.parse_args()

    folder = Path(args.input)
    if not folder.exists():
        print(f"ERROR: {folder} does not exist")
        sys.exit(1)

    if args.all:
        process_all(folder, args)
    else:
        process_folder(folder, args)


if __name__ == "__main__":
    main()
