#!/usr/bin/env python3
"""Generate the Kawaii Animals icon pack.

Every icon is composed from three layers:

    base        per-animal ears / head / markings (hand-tuned, in ANIMALS)
    expression  eyes + mouth + extras, placed on the animal's anchors
    badge       optional status badge in the bottom-right corner

    python3 scripts/build_icons.py                    rebuild svg/
    python3 scripts/build_icons.py rabbit sleepy away  print one composed icon
"""

import json
import math
import shutil
import sys
from pathlib import Path

from animal_paws import GESTURE_LABELS, GESTURE_ORDER
from animal_paws import PALETTE as PAW_PALETTE
from animal_paws import render as render_paw
from animal_bodies import BODY, POSE_LABELS, POSE_ORDER, pose as body_pose
from animal_jobs import JOB_LABELS, JOB_ORDER, outfit
from animal_actions import ACTION_LABELS, ACTION_ORDER, prop
from animal_actions import body as action_body
from animal_extras import ACCESSORY_LABELS, ACCESSORY_ORDER, SNACKS, SNACK_LABEL, accessory
from outline import INKS, sticker
from ui_icons import FACES, UI_ICONS, groups
from ui_icons import render as render_ui

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "svg"
WHITE = "#FFFFFF"

# a head tilt applied to the entire drawing, layers included
TILT = {"owl": -7}

# sticker keyline, in output px: a face alone, and a face inside a composition
OUTLINE_FACE = 6
OUTLINE_SCENE = 4.5


def _ink(animal):
    return ANIMALS[animal]["ink"]


def _inset(art, s=0.94):
    """Pull a sticker in from the canvas edge so the keyline is never clipped."""
    o = 128 * (1 - s)
    return f'<g transform="translate({o:g},{o:g}) scale({s:g})">{art}</g>'


# ---------------------------------------------------------------- animals

