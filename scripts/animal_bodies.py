#!/usr/bin/env python3
"""Full-body poses.

The body is assembled from parts — torso, belly, two arms, two legs, head — so a
pose is a set of limb angles rather than a new drawing. Limb colour is a species
detail: the panda's arms and legs are black, the owl's read as wings, and the red
panda and raccoon get their ringed tails at full size.
"""

import math

POSE_LABELS = {
    "standing": "Standing", "sitting": "Sitting", "waving": "Waving",
    "running": "Running", "jumping": "Jumping", "dancing": "Dancing",
    "tennis": "Tennis", "football": "Football", "basketball": "Basketball",
    "cycling": "Cycling", "swimming": "Swimming", "yoga": "Yoga",
    "skateboarding": "Skateboarding", "baseball": "Baseball", "volleyball": "Volleyball",
    "rugby": "Rugby", "golf": "Golf", "cricket": "Cricket", "ping_pong": "Table tennis",
    "badminton": "Badminton", "bowling": "Bowling", "hockey": "Hockey", "skiing": "Skiing",
    "snowboarding": "Snowboarding", "surfing": "Surfing", "boxing": "Boxing",
    "karate": "Karate", "weightlifting": "Weightlifting", "archery": "Archery",
    "climbing": "Climbing", "rowing": "Rowing", "fishing": "Fishing",
    "ice_skating": "Ice skating",
}
POSE_ORDER = list(POSE_LABELS)

# torso, belly, limb, keyline
BODY = {
    "red_panda": ("#E97A4E", "#FFF4E8", "#DA6A44", None),
    "rabbit": ("#FDFBFF", "#FFF6FA", "#F4F0FB", "#D5CDE6"),
    "panda": ("#FFFFFF", "#F7F5FB", "#3A3335", "#DFDAEC"),
    "hamster": ("#F5C377", "#FFF3DE", "#EAB268", None),
    "raccoon": ("#A7AEBC", "#FBF7F2", "#99A1B0", None),
    "owl": ("#9C8AD1", "#FFF3DE", "#8878C2", None),
}

DARK, LINE, WOOD = "#5A5560", "#D9D3E6", "#C9A87C"


def _ringed_tail(fur, ring, d="M180 214C224 208 244 172 236 132"):
    return (f'<path d="{d}" fill="none" stroke="{fur}" stroke-width="36" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{ring}" stroke-width="36" stroke-dasharray="14 26" '
            'stroke-dashoffset="22"/>')


TAILS = {
    "red_panda": _ringed_tail("#C9552E", "#FFF4E8"),
    "raccoon": _ringed_tail("#8E96A6", "#4A4453"),
    # a rabbit's tail is a cotton puff, not a plume
    "rabbit": ('<circle cx="180" cy="196" r="17" fill="#FDFBFF" stroke="#E4E0F0" stroke-width="5"/>'
               '<circle cx="174" cy="190" r="5" fill="#F3EDFA"/>'),
    "hamster": '<ellipse cx="188" cy="206" rx="14" ry="11" fill="#E0A65F"/>',
}


def _parts(animal):
    torso, belly, limb, key = BODY[animal]
    k = f' stroke="{key}" stroke-width="6"' if key else ""
    return torso, belly, limb, k


# Species build. Real animals are not one shape in six colours: the panda is a barrel
# with thick limbs, the rabbit is narrow with big hind haunches, the hamster is almost
# spherical with stubby legs, the raccoon has long dexterous hands.
BUILD = {
    "red_panda": {"paw": 13, "torso": (56, 48), "arm": (16, 29), "legs": "paw"},
    "rabbit": {"paw": 12, "torso": (47, 51), "arm": (13, 25), "legs": "hare"},
    "panda": {"paw": 13, "torso": (62, 52), "arm": (21, 29), "legs": "thick"},
    "hamster": {"paw": 11, "torso": (58, 52), "arm": (14, 21), "legs": "stub"},
    "raccoon": {"paw": 12, "torso": (52, 48), "arm": (16, 31), "legs": "hand"},
    "owl": {"paw": 12, "torso": (54, 50), "arm": (17, 30), "legs": "bird"},
}

