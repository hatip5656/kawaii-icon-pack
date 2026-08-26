#!/usr/bin/env python3
"""Hand gestures, drawn with each species' actual hand anatomy.

This family is the one place in the pack where a paw is big enough (256 canvas)
to show how the animal is really built, so it does:

    red_panda  5 digits, semi-retractable claws, plus the false thumb — an
               enlarged wrist bone — it grips bamboo with
    panda      5 digits and the famous pseudo-thumb, heavy blunt claws
    raccoon    5 long dexterous fingers, the longest in the pack, fine claws
    hamster    4 slender fingers and a thumb stub, small pale nails
    rabbit     4 furred digits, blunt non-retractable claws, narrow paw
    owl        no hands at all. Wing (coverts + primaries, serrated leading
               edge) for anything you would do with an open hand; zygodactyl
               talon — two toes forward, two back — for grasping and pointing.
               Its "thumbs up" raises the alula, the thumb a bird actually has.

Public contract used by build_icons.py: PALETTE, GESTURE_ORDER, GESTURE_LABELS,
render(animal, kind, label).
"""

PALETTE = {
    "red_panda": {
        "fur": "#E97A4E", "pad": "#FFF4E8", "line": "#C9552E", "key": None,
        "edge": "#C9552E", "claw": "#7A3419",
        "digits": 5, "flen": 76, "fw": 29, "spread": 22, "pw": 126,
        "claw_len": 1.0, "thumb": ("false", 0.46, -58, 1.0),
    },
    "rabbit": {
        "fur": "#FDFBFF", "pad": "#FFC2D1", "line": "#B9AFC9", "key": "#E4E0F0",
        "edge": "#E4E0F0", "claw": "#CFC7DE",
        "digits": 4, "flen": 64, "fw": 29, "spread": 18, "pw": 122,
        "claw_len": 0.55, "thumb": ("dewclaw", 0.24, -72, 0.62),
    },
    "panda": {
        "fur": "#3A3335", "pad": "#FF9EB5", "line": "#3A3335", "key": None,
        "edge": "#5C5054", "claw": "#1C1819",
        "digits": 5, "flen": 72, "fw": 32, "spread": 20, "pw": 138,
        "claw_len": 1.15, "thumb": ("pseudo", 0.52, -62, 1.18),
    },
    "hamster": {
        "fur": "#F5C377", "pad": "#FFC3C9", "line": "#D89A4E", "key": None,
        "edge": "#D89A4E", "claw": "#B07C3C",
        "digits": 4, "flen": 88, "fw": 21, "spread": 21, "pw": 112,
        "claw_len": 0.6, "thumb": ("stub", 0.32, -62, 1.0),
    },
    "raccoon": {
        "fur": "#A7AEBC", "pad": "#FFC2D1", "line": "#7D8492", "key": None,
        "edge": "#7D8492", "claw": "#4E5561",
        "digits": 5, "flen": 98, "fw": 23, "spread": 24, "pw": 118,
        "claw_len": 0.85, "thumb": ("long", 0.62, -52, 0.95),
    },
    "owl": {
        "fur": "#9C8AD1", "pad": "#FFF3DE", "line": "#7E6BB8", "key": None,
        "edge": "#7E6BB8", "claw": "#3A3335", "quill": "#8878C2",
        "toe": "#E0A96A", "wing": True,
    },
}

GESTURE_ORDER = ["high_five", "wave", "thumbs_up", "point", "tap",
                 "grab", "clap", "peace", "heart_hands", "swipe"]

GESTURE_LABELS = {
    "high_five": "High five", "wave": "Wave", "thumbs_up": "Thumbs up", "point": "Point",
    "tap": "Tap", "grab": "Grab", "clap": "Clap", "peace": "Peace",
    "heart_hands": "Heart hands", "swipe": "Swipe",
}

PALM_TOP = 138          # knuckle line
PALM_BOTTOM = 230       # heel of the palm
KNUCKLE = PALM_TOP + 14  # fingers are rooted just inside the palm


# ------------------------------------------------------------------ pieces

def _fur(p, extra=""):
    a = f'fill="{p["fur"]}" stroke="{p["edge"]}" stroke-width="5" stroke-linejoin="round"'
    return f"{a} {extra}" if extra else a


