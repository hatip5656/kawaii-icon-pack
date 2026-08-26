#!/usr/bin/env python3
"""Verbs: the characters doing things.

Layout is fixed so the set reads as a family — the face sits in the upper two
thirds, the prop occupies y 160-244, and two paw pads grip it. Props are neutral
(white, paper, wood) with one accent element in the character's own fur colour,
which is what stops fifty icons looking like clip art.
"""

ACTION_LABELS = {
    "reading": "Reading", "working": "Working", "calling": "Calling",
    "searching": "Searching", "shopping": "Shopping", "celebrating": "Celebrating",
    "thinking": "Thinking", "drinking": "Drinking", "delivering": "Delivering",
    "painting": "Painting", "mailing": "Mailing", "gardening": "Gardening",
    "gaming": "Gaming", "photographing": "Photographing", "cooking": "Cooking",
    "exercising": "Exercising", "travelling": "Travelling", "singing": "Singing",
}
ACTION_ORDER = list(ACTION_LABELS)

PAPER, LINE, WOOD, KRAFT = "#FFFFFF", "#D9D3E6", "#C9A87C", "#F0E2CC"
CONFETTI = ("#FF8FA9", "#FFD86B", "#7EC8E3", "#9BC58E")


def _pads(spots, fur, pad, key):
    """Paw pads gripping the prop."""
    stroke = f' stroke="{key}" stroke-width="6"' if key else ""
    out = []
    for x, y, rot in spots:
        out.append(f'<g transform="rotate({rot} {x} {y})">'
                   f'<ellipse cx="{x}" cy="{y}" rx="21" ry="26" fill="{fur}"{stroke}/>'
                   f'<ellipse cx="{x}" cy="{y + 3}" rx="11" ry="14" fill="{pad}"/></g>')
    return "".join(out)