ANIMALS = {
    # bright orange, dark russet ears and limbs, white muzzle, cheek patches and brow spots
    "red_panda": {
        "ink": "#5A2412",
        "label": "Red panda",
        "line": "#5A2412",
        "over_eye": "#5A2412",
        "eye": {"style": "dot", "cx": (94, 162), "cy": 122, "rx": 11, "ry": 13, "ink": "#2E1610"},
        "brow_dy": 28, "brow_w": 15,
        "mouth_kind": "line", "mouth_y": 186, "mouth_w": 15, "mouth_sw": 5,
        "nose": '<path d="M116 160a12 7.5 0 0 1 24 0c0 5.5-5.5 11-12 15-6.5-4-12-9.5-12-15z" fill="#2E1610"/>',
        "teeth": None,
        "blush": {"cx": (70, 186), "cy": 150, "rx": 12, "ry": 7.5, "fill": "#F4737F", "opacity": 0.4},
        "behind": """  <path d="M78 208C40 208 18 184 18 154" fill="none" stroke="#F28A2E" stroke-width="34" stroke-linecap="round"/>
  <path d="M78 208C40 208 18 184 18 154" fill="none" stroke="#7A2E1C" stroke-width="34" stroke-dasharray="13 25" stroke-dashoffset="20"/>""",
        "base": """  <ellipse cx="62" cy="76" rx="35" ry="34" fill="#7A2E1C"/>
  <ellipse cx="64" cy="80" rx="21" ry="20" fill="#F6B9A8"/>
  <ellipse cx="194" cy="76" rx="35" ry="34" fill="#7A2E1C"/>
  <ellipse cx="192" cy="80" rx="21" ry="20" fill="#F6B9A8"/>
  <ellipse cx="128" cy="140" rx="86" ry="78" fill="#F28A2E"/>
  <defs><clipPath id="clip-red_panda"><ellipse cx="128" cy="140" rx="86" ry="78"/></clipPath></defs>
  <g clip-path="url(#clip-red_panda)">
    <ellipse cx="98" cy="88" rx="11" ry="8" fill="#FFF8F0"/>
    <ellipse cx="158" cy="88" rx="11" ry="8" fill="#FFF8F0"/>
    <ellipse cx="56" cy="168" rx="24" ry="28" fill="#FFF8F0"/>
    <ellipse cx="200" cy="168" rx="24" ry="28" fill="#FFF8F0"/>
    <ellipse cx="128" cy="178" rx="34" ry="28" fill="#FFF8F0"/>
  </g>""",
    },
    # white head and body, long ears with peach lining, peach limbs, lashes
    "rabbit": {
        "ink": "#6B5250",
        "label": "Rabbit",
        "line": "#6B5250",
        "over_eye": "#6B5250",
        "eye": {"style": "dot", "cx": (102, 154), "cy": 142, "rx": 10, "ry": 12.5, "ink": "#2A2226",
                "lashes": True},
        "brow_dy": 26, "brow_w": 14,
        "mouth_kind": "line", "mouth_y": 182, "mouth_w": 13, "mouth_sw": 4.5,
        "nose": '<path d="M119 164a9 6 0 0 1 18 0c0 4-4 8-9 11-5-3-9-7-9-11z" fill="#E8949A"/>'
                '<path d="M128 175v7" stroke="#6B5250" stroke-width="4" stroke-linecap="round"/>',
        "teeth": None,
        "blush": {"cx": (74, 182), "cy": 166, "rx": 13, "ry": 8, "fill": "#FF8FA9", "opacity": 0.45},
        "base": """  <g transform="rotate(-12 106 70)">
    <rect x="84" y="4" width="44" height="116" rx="22" fill="#FFFDFB"/>
    <rect x="96" y="18" width="20" height="88" rx="10" fill="#F8C4A8"/>
  </g>
  <g transform="rotate(12 150 70)">
    <rect x="128" y="4" width="44" height="116" rx="22" fill="#FFFDFB"/>
    <rect x="140" y="18" width="20" height="88" rx="10" fill="#F8C4A8"/>
  </g>
  <ellipse cx="128" cy="152" rx="72" ry="68" fill="#FFFDFB"/>""",
    },
    "panda": {
        "ink": "#2E282A",
        "label": "Panda",
        "line": "#3A3335",
        "over_eye": WHITE,
        "eye": {"style": "patch", "cx": (97, 159), "cy": 138, "r": 12, "pr": 7, "ink": "#3A3335"},
        "brow_dy": 20, "brow_w": 12,
        "mouth_kind": "line", "mouth_y": 185, "mouth_w": 16, "mouth_sw": 5,
        "nose": '<path d="M114 162a14 8 0 0 1 28 0c0 6-6 12-14 17-8-5-14-11-14-17z" fill="#3A3335"/>',
        "teeth": None,
        "blush": {"cx": (70, 186), "cy": 168, "rx": 14, "ry": 8.5, "fill": "#FF8FA9", "opacity": 0.45},
        "base": """  <circle cx="60" cy="80" r="32" fill="#2F2A2C"/>
  <circle cx="196" cy="80" r="32" fill="#2F2A2C"/>
  <ellipse cx="128" cy="146" rx="87" ry="79" fill="#FFFFFF"/>
  <ellipse cx="94" cy="136" rx="25" ry="30" fill="#2F2A2C" transform="rotate(-18 94 136)"/>
  <ellipse cx="162" cy="136" rx="25" ry="30" fill="#2F2A2C" transform="rotate(18 162 136)"/>""",
    },
    # grey-taupe round body, white cheeks and muzzle, peach ear linings, pink stitched mouth
    "hamster": {
        "ink": "#4A3E38",
        "label": "Hamster",
        "line": "#C9708A",
        "over_eye": "#4A3E38",
        "eye": {"style": "dot", "cx": (98, 158), "cy": 126, "rx": 12, "ry": 14, "ink": "#161214"},
        "brow_dy": 26, "brow_w": 16,
        "mouth_kind": "line", "mouth_y": 173, "mouth_w": 13, "mouth_sw": 4.5,
        "nose": '<path d="M120 154a8 5 0 0 1 16 0c0 4-4 7-8 10-4-3-8-6-8-10z" fill="#E8798C"/>',
        "teeth": None,
        "blush": {"cx": (70, 186), "cy": 156, "rx": 14, "ry": 8.5, "fill": "#F4737F", "opacity": 0.38},
        "base": """  <circle cx="74" cy="72" r="24" fill="#8F847D"/>
  <circle cx="75" cy="74" r="13" fill="#F4A48C"/>
  <circle cx="182" cy="72" r="24" fill="#8F847D"/>
  <circle cx="181" cy="74" r="13" fill="#F4A48C"/>
  <circle cx="54" cy="162" r="32" fill="#9A8F88"/>
  <circle cx="202" cy="162" r="32" fill="#9A8F88"/>
  <ellipse cx="128" cy="142" rx="84" ry="76" fill="#9A8F88"/>
  <defs><clipPath id="clip-hamster"><ellipse cx="128" cy="142" rx="84" ry="76"/></clipPath></defs>
  <g clip-path="url(#clip-hamster)">
    <ellipse cx="128" cy="184" rx="70" ry="44" fill="#FFFFFF"/>
  </g>
  <ellipse cx="56" cy="170" rx="27" ry="22" fill="#FFFFFF"/>
  <ellipse cx="200" cy="170" rx="27" ry="22" fill="#FFFFFF"/>""",
    },
    # grey, dark brown mask with white brows over it, white muzzle and ear linings
    "raccoon": {
        "ink": "#3A2C26",
        "label": "Raccoon",
        "line": "#3A2C26",
        "over_eye": "#FFFFFF",
        "eye": {"style": "patch", "cx": (94, 162), "cy": 128, "r": 11.5, "pr": 6.5, "ink": "#1E1614"},
        "brow_dy": 22, "brow_w": 14,
        "mouth_kind": "line", "mouth_y": 185, "mouth_w": 15, "mouth_sw": 5,
        "nose": '<path d="M114 160a14 8 0 0 1 28 0c0 6-6 12-14 17-8-5-14-11-14-17z" fill="#1E1614"/>',
        "teeth": None,
        "blush": {"cx": (70, 186), "cy": 176, "rx": 13, "ry": 8, "fill": "#FF8FA9", "opacity": 0.35},
        "behind": """  <path d="M78 208C40 208 18 184 18 154" fill="none" stroke="#A9AAB0" stroke-width="34" stroke-linecap="round"/>
  <path d="M78 208C40 208 18 184 18 154" fill="none" stroke="#4A3428" stroke-width="34" stroke-dasharray="13 25" stroke-dashoffset="20"/>""",
        "base": """  <path d="M40 104 52 44l52 22z" fill="#A9AAB0" stroke="#A9AAB0" stroke-width="16" stroke-linejoin="round"/>
  <path d="M56 86 62 58l24 12z" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>
  <path d="M216 104 204 44l-52 22z" fill="#A9AAB0" stroke="#A9AAB0" stroke-width="16" stroke-linejoin="round"/>
  <path d="M200 86 194 58l-24 12z" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>
  <ellipse cx="44" cy="160" rx="22" ry="20" fill="#FFFFFF"/>
  <ellipse cx="212" cy="160" rx="22" ry="20" fill="#FFFFFF"/>
  <ellipse cx="128" cy="140" rx="86" ry="78" fill="#A9AAB0"/>
  <defs><clipPath id="clip-raccoon"><ellipse cx="128" cy="140" rx="86" ry="78"/></clipPath></defs>
  <g clip-path="url(#clip-raccoon)">
    <ellipse cx="86" cy="100" rx="40" ry="16" fill="#FFFFFF" transform="rotate(-14 86 100)"/>
    <ellipse cx="170" cy="100" rx="40" ry="16" fill="#FFFFFF" transform="rotate(14 170 100)"/>
    <ellipse cx="94" cy="128" rx="34" ry="26" fill="#4A3428" transform="rotate(-10 94 128)"/>
    <ellipse cx="162" cy="128" rx="34" ry="26" fill="#4A3428" transform="rotate(10 162 128)"/>
    <ellipse cx="128" cy="178" rx="40" ry="30" fill="#FFFFFF"/>
  </g>""",
    },
    # grey, white facial discs and belly, dark tufts, yellow eyes, grey beak
    "owl": {
        "ink": "#45434B",
        "label": "Owl",
        "line": "#6E6A72",
        "over_eye": "#3A3335",
        "eye": {"style": "owl", "cx": (98, 158), "cy": 138, "r": 19, "ink": "#161214"},
        "brow_dy": 30, "brow_w": 20,
        "mouth_kind": "beak", "mouth_y": 166, "mouth_w": 15, "mouth_sw": 5,
        "nose": None,
        "teeth": None,
        "blush": {"cx": (82, 174), "cy": 168, "rx": 11, "ry": 7, "fill": "#F4737F", "opacity": 0.5},
        "base": """  <ellipse cx="54" cy="176" rx="20" ry="34" transform="rotate(14 54 176)" fill="#969BA3"/>
  <ellipse cx="202" cy="176" rx="20" ry="34" transform="rotate(-14 202 176)" fill="#969BA3"/>
  <ellipse cx="80" cy="76" rx="12" ry="28" transform="rotate(-48 80 76)" fill="#6E6A72"/>
  <ellipse cx="176" cy="76" rx="12" ry="28" transform="rotate(48 176 76)" fill="#6E6A72"/>
  <ellipse cx="128" cy="144" rx="84" ry="80" fill="#A9AEB5"/>
  <defs><clipPath id="clip-owl"><ellipse cx="128" cy="144" rx="84" ry="80"/></clipPath></defs>
  <g clip-path="url(#clip-owl)">
    <ellipse cx="128" cy="214" rx="50" ry="32" fill="#FFFFFF"/>
    <path d="M110 206q6-5 12 0M134 206q6-5 12 0M122 218q6-5 12 0" fill="none" stroke="#A9AEB5" stroke-width="4" stroke-linecap="round"/>
  </g>
  <circle cx="96" cy="140" r="36" fill="#FFFFFF"/>
  <circle cx="160" cy="140" r="36" fill="#FFFFFF"/>""",
    },
}