def _layout(p):
    """(x offset, angle, length multiplier) per digit, thumb excluded."""
    n, s, pw = p["digits"], p["spread"], p["pw"]
    if n == 5:
        return list(zip((-0.36, -0.18, 0.0, 0.18, 0.36),
                        (-s, -s * 0.45, 0, s * 0.45, s),
                        (0.76, 0.93, 1.0, 0.92, 0.74)))
    return list(zip((-0.30, -0.10, 0.10, 0.30),
                    (-s, -s * 0.33, s * 0.33, s),
                    (0.84, 1.0, 0.95, 0.78)))


def _finger(p, cx, angle, length, width=None, claw=True, pad=True):
    """One digit rooted at the knuckle line, with its claw and finger pad.

    Everything shares a single rotate group — three copies of the same
    transform is most of what a paw icon used to weigh.
    """
    w = width or p["fw"]
    top = KNUCKLE - length
    cl = p.get("claw_len", 1.0)
    parts = [f'<rect x="{cx - w / 2:.4g}" y="{top:.4g}" width="{w:.4g}" '
             f'height="{length + 18:.4g}" rx="{w / 2:.4g}" {_fur(p)}/>',
             f'<circle cx="{cx:.4g}" cy="{top + w * 0.5:.4g}" r="{w * 0.5:.4g}" {_fur(p)}/>']
    if claw:
        parts.append(f'<path d="M{cx - w * 0.34:.4g} {top + 3:.4g}'
                     f'q{w * 0.34:.4g}{-19 * cl:.4g} {w * 0.68:.4g} 0z" fill="{p["claw"]}"/>')
    if pad:
        parts.append(f'<ellipse cx="{cx:.4g}" cy="{top + w * 0.62:.4g}" '
                     f'rx="{w * 0.32:.4g}" ry="{w * 0.38:.4g}" fill="{p["pad"]}"/>')
    return (f'<g transform="rotate({angle:.4g} {cx:.4g} {KNUCKLE})">'
            + "".join(parts) + "</g>")


def _knuckles(p):
    """Curled fingers seen end-on — the row of bumps on top of a fist."""
    w = p["fw"]
    out = []
    for dx, _, _ in _layout(p):
        cx = 128 + dx * p["pw"]
        out.append(f'<rect x="{cx - w / 2:.4g}" y="{PALM_TOP - w * 1.05:.4g}" width="{w:.4g}" '
                   f'height="{w * 1.75:.4g}" rx="{w / 2:.4g}" {_fur(p)}/>')
    return "".join(out)


def _palm(p):
    """Wide across the knuckles, tapering to a rounded heel — not a brick."""
    hw = p["pw"] / 2
    hb = hw * 0.86
    top, bot = PALM_TOP - 10, PALM_BOTTOM + 4
    d = (f'M{128 - hw:.4g} {top + 22:.4g}'
         f'C{128 - hw:.4g} {top:.4g} {128 - hw + 14:.4g} {top:.4g} {128 - hw + 28:.4g} {top:.4g}'
         f'H{128 + hw - 28:.4g}'
         f'C{128 + hw - 14:.4g} {top:.4g} {128 + hw:.4g} {top:.4g} {128 + hw:.4g} {top + 22:.4g}'
         f'C{128 + hw:.4g} {top + 76:.4g} {128 + hb:.4g} {bot:.4g} 128 {bot:.4g}'
         f'C{128 - hb:.4g} {bot:.4g} {128 - hw:.4g} {top + 76:.4g} {128 - hw:.4g} {top + 22:.4g}Z')
    return (f'<path d="{d}" {_fur(p)}/>'
            f'<ellipse cx="128" cy="{PALM_TOP + 50:.4g}" rx="{p["pw"] * 0.31:.4g}" ry="31" '
            f'fill="{p["pad"]}"/>')


def _thumb(p, raised=False, side=-1):
    kind, ratio, angle, wr = p["thumb"]
    w = p["fw"] * wr * (1.4 if raised else 1.0)
    length = p["flen"] * (1.05 if raised else ratio)
    angle = -10 * side if raised else angle * -side
    cx = 128 + side * p["pw"] * (0.40 if kind != "dewclaw" else 0.46)
    root = KNUCKLE + (34 if not raised else 2)
    top = root - length
    spin = f'<g transform="rotate({angle:.4g} {cx:.4g} {root:.4g})">'
    out = [f'{spin}<rect x="{cx - w / 2:.4g}" y="{top:.4g}" width="{w:.4g}" '
           f'height="{length + 16:.4g}" rx="{w / 2:.4g}" {_fur(p)}/></g>']
    if kind not in ("dewclaw", "stub") or raised:
        out.append(f'{spin}<ellipse cx="{cx:.4g}" cy="{top + w * 0.66:.4g}" '
                   f'rx="{w * 0.32:.4g}" ry="{w * 0.38:.4g}" fill="{p["pad"]}"/></g>')
    return "".join(out)