# Bone chains, proximal to distal, as (length, width). Forelimb is humerus + radius;
# hindlimb is femur + tibia + metatarsus. The ratios are the species morphology: a
# rabbit's tibia is nearly as long as its femur and its metatarsus is long again, which
# is what gives it a hare's crouch; a panda's bones are short and thick.
SKELETON = {
    "red_panda": {"fore": [(26, 18), (23, 15)], "hind": [(22, 23), (20, 19), (12, 16)],
                  "elbow": 26, "knee": (34, -30), "foot": (25, 11)},
    "rabbit": {"fore": [(24, 17), (22, 14)], "hind": [(25, 25), (23, 18), (14, 15)],
               "elbow": 30, "knee": (52, -46), "foot": (30, 11)},
    "panda": {"fore": [(30, 24), (27, 20)], "hind": [(22, 29), (20, 25), (10, 21)],
              "elbow": 16, "knee": (24, -20), "foot": (28, 13)},
    "hamster": {"fore": [(21, 17), (19, 15)], "hind": [(17, 19), (15, 16), (9, 14)],
                "elbow": 32, "knee": (40, -36), "foot": (21, 10)},
    "raccoon": {"fore": [(26, 17), (25, 14)], "hind": [(23, 22), (21, 18), (12, 15)],
                "elbow": 30, "knee": (38, -34), "foot": (24, 11)},
    "owl": {"fore": [(25, 18), (23, 15)], "hind": [(20, 14), (18, 12), (10, 11)],
            "elbow": 20, "knee": (40, -44), "foot": (0, 0)},
}

# How far the knee is flexed in a resting pose. A standing animal is nearly straight;
# the crouch belongs to running and jumping.
_FLEX = 0.42

def _sk(key):
    return SKELETON[_ANIMAL][key]


def _anchors():
    """Shoulders and hips sit on the ribcage and pelvis, not wherever a pose puts them."""
    rx, ry = _b("torso")
    cx, cy = 128, 152
    return ((cx - rx * 0.60, cy - ry * 0.42), (cx + rx * 0.60, cy - ry * 0.42),
            (cx - rx * 0.42, cy + ry * 0.48), (cx + rx * 0.42, cy + ry * 0.48))


# state for whichever animal is being drawn
_PAD = "#FFFFFF"
_BIRD = False
_ANIMAL = "red_panda"
_DEFERRED = []
_WRISTS = []
_OUTLINE = []


def _b(key):
    return BUILD[_ANIMAL][key]


def _catmull(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return (0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                   + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                   + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
            0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                   + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                   + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3))


def _centreline(joints, widths, per_bone=9, bulge=0.13):
    """Smooth the joint polyline into a curve, carrying a width at every sample.

    A limb is not a pipe: it tapers from the proximal bone to the distal one and
    swells a little over the muscle, so width is sampled rather than constant."""
    ext = [joints[0]] + list(joints) + [joints[-1]]
    pts, ws = [], []
    for i in range(len(joints) - 1):
        w0, w1 = widths[i], widths[i + 1]
        for j in range(per_bone):
            t = j / per_bone
            pts.append(_catmull(ext[i], ext[i + 1], ext[i + 2], ext[i + 3], t))
            swell = 1 + bulge * math.sin(math.pi * t) if i == 0 else 1
            ws.append((w0 + (w1 - w0) * t) * swell)
    pts.append(joints[-1])
    ws.append(widths[-1])
    return pts, ws


def _outline(pts, ws):
    """Close a tapered silhouette around a centreline, rounded at both ends."""
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        px, py = pts[max(i - 1, 0)]
        nx, ny = pts[min(i + 1, len(pts) - 1)]
        tx, ty = nx - px, ny - py
        L = math.hypot(tx, ty) or 1
        ox, oy = -ty / L * ws[i] / 2, tx / L * ws[i] / 2
        left.append((x + ox, y + oy))
        right.append((x - ox, y - oy))
    r0, r1 = max(ws[0] / 2, 0.5), max(ws[-1] / 2, 0.5)
    d = "M%.1f %.1f" % left[0]
    d += "".join("L%.1f %.1f" % q for q in left[1:])
    d += "A%.1f %.1f 0 0 1 %.1f %.1f" % (r1, r1, right[-1][0], right[-1][1])
    d += "".join("L%.1f %.1f" % q for q in reversed(right[:-1]))
    d += "A%.1f %.1f 0 0 1 %.1f %.1f" % (r0, r0, left[0][0], left[0][1])
    return d + "Z"


def _chain(ox, oy, bones, angles, fill, k, tip=0.6, wing=False):
    """Walk a bone chain, then wrap it in a tapered silhouette."""
    joints, a = [(ox, oy)], 0.0
    for (ln, _w), ang in zip(bones, angles):
        a += ang
        r = math.radians(a)
        joints.append((joints[-1][0] + math.sin(r) * ln, joints[-1][1] + math.cos(r) * ln))

    widths = [b[1] for b in bones] + [bones[-1][1] * tip]
    if wing:
        widths = [bones[0][1] * 1.7, bones[0][1] * 1.3, bones[-1][1] * 0.85, bones[-1][1] * 0.35]
    pts, ws = _centreline(joints, widths, bulge=0.05 if wing else 0.13)

    d = _outline(pts, ws)
    if k:
        col = k.split('stroke="')[1].split('"')[0]
        _OUTLINE.append(f'<path d="{d}" fill="{col}" stroke="{col}" stroke-width="7" '
                        'stroke-linejoin="round"/>')
    art = f'<path d="{d}" fill="{fill}"/>'
    return art, joints[-1], a