# ------------------------------------------------------------------- eyes

def _eye_open(a, cx, cy, scale=1.0):
    e = a["eye"]
    ink = e["ink"]
    if e["style"] == "patch":
        r, pr = e["r"] * scale, e["pr"] * scale
        inward = 1 if cx < 128 else -1
        return (f'<circle cx="{cx}" cy="{cy}" r="{r:g}" fill="{WHITE}"/>'
                f'<circle cx="{cx + inward}" cy="{cy + 1}" r="{pr:g}" fill="{ink}"/>'
                f'<circle cx="{cx - 3}" cy="{cy - 4}" r="{pr * 0.4:g}" fill="{WHITE}"/>')
    if e["style"] == "owl":
        r = e["r"] * scale
        return (f'<circle cx="{cx}" cy="{cy}" r="{r:g}" fill="#F2B630"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r * 0.7:.1f}" fill="{ink}"/>'
                f'<circle cx="{cx - 4}" cy="{cy - 5}" r="{r * 0.24:.1f}" fill="{WHITE}"/>'
                f'<circle cx="{cx + 4}" cy="{cy + 5}" r="{r * 0.1:.1f}" fill="{WHITE}"/>')
    if e["style"] == "big":
        r = e["r"] * scale
        return (f'<circle cx="{cx}" cy="{cy}" r="{r:g}" fill="{ink}"/>'
                f'<circle cx="{cx - 6}" cy="{cy - 6}" r="{r * 0.33:g}" fill="{WHITE}" opacity="0.95"/>'
                f'<circle cx="{cx + 5}" cy="{cy + 7}" r="{r * 0.17:g}" fill="{WHITE}" opacity="0.7"/>')
    rx, ry = e["rx"] * scale, e["ry"] * scale
    lashes = ""
    if e.get("lashes"):
        out = -1 if cx < 128 else 1
        lashes = "".join(
            f'<path d="M{cx + out * rx * 0.55:.1f} {cy - ry * 0.75:.1f}l{out * dx:g} {dy:g}" '
            f'stroke="{ink}" stroke-width="3.2" stroke-linecap="round"/>'
            for dx, dy in ((7, -6), (9, 0)))
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx:g}" ry="{ry:g}" fill="{ink}"/>'
            f'<circle cx="{cx - 4}" cy="{cy - 5}" r="{rx * 0.36:g}" fill="{WHITE}" opacity="0.95"/>'
            + lashes)


# glitter ring for the big "sparkly" eyes — one colour per character
SPARKLE_RING = {
    "red_panda": ("#2FB5A8", "#9BEBE2"), "rabbit": ("#F27BA6", "#FFD0E1"),
    "panda": ("#3E8FD8", "#AFDCFF"), "hamster": ("#4DB37A", "#B8F0CC"),
    "raccoon": ("#C9952E", "#FFE29A"), "owl": ("#F2B630", "#FFE7A0"),
}


def _eye_sparkly(a, key, cx, cy, R):
    """Oversized glossy eye: glitter ring, deep pupil, two catchlights and a gloss arc."""
    ring, glint = SPARKLE_RING[key]
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R:g}" fill="{ring}"/>']
    # glitter: light and dark flecks scattered round the ring
    for i in range(14):
        ang = math.radians(i * 360 / 14 + (i % 3) * 9)
        rr = R * (0.86 if i % 2 else 0.93)
        x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        fill = glint if i % 3 else WHITE
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.5 if i % 2 else 1.9}" fill="{fill}" '
                   'opacity="0.7"/>')
    pr = R * 0.68
    out.append(f'<circle cx="{cx}" cy="{cy + 1:g}" r="{pr:.1f}" fill="#1E1A22"/>')
    out.append(f'<path d="M{cx - pr * 0.62:.1f} {cy + pr * 0.45:.1f}a{pr * 0.78:.1f} {pr * 0.78:.1f} '
               f'0 0 0 {pr * 1.24:.1f} 0" fill="none" stroke="{WHITE}" stroke-width="2.5" '
               'stroke-linecap="round" opacity="0.28"/>')
    out.append(f'<ellipse cx="{cx - pr * 0.36:.1f}" cy="{cy - pr * 0.34:.1f}" rx="{pr * 0.34:.1f}" '
               f'ry="{pr * 0.28:.1f}" fill="{WHITE}"/>')
    out.append(f'<circle cx="{cx + pr * 0.38:.1f}" cy="{cy + pr * 0.36:.1f}" r="{pr * 0.14:.1f}" '
               f'fill="{WHITE}"/>')
    return "".join(out)


