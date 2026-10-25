#!/usr/bin/env python3
"""Generate 800px WebP thumbnails for post covers.

List pages reference the variants via scripts/covers.js; article banners keep
the original files. Re-run after adding posts with covers.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
COVER_GLOB = "images/posts/*/cover.*"
THUMB_WIDTH = 800
QUALITY = 80


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    posts_dir = ROOT / "source" / "images" / "posts"
    generated, skipped = 0, 0
    for cover in sorted(posts_dir.glob("*/cover.*")):
        if cover.suffix.lower() == ".md":
            continue
        target = cover.with_name("cover-800.webp")
        with Image.open(cover) as raw:
            image = ImageOps.exif_transpose(raw).convert("RGB")
            if image.width <= THUMB_WIDTH:
                print(f"SKIP {cover.parent.name}: source not wider than {THUMB_WIDTH}px")
                skipped += 1
                continue
            height = round(image.height * THUMB_WIDTH / image.width)
            thumb = image.resize((THUMB_WIDTH, height), Image.Resampling.LANCZOS)
            thumb.save(target, "WEBP", quality=QUALITY, method=6)
        generated += 1
        print(f"OK   {cover.parent.name}: {cover.stat().st_size // 1000}KB -> {target.stat().st_size // 1000}KB")
    print(f"\nDone: {generated} generated, {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