def _place(art, x, y, rot=0, scale=1.0):
    """Drop a hand (drawn around 128,184) so its palm lands on x,y."""
    return (f'<g transform="translate({x} {y}) rotate({rot:.4g}) scale({scale:.4g}) '
            f'translate(-128 -184)">{art}</g>')


def _curl_finger(p, cx, angle, length):
    """A digit hooked over toward the palm — what a grasping paw actually does."""
    w = p["fw"]
    prox = length * 0.62
    inward = 52 if cx <= 128 else -52
    return (f'<g transform="rotate({angle:.4g} {cx:.4g} {KNUCKLE})">'
            f'<rect x="{cx - w / 2:.4g}" y="{KNUCKLE - prox:.4g}" width="{w:.4g}" '
            f'height="{prox + 18:.4g}" rx="{w / 2:.4g}" {_fur(p)}/>'
            f'<g transform="translate({cx:.4g} {KNUCKLE - prox:.4g}) rotate({inward})">'
            f'<rect x="{-w / 2:.4g}" y="{-length * 0.54:.4g}" width="{w:.4g}" '
            f'height="{length * 0.54 + w * 0.6:.4g}" rx="{w / 2:.4g}" {_fur(p)}/>'
            f'<path d="M{-w * 0.34:.4g} {-length * 0.54 + 4:.4g}'
            f'q{w * 0.34:.4g}-14 {w * 0.68:.4g} 0z" fill="{p["claw"]}"/>'
            '</g></g>')


def _hand(p, pose):
    """One upright hand.

    Extended digits go behind the palm so their roots disappear into it; the
    folded ones sit in front, the way knuckles crown a real fist.
    """
    lay = _layout(p)
    behind, overlay = [], []

    if pose == "open":
        behind = [_finger(p, 128 + dx * p["pw"], a, p["flen"] * m) for dx, a, m in lay]
    elif pose == "peace":
        # index and middle up in a V, the rest folded in front of the palm
        behind = [_finger(p, 128 - p["pw"] * 0.17, -20, p["flen"] * 1.06),
                  _finger(p, 128 + p["pw"] * 0.09, 7, p["flen"] * 1.1)]
        overlay = [_knuckles(p)]
    elif pose in ("point", "tap"):
        behind = [_finger(p, 128 - p["pw"] * 0.08, -3,
                          p["flen"] * (1.3 if pose == "point" else 1.0))]
        overlay = [_knuckles(p)]
    elif pose == "fist":
        overlay = [_knuckles(p)]
    elif pose == "grab":
        behind = [_curl_finger(p, 128 + dx * p["pw"], a * 1.3, p["flen"] * m)
                  for dx, a, m in lay]

    art = "".join(behind) + _palm(p) + "".join(overlay)

    if pose == "fist":
        art += _thumb(p, raised=True)
    elif pose == "grab":
        art += _thumb(p, side=1)
    elif pose == "open":
        art += _thumb(p)
    return art


# --------------------------------------------------------------------- owl

FEATHER = ("M-18 0C-21-58-16-88-8-104Q0-115 8-104C16-88 21-58 18 0 8 10-8 10-18 0Z")


def _feather(p, cx, cy, angle, scale, shade=False):
    fill = p["quill"] if shade else p["fur"]
    return (f'<g transform="translate({cx:.4g} {cy:.4g}) rotate({angle:.4g}) scale({scale:.4g})">'
            f'<path d="{FEATHER}" fill="{fill}" stroke="{p["line"]}" stroke-width="5" '
            f'stroke-linejoin="round"/>'
            f'<path d="M0-14V-96" fill="none" stroke="{p["line"]}" stroke-width="4" '
            f'stroke-linecap="round" opacity="0.55"/></g>')


