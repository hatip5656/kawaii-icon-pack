#!/usr/bin/env python3
"""Path data for the functional UI layer.

Contract: 24 x 24 grid, 2px stroke, round caps and joins, `currentColor`, no fills
except where a shape is deliberately solid (dots, toggles, filled variants).
Artwork stays inside 2..22 so nothing clips when the icon is boxed.
"""

import math


def _gear(teeth=8, r_out=9.6, r_in=7.3, hub=3.3, cx=12, cy=12):
    """Flat-topped cog — a star polygon would just look like the sun icon."""
    pts, step = [], math.pi / teeth
    for i in range(teeth):
        a = i * 2 * step
        for r, w in ((r_in, step * 0.72), (r_out, step * 0.42),
                     (r_out, -step * 0.42), (r_in, -step * 0.72)):
            pts.append((cx + r * math.cos(a - w), cy + r * math.sin(a - w)))
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
    return f'<path d="{d}"/><circle cx="{cx}" cy="{cy}" r="{hub}"/>'


def _star(points=8, r_out=9.6, r_in=3.4, cx=12, cy=12):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = i * math.pi / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return '<path d="M' + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + 'Z"/>'


def _petals(n=5, rx=2.7, ry=4.3, dist=4.4, hub=2.2, cx=12, cy=12):
    out = "".join(
        f'<ellipse cx="{cx}" cy="{cy - dist}" rx="{rx}" ry="{ry}" '
        f'transform="rotate({i * 360 / n:.0f} {cx} {cy})"/>'
        for i in range(n)
    )
    return out + f'<circle cx="{cx}" cy="{cy}" r="{hub}"/>'


def _scallop(bumps=11, r=8.3, cx=12, cy=12):
    """Sticker edge — a circle made of little bumps."""
    step = 2 * math.pi / bumps
    br = r * math.tan(step / 2) * 1.25
    pts = [(cx + r * math.cos(i * step - math.pi / 2), cy + r * math.sin(i * step - math.pi / 2))
           for i in range(bumps + 1)]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for x, y in pts[1:]:
        d += f"A{br:.1f} {br:.1f} 0 0 1 {x:.1f} {y:.1f}"
    return f'<path d="{d}Z"/>'


def _spiral(turns=2.4, r_max=8.8, cx=12, cy=12, steps=64):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a, r = t * turns * 2 * math.pi, r_max * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return '<path d="M' + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + '"/>'


def _rating(mouth, happy_eyes=False, blush=False):
    eyes = ('<path d="M7.6 11.2q1.6-2 3.2 0M13.2 11.2q1.6-2 3.2 0" stroke-width="1.9"/>'
            if happy_eyes else DOT % (9.2, 10.4, 1.15) + DOT % (14.8, 10.4, 1.15))
    cheeks = (DOT % (6.3, 13.6, 1.05) + DOT % (17.7, 13.6, 1.05)) if blush else ""
    return f'<circle cx="12" cy="12" r="9"/>{eyes}{cheeks}{mouth}'


def _heart(cx, cy, s=1.0):
    return (f'<path d="M0 8.4 -5.6 2.8a3.9 3.9 0 0 1 5.6-5.4 3.9 3.9 0 0 1 5.6 5.4z" '
            f'transform="translate({cx},{cy}) scale({s:g})"/>')


def _pawprint(cx, cy, s=1.0):
    return (f'<g transform="translate({cx},{cy}) scale({s:g})">'
            '<ellipse cx="-3.4" cy="-2.6" rx="1.5" ry="2"/><ellipse cx="0" cy="-4" rx="1.5" ry="2.1"/>'
            '<ellipse cx="3.4" cy="-2.6" rx="1.5" ry="2"/>'
            '<path d="M0 1.2c2.7 0 4.6 1.7 4.6 3.5S2.7 7.4 0 7.4-4.6 6.5-4.6 4.7 -2.7 1.2 0 1.2z"/></g>')


# Reusable fragments
DOT = '<circle cx="%s" cy="%s" r="%s" fill="currentColor" stroke="none"/>'
SLASH = '<path d="m4 4 16 16"/>'


def face(cx, cy, s=1.0):
    """Two dot eyes and a smile — the kawaii tell, in currentColor like everything else."""
    r, dx = round(1.05 * s, 2), 2.7 * s
    w, drop = 1.7 * s, 2.1 * s
    smile = (f'<path d="M{cx - w:.1f} {cy + drop:.1f}q{w:.1f} {1.7 * s:.1f} {2 * w:.1f} 0" '
             f'stroke-width="{1.7 * s:.1f}"/>')
    return DOT % (round(cx - dx, 1), cy, r) + DOT % (round(cx + dx, 1), cy, r) + smile


def toes(*spec):
    """Rounded toe pads: toes((x, y), (x, y, rx, ry), ...)"""
    out = []
    for t in spec:
        x, y = t[0], t[1]
        rx, ry = (t[2], t[3]) if len(t) > 2 else (1.75, 2.2)
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>')
    return "".join(out)


# Objects that get a face, and where it sits: name -> (cx, cy, scale)
FACES = {
    "home": (12, 12.6, 0.8), "folder": (12, 14.6, 1.0), "folder_open": (12, 15.8, 0.85),
    "file": (11.8, 14.6, 0.85), "mail": (12, 14.6, 0.85), "mail_open": (12, 15.6, 0.8),
    "inbox": (12, 8.2, 0.85), "cloud": (12, 13.4, 0.9), "cart": (13, 10.8, 0.8),
    "bell": (12, 11, 0.9), "trash": (12, 13.4, 0.85), "calendar": (12, 15.4, 0.9),
    "wallet": (10.5, 15, 0.8), "truck": (8, 11, 0.9), "lock": (12, 15.2, 0.8),
    "unlock": (12, 15.2, 0.8), "search": (10.5, 10.4, 0.85), "settings": (12, 12, 0.62),
    "chat": (12, 11.4, 0.9), "comment": (12, 10.6, 0.9), "video": (9, 12, 0.9),
    "mic": (12, 7.6, 0.8), "heart": (12, 12.4, 0.85), "star": (12, 12.2, 0.78),
    "bookmark": (12, 10.2, 0.85), "fire": (12, 15, 0.85),
    # the cute layer wears faces too
    "box": (12, 14.6, 0.85), "camera": (12, 13.8, 0.85), "store": (12, 16.4, 0.8),
    "credit_card": (8.6, 15, 0.8), "tag": (12.4, 12.6, 0.8), "save": (12, 17.4, 0.8),
    "cupcake": (12, 17.2, 0.85), "donut": (12, 12, 0.8), "cookie": (12, 12.4, 0.75),
    "balloon": (12, 9.4, 0.9), "gift": (12, 15.6, 0.85),     "mushroom": (12, 15.8, 0.75), "sun_face": (12, 12, 0.85), "moon_face": (14.2, 12.4, 0.8),
    "milk": (12, 15.4, 0.85), "coffee": (10.2, 14, 0.85), "boba": (12, 12.8, 0.8),
    "sticker": (12, 12, 0.95), "frame_cloud": (12, 13, 0.85),
    "strawberry": (12, 13.6, 0.8),
}

_THUMB = ('<rect x="3.4" y="11.6" width="4.8" height="9.4" rx="2.4"/>'
          '<path d="M8.8 12.4 11.1 5.7a2.3 2.3 0 0 1 4.4 1.4l-.8 3.7h3.7a2.6 2.6 0 0 1 2.5 3.2'
          'l-1.1 4.6A3 3 0 0 1 17.9 21H8.8z"/>'
          + DOT % (12.9, 15.8, 0.85) + DOT % (15.8, 15.8, 0.85) + DOT % (18.6, 15.8, 0.85))

