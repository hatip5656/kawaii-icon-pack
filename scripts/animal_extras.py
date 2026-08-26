#!/usr/bin/env python3
"""Accessories and signature snacks — the layer that gives each character personality.

Accessories are anchored per animal because the heads differ: the rabbit's ears own
the top of the canvas, so its party hat perches to one side; the panda's eyes sit
close together, so its glasses are narrower.
"""

# head geometry: cx, cy, rx, ry
HEADS = {
    "red_panda": (128, 140, 86, 78),
    "rabbit": (128, 152, 73, 70),
    "panda": (128, 146, 87, 79),
    "hamster": (128, 142, 88, 76),
    "raccoon": (128, 140, 86, 78),
    "owl": (128, 142, 84, 78),
}

# where a hat sits: x, y (base centre), rotation
HAT = {
    "red_panda": (128, 78, 0),
    "rabbit": (186, 108, 26),
    "panda": (128, 86, 0),
    "hamster": (128, 80, 0),
    "raccoon": (128, 78, 0),
    "owl": (128, 88, 0),
}

# eye anchors mirror build_icons: lx, rx, cy, lens radius
EYES = {
    "red_panda": (94, 162, 118, 24),
    "rabbit": (100, 156, 142, 24),
    "panda": (97, 159, 138, 26),
    "hamster": (98, 158, 128, 25),
    "raccoon": (94, 162, 124, 26),
    "owl": (98, 158, 138, 30),
}

ACCESSORY_LABELS = {
    "party_hat": "Party hat", "glasses": "Glasses", "headphones": "Headphones",
    "scarf": "Scarf", "flower_crown": "Flower crown",
}
ACCESSORY_ORDER = list(ACCESSORY_LABELS)

SNACK_LABEL = "Snack"


def _flower(cx, cy, r=9, petal="#FFFFFF", hub="#FFD86B"):
    from math import cos, pi, sin
    petals = "".join(
        f'<circle cx="{cx + r * cos(i * 2 * pi / 5 - pi / 2):.0f}" '
        f'cy="{cy + r * sin(i * 2 * pi / 5 - pi / 2):.0f}" r="{r * 0.72:.0f}" fill="{petal}"/>'
        for i in range(5)
    )
    return petals + f'<circle cx="{cx}" cy="{cy}" r="{r * 0.5:.0f}" fill="{hub}"/>'


def accessory(animal, kind):
    cx, cy, rx, ry = HEADS[animal]

    if kind == "party_hat":
        x, y, rot = HAT[animal]
        return (f'<g transform="translate({x},{y}) rotate({rot})">'
                '<path d="M0-64-36 2h72z" fill="#FF8FA9"/>'
                '<path d="M-27-16h54M-18-38h36" stroke="#FFD86B" stroke-width="8" '
                'stroke-linecap="round" fill="none"/>'
                '<circle cx="0" cy="-68" r="11" fill="#FFD86B"/></g>')

    if kind == "glasses":
        lx, ex, ey, r = EYES[animal]
        return (f'<g fill="#FFFFFF" fill-opacity="0.35" stroke="#4A4453" stroke-width="8">'
                f'<circle cx="{lx}" cy="{ey}" r="{r}"/><circle cx="{ex}" cy="{ey}" r="{r}"/></g>'
                f'<g fill="none" stroke="#4A4453" stroke-width="8" stroke-linecap="round">'
                f'<path d="M{lx + r} {ey}H{ex - r}"/><path d="M{lx - r} {ey}h-16"/>'
                f'<path d="M{ex + r} {ey}h16"/></g>')

    if kind == "headphones":
        band_r = rx - 6
        return (f'<path d="M{cx - band_r} {cy}a{band_r} {ry + 16} 0 0 1 {2 * band_r} 0" '
                'fill="none" stroke="#5A5560" stroke-width="14" stroke-linecap="round"/>'
                + "".join(
                    f'<rect x="{x}" y="{cy - 22}" width="30" height="60" rx="15" fill="#5A5560"/>'
                    f'<rect x="{x + 6}" y="{cy - 14}" width="18" height="44" rx="9" fill="#FF9EB5"/>'
                    for x in (cx - band_r - 15, cx + band_r - 15))) 

    if kind == "scarf":
        y = cy + ry - 18
        w = rx * 0.86
        return (f'<path d="M{cx - w:.0f} {y:.0f}q{w:.0f} 30 {2 * w:.0f} 0v30q-{w:.0f} 30 -{2 * w:.0f} 0z" '
                'fill="#E4574C"/>'
                f'<path d="M{cx + w * 0.3:.0f} {y + 26:.0f}h32l-8 56h-30z" fill="#C7463C"/>'
                f'<path d="M{cx - w:.0f} {y + 14:.0f}q{w:.0f} 30 {2 * w:.0f} 0" fill="none" '
                'stroke="#C7463C" stroke-width="6"/>')

    if kind == "flower_crown":
        from math import cos, pi, sin
        out = []
        for i in range(5):
            t = -0.82 + i * 0.41
            out.append(_flower(cx + rx * 0.92 * sin(t), cy - ry * 0.94 * cos(t) + 4,
                               petal="#FFFFFF" if i % 2 else "#FFC2D1"))
        return "".join(out)

    raise ValueError(kind)