def _eye_arc(a, cx, cy, depth):
    """Closed eye: depth < 0 curves up (content), depth > 0 curves down (sleepy)."""
    e = a["eye"]
    w = e.get("rx", e.get("r", 12)) * 1.3
    return (f'<path d="M{cx - w:g} {cy} q{w:g} {depth} {2 * w:g} 0" fill="none" '
            f'stroke="{a["over_eye"]}" stroke-width="6" stroke-linecap="round"/>')


def _eye_heart(a, cx, cy):
    return ('<path d="M0 8C-12 0-16-6-16-11c0-6 8-8 16 0 8-8 16-6 16 0 0 5-4 11-16 19z" '
            f'transform="translate({cx},{cy - 2}) scale(0.8)" fill="#FF6E8A"/>')


def _eye_cross(a, cx, cy):
    return (f'<g stroke="{a["over_eye"]}" stroke-width="6" stroke-linecap="round">'
            f'<path d="M{cx - 9} {cy - 9} {cx + 9} {cy + 9}"/>'
            f'<path d="M{cx + 9} {cy - 9} {cx - 9} {cy + 9}"/></g>')


def _sunglasses(a):
    """Shades sized to the animal's own eyes, never wider than the gap between them."""
    lx, rx = a["eye"]["cx"]
    cy = a["eye"]["cy"]
    e = a["eye"]
    base = e.get("rx", e.get("r", 12))
    hw = min(base * 2.4, (rx - lx) / 2 - 3)
    hh = e.get("ry", e.get("r", 12)) * 1.35
    lens = "".join(
        f'<rect x="{cx - hw:g}" y="{cy - hh:g}" width="{2 * hw:g}" height="{2 * hh:g}" '
        f'rx="{hh * 0.7:g}" fill="#2F3A4A"/>'
        f'<path d="M{cx - hw * 0.45:g} {cy + hh * 0.55:g} {cx + hw * 0.1:g} {cy - hh * 0.6:g}" '
        f'stroke="{WHITE}" stroke-width="4" stroke-linecap="round" opacity="0.45"/>'
        for cx in (lx, rx)
    )
    bridge = (f'<path d="M{lx + hw:g} {cy - hh * 0.45:g}H{rx - hw:g}" stroke="#2F3A4A" '
              'stroke-width="6" stroke-linecap="round"/>')
    return lens + bridge


def eyes(a, kind="open", scale=1.0):
    lx, rx = a["eye"]["cx"]
    cy = a["eye"]["cy"]
    if kind == "open":
        return _eye_open(a, lx, cy, scale) + _eye_open(a, rx, cy, scale)
    if kind == "happy":
        return _eye_arc(a, lx, cy, -13) + _eye_arc(a, rx, cy, -13)
    if kind == "sleepy":
        return _eye_arc(a, lx, cy, 13) + _eye_arc(a, rx, cy, 13)
    if kind == "wink":
        return _eye_open(a, lx, cy) + _eye_arc(a, rx, cy, -13)
    if kind == "heart":
        return _eye_heart(a, lx, cy) + _eye_heart(a, rx, cy)
    if kind == "cross":
        return _eye_cross(a, lx, cy) + _eye_cross(a, rx, cy)
    if kind == "shades":
        return _sunglasses(a)
    if kind == "sparkly":
        key = next(k for k, v in ANIMALS.items() if v is a)
        R = min(25 if a["eye"]["style"] in ("big", "owl") else 22, (rx - lx) / 2 - 6)
        return _eye_sparkly(a, key, lx, cy, R) + _eye_sparkly(a, key, rx, cy, R)
    raise ValueError(kind)


def brows(a, kind):
    lx, rx = a["eye"]["cx"]
    y = a["eye"]["cy"] - a["brow_dy"]
    w, col = a["brow_w"], a["over_eye"]

    def seg(cx, angle, dy=0):
        return (f'<path d="M{-w} 0h{2 * w}" transform="translate({cx},{y + dy}) rotate({angle})" '
                f'fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')

    if kind == "sad":
        return seg(lx, -16) + seg(rx, 16)
    if kind == "angry":
        return seg(lx, 16) + seg(rx, -16)
    if kind == "confused":
        return seg(lx, 0, -8) + seg(rx, 16)
    if kind == "flat":
        return seg(lx, 0) + seg(rx, 0)
    raise ValueError(kind)


# ------------------------------------------------------------------ mouth

BEAK_CLOSED = '<path d="M128 150l13 15-13 19-13-19z" fill="#6E6A72"/>'
BEAK_SMILE = ('<path d="M128 148l15 15h-30z" fill="#6E6A72"/>'
              '<path d="M113 163h30q0 17-15 17t-15-17z" fill="#57535B"/>')
BEAK_OPEN = ('<path d="M128 144l16 16h-32z" fill="#6E6A72"/>'
             '<path d="M112 166h32l-16 20z" fill="#57535B"/>')


