#!/usr/bin/env python3
"""Validate the generated pack. Run by CI, useful locally before a release.

    python3 scripts/check_icons.py
"""

import json
import re
import sys
import xml.dom.minidom
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "svg"
# Per-layer size ceilings, set ~25% above what each layer actually ships today.
# The point is to catch a regression — an icon that suddenly doubles — not to
# argue with the artwork: a full body with a prop is fairly meant to outweigh a
# 24px UI glyph.
BUDGET = {
    "actions": 4_000,
    "badges": 500,
    "bodies": 11_250,
    "characters": 3_250,
    "extras": 4_500,
    "frames": 3_250,
    "jobs": 12_000,
    "paws": 7_250,
    "status": 3_250,
    "ui": 1_500,
}

failures: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def main() -> int:
    manifest = json.loads((ROOT / "icons.json").read_text())
    files = sorted(SVG_DIR.rglob("*.svg"))

    # 1. every file is well-formed XML
    for f in files:
        try:
            xml.dom.minidom.parse(str(f))
        except Exception as exc:  # noqa: BLE001 — report whatever the parser says
            fail(f"{f.relative_to(ROOT)} is not valid XML: {exc}")

    # 2. the manifest agrees with what is on disk
    if manifest["total"] != len(files):
        fail(f'icons.json says {manifest["total"]} icons, svg/ holds {len(files)}')
    for layer, expected in manifest["counts"].items():
        found = len(list((SVG_DIR / layer).glob("*.svg")))
        if found != expected:
            fail(f"layer {layer}: manifest says {expected}, found {found}")

    # 3. the UI layer stays themeable — no baked-in colours (SPEC part 5)
    for f in sorted((SVG_DIR / "ui").glob("*.svg")):
        if re.search(r"#[0-9A-Fa-f]{3,6}\b", f.read_text()):
            fail(f"{f.relative_to(ROOT)} hardcodes a colour; the ui layer must use currentColor")

    # 4. every icon carries a title, so screen readers have something to say
    for f in files:
        if "<title" not in f.read_text():
            fail(f"{f.relative_to(ROOT)} has no <title>")

    # 5. per-layer size budget
    for layer, cap in BUDGET.items():
        sizes = [(f, f.stat().st_size) for f in (SVG_DIR / layer).glob("*.svg")]
        for f, size in sizes:
            if size > cap:
                fail(f"{f.relative_to(ROOT)} is {size} B, over the {cap} B budget for {layer}/")
        if sizes:
            worst = max(sizes, key=lambda x: x[1])
            notes.append(f"{layer}/ largest {worst[1]} B of {cap} B "
                         f"({worst[0].name})")
    unbudgeted = {d.name for d in SVG_DIR.iterdir() if d.is_dir()} - set(BUDGET)
    for layer in sorted(unbudgeted):
        fail(f"layer {layer}/ has no size budget — add one to BUDGET in this script")

    for note in notes:
        print(f"note: {note}")
    if failures:
        print(f"\n{len(failures)} problem(s):", file=sys.stderr)
        for msg in failures[:40]:
            print(f"  - {msg}", file=sys.stderr)
        if len(failures) > 40:
            print(f"  ... and {len(failures) - 40} more", file=sys.stderr)
        return 1

    print(f"ok — {len(files)} icons, {len(manifest['counts'])} layers, all valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