def _solid(head, fill, k):
    """Emit a shape's fill now and its keyline into the silhouette pass."""
    if k:
        col = k.split('stroke="')[1].split('"')[0]
        _OUTLINE.append(f'{head} fill="{col}" stroke="{col}" stroke-width="7"/>')
    return f'{head} fill="{fill}"/>'


def _paw(x, y, rot, fill, k, r):
    """A real paw: central pad plus toe beans, turned to follow the forearm."""
    return (f'<g transform="rotate({rot:.0f} {x:.0f} {y:.0f})">'
            + _solid(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r}" ry="{r * 0.94:.1f}"', fill, k)
            + f'<ellipse cx="{x:.0f}" cy="{y + r * 0.22:.0f}" rx="{r * 0.5:.1f}" ' 
            f'ry="{r * 0.4:.1f}" fill="{_PAD}"/>'
            + "".join(f'<circle cx="{x + dx * r:.0f}" cy="{y - r * 0.45:.0f}" '
                      f'r="{r * 0.21:.1f}" fill="{_PAD}"/>' for dx in (-0.46, 0, 0.46))
            + "</g>")


def _wing(x, y, rot, fill, rx, ry):
    """A wing is a limb too: humerus, radius, manus — broad at the shoulder, tapering
    to primary feathers at the tip."""
    sl, sr, _, _ = _anchors()
    side = 0 if x < 128 else 1
    ox, oy = (sl, sr)[side]
    if y < oy + 8:
        rot = math.degrees(math.atan2(x - ox, y - oy))
    sign = 1 if side else -1
    art, (tx, ty), a = _chain(ox, oy, [(27, 24), (25, 19), (19, 14)],
                              (rot, 11 * sign, 13 * sign), fill, "", wing=True)
    r = math.radians(a)
    ux, uy = math.sin(r), math.cos(r)
    feathers = "".join(
        f'<path d="M{tx - ux * 20 + i * 6 * uy:.0f} {ty - uy * 20 - i * 6 * ux:.0f}'
        f'l{ux * 17:.0f} {uy * 17:.0f}" stroke="#7E6BB8" stroke-width="3.5" '
        'stroke-linecap="round" fill="none"/>' for i in (-1, 0, 1))
    _WRISTS.append((tx, ty))
    _DEFERRED.append(art + feathers)
    return ""            # painted after the torso, so a folded wing is actually visible


def _arm(x, y, rot, fill, k, rx=None, ry=None):
    """A forelimb rooted at the shoulder. `rot` drives the humerus; the radius follows
    at the species' elbow angle, bent away from the body."""
    if _BIRD:
        return _wing(x, y, rot, fill, rx or _b("arm")[0], ry or _b("arm")[1])
    sl, sr, _, _ = _anchors()
    side = 0 if x < 128 else 1
    ox, oy = (sl, sr)[side]
    if y < oy + 8:                      # the pose wants this limb raised
        rot = math.degrees(math.atan2(x - ox, y - oy))
    elbow = _sk("elbow") * (1 if side else -1)
    art, (wx, wy), a = _chain(ox, oy, _sk("fore"), (rot, elbow), fill, k)
    _WRISTS.append((wx, wy))
    _DEFERRED.append(art + _paw(wx, wy, a, fill, k, _b("paw")))
    return ""


def _leg(x, limb, k, y=206, rot=0):
    """A hindlimb rooted at the hip: femur, tibia, metatarsus, then a foot."""
    _, _, hl, hr = _anchors()
    side = 0 if x < 128 else 1
    ox, oy = (hl, hr)[side]
    sign = 1 if side else -1

    if _BIRD:
        k1, k2 = (v * _FLEX for v in _sk("knee"))
        art, (fx, fy), _ = _chain(ox, oy, _sk("hind"), (rot, k1 * sign, k2 * sign),
                                  "#E8912B", "")
        return (art + f'<g stroke="#FFB13B" stroke-width="8" stroke-linecap="round" fill="none">'
                f'<path d="M{fx:.0f} {fy:.0f}l-16 11M{fx:.0f} {fy:.0f}v13'
                f'M{fx:.0f} {fy:.0f}l16 11"/></g>')

    k1, k2 = (v * _FLEX for v in _sk("knee"))
    art, (fx, fy), a = _chain(ox, oy, _sk("hind"), (rot, k1 * sign, k2 * sign), limb, k)
    fw, fh = _sk("foot")
    toe = fw * 0.34 * sign
    return (art
            + _solid(f'<ellipse cx="{fx + toe:.0f}" cy="{fy + 4:.0f}" rx="{fw}" ry="{fh}"',
                     limb, k)
            + f'<ellipse cx="{fx + toe:.0f}" cy="{fy + 5:.0f}" rx="{fw * 0.44:.0f}" '
              f'ry="{fh * 0.5:.0f}" fill="{_PAD}"/>')