def _beak(kind):
    """The owl has no mouth, so the beak carries the expression."""
    if kind in ("o", "open", "wobble"):
        return BEAK_OPEN
    if kind == "smile":
        return BEAK_SMILE
    line = ('<path d="M114 192q14 -12 28 0" fill="none" stroke="#6E6A72" stroke-width="5" '
            'stroke-linecap="round"/>') if kind == "frown" else ""
    if kind == "wavy":
        line = ('<path d="M114 190q7-8 14 0 7 8 14 0" fill="none" stroke="#6E6A72" '
                'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    return BEAK_CLOSED + line


def mouth(a, kind):
    if a["mouth_kind"] == "beak":
        return _beak("frown" if kind.startswith("frown") else kind)

    cx, y, col, sw, w = 128, a["mouth_y"], a["line"], a["mouth_sw"], a["mouth_w"]
    stroke = (f'fill="none" stroke="{col}" stroke-width="{sw:g}" stroke-linecap="round" '
              'stroke-linejoin="round"')

    if kind == "smile":
        return f'<path d="M{cx - w} {y}q{w / 2:g} 11 {w} 0 q{w / 2:g} 11 {w} 0" {stroke}/>'
    if kind == "straight":
        return f'<path d="M{cx - 9} {y + 3}h18" {stroke}/>'
    if kind == "frown":
        return f'<path d="M{cx - 13} {y + 8}q13-14 26 0" {stroke}/>'
    if kind == "frown_deep":
        return f'<path d="M{cx - 15} {y + 11}q15-19 30 0" {stroke}/>'
    if kind == "frown_small":
        return f'<path d="M{cx - 11} {y + 5}q11-8 22 0" {stroke}/>'
    if kind == "wavy":
        return f'<path d="M{cx - 14} {y + 2}q7-9 14 0 7 9 14 0" {stroke}/>'
    if kind == "smirk":
        return f'<path d="M{cx - 13} {y + 6}q13 6 26-10" {stroke}/>'
    if kind == "o":
        return f'<ellipse cx="{cx}" cy="{y + 6}" rx="8" ry="10" fill="{col}"/>'
    if kind == "open":
        return (f'<path d="M{cx - 19} {y - 2}q19 32 38 0z" fill="{col}"/>'
                f'<path d="M{cx - 8} {y + 6}q8 9 16 0z" fill="#FF8FA9"/>')
    if kind == "wobble":
        return f'<path d="M{cx - 15} {y + 2}q15 22 30 0-15 10-30 0z" fill="{col}"/>'
    raise ValueError(kind)


# ----------------------------------------------------------------- extras

def teardrop(x, y, s=1.0, fill="#7EC8E3"):
    return (f'<g transform="translate({x},{y}) scale({s:g})">'
            f'<path d="M0-11c-6 9-9 13-9 17a9 9 0 0 0 18 0c0-4-3-8-9-17z" fill="{fill}"/>'
            f'<ellipse cx="-3" cy="7" rx="2.5" ry="3.5" fill="{WHITE}" opacity="0.55"/></g>')


def sparkle(x, y, s=1.0, fill="#FFD86B"):
    return (f'<path d="M0-12q1.5 10.5 12 12-10.5 1.5-12 12-1.5-10.5-12-12 10.5-1.5 12-12z" '
            f'transform="translate({x},{y}) scale({s:g})" fill="{fill}"/>')


def heart(x, y, s=1.0, fill="#FF6E8A"):
    return ('<path d="M0 8C-12 0-16-6-16-11c0-6 8-8 16 0 8-8 16-6 16 0 0 5-4 11-16 19z" '
            f'transform="translate({x},{y}) scale({s:g})" fill="{fill}"/>')


def zzz(x=190, y=62, col="#6C7A8C"):
    out = []
    for dx, dy, s in ((0, 0, 1.0), (26, -26, 0.72), (44, -46, 0.52)):
        w = 16 * s
        out.append(f'<path d="M{x + dx:g} {y + dy:g}h{w:g}l{-w:g} {w:g}h{w:g}" fill="none" '
                   f'stroke="{col}" stroke-width="{5 * s:g}" stroke-linecap="round" '
                   'stroke-linejoin="round"/>')
    return "".join(out)


def question(x=212, y=44, col="#6C7A8C"):
    return (f'<g transform="translate({x},{y})" fill="none" stroke="{col}" stroke-width="6" '
            'stroke-linecap="round"><path d="M-8-10a9 9 0 0 1 16 5c0 6-8 6-8 12"/></g>'
            f'<circle cx="{x}" cy="{y + 18}" r="3.5" fill="{col}"/>')


def anger_mark(x=204, y=64):
    return (f'<g transform="translate({x},{y})" fill="none" stroke="#E4574C" stroke-width="5" '
            'stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M-11 0 0-11 11 0"/><path d="M-11 10 0-1 11 10"/></g>')


def motion_lines(x=214, y=110, col="#B9AFC9"):
    return (f'<g transform="translate({x},{y})" stroke="{col}" stroke-width="5" '
            'stroke-linecap="round"><path d="M0 0h16"/><path d="M4 14h16"/></g>')


# ------------------------------------------------------------ expressions

def _expr(eyes_kind="open", mouth_kind="smile", scale=1.0, brow=None, extras="",
          teeth=True, blush_scale=1.0, blush_fill=None, blush_opacity=None):
    return {
        "eyes": eyes_kind, "mouth": mouth_kind, "scale": scale, "brow": brow,
        "extras": extras, "teeth": teeth, "blush_scale": blush_scale,
        "blush_fill": blush_fill, "blush_opacity": blush_opacity,
    }


def expressions(a):
    """Expression table for one animal — extras depend on its anchors."""
    lx, rx = a["eye"]["cx"]
    ey = a["eye"]["cy"]
    below = ey + a["eye"].get("ry", a["eye"].get("r", 12)) + 10

    return {
        "happy": _expr(),
        "neutral": _expr(mouth_kind="straight", blush_opacity=0.22),
        "sad": _expr(mouth_kind="frown", brow="sad", blush_opacity=0.22),
        "crying": _expr(eyes_kind="happy", mouth_kind="wobble", brow="sad", teeth=False,
                        extras=teardrop(lx - 2, below, 1.15) + teardrop(rx + 2, below, 1.15)),
        "angry": _expr(mouth_kind="frown", brow="angry", extras=anger_mark(216, 48)),
        "surprised": _expr(mouth_kind="o", scale=1.3, brow="flat", teeth=False),
        "sleepy": _expr(eyes_kind="sleepy", mouth_kind="o", teeth=False, extras=zzz()),
        "love": _expr(eyes_kind="heart", mouth_kind="open", teeth=False, blush_opacity=0.55,
                      extras=heart(46, 56, 0.6) + heart(212, 40, 0.45)),
        "wink": _expr(eyes_kind="wink", extras=sparkle(206, 62, 0.9)),
        "laughing": _expr(eyes_kind="happy", mouth_kind="open", teeth=False, blush_opacity=0.6),
        "cool": _expr(eyes_kind="shades", mouth_kind="smirk", teeth=False, extras=sparkle(212, 70, 0.85)),
        "confused": _expr(mouth_kind="wavy", brow="confused", extras=question()),
        "shy": _expr(eyes_kind="happy", mouth_kind="wavy", blush_scale=1.35, blush_opacity=0.65,
                     extras=motion_lines()),
        "sparkly": _expr(eyes_kind="sparkly", blush_scale=1.15, blush_opacity=0.55,
                         extras=sparkle(212, 58, 0.8) + sparkle(44, 70, 0.55)),
        "sick": _expr(eyes_kind="cross", mouth_kind="wavy", teeth=False, blush_fill="#9BC58E",
                      blush_opacity=0.5, extras=teardrop(206, 108, 1.05, "#9BD7F0")),

        # rating scale
        "rate_1": _expr(mouth_kind="frown_deep", brow="sad", teeth=False, blush_opacity=0.18,
                        extras=teardrop(rx + 4, below, 1.1)),
        "rate_2": _expr(mouth_kind="frown_small", brow="sad", blush_opacity=0.22),
        "rate_3": _expr(mouth_kind="straight", blush_opacity=0.3),
        "rate_4": _expr(mouth_kind="smile"),
        "rate_5": _expr(eyes_kind="happy", mouth_kind="open", teeth=False, blush_scale=1.25,
                        blush_opacity=0.62,
                        extras=sparkle(48, 60, 0.75) + sparkle(210, 52, 0.9)),
    }


FRAME_LABELS = {
    "bubble": "Speech bubble", "sticker": "Sticker", "peek": "Peeking", "hug": "Hug",
}
FRAME_ORDER = list(FRAME_LABELS)

RATING_LABELS = {
    "rate_1": "Terrible", "rate_2": "Poor", "rate_3": "Okay",
    "rate_4": "Good", "rate_5": "Great",
}
RATING_ORDER = list(RATING_LABELS)

EXPRESSION_ORDER = ["happy", "neutral", "sad", "crying", "angry", "surprised", "sleepy",
                    "love", "wink", "laughing", "cool", "confused", "shy", "sick", "sparkly"]


# ---------------------------------------------------------------- badges

BADGES = {
    "online": ("#3FBF6F", f'<circle cx="48" cy="48" r="15" fill="{WHITE}"/>'),
    "away": ("#F5A623", f'<path d="M48 28v21l14 9" fill="none" stroke="{WHITE}" stroke-width="8" '
                        'stroke-linecap="round" stroke-linejoin="round"/>'),
    "busy": ("#E4574C", f'<rect x="26" y="41" width="44" height="14" rx="7" fill="{WHITE}"/>'),
    "offline": ("#9AA0AC", f'<circle cx="48" cy="48" r="14" fill="none" stroke="{WHITE}" stroke-width="8"/>'),
    "typing": ("#5B7BE8", f'<circle cx="30" cy="48" r="6.5" fill="{WHITE}"/>'
                          f'<circle cx="48" cy="48" r="6.5" fill="{WHITE}"/>'
                          f'<circle cx="66" cy="48" r="6.5" fill="{WHITE}"/>'),
    "notification": ("#E4574C", f'<path d="M48 22a14 14 0 0 0-14 14c0 14-6 16-6 20h40c0-4-6-6-6-20a14 14 0 0 0-14-14z" fill="{WHITE}"/>'
                                f'<path d="M40 62a8 8 0 0 0 16 0z" fill="{WHITE}"/>'),
    "muted": ("#6B7280", f'<path d="M44 34 30 44H22v10h8l14 10z" fill="{WHITE}"/>'
                         f'<path d="M54 40 70 56M70 40 54 56" stroke="{WHITE}" stroke-width="7" stroke-linecap="round"/>'),
    "verified": ("#2F9BE8", f'<path d="M31 49 43 61 66 36" fill="none" stroke="{WHITE}" stroke-width="9" '
                            'stroke-linecap="round" stroke-linejoin="round"/>'),
    "locked": ("#7A6FA8", f'<path d="M37 44v-7a11 11 0 0 1 22 0v7" fill="none" stroke="{WHITE}" stroke-width="7"/>'
                          f'<rect x="30" y="44" width="36" height="28" rx="8" fill="{WHITE}"/>'),
    "star": ("#F5A623", f'<path d="M48 24l7.4 15.6 16.6 2.2-12 11.8 3 16.9L48 62.5 32.9 70.5l3-16.9-12-11.8 16.6-2.2z" fill="{WHITE}"/>'),
}

BADGE_ORDER = list(BADGES)

BADGE_LABELS = {
    "online": "Online", "away": "Away", "busy": "Busy / do not disturb", "offline": "Offline",
    "typing": "Typing", "notification": "Notification", "muted": "Muted",
    "verified": "Verified", "locked": "Private", "star": "Featured",
}


def badge_body(name, r=44):
    fill, glyph = BADGES[name]
    return f'<circle cx="48" cy="48" r="{r}" fill="{fill}"/>{glyph}'


def badge_overlay(name):
    """Badge placed in the bottom-right corner of a 256 icon, with a white cut-out ring."""
    cx = cy = 204
    scale = 38 / 44
    return (f'  <circle cx="{cx}" cy="{cy}" r="45" fill="{WHITE}"/>\n'
            f'  <g transform="translate({cx},{cy}) scale({scale:g}) translate(-48,-48)">'
            f'{badge_body(name)}</g>')


# ---------------------------------------------------------------- render

def blush(a, expr):
    b = a["blush"]
    s = expr["blush_scale"]
    fill = expr["blush_fill"] or b["fill"]
    opacity = b["opacity"] if expr["blush_opacity"] is None else expr["blush_opacity"]
    return "".join(
        f'<ellipse cx="{cx}" cy="{b["cy"]}" rx="{b["rx"] * s:g}" ry="{b["ry"] * s:g}" '
        f'fill="{fill}" opacity="{opacity:g}"/>'
        for cx in b["cx"]
    )


def render(animal_key, expr_key, badge_key=None, outline=True):
    a = ANIMALS[animal_key]
    expr = expressions(a)[expr_key]

    layers = ([a["behind"]] if a.get("behind") else []) + [a["base"]]
    layers.append("  " + eyes(a, expr["eyes"], expr["scale"]))
    if expr["brow"]:
        layers.append("  " + brows(a, expr["brow"]))
    layers.append("  " + blush(a, expr))
    if a["nose"]:
        layers.append("  " + a["nose"])
    layers.append("  " + mouth(a, expr["mouth"]))
    if a["teeth"] and expr["teeth"]:
        layers.append("  " + a["teeth"])
    if a.get("front"):
        layers.append(a["front"])
    if expr["extras"]:
        layers.append("  " + expr["extras"])

    if outline:
        layers = [_inset(sticker("\n".join(layers), a["ink"], OUTLINE_FACE))]

    if badge_key:
        # shrink the face a touch so the corner badge does not crowd it
        face = "\n".join(layers)
        layers = [f'  <g transform="translate(4,-4) scale(0.88)">\n{face}\n  </g>',
                  badge_overlay(badge_key)]

    if animal_key in TILT:
        layers = [f'  <g transform="rotate({TILT[animal_key]} 128 150)">',
                  "\n".join(layers), "  </g>"]

    name = badge_key or expr_key
    label = f'{a["label"]} — {BADGE_LABELS.get(name, RATING_LABELS.get(name, name))}'
    slug = f"{name}_{animal_key}"
    body = "\n".join(layers)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" '
            f'role="img" aria-labelledby="t-{slug}">\n'
            f'  <title id="t-{slug}">{label}</title>\n{body}\n</svg>\n')