def prop(kind, fur, pad, key):
    P = _pads

    if kind == "reading":
        return ('<path d="M128 186c-19-14-50-18-78-16v60c28-2 59 2 78 16 19-14 50-18 78-16v-60'
                f'c-28-2-59 2-78 16z" fill="{PAPER}" stroke="{LINE}" stroke-width="7" '
                'stroke-linejoin="round"/>'
                f'<rect x="121" y="182" width="14" height="64" rx="5" fill="{fur}"/>'
                + P([(44, 214, -12), (212, 214, 12)], fur, pad, key))

    if kind == "working":
        return (f'<rect x="66" y="158" width="124" height="62" rx="8" fill="{PAPER}" '
                f'stroke="{LINE}" stroke-width="7"/>'
                f'<rect x="66" y="158" width="124" height="16" rx="8" fill="{fur}"/>'
                f'<path d="M46 226h164l-9 16H55z" fill="{LINE}"/>'
                + P([(52, 202, -14), (204, 202, 14)], fur, pad, key))

    if kind == "calling":
        return (f'<g transform="rotate(24 192 178)"><rect x="172" y="132" width="40" height="96" '
                f'rx="20" fill="{fur}"/><rect x="180" y="146" width="24" height="60" rx="12" '
                f'fill="{pad}"/></g>'
                f'<g fill="none" stroke="{fur}" stroke-width="9" stroke-linecap="round">'
                '<path d="M226 156a30 30 0 0 1 0 44"/></g>'
                + P([(166, 216, 18)], fur, pad, key))

    if kind == "searching":
        return (f'<circle cx="146" cy="192" r="40" fill="{PAPER}" fill-opacity="0.6" '
                f'stroke="{fur}" stroke-width="13"/>'
                f'<path d="m176 222 26 26" stroke="{fur}" stroke-width="15" stroke-linecap="round"/>'
                + P([(84, 206, -18)], fur, pad, key))

    if kind == "shopping":
        return (f'<path d="M74 180h108l-11 64H85z" fill="{fur}"/>'
                f'<path d="M104 180v-12a24 24 0 0 1 48 0v12" fill="none" stroke="{fur}" '
                'stroke-width="10" stroke-linecap="round"/>'
                f'<path d="M128 226 112 210a10 10 0 0 1 15-13l1 1 1-1a10 10 0 0 1 15 13z" fill="{pad}"/>'
                + P([(56, 208, -16), (200, 208, 16)], fur, pad, key))

    if kind == "celebrating":
        bits = "".join(
            f'<rect x="{x}" y="{y}" width="11" height="17" rx="5" transform="rotate({r} {x} {y})" '
            f'fill="{CONFETTI[i % 4]}"/>'
            for i, (x, y, r) in enumerate(((30, 44, -22), (208, 34, 26), (56, 96, 14),
                                           (196, 104, -18), (14, 140, 8), (232, 138, -12)))
        )
        return (bits + P([(48, 176, -34), (208, 176, 34)], fur, pad, key)
                + f'<path d="M40 138v-16M216 130v-16" stroke="{fur}" stroke-width="8" '
                'stroke-linecap="round"/>')

    if kind == "thinking":
        return (f'<path d="M232 82a26 26 0 0 1-26 26h-38a24 24 0 0 1-4-47 27 27 0 0 1 52-5 26 26 0 0 1 '
                f'16 26z" fill="{PAPER}" stroke="{LINE}" stroke-width="7"/>'
                + "".join(f'<circle cx="{cx}" cy="82" r="6" fill="{fur}"/>' for cx in (176, 196, 216))
                + f'<circle cx="160" cy="126" r="11" fill="{PAPER}" stroke="{LINE}" stroke-width="6"/>'
                f'<circle cx="142" cy="146" r="6" fill="{PAPER}" stroke="{LINE}" stroke-width="5"/>')

    if kind == "drinking":
        return (f'<path d="M86 174h72v48a26 26 0 0 1-26 26h-20a26 26 0 0 1-26-26z" fill="{PAPER}" '
                f'stroke="{LINE}" stroke-width="7"/>'
                f'<path d="M158 190h14a19 19 0 0 1 0 38h-14" fill="none" stroke="{LINE}" stroke-width="7"/>'
                f'<rect x="90" y="196" width="64" height="14" fill="{fur}"/>'
                f'<g fill="none" stroke="{LINE}" stroke-width="7" stroke-linecap="round">'
                '<path d="M108 158c-8-10 8-18 0-28"/><path d="M136 158c-8-10 8-18 0-28"/></g>'
                + P([(196, 214, 16)], fur, pad, key))

    if kind == "delivering":
        return (f'<rect x="62" y="172" width="132" height="72" rx="6" fill="{KRAFT}" '
                f'stroke="{WOOD}" stroke-width="6"/>'
                f'<path d="M62 198h132" stroke="{WOOD}" stroke-width="6"/>'
                f'<rect x="116" y="172" width="24" height="72" fill="{fur}" opacity="0.75"/>'
                + P([(50, 206, -14), (206, 206, 14)], fur, pad, key))

    if kind == "painting":
        return (f'<ellipse cx="112" cy="206" rx="54" ry="38" fill="{PAPER}" stroke="{LINE}" '
                'stroke-width="7"/>'
                f'<circle cx="138" cy="218" r="11" fill="#FFFCF8" stroke="{LINE}" stroke-width="5"/>'
                + "".join(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{CONFETTI[i]}"/>'
                          for i, (cx, cy) in enumerate(((86, 190), (110, 182), (134, 190), (86, 216))))
                + f'<path d="m182 240 30-52" stroke="{WOOD}" stroke-width="11" stroke-linecap="round"/>'
                f'<path d="m208 194 12-22" stroke="{fur}" stroke-width="16" stroke-linecap="round"/>')

    if kind == "mailing":
        return (f'<rect x="62" y="172" width="132" height="76" rx="10" fill="{PAPER}" '
                f'stroke="{LINE}" stroke-width="7"/>'
                f'<path d="m66 180 55 40a12 12 0 0 0 14 0l55-40" fill="none" stroke="{fur}" '
                'stroke-width="8" stroke-linejoin="round"/>'
                + P([(48, 210, -14), (208, 210, 14)], fur, pad, key))

    if kind == "gardening":
        return (f'<path d="M92 200h72l-9 44H101z" fill="{KRAFT}" stroke="{WOOD}" stroke-width="6"/>'
                f'<rect x="84" y="184" width="88" height="20" rx="8" fill="{WOOD}"/>'
                '<path d="M128 184v-30" stroke="#6FBF7F" stroke-width="9" stroke-linecap="round"/>'
                '<path d="M128 160c0-18 14-32 32-32 0 18-14 32-32 32z" fill="#8FC46A"/>'
                '<path d="M128 172c-16 0-30-12-30-28 16 0 30 12 30 28z" fill="#6FBF7F"/>'
                + P([(62, 216, -16), (194, 216, 16)], fur, pad, key))

    if kind == "gaming":
        return (f'<path d="M78 184h100a30 30 0 0 1 0 60H78a30 30 0 0 1 0-60z" fill="{PAPER}" '
                f'stroke="{LINE}" stroke-width="7"/>'
                f'<path d="M104 200v26M91 213h26" stroke="{fur}" stroke-width="11" stroke-linecap="round"/>'
                f'<circle cx="160" cy="204" r="9" fill="{CONFETTI[0]}"/>'
                f'<circle cx="176" cy="222" r="9" fill="{CONFETTI[2]}"/>'
                + P([(56, 214, -14), (200, 214, 14)], fur, pad, key))

    if kind == "photographing":
        return (f'<rect x="62" y="180" width="132" height="66" rx="12" fill="{PAPER}" '
                f'stroke="{LINE}" stroke-width="7"/>'
                f'<path d="m104 180 9-15h30l9 15z" fill="{fur}"/>'
                f'<circle cx="128" cy="214" r="25" fill="#FFFCF8" stroke="{fur}" stroke-width="10"/>'
                f'<circle cx="176" cy="196" r="7" fill="{CONFETTI[1]}"/>'
                + P([(48, 212, -14), (208, 212, 14)], fur, pad, key))

    if kind == "cooking":
        return ('<path d="M56 194h102v16a30 30 0 0 1-30 30H86a30 30 0 0 1-30-30z" fill="#5A5560"/>'
                f'<rect x="156" y="198" width="54" height="13" rx="7" fill="{WOOD}"/>'
                '<ellipse cx="106" cy="194" rx="22" ry="8" fill="#FFFFFF"/>'
                '<circle cx="106" cy="192" r="7" fill="#FFD86B"/>'
                f'<g fill="none" stroke="{LINE}" stroke-width="7" stroke-linecap="round">'
                '<path d="M92 174c-8-10 8-18 0-28"/><path d="M124 174c-8-10 8-18 0-28"/></g>'
                + P([(46, 216, -16)], fur, pad, key))

    if kind == "exercising":
        return (f'<rect x="98" y="202" width="60" height="16" rx="8" fill="{LINE}"/>'
                f'<rect x="68" y="184" width="30" height="52" rx="11" fill="{fur}"/>'
                f'<rect x="158" y="184" width="30" height="52" rx="11" fill="{fur}"/>'
                f'<rect x="76" y="196" width="14" height="28" rx="7" fill="{pad}"/>'
                f'<rect x="166" y="196" width="14" height="28" rx="7" fill="{pad}"/>'
                '<path d="M212 150c-7 10-11 15-11 19a11 11 0 0 0 22 0c0-4-4-9-11-19z" fill="#7EC8E3"/>')

    if kind == "travelling":
        return (f'<rect x="68" y="184" width="120" height="64" rx="13" fill="{fur}"/>'
                f'<path d="M108 184v-10a20 20 0 0 1 40 0v10" fill="none" stroke="{fur}" '
                'stroke-width="10" stroke-linecap="round"/>'
                f'<rect x="68" y="204" width="120" height="15" fill="{pad}"/>'
                f'<circle cx="162" cy="234" r="8" fill="{pad}"/>'
                + P([(48, 212, -14), (208, 212, 14)], fur, pad, key))

    if kind == "singing":
        return (f'<rect x="110" y="164" width="38" height="60" rx="19" fill="{fur}"/>'
                f'<rect x="119" y="176" width="20" height="34" rx="10" fill="{pad}"/>'
                f'<path d="M98 208a31 31 0 0 0 62 0" fill="none" stroke="{LINE}" stroke-width="8" '
                'stroke-linecap="round"/>'
                f'<path d="M129 226v20" stroke="{LINE}" stroke-width="8" stroke-linecap="round"/>'
                f'<path d="M56 196v-26l22-5v26" fill="none" stroke="{CONFETTI[0]}" stroke-width="7" '
                'stroke-linecap="round"/>'
                f'<circle cx="51" cy="197" r="7" fill="{CONFETTI[0]}"/>'
                f'<circle cx="73" cy="192" r="7" fill="{CONFETTI[0]}"/>'
                f'<path d="M196 182v-22" stroke="{CONFETTI[2]}" stroke-width="7" stroke-linecap="round"/>'
                f'<circle cx="191" cy="183" r="7" fill="{CONFETTI[2]}"/>')

    raise ValueError(kind)
