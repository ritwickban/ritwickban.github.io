#!/usr/bin/env python3
"""
Optimize Studio photography and refresh gallery/quotes JSON plus studio-data.js
(for local file:// viewing without a web server).

Run from anywhere:
  python3 scripts/refresh-studio.py

Or from the site root:
  ./scripts/refresh-studio.sh
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "assets" / "img" / "png"
GALLERY_DIR = REPO_ROOT / "assets" / "img" / "optimized" / "gallery"
GALLERY_JSON = REPO_ROOT / "assets" / "gallery.json"
QUOTES_JSON = REPO_ROOT / "assets" / "quotes.json"
STUDIO_DATA_JS = REPO_ROOT / "assets" / "js" / "studio-data.js"

FEATURED = [
    "assets/img/optimized/me-7-1600.jpg",
    "assets/img/optimized/me-2-1600.jpg",
    "assets/img/optimized/me-1-1600.jpg",
]

MAX_EDGE = 1400
JPEG_QUALITY = 85
DEFAULT_ALT = "Photography by Ritwick Banerjee"
QUOTE_KINDS = frozenset({"original", "found"})


def sort_clicked(path: Path) -> int:
    match = re.search(r"Clicked\s*-\s*(\d+)", path.name, re.I)
    return int(match.group(1)) if match else 0


def find_clicked_sources() -> list[Path]:
    patterns = ("Clicked*.png", "Clicked*.jpg", "Clicked*.jpeg", "Clicked*.JPG", "Clicked*.PNG")
    files: list[Path] = []
    for pattern in patterns:
        files.extend(SRC_DIR.glob(pattern))
    return sorted({p.resolve() for p in files}, key=sort_clicked)


def optimize_gallery() -> list[str]:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit(
            "Pillow is required. Install with: pip3 install Pillow"
        ) from exc

    sources = find_clicked_sources()
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)

    for old in GALLERY_DIR.glob("clicked-*.jpg"):
        old.unlink()

    written: list[str] = []
    for index, src in enumerate(sources, start=1):
        out = GALLERY_DIR / f"clicked-{index:02d}.jpg"
        image = Image.open(src)
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        image.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        image.save(out, "JPEG", quality=JPEG_QUALITY, optimize=True)
        written.append(out.name)
        size_kb = out.stat().st_size / 1024
        print(f"  optimized {src.name} -> {out.name} ({size_kb:.0f} KB)")

    if not sources:
        print("  no Clicked* sources found in assets/img/png/")
    return written


def build_gallery(clicked_files: list[str]) -> list[dict[str, str]]:
    images: list[dict[str, str]] = []

    for rel in FEATURED:
        path = REPO_ROOT / rel
        if not path.is_file():
            print(f"  warning: featured image missing: {rel}", file=sys.stderr)
            continue
        images.append({"src": f"../{rel}", "alt": DEFAULT_ALT})

    for name in clicked_files:
        rel = f"assets/img/optimized/gallery/{name}"
        images.append({"src": f"../{rel}", "alt": DEFAULT_ALT})

    return images


def write_gallery_json(images: list[dict[str, str]]) -> int:
    GALLERY_JSON.write_text(json.dumps(images, indent=2) + "\n", encoding="utf-8")
    return len(images)


def refresh_quotes() -> list[dict]:
    if not QUOTES_JSON.is_file():
        QUOTES_JSON.write_text("[]\n", encoding="utf-8")
        print("  created empty assets/quotes.json")
        return []

    try:
        data = json.loads(QUOTES_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {QUOTES_JSON}: {exc}") from exc

    if not isinstance(data, list):
        raise SystemExit(f"{QUOTES_JSON} must be a JSON array of quote objects.")

    cleaned: list[dict] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            print(f"  warning: quote #{index} is not an object — skipped", file=sys.stderr)
            continue

        text = str(item.get("text", "")).strip()
        attribution = str(item.get("attribution", "Unknown")).strip() or "Unknown"
        kind = str(item.get("kind", "found")).strip().lower()

        if not text:
            print(f"  warning: quote #{index} has empty text — skipped", file=sys.stderr)
            continue
        if kind not in QUOTE_KINDS:
            print(
                f"  warning: quote #{index} has invalid kind '{kind}' — using 'found'",
                file=sys.stderr,
            )
            kind = "found"

        quote: dict[str, str] = {
            "text": text,
            "attribution": attribution,
            "kind": kind,
        }
        note = item.get("note")
        if note is not None and str(note).strip():
            quote["note"] = str(note).strip()

        cleaned.append(quote)

    QUOTES_JSON.write_text(json.dumps(cleaned, indent=2) + "\n", encoding="utf-8")
    return cleaned


def write_studio_data_js(quotes: list[dict], gallery: list[dict[str, str]]) -> None:
    STUDIO_DATA_JS.parent.mkdir(parents=True, exist_ok=True)
    payload = {"STUDIO_QUOTES": quotes, "STUDIO_GALLERY": gallery}
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    content = (
        "/* Generated by scripts/refresh-studio.py — do not edit by hand. */\n"
        "(function () {\n"
        f"  var data = {body};\n"
        "  window.STUDIO_QUOTES = data.STUDIO_QUOTES;\n"
        "  window.STUDIO_GALLERY = data.STUDIO_GALLERY;\n"
        "})();\n"
    )
    STUDIO_DATA_JS.write_text(content, encoding="utf-8")


def main() -> None:
    os.chdir(REPO_ROOT)
    print(f"Studio refresh ({REPO_ROOT.name})")
    print()

    print("1) Optimizing Clicked photos…")
    clicked = optimize_gallery()
    print(f"   {len(clicked)} image(s) in {GALLERY_DIR.relative_to(REPO_ROOT)}")
    print()

    print("2) Writing gallery.json…")
    gallery = build_gallery(clicked)
    gallery_count = write_gallery_json(gallery)
    print(f"   {gallery_count} entr(ies) -> {GALLERY_JSON.relative_to(REPO_ROOT)}")
    print()

    print("3) Refreshing quotes.json…")
    quotes = refresh_quotes()
    print(f"   {len(quotes)} quote(s) -> {QUOTES_JSON.relative_to(REPO_ROOT)}")
    print()

    print("4) Writing studio-data.js (for opening HTML files locally)…")
    write_studio_data_js(quotes, gallery)
    print(f"   -> {STUDIO_DATA_JS.relative_to(REPO_ROOT)}")
    print()
    print("Done. Hard-refresh the Studio page in your browser to see changes.")


if __name__ == "__main__":
    main()