def _foot(x, y, rot, fill, k, rx=27, ry=15):
    return _solid(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({rot} {x} {y})"', fill, k)



def _torso(fur, k, cx=128, cy=152, rx=None, ry=None, rot=0):
    """Torso proportions come from the species build unless a pose overrides them."""
    rx = rx if rx is not None else _b("torso")[0]
    ry = ry if ry is not None else _b("torso")[1]
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    band = ""
    if _ANIMAL == "panda":     # the black band that joins a panda's forelimbs
        band = (f'<path d="M{cx - rx + 10} {cy - 8}a{rx - 10} {ry - 8} 0 0 1 {2 * (rx - 10)} 0" '
                f'fill="none" stroke="#3A3335" stroke-width="26"{t}/>')
    return _solid(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"{t}', fur, k) + band


def _belly(pad, cx=128, cy=158, rx=None, ry=None, rot=0):
    rx = rx if rx is not None else round(_b("torso")[0] * 0.58)
    ry = ry if ry is not None else round(_b("torso")[1] * 0.68)
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{pad}"{t}/>'


def _head(art, x=128, y=74, s=0.5, rot=0):
    r = f" rotate({rot})" if rot else ""
    return f'<g transform="translate({x},{y}){r} scale({s}) translate(-128,-126)">{art}</g>'


def _ball(cx, cy, r, fill, detail):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="#D9D3E6" stroke-width="4"/>'
            f'<path d="M{cx - r + 3} {cy - 5}q{r - 3} 8 {2 * r - 6} 0M{cx - r + 3} {cy + 6}'
            f'q{r - 3} -8 {2 * r - 6} 0" fill="none" stroke="{detail}" stroke-width="3"/>')


def _speed(x=34, y=150, n=3, colour=LINE):
    return "".join(f'<path d="M{x} {y + i * 22}h{34 - i * 8}" stroke="{colour}" stroke-width="8" '
                   'stroke-linecap="round" fill="none"/>' for i in range(n))


def _pose_art(animal, name, head_art):
    global _PAD, _BIRD, _ANIMAL
    fur, pad, limb, k = _parts(animal)
    _PAD, _BIRD, _ANIMAL = pad, animal == "owl", animal
    tail = TAILS.get(animal, "")

    if name == "standing":
        arms = _arm(60, 160, -14, limb, k) + _arm(196, 160, 14, limb, k)
        feet = _leg(100, limb, k) + _leg(156, limb, k)
        return (tail + arms
                + _torso(fur, k) + _belly(pad) + feet + _head(head_art))

    if name == "sitting":
        return (tail + _arm(56, 188, -10, limb, k) + _arm(200, 188, 10, limb, k)
                + _torso(fur, k, cy=170, rx=60, ry=54) + _belly(pad, cy=176, ry=38)
                + _leg(94, limb, k, rot=-8) + _leg(162, limb, k, rot=8)
                + _head(head_art, y=90, s=0.56))

    if name == "waving":
        return (tail + _arm(56, 176, -16, limb, k)
                + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(208, 128, 38, limb, k)
                + f'<g fill="none" stroke="{LINE}" stroke-width="8" stroke-linecap="round">'
                '<path d="M224 96a34 34 0 0 1 0 44"/></g>' + _head(head_art))

    if name == "running":
        return (_speed() + tail
                + _arm(196, 104, 0, limb, k)          # lead foreleg swung up and forward
                + _arm(62, 152, 42, limb, k)          # trailing foreleg swung back
                + _torso(fur, k, cx=134, cy=152, rot=-12)
                + _belly(pad, cx=134, cy=158, rot=-12)
                + _leg(100, limb, k, rot=-34)         # trailing hind leg
                + _leg(156, limb, k, rot=30)          # leading hind leg
                + _head(head_art, x=136, y=72, rot=-10))

    if name == "jumping":
        return (tail + _arm(50, 122, -44, limb, k) + _arm(206, 122, 44, limb, k)
                + _torso(fur, k, cy=158) + _belly(pad, cy=164)
                + _arm(96, 222, -28, limb, k, 17, 26) + _arm(160, 222, 28, limb, k, 17, 26)
                + f'<g fill="none" stroke="{LINE}" stroke-width="7" stroke-linecap="round">'
                '<path d="M64 240h30M162 240h30"/></g>' + _head(head_art, y=76))

    if name == "dancing":
        return (tail + _arm(42, 122, -54, limb, k)
                + _torso(fur, k, cx=132, cy=164, rot=10) + _belly(pad, cx=132, cy=170, rot=10)
                + _arm(214, 196, 40, limb, k)
                + _leg(104, limb, k, rot=-18) + _leg(166, limb, k, rot=22)
                + '<path d="M40 92v-26l20-5v26" fill="none" stroke="#FF8FA9" stroke-width="7" '
                'stroke-linecap="round"/><circle cx="35" cy="93" r="7" fill="#FF8FA9"/>'
                '<circle cx="55" cy="88" r="7" fill="#FF8FA9"/>'
                '<path d="M214 78v-22" stroke="#7EC8E3" stroke-width="7" stroke-linecap="round"/>'
                '<circle cx="209" cy="79" r="7" fill="#7EC8E3"/>'
                + _head(head_art, x=132, y=84, rot=8))

    if name == "tennis":
        return (tail + _arm(58, 180, -12, limb, k)
                + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(200, 140, 34, limb, k)
                + f'<g transform="rotate(28 214 84)"><ellipse cx="214" cy="84" rx="26" ry="31" '
                f'fill="#FFFCF8" stroke="{DARK}" stroke-width="8"/>'
                f'<path d="M196 74h36M196 90h36M206 58v52M222 58v52" stroke="{LINE}" '
                'stroke-width="4"/>'
                f'<rect x="208" y="112" width="12" height="32" rx="6" fill="{WOOD}"/></g>'
                '<circle cx="52" cy="70" r="14" fill="#D6E85B"/>'
                '<path d="M40 64a30 30 0 0 0 24 12" fill="none" stroke="#B9CC3F" stroke-width="3"/>'
                + _head(head_art))

    if name == "football":
        return (tail + _arm(58, 176, -14, limb, k) + _arm(198, 176, 14, limb, k)
                + _torso(fur, k) + _belly(pad)
                + _leg(158, limb, k, rot=6) + _leg(96, limb, k, rot=-34)
                + '<circle cx="48" cy="216" r="27" fill="#FFFCF8" stroke="#3A3335" stroke-width="6"/>'
                '<path d="m48 202 12 9-5 14H41l-5-14z" fill="#3A3335"/>'
                + _head(head_art))

    if name == "basketball":
        return (tail + _arm(56, 178, -14, limb, k)
                + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(206, 132, 30, limb, k)
                + '<circle cx="212" cy="66" r="30" fill="#E8873C"/>'
                '<path d="M182 66h60M212 36v60M190 44c14 12 14 32 0 44M234 44c-14 12-14 32 0 44" '
                'fill="none" stroke="#B5642A" stroke-width="4"/>' + _head(head_art))

    if name == "cycling":
        # no tail here — it collides with the rear wheel, and a bicycle is already
        # a lot of thin geometry at this size
        return (f'<g fill="none" stroke="{DARK}" stroke-width="11" stroke-linecap="round">'
                '<circle cx="58" cy="204" r="34"/><circle cx="198" cy="204" r="34"/>'
                '<path d="M58 204h52l30-54M110 204l30-54M140 150h34M174 150v-18"/></g>'
                f'<rect x="88" y="168" width="34" height="12" rx="6" fill="{DARK}"/>'
                f'<circle cx="128" cy="204" r="12" fill="none" stroke="{DARK}" stroke-width="8"/>'
                + _arm(156, 156, 58, limb, k, 15, 30)
                + _torso(fur, k, cx=112, cy=140, rx=46, ry=42, rot=-12)
                + _belly(pad, cx=112, cy=146, rx=27, ry=25)
                + _arm(118, 182, -20, limb, k, 14, 26)
                + _head(head_art, x=112, y=80, s=0.48, rot=-10))

    if name == "swimming":
        return (_arm(56, 168, -18, limb, k) + _arm(200, 168, 18, limb, k)
                + _torso(fur, k, cy=158, ry=54) + _belly(pad, cy=164, ry=36)
                + '<circle cx="128" cy="196" r="62" fill="none" stroke="#FF8FA9" stroke-width="26"/>'
                '<circle cx="128" cy="196" r="62" fill="none" stroke="#FFFCF8" stroke-width="26" '
                'stroke-dasharray="30 30" stroke-dashoffset="16"/>'
                f'<g fill="none" stroke="#7EC8E3" stroke-width="8" stroke-linecap="round">'
                '<path d="M8 234q14-12 28 0t28 0"/><path d="M192 234q14-12 28 0t28 0"/></g>'
                + _head(head_art, y=88))

    if name == "yoga":
        return ('<rect x="20" y="226" width="216" height="20" rx="10" fill="#7EC8E3"/>'
                '<path d="M40 236h176" stroke="#5FB0CC" stroke-width="4" stroke-linecap="round"/>'
                + tail + _arm(36, 186, -48, limb, k) + _arm(220, 186, 48, limb, k)
                + _torso(fur, k, cy=168, rx=52, ry=50) + _belly(pad, cy=174, ry=34)
                + _leg(100, limb, k, rot=22) + _leg(156, limb, k, rot=-22)
                + _head(head_art, y=88, s=0.55))

    if name == "skateboarding":
        return (tail + _arm(54, 168, -34, limb, k)
                + _torso(fur, k, cx=132, cy=158, rot=-8) + _belly(pad, cx=132, cy=164, rot=-8)
                + _arm(206, 154, 34, limb, k)
                + _leg(102, limb, k, rot=-12) + _leg(166, limb, k, rot=12)
                + f'<rect x="46" y="226" width="164" height="14" rx="7" fill="{WOOD}"/>'
                f'<circle cx="82" cy="246" r="10" fill="{DARK}"/>'
                f'<circle cx="174" cy="246" r="10" fill="{DARK}"/>'
                + _head(head_art, x=134, y=80, rot=-6))

    if name == "baseball":
        return (tail + _arm(56, 180, -14, limb, k) + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(202, 142, 30, limb, k)
                + f'<g transform="rotate(24 206 96)">'
                f'<rect x="196" y="34" width="24" height="86" rx="12" fill="{WOOD}"/>'
                f'<rect x="200" y="112" width="16" height="36" rx="8" fill="#A8814F"/></g>'
                + _ball(50, 74, 16, "#FFFCF8", "#E4574C") + _head(head_art))

    if name == "volleyball":
        return (tail + _arm(44, 126, -46, limb, k) + _arm(212, 126, 46, limb, k)
                + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _head(head_art)
                + '<circle cx="188" cy="42" r="32" fill="#FFFCF8" stroke="#3F5BC0" stroke-width="7"/>'
                '<path d="M165 23c14 12 14 26 0 38M211 23c-14 12-14 26 0 38M157 42h62" fill="none" '
                'stroke="#3F5BC0" stroke-width="6"/>')

    if name == "rugby":
        return (tail + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + '<g transform="rotate(-22 56 190)"><ellipse cx="56" cy="190" rx="36" ry="24" '
                'fill="#8A5A2B"/><path d="M40 190h32M48 182v16M64 182v16" stroke="#FFFCF8" '
                'stroke-width="5" stroke-linecap="round"/></g>'
                + _arm(60, 170, -32, limb, k) + _arm(200, 176, 16, limb, k) + _head(head_art))

    if name == "golf":
        return (tail + _torso(fur, k) + _belly(pad)
                + _leg(104, limb, k, rot=0) + _leg(160, limb, k, rot=0)
                + _arm(196, 150, 26, limb, k)
                + f'<path d="M180 128 92 226" stroke="{WOOD}" stroke-width="10" stroke-linecap="round"/>'
                f'<path d="M92 226h-26v14h26z" fill="{DARK}"/>'
                + '<circle cx="44" cy="230" r="11" fill="#FFFCF8" stroke="#D9D3E6" stroke-width="4"/>'
                f'<path d="M44 240v8" stroke="{WOOD}" stroke-width="6" stroke-linecap="round"/>'
                + _head(head_art))

    if name == "cricket":
        return (tail + _arm(56, 180, -14, limb, k) + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(200, 156, 22, limb, k)
                + '<g transform="rotate(16 208 148)">'
                f'<rect x="192" y="120" width="32" height="86" rx="8" fill="{WOOD}"/>'
                f'<rect x="202" y="72" width="12" height="52" rx="6" fill="#A8814F"/></g>'
                + _ball(48, 214, 16, "#C0392B", "#FFFCF8") + _head(head_art))

    if name == "ping_pong":
        return (tail + _arm(56, 180, -14, limb, k) + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(200, 148, 28, limb, k)
                + '<g transform="rotate(22 208 96)"><circle cx="208" cy="96" r="26" fill="#E4574C" '
                'stroke="#3A3335" stroke-width="5"/>'
                f'<rect x="200" y="120" width="16" height="30" rx="8" fill="{WOOD}"/></g>'
                + '<circle cx="52" cy="88" r="11" fill="#FFFCF8" stroke="#D9D3E6" stroke-width="4"/>'
                + _head(head_art))

    if name == "badminton":
        return (tail + _arm(56, 180, -14, limb, k) + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(200, 144, 30, limb, k)
                + f'<g transform="rotate(26 210 86)"><ellipse cx="210" cy="86" rx="24" ry="30" '
                f'fill="#FFFCF8" stroke="{DARK}" stroke-width="7"/>'
                f'<path d="M192 78h36M192 94h36M202 60v52M218 60v52" stroke="{LINE}" stroke-width="4"/>'
                f'<rect x="204" y="114" width="12" height="30" rx="6" fill="{WOOD}"/></g>'
                + '<path d="M46 56 30 88h32z" fill="#FFFCF8" stroke="#D9D3E6" stroke-width="5" '
                'stroke-linejoin="round"/><circle cx="46" cy="52" r="10" fill="#FFD86B"/>'
                + _head(head_art))

    if name == "bowling":
        return (tail + _arm(200, 178, 16, limb, k) + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(58, 176, -26, limb, k)
                + f'<circle cx="46" cy="204" r="30" fill="{DARK}"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#FFFCF8"/>'
                          for x, y in ((38, 194), (52, 192), (46, 208)))
                + '<path d="M214 178c8 0 12 8 12 18s-4 14-4 22 4 10 4 18h-24c0-8 4-10 4-18s-4-12-4-22'
                ' 4-18 12-18z" fill="#FFFCF8" stroke="#D9D3E6" stroke-width="5"/>'
                '<path d="M204 206h20" stroke="#E4574C" stroke-width="6"/>' + _head(head_art))

    if name == "hockey":
        return (tail + _arm(56, 180, -14, limb, k) + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(198, 158, 24, limb, k)
                + f'<path d="M186 132 86 226h-30" fill="none" stroke="{WOOD}" stroke-width="11" '
                'stroke-linecap="round" stroke-linejoin="round"/>'
                + f'<ellipse cx="40" cy="238" rx="22" ry="10" fill="{DARK}"/>' + _head(head_art))

    if name == "skiing":
        return (tail + _arm(48, 168, -30, limb, k) + _arm(208, 168, 30, limb, k)
                + _torso(fur, k, cx=130, rot=-8) + _belly(pad, cx=130, rot=-8)
                + f'<g stroke="{DARK}" stroke-width="8" stroke-linecap="round" fill="none">'
                '<path d="M44 174v56M212 174v56"/></g>'
                + f'<g fill="#5B7BE8"><rect x="26" y="228" width="86" height="13" rx="6" '
                'transform="rotate(-8 69 234)"/><rect x="144" y="228" width="86" height="13" rx="6" '
                'transform="rotate(-8 187 234)"/></g>'
                + _leg(84, limb, k, rot=-8) + _leg(174, limb, k, rot=-8)
                + _head(head_art, x=130, rot=-6))

    if name == "snowboarding":
        return (tail + _arm(44, 150, -44, limb, k) + _arm(214, 168, 40, limb, k)
                + _torso(fur, k, cx=130, cy=158, rot=-14) + _belly(pad, cx=130, cy=164, rot=-14)
                + _leg(100, limb, k, rot=-16) + _leg(164, limb, k, rot=-16)
                + '<rect x="34" y="222" width="188" height="18" rx="9" '
                'transform="rotate(-10 128 231)" fill="#7EC8E3"/>'
                '<rect x="34" y="222" width="188" height="18" rx="9" '
                'transform="rotate(-10 128 231)" fill="none" stroke="#5B7BE8" stroke-width="4"/>'
                + _head(head_art, x=130, y=80, rot=-12))

    if name == "surfing":
        return (tail + _arm(46, 156, -40, limb, k) + _arm(212, 156, 40, limb, k)
                + _torso(fur, k, cx=130, cy=156, rot=-10) + _belly(pad, cx=130, cy=162, rot=-10)
                + _leg(102, limb, k, rot=-12) + _leg(162, limb, k, rot=-12)
                + '<ellipse cx="128" cy="226" rx="94" ry="17" transform="rotate(-8 128 226)" '
                'fill="#FFD86B"/><path d="M44 228h168" stroke="#E8A93C" stroke-width="4"/>'
                '<g fill="none" stroke="#7EC8E3" stroke-width="9" stroke-linecap="round">'
                '<path d="M6 246q16-14 32 0t32 0"/><path d="M186 246q16-14 32 0t32 0"/></g>'
                + _head(head_art, x=130, y=80, rot=-8))

    if name == "boxing":
        body = (tail + _arm(84, 112, 0, limb, k) + _arm(172, 112, 0, limb, k)
                + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k) + _leg(156, limb, k)
                + _head(head_art))
        gloves = "".join(
            f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="24" fill="#E4574C"/>'
            f'<path d="M{gx - 22:.0f} {gy + 4:.0f}a24 24 0 0 0 20 18" fill="none" '
            f'stroke="#C0392B" stroke-width="6"/>' for gx, gy in _WRISTS[-2:])
        return body + gloves

    if name == "karate":
        return (tail + _arm(36, 168, -76, limb, k) + _torso(fur, k) + _belly(pad)
                + f'<rect x="70" y="196" width="116" height="16" rx="8" fill="{DARK}"/>'
                f'<path d="M186 196v34M172 200v30" stroke="{DARK}" stroke-width="10" '
                'stroke-linecap="round"/>'
                + _arm(206, 182, 34, limb, k)
                + _leg(96, limb, k, rot=-14) + _leg(162, limb, k, rot=14)
                + _head(head_art))

    if name == "weightlifting":
        return (tail + _arm(48, 122, -30, limb, k) + _arm(208, 122, 30, limb, k)
                + _torso(fur, k) + _belly(pad)
                + _leg(96, limb, k, rot=-12) + _leg(160, limb, k, rot=12)
                + f'<rect x="40" y="52" width="176" height="14" rx="7" fill="{LINE}"/>'
                + "".join(f'<rect x="{x}" y="30" width="24" height="58" rx="10" fill="{DARK}"/>'
                          for x in (26, 206))
                + _head(head_art))

    if name == "archery":
        return (tail + _arm(56, 172, -20, limb, k) + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(200, 156, 26, limb, k)
                + f'<path d="M212 78a76 76 0 0 1 0 132" fill="none" stroke="{WOOD}" '
                'stroke-width="11" stroke-linecap="round"/>'
                f'<path d="M212 78 176 144l36 66" fill="none" stroke="{LINE}" stroke-width="5"/>'
                f'<path d="M176 144H72" stroke="{DARK}" stroke-width="7" stroke-linecap="round"/>'
                '<path d="m72 144 18-11v22z" fill="#E4574C"/>' + _head(head_art))

    if name == "climbing":
        return (f'<path d="M212 8v240" stroke="{WOOD}" stroke-width="10" stroke-linecap="round"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="#6FBF7F"/>'
                          for x, y in ((44, 70), (54, 190)))
                + tail + _arm(50, 118, -40, limb, k) + _arm(200, 130, 34, limb, k)
                + _torso(fur, k, cy=160, ry=56) + _belly(pad, cy=166, ry=38)
                + _leg(102, limb, k, rot=-20) + _leg(158, limb, k, rot=20)
                + _head(head_art, y=78))

    if name == "rowing":
        return (tail + _arm(50, 160, -34, limb, k) + _arm(208, 178, 30, limb, k)
                + _torso(fur, k, cy=162, rot=-8) + _belly(pad, cy=168, rot=-8)
                + f'<path d="M42 140 216 214" stroke="{WOOD}" stroke-width="10" '
                'stroke-linecap="round"/>'
                '<ellipse cx="34" cy="136" rx="20" ry="13" transform="rotate(22 34 136)" '
                'fill="#5B7BE8"/>'
                + '<g fill="none" stroke="#7EC8E3" stroke-width="9" stroke-linecap="round">'
                '<path d="M8 240q16-14 32 0t32 0"/><path d="M184 240q16-14 32 0t32 0"/></g>'
                + _head(head_art, y=84, rot=-6))

    if name == "fishing":
        return (tail + _arm(56, 176, -16, limb, k) + _torso(fur, k) + _belly(pad)
                + _leg(100, limb, k, rot=0) + _leg(156, limb, k, rot=0)
                + _arm(198, 150, 28, limb, k)
                + f'<path d="M182 128 44 42" stroke="{WOOD}" stroke-width="9" stroke-linecap="round"/>'
                f'<path d="M44 42v88" stroke="{LINE}" stroke-width="4"/>'
                '<ellipse cx="44" cy="146" rx="22" ry="14" fill="#7EC8E3"/>'
                '<path d="m66 146 14-10v20z" fill="#7EC8E3"/>' + _head(head_art))

    if name == "ice_skating":
        return (tail + _arm(48, 158, -38, limb, k) + _arm(210, 166, 34, limb, k)
                + _torso(fur, k, cx=130, rot=-8) + _belly(pad, cx=130, rot=-8)
                + _leg(98, limb, k, rot=-14) + _leg(166, limb, k, rot=16)
                + f'<g stroke="{DARK}" stroke-width="7" stroke-linecap="round" fill="none">'
                '<path d="M70 242h56M138 246h56"/></g>'
                + _head(head_art, x=130, rot=-6))

    raise ValueError(name)


def pose(animal, name, head_art):
    """Draw the body, then paint any deferred parts — the owl's wings — over it."""
    global _DEFERRED, _WRISTS, _OUTLINE
    _DEFERRED, _WRISTS, _OUTLINE = [], [], []
    art = _pose_art(animal, name, head_art)
    body = "".join(_OUTLINE) + art + "".join(_DEFERRED)
    _DEFERRED, _OUTLINE = [], []
    return body


def standing(animal, head_art):
    return pose(animal, "standing", head_art)