def _serrations(p, cx, cy, angle):
    """The comb on an owl's leading edge — the reason it flies silently."""
    teeth = "".join(f'<path d="M{-14 + i * 7} {-96 + i * 11}l-9 3 8 4z" fill="{p["line"]}"/>'
                    for i in range(5))
    return (f'<g transform="translate({cx:.4g} {cy:.4g}) rotate({angle:.4g})">{teeth}</g>')


# Primaries are rooted along the wrist, not spun about one point, so they
# overlap into a sheet the way a real wing does.
WING_FANS = {
    "open": [(-31, -24, 0.86), (-15, -12, 0.95), (0, 0, 1.0), (15, 12, 0.95), (31, 24, 0.86)],
    "half": [(-20, -15, 0.9), (-7, -5, 0.99), (7, 6, 0.97), (21, 17, 0.88)],
    "closed": [(-12, -8, 0.93), (0, 0, 1.0), (12, 8, 0.93)],
    "vee": [(-28, -24, 1.0), (13, 10, 1.0)],
}


def _wing(p, spread, cx=128, cy=178, rot=0, scale=1.0, alula=False):
    fan = WING_FANS[spread]
    art = "".join(_feather(p, dx, 0, a, sc, shade=bool(i % 2))
                  for i, (dx, a, sc) in enumerate(fan))
    art += _serrations(p, fan[0][0], 0, fan[0][1])
    coverts = (f'<ellipse cx="0" cy="30" rx="70" ry="38" fill="{p["fur"]}" '
               f'stroke="{p["line"]}" stroke-width="5"/>'
               f'<path d="M-50 16q17-15 34 0 17-15 34 0 17-15 34 0" fill="none" '
               f'stroke="{p["line"]}" stroke-width="5" stroke-linecap="round" opacity="0.6"/>'
               f'<path d="M-38 40q19-14 38 0 19-14 38 0" fill="none" stroke="{p["line"]}" '
               'stroke-width="5" stroke-linecap="round" opacity="0.45"/>')
    if alula:
        # the alula — the thumb a bird actually has — raised on the leading edge
        coverts += (f'<g transform="translate(-58 4) rotate(-16)">'
                    f'<path d="{FEATHER}" transform="scale(0.46)" fill="{p["pad"]}" '
                    f'stroke="{p["line"]}" stroke-width="10" stroke-linejoin="round"/></g>')
    return (f'<g transform="translate({cx:.4g} {cy:.4g}) rotate({rot:.4g}) scale({scale:.4g})">'
            f'{coverts}{art}</g>')


def _toe(p, angle, seg1, seg2, curl, w1=30, w2=25):
    """One scaled toe: two segments and a hooked claw, swung out from the pad."""
    return (f'<g transform="rotate({angle:.4g})">'
            f'<path d="M0 0V{-seg1:.4g}" stroke="{p["toe"]}" stroke-width="{w1}" '
            'stroke-linecap="round"/>'
            f'<g transform="translate(0 {-seg1:.4g}) rotate({curl:.4g})">'
            f'<path d="M0 0V{-seg2:.4g}" stroke="{p["toe"]}" stroke-width="{w2}" '
            'stroke-linecap="round"/>'
            f'<g transform="translate(0 {-seg2:.4g})">'
            f'<path d="M-11 4q3-19 23-25-13 13-10 30z" fill="{p["claw"]}"/>'
            '</g></g></g>')


# Zygodactyl: two toes forward, two back. Held toes-up like the mammal hands,
# the back pair reads as the X-shaped grip an owl actually has.
TALON_POSES = {
    "grab":  {"back": [(-138, 46, 34, 40), (142, 46, 34, -40)],
              "front": [(-50, 68, 52, 44), (16, 70, 54, -44)]},
    "point": {"back": [(-140, 40, 28, 34), (146, 40, 28, -34)],
              "front": [(-4, 84, 50, -2), (54, 44, 32, -66)]},
    "tap":   {"back": [(-140, 38, 26, 34), (146, 38, 26, -34)],
              "front": [(-4, 62, 40, -6), (54, 42, 30, -66)]},
}


