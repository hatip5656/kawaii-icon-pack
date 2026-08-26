#!/usr/bin/env python3
"""Render every icon into one grid SVG, for eyeballing the whole set at once.

    python3 scripts/contact_sheet.py            all faces
    python3 scripts/contact_sheet.py rabbit     one animal
    python3 scripts/contact_sheet.py status     badges + composed avatars
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "svg"
OUT = ROOT / "preview" / "contact-sheet.svg"

CELL = 128
PAD = 8


def uniquify(svg: str, suffix: str) -> str:
    """Namespace ids so many icons can live in one document."""
    for ident in set(re.findall(r'id="([^"]+)"', svg)):
        new = f"{ident}-{suffix}"
        svg = svg.replace(f'id="{ident}"', f'id="{new}"')
        svg = svg.replace(f"url(#{ident})", f"url(#{new})")
        svg = svg.replace(f'href="#{ident}"', f'href="#{new}"')
        svg = svg.replace(f'aria-labelledby="{ident}"', f'aria-labelledby="{new}"')
    return svg


def cell(path: Path, index: int, col: int, row: int) -> str:
    svg = uniquify(path.read_text().strip(), str(index))
    svg = re.sub(r'\swidth="\d+"\sheight="\d+"', "", svg, count=1)
    svg = svg.replace(
        "<svg ",
        f'<svg x="{col * CELL + PAD}" y="{row * CELL + PAD}" width="{CELL - 2 * PAD}" '
        f'height="{CELL - 2 * PAD}" ',
        1,
    )
    return svg


def main() -> None:
    what = sys.argv[1] if len(sys.argv) > 1 else "faces"
    if what == "status":
        files = sorted((SVG_DIR / "badges").glob("*.svg")) + sorted((SVG_DIR / "status").glob("*.svg"))
        cols = 10
    elif (SVG_DIR / what).is_dir():
        files = sorted((SVG_DIR / what).glob("*.svg"))
        cols = 12 if len(files) > 60 else 7
    else:
        files = sorted((SVG_DIR / "characters").glob("*.svg"))
        cols = 14

    rows = (len(files) + cols - 1) // cols
    cells = [cell(p, i, i % cols, i // cols) for i, p in enumerate(files)]
    w, h = cols * CELL, rows * CELL
    side = max(w, h)  # square output: Quick Look crops non-square SVGs instead of scaling
    OUT.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{side}" height="{side}" '
        f'viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">\n'
        f'<rect width="100%" height="100%" fill="#FFFCF8"/>\n' + "\n".join(cells) + "\n</svg>\n"
    )
    print(f"{len(files)} icons -> {OUT.relative_to(ROOT)} ({cols}x{rows})")


if __name__ == "__main__":
    main()