def _scallop256(bumps=13, r=104, cx=128, cy=128):
    step = 2 * math.pi / bumps
    br = r * math.tan(step / 2) * 1.3
    pts = [(cx + r * math.cos(i * step - math.pi / 2), cy + r * math.sin(i * step - math.pi / 2))
           for i in range(bumps + 1)]
    d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"
    for x, y in pts[1:]:
        d += f"A{br:.0f} {br:.0f} 0 0 1 {x:.0f} {y:.0f}"
    return d + "Z"


def _face_art(animal, expr="happy", behind=True):
    """The drawn layers of a face, without its <svg> wrapper.

    `behind=False` drops the layer that sits behind the head — the red panda's
    tail — so a full body can draw a full-size one instead."""
    svg = render(animal, expr, outline=False)
    art = svg[svg.index("</title>") + 8:svg.rindex("</svg>")].strip()
    if not behind and ANIMALS[animal].get("behind"):
        art = art.replace(ANIMALS[animal]["behind"].strip(), "").strip()
    return art


def _placed(animal, cx, cy, scale, expr="happy"):
    return (f'<g transform="translate({cx},{cy}) scale({scale:g}) translate(-128,-126)">'
            f'{_face_art(animal, expr)}</g>')


def render_frame(animal, frame):
    """The character composed into a container shape."""
    fur = PAW_PALETTE[animal]["fur"]
    slug = f"{frame}_{animal}"
    label = f'{ANIMALS[animal]["label"]} — {FRAME_LABELS[frame]}'

    if frame == "bubble":
        art = ('<path d="M34 22h188a26 26 0 0 1 26 26v106a26 26 0 0 1-26 26H116l-52 40v-40H34'
               f'a26 26 0 0 1-26-26V48a26 26 0 0 1 26-26z" fill="{WHITE}" stroke="{fur}" '
               'stroke-width="9" stroke-linejoin="round"/>' + _placed(animal, 128, 100, 0.56))
    elif frame == "sticker":
        art = (f'<path d="{_scallop256()}" fill="{WHITE}" stroke="{fur}" stroke-width="9" '
               'stroke-linejoin="round"/>' + _placed(animal, 128, 130, 0.62))
    elif frame == "peek":
        art = (_placed(animal, 128, 118, 0.78)
               + f'<rect x="4" y="182" width="248" height="70" rx="26" fill="{fur}"/>'
               f'<rect x="26" y="200" width="204" height="12" rx="6" fill="{WHITE}" opacity="0.45"/>')
    elif frame == "hug":
        pad = PAW_PALETTE[animal]["pad"]
        key = PAW_PALETTE[animal].get("key")
        stroke = f' stroke="{key}" stroke-width="7"' if key else ""
        art = (_placed(animal, 128, 112, 0.74)
               + f'<ellipse cx="46" cy="196" rx="34" ry="42" transform="rotate(-24 46 196)" '
               f'fill="{fur}"{stroke}/><ellipse cx="46" cy="200" rx="19" ry="24" '
               f'transform="rotate(-24 46 200)" fill="{pad}"/>'
               f'<ellipse cx="210" cy="196" rx="34" ry="42" transform="rotate(24 210 196)" '
               f'fill="{fur}"{stroke}/><ellipse cx="210" cy="200" rx="19" ry="24" '
               f'transform="rotate(24 210 200)" fill="{pad}"/>')
    else:
        raise ValueError(frame)
    art = sticker(art, _ink(animal), OUTLINE_SCENE)

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" '
            f'role="img" aria-labelledby="t-{slug}">\n  <title id="t-{slug}">{label}</title>\n'
            f'  {art}\n</svg>\n')