def _talon(p, pose, cx=128, cy=170):
    spec = TALON_POSES[pose]
    tarsus = (f'<rect x="-30" y="-6" width="60" height="86" rx="28" fill="{p["fur"]}" '
              f'stroke="{p["line"]}" stroke-width="5"/>'
              f'<path d="M-24 44q12 14 24 0 12 14 24 0" fill="none" stroke="{p["line"]}" '
              'stroke-width="5" stroke-linecap="round" opacity="0.6"/>')
    back = "".join(_toe(p, a, s1, s2, c, 26, 21) for a, s1, s2, c in spec["back"])
    front = "".join(_toe(p, a, s1, s2, c) for a, s1, s2, c in spec["front"])
    pad = f'<circle cx="0" cy="0" r="32" fill="{p["toe"]}"/>'
    return f'<g transform="translate({cx} {cy})">{tarsus}{back}{pad}{front}</g>'


# ---------------------------------------------------------------- gestures

def _arcs(p, x, y, flip=False):
    return (f'<g transform="translate({x} {y}){" scale(-1,1)" if flip else ""}" fill="none" '
            f'stroke="{p["line"]}" stroke-width="12" stroke-linecap="round">'
            '<path d="M0 0a48 48 0 0 1 0 80"/><path d="M26-24a76 76 0 0 1 0 128"/></g>')


def _arrow(p):
    return (f'<g fill="none" stroke="{p["line"]}" stroke-width="14" stroke-linecap="round" '
            'stroke-linejoin="round"><path d="M34 46h150"/><path d="m152 14 34 32-34 32"/></g>')


def _sparks(p):
    return (f'<g fill="none" stroke="{p["line"]}" stroke-width="12" stroke-linecap="round">'
            '<path d="M128 26v30"/><path d="m78 40 14 26"/><path d="m178 40-14 26"/></g>')


def _heart():
    return ('<path d="M128 214 62 148a38 38 0 0 1 52-55l14 13 14-13a38 38 0 0 1 52 55z" '
            'fill="#FF6E8A"/>')


def gesture(animal, kind):
    p = PALETTE[animal]

    if p.get("wing"):
        if kind == "high_five":
            return _wing(p, "open")
        if kind == "wave":
            return _wing(p, "open", cx=112, rot=-13, scale=0.92) + _arcs(p, 200, 108)
        if kind == "swipe":
            return _wing(p, "half", cy=206, scale=0.78) + _arrow(p)
        if kind == "peace":
            return _wing(p, "vee")
        if kind == "thumbs_up":
            return _wing(p, "closed", cy=190, scale=0.92, alula=True)
        if kind == "clap":
            return (_wing(p, "half", cx=92, cy=198, rot=-28, scale=0.64)
                    + _wing(p, "half", cx=164, cy=198, rot=28, scale=0.64) + _sparks(p))
        if kind == "heart_hands":
            return ('<g transform="translate(128 176) scale(0.82) translate(-128 -176)">'
                    f'{_heart()}</g>'
                    + _wing(p, "half", cx=68, cy=214, rot=-38, scale=0.54)
                    + _wing(p, "half", cx=188, cy=214, rot=38, scale=0.54))
        return _talon(p, kind)

    hand = _hand(p, "open")
    if kind == "high_five":
        return hand
    if kind == "wave":
        return _place(hand, 118, 188, -13, 0.92) + _arcs(p, 206, 104)
    if kind == "swipe":
        return _place(hand, 142, 214, 0, 0.82) + _arrow(p)
    if kind == "thumbs_up":
        return _hand(p, "fist")
    if kind == "point":
        return _hand(p, "point")
    if kind == "tap":
        return _hand(p, "tap") + (
            f'<g fill="none" stroke="{p["line"]}" stroke-width="12" stroke-linecap="round">'
            '<path d="M64 52a72 72 0 0 1 20-38"/><path d="M192 52a72 72 0 0 0-20-38"/></g>')
    if kind == "grab":
        return _hand(p, "grab")
    if kind == "clap":
        return (_place(hand, 98, 196, -28, 0.7) + _place(hand, 158, 196, 28, 0.7)
                + _sparks(p))
    if kind == "peace":
        return _hand(p, "peace")
    if kind == "heart_hands":
        return ('<g transform="translate(128 176) scale(0.82) translate(-128 -176)">'
                f'{_heart()}</g>'
                + _place(hand, 76, 212, -38, 0.58) + _place(hand, 180, 212, 38, 0.58))

    raise ValueError(kind)


def render(animal, kind, label):
    slug = f"{kind}_{animal}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" '
            f'role="img" aria-labelledby="t-{slug}">\n  <title id="t-{slug}">{label}</title>\n'
            f'  {gesture(animal, kind)}\n</svg>\n')