UI_ICONS = {
    # ------------------------------------------------------ navigation (16)
    "home": '<path d="M3 10.3 12 3l9 7.3"/><path d="M5.5 9v10.5A1.5 1.5 0 0 0 7 21h10a1.5 1.5 0 0 0 1.5-1.5V9"/><path d="M9.5 21v-6.5h5V21"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
    "chevron_up": '<path d="m6 14.5 6-6 6 6"/>',
    "chevron_down": '<path d="m6 9.5 6 6 6-6"/>',
    "chevron_left": '<path d="m14.5 6-6 6 6 6"/>',
    "chevron_right": '<path d="m9.5 6 6 6-6 6"/>',
    "arrow_up": '<path d="M12 20.5V4.5"/><path d="m5.5 11 6.5-6.5 6.5 6.5"/>',
    "arrow_down": '<path d="M12 3.5v16"/><path d="m5.5 13 6.5 6.5 6.5-6.5"/>',
    "arrow_left": '<path d="M19.5 12h-16"/><path d="m11 5.5-6.5 6.5 6.5 6.5"/>',
    "arrow_right": '<path d="M4.5 12h16"/><path d="m13 5.5 6.5 6.5-6.5 6.5"/>',
    "external_link": '<path d="M14 3.5h6.5V10"/><path d="M20.5 3.5 11.5 12.5"/><path d="M17.5 13.5V19a2 2 0 0 1-2 2h-11a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2H10"/>',
    "refresh": '<path d="M20 4.5v5h-5"/><path d="M4 19.5v-5h5"/><path d="M19.4 9.5A7.6 7.6 0 0 0 6.3 6.7"/><path d="M4.6 14.5a7.6 7.6 0 0 0 13.1 2.8"/>',
    "grid_view": '<rect x="3.5" y="3.5" width="7" height="7" rx="1.8"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.8"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.8"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.8"/>',
    "list_view": '<path d="M9 6.5h11M9 12h11M9 17.5h11"/><rect x="3.3" y="5.3" width="2.4" height="2.4" rx=".7"/><rect x="3.3" y="10.8" width="2.4" height="2.4" rx=".7"/><rect x="3.3" y="16.3" width="2.4" height="2.4" rx=".7"/>',
    "more_horizontal": DOT % (5, 12, 1.7) + DOT % (12, 12, 1.7) + DOT % (19, 12, 1.7),

    # --------------------------------------------------------- actions (20)
    "search": '<circle cx="10.5" cy="10.5" r="6.8"/><path d="m15.4 15.4 4.6 4.6"/>',
    "filter": '<path d="M3.5 5.5h17l-6.6 7.8V20l-3.8-2.1v-4.6z"/>',
    "sort": '<path d="M7 4.5v15"/><path d="m3.5 16 3.5 3.5L10.5 16"/><path d="M17 19.5v-15"/><path d="M13.5 8 17 4.5 20.5 8"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "edit": '<path d="M12 20.5h8.5"/><path d="M16.3 3.7a2.2 2.2 0 0 1 3.1 3.1L8.2 18h-4v-4z"/>',
    "trash": '<path d="M4.5 6.5h15"/><path d="M9.5 6.5V5a1.5 1.5 0 0 1 1.5-1.5h2A1.5 1.5 0 0 1 14.5 5v1.5"/><path d="m6.8 6.5 1 12.6a1.7 1.7 0 0 0 1.7 1.4h5a1.7 1.7 0 0 0 1.7-1.4l1-12.6"/>',
    "save": '<path d="M4.5 5.5a2 2 0 0 1 2-2h9.1l3.9 3.9v11.1a2 2 0 0 1-2 2h-11a2 2 0 0 1-2-2z"/><path d="M8 3.5v5h7v-5"/><path d="M8 20.5v-6h8v6"/>',
    "copy": '<rect x="8.5" y="8.5" width="12" height="12" rx="2.2"/><path d="M15.5 5.5a2 2 0 0 0-2-2h-8a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2"/>',
    "download": '<path d="M12 3.5v11.5"/><path d="m7.5 10.5 4.5 4.5 4.5-4.5"/><path d="M4 17v2.5a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V17"/>',
    "upload": '<path d="M12 15V3.5"/><path d="M7.5 8 12 3.5 16.5 8"/><path d="M4 17v2.5a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V17"/>',
    "share": '<circle cx="18" cy="5.5" r="2.6"/><circle cx="6" cy="12" r="2.6"/><circle cx="18" cy="18.5" r="2.6"/><path d="m8.3 10.7 7.4-3.9M8.3 13.3l7.4 3.9"/>',
    "settings": _gear(),
    "check": '<path d="m4.5 12.5 5 5 10-11"/>',
    "send": '<path d="m20.5 3.5-9.4 9.4"/><path d="M20.5 3.5 14.4 20.5 11.1 12.9 3.5 9.6z"/>',
    "attach": '<path d="M19.5 11.5 11.8 19.2a4.6 4.6 0 0 1-6.5-6.5l8.3-8.3a3.1 3.1 0 0 1 4.4 4.4l-8.3 8.3a1.6 1.6 0 0 1-2.2-2.2l7.6-7.6"/>',
    "link": '<path d="M10.2 13.8a3.9 3.9 0 0 0 5.6 0l2.9-2.9a3.9 3.9 0 0 0-5.6-5.6l-1.5 1.5"/><path d="M13.8 10.2a3.9 3.9 0 0 0-5.6 0l-2.9 2.9a3.9 3.9 0 0 0 5.6 5.6l1.5-1.5"/>',
    "lock": '<rect x="4.5" y="10.3" width="15" height="10.2" rx="2.3"/><path d="M8 10.3V7.8a4 4 0 0 1 8 0v2.5"/>',
    "unlock": '<rect x="4.5" y="10.3" width="15" height="10.2" rx="2.3"/><path d="M8 10.3V7.8a4 4 0 0 1 7.4-2.1"/>',
    "pin": '<path d="M9.5 3.5h5l-.8 5.3 3.3 3.2h-11l3.3-3.2z"/><path d="M12 12v8.5"/>',

    # ------------------------------------------------------ visibility (2)
    "eye": '<path d="M2.5 12S6.3 5.5 12 5.5 21.5 12 21.5 12 17.7 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3.1"/>',
    "eye_off": '<path d="M9.8 5.8A9.7 9.7 0 0 1 12 5.5c5.7 0 9.5 6.5 9.5 6.5a17.6 17.6 0 0 1-3.4 4.2"/><path d="M6.2 7.9A17.4 17.4 0 0 0 2.5 12S6.3 18.5 12 18.5a9.5 9.5 0 0 0 4-.9"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/>' + SLASH,

    # ----------------------------------------------------------- forms (10)
    "checkbox_on": '<rect x="3.5" y="3.5" width="17" height="17" rx="4"/><path d="m7.8 12.2 2.9 3 5.5-6.4"/>',
    "checkbox_off": '<rect x="3.5" y="3.5" width="17" height="17" rx="4"/>',
    "radio_on": '<circle cx="12" cy="12" r="8.5"/>' + DOT % (12, 12, 3.7),
    "radio_off": '<circle cx="12" cy="12" r="8.5"/>',
    "toggle_on": '<rect x="2.5" y="6.5" width="19" height="11" rx="5.5"/>' + DOT % (16, 12, 3.2),
    "toggle_off": '<rect x="2.5" y="6.5" width="19" height="11" rx="5.5"/>' + DOT % (8, 12, 3.2),
    "caret_down": '<path d="m7 9.8 5 5 5-5z" fill="currentColor"/>',
    "required": '<path d="M12 4.5v15M5.5 8.2l13 7.6M18.5 8.2l-13 7.6"/>',
    "dropzone": '<rect x="3.5" y="4.5" width="17" height="15" rx="3" stroke-dasharray="3.5 3"/><path d="M12 16V9"/><path d="m9 12 3-3 3 3"/>',
    "slider": '<path d="M3 8.5h18M3 15.5h18"/>' + DOT % (8.5, 8.5, 2.6) + DOT % (15.5, 15.5, 2.6),

    # -------------------------------------------------------- feedback (8)
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11.2v5.4"/>' + DOT % (12, 7.9, 1.15),
    "check_circle": '<circle cx="12" cy="12" r="8.5"/><path d="m8.2 12.3 2.6 2.7 5-5.8"/>',
    "alert_triangle": '<path d="M10.3 4.3a2 2 0 0 1 3.4 0l7.4 13.2a2 2 0 0 1-1.7 3H4.6a2 2 0 0 1-1.7-3z"/><path d="M12 9.5v4.2"/>' + DOT % (12, 17, 1.15),
    "x_circle": '<circle cx="12" cy="12" r="8.5"/><path d="m9.2 9.2 5.6 5.6M14.8 9.2l-5.6 5.6"/>',
    "help_circle": '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.4a2.5 2.5 0 0 1 4.9.6c0 1.7-2.5 2.1-2.5 3.7"/>' + DOT % (12, 16.6, 1.15),
    "spinner": '<path d="M12 3.5a8.5 8.5 0 1 1-6 2.5"/>',
    "bell": '<path d="M18 9.8a6 6 0 0 0-12 0c0 5.7-2.2 7.2-2.2 7.2h16.4S18 15.5 18 9.8z"/><path d="M10.1 20.4a2.2 2.2 0 0 0 3.8 0"/>',
    "bell_off": '<path d="M8.4 4.9A6 6 0 0 1 18 9.8c0 2.6.5 4.4 1 5.5"/><path d="M6.1 8.2A6 6 0 0 0 6 9.8C6 15.5 3.8 17 3.8 17h13"/><path d="M10.1 20.4a2.2 2.2 0 0 0 3.8 0"/>' + SLASH,

    # ------------------------------------------------------------ user (7)
    "user": '<circle cx="12" cy="8.2" r="3.9"/><path d="M4.5 20.4a7.5 7.5 0 0 1 15 0"/>',
    "users": '<circle cx="9.3" cy="8.2" r="3.7"/><path d="M2.5 20.2a6.8 6.8 0 0 1 13.6 0"/><path d="M16 4.9a3.7 3.7 0 0 1 0 6.6"/><path d="M17.8 14.2a6.6 6.6 0 0 1 3.7 6"/>',
    "user_add": '<circle cx="9.5" cy="8.2" r="3.9"/><path d="M2.5 20.4a7 7 0 0 1 14 0"/><path d="M18.5 7v6M15.5 10h6"/>',
    "avatar": '<circle cx="12" cy="12" r="8.7"/><circle cx="12" cy="9.8" r="3"/><path d="M6.3 18.7a6.3 6.3 0 0 1 11.4 0"/>',
    "login": '<path d="M13.5 3.5H18a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2h-4.5"/><path d="M4 12h9.5"/><path d="m10 8.5 3.5 3.5-3.5 3.5"/>',
    "logout": '<path d="M10.5 3.5H6a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h4.5"/><path d="M10.5 12H20"/><path d="m16.5 8.5 3.5 3.5-3.5 3.5"/>',
    "key": '<circle cx="7.8" cy="14.5" r="4.3"/><path d="m10.9 11.4 8.6-8.6"/><path d="m15.2 7.1 2.4 2.4"/><path d="m17.9 4.4 2.4 2.4"/>',

    # -------------------------------------------------------- commerce (13)
    "cart": DOT % (10, 20, 1.5) + DOT % (17.5, 20, 1.5) + '<path d="M2.5 3.5h2.7l2.6 11.6a1.6 1.6 0 0 0 1.6 1.3h8a1.6 1.6 0 0 0 1.6-1.3L20.5 7.5H6"/>',
    "cart_add": DOT % (10, 20, 1.5) + DOT % (17.5, 20, 1.5) + '<path d="M2.5 3.5h2.7l2.6 11.6a1.6 1.6 0 0 0 1.6 1.3h8a1.6 1.6 0 0 0 1.6-1.3l.4-1.8"/><path d="M17 4v6M14 7h6"/>',
    "tag": '<path d="M11.4 3.5H5a1.5 1.5 0 0 0-1.5 1.5v6.4a2 2 0 0 0 .6 1.4l7.2 7.2a2 2 0 0 0 2.8 0l6-6a2 2 0 0 0 0-2.8l-7.2-7.2a2 2 0 0 0-1.5-.5z"/><circle cx="8.2" cy="8.2" r="1.6"/>',
    "discount": '<path d="m6.5 17.5 11-11"/><circle cx="7.8" cy="7.8" r="2.4"/><circle cx="16.2" cy="16.2" r="2.4"/>',
    "credit_card": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19"/><path d="M6 14.5h3.5"/>',
    "truck": '<path d="M2.5 6.5h11v10h-11z"/><path d="M13.5 10h3.7l3.3 3.4v3.1h-7z"/><circle cx="7" cy="18.5" r="2"/><circle cx="17" cy="18.5" r="2"/>',
    "box": '<path d="m12 2.8 8.5 4.7v9L12 21.2 3.5 16.5v-9z"/><path d="m3.7 7.6 8.3 4.6 8.3-4.6"/><path d="M12 12.2v9"/>',
    "receipt": '<path d="M5.5 3.5h13v17l-2.2-1.5-2.2 1.5-2.1-1.5-2.2 1.5-2.2-1.5-2.1 1.5z"/><path d="M9 8.5h6M9 12.5h6"/>',
    "wallet": '<rect x="3" y="5.5" width="18" height="13.5" rx="2.5"/><path d="M3 10h18"/>' + DOT % (16.5, 14.5, 1.4),
    "store": '<path d="M4.5 10.5v9h15v-9"/><path d="M3 6.8 4.6 3.5h14.8L21 6.8a3 3 0 0 1-6 .2 3 3 0 0 1-6 0 3 3 0 0 1-6-.2z"/><path d="M9.8 19.5V14h4.4v5.5"/>',
    "rating_star": '<path d="m12 3.5 2.7 5.6 6.2.9-4.5 4.3 1.1 6.1L12 17.5l-5.5 2.9 1.1-6.1-4.5-4.3 6.2-.9z" fill="currentColor"/>',
    "rating_star_half": '<path d="m12 3.5 2.7 5.6 6.2.9-4.5 4.3 1.1 6.1L12 17.5l-5.5 2.9 1.1-6.1-4.5-4.3 6.2-.9z"/><path d="M12 3.5v14l-5.5 2.9 1.1-6.1-4.5-4.3 6.2-.9z" fill="currentColor"/>',
    "checkout": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19"/><path d="m12.8 15.2 2.2 2.3 4.5-5"/>',

    # --------------------------------------------------- communication (12)
    "mail": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="m3.6 6.8 7.2 5.1a2 2 0 0 0 2.4 0l7.2-5.1"/>',
    "mail_open": '<path d="M2.5 10.5 12 4l9.5 6.5v8a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2z"/><path d="m2.5 10.5 8.3 5.2a2 2 0 0 0 2.4 0l8.3-5.2"/>',
    "inbox": '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="M2.5 13.5H8a4 4 0 0 0 8 0h5.5"/>',
    "chat": '<path d="M20.5 12a7.6 7.6 0 0 1-11 6.8l-5.4 1.6 1.6-5.1A7.6 7.6 0 1 1 20.5 12z"/>',
    "comment": '<path d="M4.5 4.5h15a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H10l-5 4v-4h-.5a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2z"/>',
    "reply": '<path d="m8.5 5.5-6 6 6 6"/><path d="M2.5 11.5h10a9 9 0 0 1 9 9"/>',
    "phone": '<path d="M6.3 3.5h3.1l1.6 4.1-2.1 1.5a11.7 11.7 0 0 0 5.9 5.9l1.5-2.1 4.1 1.6v3.1a1.7 1.7 0 0 1-1.9 1.7C10.4 18.6 5.4 13.6 4.6 5.4a1.7 1.7 0 0 1 1.7-1.9z"/>',
    "phone_off": '<path d="M6.3 3.5h3.1l1.6 4.1-2.1 1.5a11.7 11.7 0 0 0 5.9 5.9l1.5-2.1 4.1 1.6v3.1a1.7 1.7 0 0 1-1.9 1.7C10.4 18.6 5.4 13.6 4.6 5.4a1.7 1.7 0 0 1 1.7-1.9z"/>' + SLASH,
    "video": '<rect x="2.5" y="5.8" width="13.5" height="12.4" rx="2.5"/><path d="m16 11.2 5.5-3.4v8.4L16 12.8z"/>',
    "mic": '<rect x="9" y="2.8" width="6" height="11" rx="3"/><path d="M5.8 11.5a6.2 6.2 0 0 0 12.4 0"/><path d="M12 17.8v3.4"/>',
    "mic_off": '<rect x="9" y="2.8" width="6" height="11" rx="3"/><path d="M5.8 11.5a6.2 6.2 0 0 0 12.4 0"/><path d="M12 17.8v3.4"/>' + SLASH,
    "at_sign": '<circle cx="12" cy="12" r="3.7"/><path d="M15.7 8.3v5a2.9 2.9 0 0 0 5.8 0V12A9.5 9.5 0 1 0 17.6 19.6"/>',

    # ----------------------------------------------------------- media (10)
    "play": '<path d="M7.5 4.8 19.2 12 7.5 19.2z"/>',
    "pause": '<path d="M9 4.5v15M15 4.5v15"/>',
    "stop": '<rect x="5" y="5" width="14" height="14" rx="2.5"/>',
    "skip_next": '<path d="M6 5.5 15 12l-9 6.5z"/><path d="M18.5 5.5v13"/>',
    "skip_prev": '<path d="M18 5.5 9 12l9 6.5z"/><path d="M5.5 5.5v13"/>',
    "volume_high": '<path d="M11 4.8 6.3 9H2.8v6h3.5L11 19.2z"/><path d="M14.8 9.2a4 4 0 0 1 0 5.6"/><path d="M17.6 6.4a8 8 0 0 1 0 11.2"/>',
    "volume_mute": '<path d="M11 4.8 6.3 9H2.8v6h3.5L11 19.2z"/><path d="m15.5 9.5 5 5M20.5 9.5l-5 5"/>',
    "image": '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><circle cx="8.4" cy="9.6" r="1.8"/><path d="m3.5 17.6 4.7-4.3a2 2 0 0 1 2.7 0l5 4.6"/><path d="m14.5 14.5 1.8-1.6a2 2 0 0 1 2.7 0l2.5 2.3"/>',
    "camera": '<path d="M3.5 8.5h3l1.6-2.6h7.8l1.6 2.6h3a1.5 1.5 0 0 1 1.5 1.5v8.5a1.5 1.5 0 0 1-1.5 1.5h-17A1.5 1.5 0 0 1 2 18.5V10a1.5 1.5 0 0 1 1.5-1.5z"/><circle cx="12" cy="13.8" r="3.6"/>',
    "film": '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="M7.2 4.5v15M16.8 4.5v15M2.5 12h19M2.5 8.2h4.7M2.5 15.8h4.7M16.8 8.2h4.7M16.8 15.8h4.7"/>',

    # ----------------------------------------------------- files & data (9)
    "file": '<path d="M13.5 3.5H7a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V9z"/><path d="M13.5 3.5V9H19"/>',
    "file_text": '<path d="M13.5 3.5H7a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V9z"/><path d="M13.5 3.5V9H19"/><path d="M8.5 13.5h7M8.5 16.5h4.5"/>',
    "folder": '<path d="M3.5 6.5a2 2 0 0 1 2-2h3.7l2 2.6h7.3a2 2 0 0 1 2 2v9.4a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/>',
    "folder_open": '<path d="M3.5 19.5V6.5a2 2 0 0 1 2-2h3.7l2 2.6h7.3a2 2 0 0 1 2 2v1.9"/><path d="M3.5 19.5 6.4 12h15.1l-2.9 7.5z"/>',
    "cloud": '<path d="M17.4 19H7a4.6 4.6 0 0 1-.6-9.2 6.1 6.1 0 0 1 11.7 1.8A4.1 4.1 0 0 1 17.4 19z"/>',
    "cloud_upload": '<path d="M17.4 18.5H7a4.6 4.6 0 0 1-.6-9.2 6.1 6.1 0 0 1 11.7 1.8 4.1 4.1 0 0 1-.7 7.4"/><path d="M12 20.5v-8"/><path d="m9 15.5 3-3 3 3"/>',
    "chart_bar": '<path d="M3.5 20.5h17"/><path d="M7 20.5v-6M12 20.5V7.5M17 20.5v-9"/>',
    "chart_pie": '<path d="M12 3.5A8.5 8.5 0 1 0 20.5 12H12z"/><path d="M15.2 3.9A8.5 8.5 0 0 1 20.1 8.8H15.2z"/>',
    "table": '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="M2.5 9.5h19M9.5 9.5v10M2.5 14.5h19"/>',

    # ------------------------------------------------------------ text (4)
    "list_bullet": '<path d="M9 6.5h11M9 12h11M9 17.5h11"/>' + DOT % (4.7, 6.5, 1.4) + DOT % (4.7, 12, 1.4) + DOT % (4.7, 17.5, 1.4),
    "list_ordered": '<path d="M9.5 6.5h11M9.5 12h11M9.5 17.5h11"/><path d="M3.2 5 4.6 4.2v3.6"/><path d="M3.2 10.9a1.3 1.3 0 1 1 2.1 1.5L3.2 14.4h2.3"/><path d="M3.3 16.3h2.2l-1.4 1.7a1.3 1.3 0 1 1-.6 2.3"/>',
    "code": '<path d="m8.5 8-4.5 4 4.5 4"/><path d="m15.5 8 4.5 4-4.5 4"/><path d="m13.5 4.5-3 15"/>',
    "quote": '<path d="M10 6.5C7 8 5.5 10.2 5.5 13v4.5H11V12H8.2c0-1.8.6-3.3 1.8-4.2z"/><path d="M19 6.5c-3 1.5-4.5 3.7-4.5 6.5v4.5H20V12h-2.8c0-1.8.6-3.3 1.8-4.2z"/>',

    # ------------------------------------------------------------ time (4)
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 6.8V12l3.4 2"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17"/><path d="M8 2.8v4M16 2.8v4"/>',
    "history": '<path d="M3.5 12a8.5 8.5 0 1 0 2.7-6.2"/><path d="M3.5 3.8v4.8h4.8"/><path d="M12 7.5V12l3.2 1.9"/>',
    "timer": '<circle cx="12" cy="13.8" r="7.4"/><path d="M12 9.8v4"/><path d="M9.5 2.8h5"/><path d="m18.6 7.2 1.6-1.6"/>',

    # -------------------------------------------------------- location (3)
    "map_pin": '<path d="M12 21.2c0 0 7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11z"/><circle cx="12" cy="10.2" r="2.7"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.7 9.5h16.6M3.7 14.5h16.6"/><path d="M12 3.5c4 4.7 4 12.3 0 17-4-4.7-4-12.3 0-17z"/>',
    "compass": '<circle cx="12" cy="12" r="8.5"/><path d="m15.6 8.4-2.1 5.1-5.1 2.1 2.1-5.1z"/>',

    # ----------------------------------------------- theme & a11y (4)
    "light_mode": '<circle cx="12" cy="12" r="4.2"/><path d="M12 2.8v2.4M12 18.8v2.4M21.2 12h-2.4M5.2 12H2.8M18.5 5.5l-1.7 1.7M7.2 16.8l-1.7 1.7M18.5 18.5l-1.7-1.7M7.2 7.2 5.5 5.5"/>',
    "dark_mode": '<path d="M20.4 14.3A8.8 8.8 0 0 1 9.7 3.6a8.8 8.8 0 1 0 10.7 10.7z"/>',
    "language": '<path d="M2.8 6.2h9.4"/><path d="M7.5 3.8v2.4"/><path d="M10.2 6.2c-.6 4.4-3.4 7.7-7.4 9"/><path d="M5 10.8c1.2 2.5 3.4 4.4 6 5.1"/><path d="m12.4 20.5 4.2-9.6 4.2 9.6"/><path d="M13.9 17.1h5.4"/>',
    "accessibility": '<circle cx="12" cy="12" r="8.5"/>' + DOT % (12, 7.9, 1.3) + '<path d="M8 10.5h8"/><path d="m10.2 10.5.7 3.3L9.2 18M13.8 10.5l-.7 3.3 1.7 4.2"/>',

    # ------------------------------------------------------- utility (10)
    "heart": '<path d="M12 20.3 4.7 13a4.8 4.8 0 0 1 6.8-6.8l.5.5.5-.5A4.8 4.8 0 0 1 19.3 13z"/>',
    "heart_filled": '<path d="M12 20.3 4.7 13a4.8 4.8 0 0 1 6.8-6.8l.5.5.5-.5A4.8 4.8 0 0 1 19.3 13z" fill="currentColor"/>',
    "star": '<path d="m12 3.5 2.7 5.6 6.2.9-4.5 4.3 1.1 6.1L12 17.5l-5.5 2.9 1.1-6.1-4.5-4.3 6.2-.9z"/>',
    "star_filled": '<path d="m12 3.5 2.7 5.6 6.2.9-4.5 4.3 1.1 6.1L12 17.5l-5.5 2.9 1.1-6.1-4.5-4.3 6.2-.9z" fill="currentColor"/>',
    "bookmark": '<path d="M6.5 3.5h11a1 1 0 0 1 1 1v16l-6.5-4.5-6.5 4.5v-16a1 1 0 0 1 1-1z"/>',
    "sparkles": '<path d="m11 3.5 1.7 4.6 4.6 1.7-4.6 1.7L11 16.1 9.3 11.5 4.7 9.8l4.6-1.7z"/><path d="m18 14.5.9 2.3 2.3.9-2.3.9-.9 2.3-.9-2.3-2.3-.9 2.3-.9z"/>',
    "paw": '<ellipse cx="6.8" cy="9.4" rx="2.1" ry="2.7"/><ellipse cx="10.5" cy="6.9" rx="2.2" ry="2.9"/><ellipse cx="14.6" cy="6.9" rx="2.2" ry="2.9"/><ellipse cx="18.2" cy="9.4" rx="2.1" ry="2.7"/><path d="M12.5 13c3.2 0 5.8 2.3 5.8 4.7s-2.6 3.6-5.8 3.6-5.8-1.2-5.8-3.6S9.3 13 12.5 13z"/>',
    "fire": '<path d="M12 21.2c3.7 0 6.6-2.6 6.6-6.1 0-4.6-4.5-6.1-4-11.1-2.6 1-4.1 3.5-4.1 6.1 0 1.5-1 2-1.9 1.2-.7-.7-1.2-1.9-1.2-3.2-1.5 1.5-2 4-2 7 0 3.5 2.9 6.1 6.6 6.1z"/>',
    "rocket": '<path d="M12 2.5c3.6 3.1 5.2 6.9 5.2 10.7l-2.6 3.1H9.4l-2.6-3.1C6.8 9.4 8.4 5.6 12 2.5z"/><circle cx="12" cy="10.2" r="2.1"/><path d="m9.4 16.3-2.6 2.6 1.6.5.5 1.6 2.1-2.6M14.6 16.3l2.6 2.6-1.6.5-.5 1.6-2.1-2.6"/>',

    # gestures — in this pack the hand is a paw
    "thumbs_up": _THUMB,
    "thumbs_down": f'<g transform="rotate(180 12 12)">{_THUMB}</g>',
    "wave": '<g transform="rotate(-12 11 15)">'
            '<path d="M11 21.3a5.6 5.6 0 0 1-5.6-5.6v-2.1a5.6 5.6 0 0 1 11.2 0v2.1a5.6 5.6 0 0 1-5.6 5.6z"/>'
            + toes((7.3, 8.8), (11, 7.4), (14.7, 8.8)) + '</g>'
            '<path d="M18.6 9.4a6.6 6.6 0 0 1 0 7.4"/><path d="M21 7.2a10 10 0 0 1 0 11.8"/>',
    "point": '<rect x="9.9" y="2.9" width="4.3" height="9.6" rx="2.15"/>'
             '<path d="M6.8 14.4a2.7 2.7 0 0 1 2.7-2.7h4.8a5 5 0 0 1 5 5v0.9a4.8 4.8 0 0 1-4.8 4.8h-3.6'
             'a4.1 4.1 0 0 1-4.1-4.1z"/>'
             '<ellipse cx="5.2" cy="15.4" rx="1.9" ry="2.5"/>',
    "tap": '<rect x="9.9" y="6.4" width="4.3" height="7.1" rx="2.15"/>'
           '<path d="M6.8 15.4a2.7 2.7 0 0 1 2.7-2.7h4.8a5 5 0 0 1 5 5v0.4a4.8 4.8 0 0 1-4.8 4.8h-3.6'
           'a4.1 4.1 0 0 1-4.1-4.1z"/>'
           '<path d="M5.6 6.4A8 8 0 0 1 7.8 2.9"/><path d="M18.4 6.4A8 8 0 0 0 16.2 2.9"/>',
    "grab": '<path d="M5.6 14.8a6.4 6.4 0 0 1 12.8 0v1.8a4.8 4.8 0 0 1-4.8 4.8h-3.2a4.8 4.8 0 0 1-4.8-4.8z"/>'
            '<path d="M8.2 13.2V9.9a2 2 0 0 1 4 0v3.3"/>'
            '<path d="M12.2 13.2V9.3a2 2 0 0 1 4 0v3.9"/>',
    "clap": '<g transform="rotate(-24 7.4 16)"><ellipse cx="7.4" cy="16" rx="4.1" ry="5.2"/></g>'
            '<g transform="rotate(24 16.6 16)"><ellipse cx="16.6" cy="16" rx="4.1" ry="5.2"/></g>'
            '<path d="M12 3.2v2.6M6.9 4.3l1.2 2.3M17.1 4.3l-1.2 2.3"/>',
    "peace": '<rect x="6.6" y="3.2" width="3.9" height="9.4" rx="1.95" transform="rotate(-15 8.5 7.9)"/>'
             '<rect x="13.5" y="3.2" width="3.9" height="9.4" rx="1.95" transform="rotate(15 15.4 7.9)"/>'
             '<path d="M6.4 14.6A2.6 2.6 0 0 1 9 12h6a4.6 4.6 0 0 1 4.6 4.6 4.6 4.6 0 0 1-4.6 4.6h-4.3'
             'a4.3 4.3 0 0 1-4.3-4.3z"/>',
    "heart_hands": '<path d="M12 20.6 6.6 15.2a3.8 3.8 0 0 1 5.4-5.3 3.8 3.8 0 0 1 5.4 5.3z"/>'
                   '<g transform="rotate(-32 4.4 12.8)"><ellipse cx="4.4" cy="12.8" rx="2.6" ry="3.4"/></g>'
                   '<g transform="rotate(32 19.6 12.8)"><ellipse cx="19.6" cy="12.8" rx="2.6" ry="3.4"/></g>',
    "swipe": '<path d="M12 21.4a5.2 5.2 0 0 1-5.2-5.2v-1.4a5.2 5.2 0 0 1 10.4 0v1.4a5.2 5.2 0 0 1-5.2 5.2z"/>'
             + toes((8.6, 10.6, 1.5, 1.9), (12, 9.6, 1.5, 1.9), (15.4, 10.6, 1.5, 1.9))
             + '<path d="M4 3.9h13.2"/><path d="m14.5 1.2 2.9 2.7-2.9 2.7"/>',


    # -------------------------------------------------- deco & sparkle (12)
    "star_burst": _star(),
    "twinkle": '<path d="M7.8 3.2q.9 3.7 4.3 4.5-3.4 1-4.3 4.5-.9-3.5-4.3-4.5 3.4-.8 4.3-4.5z"/>'
               '<path d="M16.2 10.2q1 4.3 4.8 5.2-3.8 1.1-4.8 5.2-1-4.1-4.8-5.2 3.8-.9 4.8-5.2z"/>'
               '<circle cx="5.2" cy="17.8" r="1.6"/>',
    "confetti": '<rect x="3.6" y="4.2" width="3" height="4.8" rx="1.5" transform="rotate(-24 5.1 6.6)"/>'
                '<rect x="17" y="5.8" width="3" height="4.8" rx="1.5" transform="rotate(28 18.5 8.2)"/>'
                '<rect x="10.4" y="14.6" width="3" height="4.8" rx="1.5" transform="rotate(-14 11.9 17)"/>'
                + DOT % (12, 5.4, 1.3) + DOT % (4.8, 14.6, 1.3) + DOT % (19.2, 17.2, 1.3),
    "party_popper": '<path d="M3.4 20.6 9.4 8.4l6.2 6.2z"/>'
                    '<path d="M15.4 8.4a3.2 3.2 0 0 1 4.4-4.4"/>'
                    '<path d="M18.6 12.4h3M13.4 4.4v-3M20.2 8.8l1.8-1.8"/>' + DOT % (17.6, 17.8, 1.2),
    "bow": '<path d="M11 12 4.4 7.8v8.4z"/><path d="M13 12l6.6-4.2v8.4z"/><circle cx="12" cy="12" r="2"/>',
    "balloon": '<ellipse cx="12" cy="9.6" rx="6.2" ry="7"/>'
               '<path d="m10.6 15.8 1.4 2 1.4-2"/><path d="M12 17.8c0 2 2.4 2 2.4 4.2"/>',
    "gift": '<rect x="3.6" y="10.4" width="16.8" height="10.2" rx="2"/>'
            '<rect x="2.6" y="6.6" width="18.8" height="3.8" rx="1.4"/><path d="M12 6.6v14"/>'
            '<path d="M12 6.6C9.6 6.6 7.4 5.6 7.4 4.2a2.1 2.1 0 0 1 4.2-.4L12 6.6l.4-2.8a2.1 2.1 0 0 1 4.2.4c0 1.4-2.2 2.4-4.6 2.4z"/>',
    "crown": '<path d="m3.4 17.6 1.5-10.4 4.1 3.8L12 5.4l3 5.6 4.1-3.8 1.5 10.4z"/>'
             '<path d="M4.6 20.6h14.8"/>' + DOT % (12, 8.6, 1.1),
    "gem": '<path d="m12 21.2-8.4-9.8L7.4 4.8h9.2l3.8 6.6z"/><path d="M3.6 11.4h16.8"/>'
           '<path d="m7.4 4.8 4.6 16.4 4.6-16.4"/>',
    "rainbow": '<path d="M3.4 18.6a8.6 8.6 0 0 1 17.2 0"/><path d="M7 18.6a5 5 0 0 1 10 0"/>'
               '<path d="M10.6 18.6a1.4 1.4 0 0 1 2.8 0"/>',
    "heart_pop": '<path d="M12 18.8 6.6 13.4a3.8 3.8 0 0 1 5.4-5.3 3.8 3.8 0 0 1 5.4 5.3z"/>'
                 '<path d="M12 4.6V2.4M5.2 7.4 3.6 5.8M18.8 7.4l1.6-1.6M3.6 13.4H1.8M20.4 13.4h1.8"/>',
    "wand": '<path d="m3.4 20.6 9.4-9.4"/>' + _star(4, 5.2, 1.9, 16.6, 7.4)
            + '<path d="M20.6 13.2v2.6M19.3 14.5h2.6M8.2 3.4V6M6.9 4.7h2.6"/>',

    # ------------------------------------------------------ emote marks (10)
    "blush": '<ellipse cx="6.6" cy="12" rx="4" ry="3"/><ellipse cx="17.4" cy="12" rx="4" ry="3"/>'
             '<path d="m4.8 13.4 1.6-2.8M7 13.4l1.6-2.8M15.6 13.4l1.6-2.8M17.8 13.4l1.6-2.8" stroke-width="1.6"/>',
    "sweat_drop": '<path d="M12 3.2c-4.2 6.3-6.3 9.4-6.3 11.9a6.3 6.3 0 0 0 12.6 0c0-2.5-2.1-5.6-6.3-11.9z"/>',
    "anger_vein": '<path d="m5.6 10.4 6.4-6.4 6.4 6.4"/><path d="m5.6 18.4 6.4-6.4 6.4 6.4"/>',
    "zzz": '<path d="M3.4 15.4h5.2l-5.2 5.6h5.2"/><path d="M10.4 8.6h5.4l-5.4 5.8h5.4"/>'
           '<path d="M17 3h4.6l-4.6 5h4.6"/>',
    "music_note": '<path d="M9.4 18V5.8l9.2-2.2V16"/><ellipse cx="6.4" cy="18" rx="3" ry="2.5"/>'
                  '<ellipse cx="15.6" cy="16" rx="3" ry="2.5"/>',
    "spark_lines": '<path d="M12 2.6v4.2M12 17.2v4.2M2.6 12h4.2M17.2 12h4.2"/>'
                   '<path d="m5.6 5.6 2.6 2.6M15.8 15.8l2.6 2.6M18.4 5.6l-2.6 2.6M8.2 15.8l-2.6 2.6"/>',
    "heartbeat": '<path d="M12 20.6 6.4 15a3.9 3.9 0 0 1 5.6-5.5 3.9 3.9 0 0 1 5.6 5.5z"/>'
                 '<path d="M7.4 13.4h1.9l1.3-2.6 1.9 5 1.4-2.4h2.7" stroke-width="1.8"/>',
    "dizzy": _spiral(),
    "pop": '<path d="M12 3.6v3.4M12 17v3.4M3.6 12H7M17 12h3.4"/>'
           '<path d="m6.4 6.4 2.4 2.4M15.2 15.2l2.4 2.4M17.6 6.4 15.2 8.8M8.8 15.2l-2.4 2.4"/>',
    "exclaim": '<path d="M12 3.6v10.2" stroke-width="2.6"/>' + DOT % (12, 19, 1.7),

    # -------------------------------------------------- food & drink (12)
    "cupcake": '<path d="M6.4 13.8h11.2l-1.1 6a1.8 1.8 0 0 1-1.8 1.4H9.3a1.8 1.8 0 0 1-1.8-1.4z"/>'
               '<path d="M6.2 13.8a3.2 3.2 0 0 1 .8-5.7 4.1 4.1 0 0 1 7.6-1.8 3.3 3.3 0 0 1 3.2 7.5z"/>',
    "donut": '<circle cx="12" cy="12" r="8.8"/>'
             '<path d="M8.4 5.6 7 7M16 6.2l1.2 1.6M4.8 15.4l1.8-.6M18.4 16.2l-1.8-.8" stroke-width="1.7"/>',
    "ice_cream": '<path d="m12 21.4-4.6-8.6h9.2z"/><circle cx="9.2" cy="9.4" r="3.5"/>'
                 '<circle cx="14.8" cy="9.4" r="3.5"/><circle cx="12" cy="6" r="3.3"/>',
    "cookie": '<circle cx="12" cy="12" r="8.8"/>' + DOT % (6.6, 8.6, 1.2) + DOT % (17, 9.4, 1.2)
              + DOT % (7.4, 16.4, 1.2) + DOT % (16.6, 16, 1),
    "cake": '<path d="M3.8 20.6v-6.2a2.2 2.2 0 0 1 2.2-2.2h12a2.2 2.2 0 0 1 2.2 2.2v6.2z"/>'
            '<path d="M3.8 16.6h16.4"/><path d="M12 12.2V9.2"/>'
            '<path d="M12 9.2c1.5-1.5 0-2.8 0-2.8s-1.5 1.3 0 2.8z"/>',
    "candy": '<ellipse cx="12" cy="12" rx="5.2" ry="4.4"/><path d="M6.8 12 2.6 8.8v6.4z"/>'
             '<path d="M17.2 12l4.2-3.2v6.4z"/>',
    "lollipop": '<circle cx="13.4" cy="8.6" r="5.8"/>'
                '<path d="M13.4 8.6a2 2 0 0 1 2.1 2.1 3.7 3.7 0 0 1-5.8.4" stroke-width="1.7"/>'
                '<path d="M9.6 12.8 3.6 20.6"/>',
    "boba": '<path d="M6.4 8.8h11.2l-1.2 10.8a2.2 2.2 0 0 1-2.2 2h-4.4a2.2 2.2 0 0 1-2.2-2z"/>'
            '<path d="M5.2 8.8h13.6"/><path d="m14 8.8 3-5.4"/>' + DOT % (10, 17.6, 1.3)
            + DOT % (13.6, 18, 1.3) + DOT % (11.9, 14.6, 1.3),
    "coffee": '<path d="M4.4 9.4h11.8v6.2a4.2 4.2 0 0 1-4.2 4.2H8.6a4.2 4.2 0 0 1-4.2-4.2z"/>'
              '<path d="M16.2 10.8h1.9a2.7 2.7 0 0 1 0 5.4h-1.9"/>'
              '<path d="M8.2 6V3.6M12.4 6V3.6"/>',
    "teapot": '<path d="M5.4 11.4h11.4v3.8a4.8 4.8 0 0 1-4.8 4.8h-1.8a4.8 4.8 0 0 1-4.8-4.8z"/>'
              '<path d="M16.8 13c2.4-.4 3.8-1.8 3.8-3.8"/><path d="M5.4 13.4c-1.9.2-2.9 1.1-2.9 2.6"/>'
              '<path d="M8.2 11.4a3.9 3.9 0 0 1 7.8 0"/><circle cx="12.1" cy="6.6" r="1.4"/>',
    "milk": '<path d="M7 9.6 12 4.6l5 5v9.8a1.8 1.8 0 0 1-1.8 1.8H8.8A1.8 1.8 0 0 1 7 19.4z"/>'
            '<path d="M7 9.6h10"/><path d="M12 4.6v5"/>',
    "strawberry": '<path d="M12 21.4c-3.9-1.7-6.5-4.9-6.5-8.4A6.5 6.5 0 0 1 12 6.6a6.5 6.5 0 0 1 6.5 6.4c0 3.5-2.6 6.7-6.5 8.4z"/>'
                  '<path d="M8.4 7.2 12 3.6l3.6 3.6"/>' + DOT % (7.4, 17, 0.9) + DOT % (16.6, 17, 0.9),

    # ---------------------------------------------------------- nature (10)
    "sun_face": '<circle cx="12" cy="12" r="6.2"/>'
                '<path d="M12 2.4v2.2M12 19.4v2.2M2.4 12h2.2M19.4 12h2.2"/>'
                '<path d="m5.2 5.2 1.6 1.6M17.2 17.2l1.6 1.6M18.8 5.2l-1.6 1.6M6.8 17.2l-1.6 1.6"/>',
    "moon_face": '<path d="M20.6 14.4A8.8 8.8 0 0 1 9.6 3.4a8.8 8.8 0 1 0 11 11z"/>',
    "flower": _petals(),
    "tulip": '<path d="M7.8 7c0 4.2 1.9 6.9 4.2 6.9s4.2-2.7 4.2-6.9c0 0-1.7 1.9-2.7 1.9S12 7 12 7s-.4 1.9-1.5 1.9S7.8 7 7.8 7z"/>'
             '<path d="M12 14v7.2"/><path d="M12 18.4c-2.5 0-4.2-1.7-4.2-4.2 2.5 0 4.2 1.7 4.2 4.2z"/>',
    "leaf": '<path d="M20.6 3.4C9.6 3.4 3.4 9 3.4 16.4a5.2 5.2 0 0 0 .9 3S9 10.2 20.6 3.4z"/>'
            '<path d="M4.3 19.4C9 10.2 20.6 3.4 20.6 3.4"/>',
    "sprout": '<path d="M12 21.4v-7.2"/>'
              '<path d="M12 14.2c0-3.5 2.7-6.2 6.2-6.2 0 3.5-2.7 6.2-6.2 6.2z"/>'
              '<path d="M12 16.4c-3.1 0-5.6-2.5-5.6-5.6 3.1 0 5.6 2.5 5.6 5.6z"/>',
    "mushroom": '<path d="M3.4 11.6a8.6 8.6 0 0 1 17.2 0z"/>'
                '<path d="M8.8 11.6v6.2a3.2 3.2 0 0 0 6.4 0v-6.2"/>'
                + DOT % (8.2, 8.4, 1.2) + DOT % (14.6, 7.8, 1.4),
    "snowflake": '<path d="M12 2.6v18.8M4 7.3l16 9.4M20 7.3 4 16.7"/>'
                 '<path d="M9.4 5.2 12 7.8l2.6-2.6M9.4 18.8 12 16.2l2.6 2.6" stroke-width="1.8"/>',
    "star_night": '<path d="M19.6 14.8A8 8 0 0 1 9.2 4.4a8 8 0 1 0 10.4 10.4z"/>'
                  + _star(4, 3, 1.1, 18.4, 5.4) + _star(4, 2.2, 0.8, 13.6, 3.4),
    "cactus": '<rect x="9.6" y="5.4" width="4.8" height="15.2" rx="2.4"/>'
              '<path d="M9.6 13.4H8a2.4 2.4 0 0 1-2.4-2.4V9.2"/>'
              '<path d="M14.4 15.4H16a2.4 2.4 0 0 0 2.4-2.4v-2.8"/>',

    # ------------------------------------------------ bubbles & frames (6)
    "bubble_cloud": '<path d="M17 16.6H7.4a4.4 4.4 0 0 1-.6-8.8 5.8 5.8 0 0 1 11.1 1.7 3.9 3.9 0 0 1-.9 7.1z"/>'
                    '<circle cx="8.4" cy="19.4" r="1.7"/><circle cx="4.8" cy="21.4" r="1"/>',
    "bubble_heart": '<path d="M12 17.4 5.8 11.2a4.4 4.4 0 0 1 6.2-6.2 4.4 4.4 0 0 1 6.2 6.2z"/>'
                    '<circle cx="8.6" cy="19.6" r="1.7"/><circle cx="5" cy="21.6" r="1"/>',
    "bubble_star": _star(10, 9.8, 6.6),
    "sticker": _scallop(),
    "ticket": '<path d="M2.8 7.4h18.4v3a2.1 2.1 0 0 0 0 4.2v3H2.8v-3a2.1 2.1 0 0 0 0-4.2z"/>'
              '<path d="M12 8.8v1.8M12 13.2V15M12 17.6v1.8" stroke-width="1.8"/>',
    "frame_cloud": '<path d="M6.6 18.6a4.6 4.6 0 0 1-.7-9.1 6 6 0 0 1 11.5-.4 4.4 4.4 0 0 1 .3 8.7z"/>'
                   '<path d="M9.4 13.8h5.2" stroke-width="1.8"/>',

    # ---------------------------------------------------- doodle arrows (6)
    "arrow_curly_right": '<path d="M2.8 18.6C6.4 11 11.4 7.8 18.4 8"/><path d="m14.6 3.8 4.6 4.2-4.6 4.4"/>',
    "arrow_curly_left": '<g transform="scale(-1 1) translate(-24 0)">'
                        '<path d="M2.8 18.6C6.4 11 11.4 7.8 18.4 8"/><path d="m14.6 3.8 4.6 4.2-4.6 4.4"/></g>',
    "arrow_loop": '<path d="M3.6 20.4c0-7.6 3.8-12.4 8.4-12.4 3.2 0 5.4 2.2 5.4 4.8s-2 4.4-4 4.4-3.2-1.4-3.2-3 1.2-2.6 2.4-2.6"/>'
                  '<path d="m14.4 3.6 4.4 4.4-4.4 4.4"/>',
    "arrow_doodle_down": '<path d="M7.6 3.4c6.8 2.6 9.6 8 8 15.6"/><path d="m10.6 15.4 5 4.2 4.2-4.8"/>',
    "squiggle": '<path d="M2.6 12q2.7-5 5.3 0t5.3 0 5.3 0"/>',
    "divider_hearts": _heart(5.6, 8.6, 0.55) + _heart(12, 8.6, 0.72) + _heart(18.4, 8.6, 0.55)
                      + '<path d="M2.6 17h18.8" stroke-width="1.8"/>',

    # ----------------------------------------------------- rating faces (5)
    "rate_1": _rating('<path d="M8.6 17q3.4-3.4 6.8 0"/>'),
    "rate_2": _rating('<path d="M8.8 16.2q3.2-1.8 6.4 0"/>'),
    "rate_3": _rating('<path d="M9 15.8h6"/>'),
    "rate_4": _rating('<path d="M8.8 14.6q3.2 3 6.4 0"/>'),
    "rate_5": _rating('<path d="M8.2 14q3.8 4.4 7.6 0z"/>', happy_eyes=True, blush=True),

    # --------------------------------------------------------- paw extras (2)
    "paw_prints": _pawprint(6.4, 17.6, 0.85) + _pawprint(12, 11.6, 0.85) + _pawprint(17.6, 5.6, 0.85),
    "paw_heart": '<path d="M12 21.2c-3.4-2.6-5.6-4.6-5.6-6.8A3.2 3.2 0 0 1 12 12a3.2 3.2 0 0 1 5.6 2.4c0 2.2-2.2 4.2-5.6 6.8z"/>'
                 + toes((5.6, 8.4, 1.7, 2.2), (9.8, 6.4, 1.7, 2.3), (14.2, 6.4, 1.7, 2.3), (18.4, 8.4, 1.7, 2.2)),
    "high_five": '<g transform="rotate(-22 7 14)"><path d="M7 20.4a4.4 4.4 0 0 1-4.4-4.4v-1.8a4.4 4.4 0 1 1 8.8 0V16a4.4 4.4 0 0 1-4.4 4.4z"/>'
                 + toes((4.6, 8.8, 1.4, 1.9), (7.6, 8.2, 1.4, 1.9), (10.4, 9, 1.4, 1.9)) + '</g>'
                 '<g transform="rotate(22 17 14)"><path d="M17 20.4a4.4 4.4 0 0 1-4.4-4.4v-1.8a4.4 4.4 0 1 1 8.8 0V16a4.4 4.4 0 0 1-4.4 4.4z"/>'
                 + toes((13.6, 9, 1.4, 1.9), (16.4, 8.2, 1.4, 1.9), (19.4, 8.8, 1.4, 1.9)) + '</g>',
}