# one signature food per character
SNACKS = {
    "red_panda": '<g transform="translate(184,196)"><circle cx="0" cy="0" r="22" fill="#E4574C"/>'
                 '<circle cx="-7" cy="-7" r="6" fill="#FFFFFF" opacity="0.5"/>'
                 '<path d="M0-20c6-14 20-16 20-16s-2 16-16 18z" fill="#6FBF7F"/></g>',
    "rabbit": '<g transform="translate(182,196) rotate(18)">'
              '<path d="M0-26 16 30a16 16 0 0 1-32 0z" fill="#F08A3C"/>'
              '<path d="M-11 4h22M-13-8h26" stroke="#D9702A" stroke-width="5" stroke-linecap="round"/>'
              '<path d="M0-26c-6-16 4-26 4-26s6 14-4 26zM0-26c8-14 22-12 22-12s-8 14-22 12z" '
              'fill="#6FBF7F"/></g>',
    "panda": '<g transform="translate(186,190) rotate(-16)">'
             '<path d="M0-34v70" stroke="#8FC46A" stroke-width="12" stroke-linecap="round"/>'
             '<path d="M0-14c-16-2-26-14-26-14s14-8 26 4zM0 6c16-2 26-14 26-14s-14-8-26 4z" '
             'fill="#6FBF7F"/></g>',
    "hamster": '<g transform="translate(186,192) rotate(24)">'
               '<ellipse cx="0" cy="0" rx="16" ry="24" fill="#5C4A3A"/>'
               '<path d="M0-18v36" stroke="#F5E6D0" stroke-width="6" stroke-linecap="round"/></g>',
    "raccoon": '<g transform="translate(184,194)">'
               '<circle cx="-14" cy="-8" r="11" fill="#8E7CC3"/><circle cx="6" cy="-10" r="11" fill="#9C8AD1"/>'
               '<circle cx="-4" cy="9" r="11" fill="#8E7CC3"/><circle cx="16" cy="7" r="10" fill="#9C8AD1"/>'
               '<circle cx="-18" cy="13" r="9" fill="#7E6BB8"/>'
               '<path d="M2-21c2-13 15-17 15-17s-2 13-11 17z" fill="#6FBF7F"/></g>',
    "owl": '<g transform="translate(186,194)"><ellipse cx="0" cy="6" rx="20" ry="24" fill="#C9873F"/>'
           '<path d="M-22-12h44a6 6 0 0 1-6 10h-32a6 6 0 0 1-6-10z" fill="#8A5A2B"/>'
           '<path d="M0-12v-14" stroke="#8A5A2B" stroke-width="6" stroke-linecap="round"/></g>',
}