def render_extra(animal, kind):
    """The happy face wearing an accessory, or holding its signature snack."""
    slug = f"{kind}_{animal}"
    label_for = SNACK_LABEL if kind == "snack" else ACCESSORY_LABELS[kind]
    label = f'{ANIMALS[animal]["label"]} — {label_for}'
    overlay = SNACKS[animal] if kind == "snack" else accessory(animal, kind)
    if animal in TILT:
        overlay = f'<g transform="rotate({TILT[animal]} 128 150)">{overlay}</g>'
    art = _inset(sticker(f"{_face_art(animal)}{overlay}", _ink(animal), OUTLINE_FACE))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" '
            f'role="img" aria-labelledby="t-{slug}">\n  <title id="t-{slug}">{label}</title>\n'
            f'  {art}\n</svg>\n')


def render_action(animal, kind):
    """Face in the upper two thirds, prop below, paws gripping it."""
    pal = PAW_PALETTE[animal]
    slug = f"{kind}_{animal}"
    label = f'{ANIMALS[animal]["label"]} — {ACTION_LABELS[kind]}'
    ink = INKS[animal]
    held = prop(kind, pal["fur"], pal["pad"], None, ink)
    held = sticker(held, ink, 3.2)      # its own contour, so a fur-coloured prop reads over the body
    torso, belly, limb, _ = BODY[animal]
    face = sticker(_face_art(animal), ink, 3.2 / 0.62)
    art = (action_body(torso, belly, limb, ink)
           + f'<g transform="translate(128,92) scale(0.62) translate(-128,-126)">{face}</g>'
           + held)
    art = sticker(art, _ink(animal), OUTLINE_SCENE)
    if animal in TILT:
        art = f'<g transform="rotate({TILT[animal]} 128 150)">{art}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" '
            f'role="img" aria-labelledby="t-{slug}">\n  <title id="t-{slug}">{label}</title>\n'
            f'  {art}\n</svg>\n')