# Preview groups: (title, first icon of the group), in UI_ICONS order.
GROUP_MARKERS = [
    ("Navigation", "home"), ("Actions", "search"), ("Visibility", "eye"),
    ("Forms", "checkbox_on"), ("Feedback", "info"), ("Users", "user"),
    ("Commerce", "cart"), ("Communication", "mail"), ("Media", "play"),
    ("Files & data", "file"), ("Text", "list_bullet"), ("Time", "clock"),
    ("Location", "map_pin"), ("Theme & accessibility", "light_mode"),
    ("Utility", "heart"), ("Gestures", "thumbs_up"), ("Deco & sparkle", "star_burst"),
    ("Emote marks", "blush"), ("Food & drink", "cupcake"), ("Nature", "sun_face"),
    ("Bubbles & frames", "bubble_cloud"), ("Doodle arrows", "arrow_curly_right"),
    ("Rating faces", "rate_1"), ("Paw extras", "paw_prints"),
]


def groups():
    """[(title, [names])] — every icon lands in exactly one group."""
    names = list(UI_ICONS)
    starts = {n: t for t, n in GROUP_MARKERS}
    out, title = [], None
    for n in names:
        if n in starts:
            title = starts[n]
            out.append((title, []))
        out[-1][1].append(n)
    assert sum(len(g[1]) for g in out) == len(names), "an icon fell outside every group"
    return out


WRAPPER = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
           'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
           'stroke-linejoin="round" role="img" aria-labelledby="t-{name}">\n'
           '  <title id="t-{name}">{label}</title>\n  {body}\n</svg>\n')


def render(name, with_face=True):
    """`with_face=False` emits the *_plain variant — the face blurs below ~20px."""
    key = name[:-6] if name.endswith("_plain") else name
    label = name.replace("_", " ").capitalize()
    body = UI_ICONS[key]
    if with_face and key in FACES:
        body += face(*FACES[key])
    return WRAPPER.format(name=name, label=label, body=body)


if __name__ == "__main__":
    print(f"{len(UI_ICONS)} UI icons defined")