def render_body(animal, pose):
    slug = f"{pose}_{animal}"
    label = f'{ANIMALS[animal]["label"]} — {POSE_LABELS[pose]}'
    art = body_pose(animal, pose, _face_art(animal, behind=False))
    art = sticker(art, _ink(animal), OUTLINE_SCENE)
    if animal in TILT:
        art = f'<g transform="rotate({TILT[animal]} 128 150)">{art}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" '
            f'role="img" aria-labelledby="t-{slug}">\n  <title id="t-{slug}">{label}</title>\n'
            f'  {art}\n</svg>\n')


def render_job(animal, job):
    """Standing body, with the uniform tucked under the head and the hat and tool over it."""
    slug = f"{job}_{animal}"
    label = f'{ANIMALS[animal]["label"]} — {JOB_LABELS[job]}'
    art = body_pose(animal, "standing", _face_art(animal, behind=False))
    behind, worn, held = outfit(job)
    cut = art.rindex('<g transform="translate(128,')
    art = behind + art[:cut] + worn + art[cut:] + held
    art = sticker(art, _ink(animal), OUTLINE_SCENE)
    if animal in TILT:
        art = f'<g transform="rotate({TILT[animal]} 128 150)">{art}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" '
            f'role="img" aria-labelledby="t-{slug}">\n  <title id="t-{slug}">{label}</title>\n'
            f'  {art}\n</svg>\n')


def render_badge(name):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" '
            f'role="img" aria-labelledby="t-badge_{name}">\n'
            f'  <title id="t-badge_{name}">{BADGE_LABELS[name]}</title>\n'
            f'  {badge_body(name)}\n</svg>\n')


def build():
    """Every file is named for its icon code: <expression|status>_<animal>."""
    if SVG_DIR.exists():
        shutil.rmtree(SVG_DIR)

    ui = SVG_DIR / "ui"
    ui.mkdir(parents=True)
    ui_names = []
    for name in UI_ICONS:
        (ui / f"{name}.svg").write_text(render_ui(name))
        ui_names.append(name)
        if name in FACES:
            # face-free twin for 16px chrome, where the eyes turn to mush
            (ui / f"{name}_plain.svg").write_text(render_ui(name, with_face=False))
            ui_names.append(f"{name}_plain")

    chars = SVG_DIR / "characters"
    chars.mkdir(parents=True)
    for animal in ANIMALS:
        for expr in EXPRESSION_ORDER + RATING_ORDER:
            (chars / f"{expr}_{animal}.svg").write_text(render(animal, expr))

    paws = SVG_DIR / "paws"
    paws.mkdir(parents=True)
    for animal in ANIMALS:
        for g in GESTURE_ORDER:
            label = f'{ANIMALS[animal]["label"]} — {GESTURE_LABELS[g]}'
            svg = render_paw(animal, g, label)
            i, j = svg.index("</title>") + 8, svg.rindex("</svg>")
            svg = svg[:i] + _inset(sticker(svg[i:j], _ink(animal), OUTLINE_FACE)) + "\n" + svg[j:]
            (paws / f"{g}_{animal}.svg").write_text(svg)

    frames = SVG_DIR / "frames"
    frames.mkdir(parents=True)
    for animal in ANIMALS:
        for f in FRAME_ORDER:
            (frames / f"{f}_{animal}.svg").write_text(render_frame(animal, f))

    extras = SVG_DIR / "extras"
    extras.mkdir(parents=True)
    for animal in ANIMALS:
        for kind in ACCESSORY_ORDER + ["snack"]:
            (extras / f"{kind}_{animal}.svg").write_text(render_extra(animal, kind))

    actions = SVG_DIR / "actions"
    actions.mkdir(parents=True)
    for animal in ANIMALS:
        for kind in ACTION_ORDER:
            (actions / f"{kind}_{animal}.svg").write_text(render_action(animal, kind))

    bodies = SVG_DIR / "bodies"
    bodies.mkdir(parents=True)
    for animal in ANIMALS:
        for pose in POSE_ORDER:
            (bodies / f"{pose}_{animal}.svg").write_text(render_body(animal, pose))

    jobs = SVG_DIR / "jobs"
    jobs.mkdir(parents=True)
    for animal in ANIMALS:
        for job in JOB_ORDER:
            (jobs / f"{job}_{animal}.svg").write_text(render_job(animal, job))

    badges = SVG_DIR / "badges"
    badges.mkdir(parents=True)
    for name in BADGE_ORDER:
        (badges / f"badge_{name}.svg").write_text(render_badge(name))

    status = SVG_DIR / "status"
    status.mkdir(parents=True)
    for animal in ANIMALS:
        for name in BADGE_ORDER:
            (status / f"{name}_{animal}.svg").write_text(render(animal, "happy", name))

    counts = {
        "ui": len(ui_names),
        "characters": len(ANIMALS) * (len(EXPRESSION_ORDER) + len(RATING_ORDER)),
        "badges": len(BADGE_ORDER),
        "paws": len(ANIMALS) * len(GESTURE_ORDER),
        "frames": len(ANIMALS) * len(FRAME_ORDER),
        "extras": len(ANIMALS) * (len(ACCESSORY_ORDER) + 1),
        "actions": len(ANIMALS) * len(ACTION_ORDER),
        "bodies": len(ANIMALS) * len(POSE_ORDER),
        "jobs": len(ANIMALS) * len(JOB_ORDER),
        "status": len(ANIMALS) * len(BADGE_ORDER),
    }
    manifest = {
        "animals": {k: v["label"] for k, v in ANIMALS.items()},
        "expressions": EXPRESSION_ORDER,
        "ratings": RATING_LABELS,
        "gestures": GESTURE_LABELS,
        "frames": FRAME_LABELS,
        "extras": {**ACCESSORY_LABELS, "snack": SNACK_LABEL},
        "actions": ACTION_LABELS,
        "bodies": POSE_LABELS,
        "jobs": JOB_LABELS,
        "badges": {k: BADGE_LABELS[k] for k in BADGE_ORDER},
        "ui": ui_names,
        "ui_groups": [{"title": t, "icons": n} for t, n in groups()],
        "counts": counts,
        "total": sum(counts.values()),
    }
    (ROOT / "icons.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {manifest['total']} icons: " +
          ", ".join(f"{v} {k}" for k, v in counts.items()))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        animal, expr = sys.argv[1], sys.argv[2]
        badge = sys.argv[3] if len(sys.argv) > 3 else None
        print(render(animal, expr, badge), end="")
    else:
        build()
