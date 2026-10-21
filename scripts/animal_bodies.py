#!/usr/bin/env python3
"""Full-body poses.

The body is assembled from parts — torso, belly, two arms, two legs, head — and a
pose is a set of hand and foot targets rather than a new drawing. Limb colour is a species
detail: the panda's arms and legs are black, the owl's read as wings, and the red
panda and raccoon get their ringed tails at full size.
"""

import math

from outline import INKS, sticker

# inner contour on limbs, so a limb crossing the torso still reads as a limb
INNER = 3.2

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
    "red_panda": ("#F28A2E", "#F7A452", "#7A2E1C", None),
    "rabbit": ("#FFFDFB", "#FFFFFF", "#F2A99A", None),
    "panda": ("#FFFFFF", "#F7F5FB", "#2F2A2C", None),
    "hamster": ("#9A8F88", "#FFFFFF", "#F4A48C", None),
    "raccoon": ("#A9AAB0", "#F7F5F2", "#4A3428", None),
    "owl": ("#A9AEB5", "#FFFFFF", "#969BA3", None),
}

# paw beans and foot soles — not always the belly colour: the panda has grey soles
# with beige pads, the dark-limbed red panda and raccoon have pink ones
BEANS = {
    "red_panda": "#F6B9A8", "rabbit": "#FFE0D6", "panda": "#F3C98B",
    "hamster": "#FFD9CC", "raccoon": "#D9B3A3", "owl": "#FFFFFF",
}

DARK, LINE, WOOD = "#5A5560", "#D9D3E6", "#C9A87C"


def _ringed_tail(fur, ring, d="M180 214C224 208 244 172 236 132"):
    return (f'<path d="{d}" fill="none" stroke="{fur}" stroke-width="36" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{ring}" stroke-width="36" stroke-dasharray="14 26" '
            'stroke-dashoffset="22"/>')


TAILS = {
    "red_panda": _ringed_tail("#F28A2E", "#7A2E1C"),
    "raccoon": _ringed_tail("#A9AAB0", "#4A3428"),
    # a rabbit's tail is a cotton puff, not a plume
    # front view: the puff only peeks out beside the hip
    "rabbit": '<circle cx="166" cy="184" r="15" fill="#FFFFFF"/>',
    "hamster": '<ellipse cx="170" cy="192" rx="12" ry="9" fill="#8F847D"/>',
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


def _outline(pts, ws, tans=None):
    """Close a tapered silhouette around a centreline, rounded at both ends."""
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        if tans:
            tx, ty = tans[i]
        else:
            px, py = pts[max(i - 1, 0)]
            nx, ny = pts[min(i + 1, len(pts) - 1)]
            tx, ty = nx - px, ny - py
        L = math.hypot(tx, ty) or 1
        ox, oy = -ty / L * ws[i] / 2, tx / L * ws[i] / 2
        left.append((x + ox, y + oy))
        right.append((x - ox, y - oy))
    r0, r1 = max(ws[0] / 2, 0.5), max(ws[-1] / 2, 0.5)

    def sweep(frm, centre, out):
        # 1 if turning from `frm` towards the outward direction is clockwise on screen
        ax, ay = frm[0] - centre[0], frm[1] - centre[1]
        return 1 if ax * out[1] - ay * out[0] > 0 else 0

    def tangent(i):
        if tans:
            tx, ty = tans[i]
        else:
            a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
            tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1
        return tx / L, ty / L

    te, ts = tangent(len(pts) - 1), tangent(0)
    d = "M%.1f %.1f" % left[0]
    d += "".join("L%.1f %.1f" % q for q in left[1:])
    d += "A%.1f %.1f 0 0 %d %.1f %.1f" % (r1, r1, sweep(left[-1], pts[-1], te), right[-1][0], right[-1][1])
    d += "".join("L%.1f %.1f" % q for q in reversed(right[:-1]))
    d += "A%.1f %.1f 0 0 %d %.1f %.1f" % (r0, r0, sweep(right[0], pts[0], (-ts[0], -ts[1])),
                                          left[0][0], left[0][1])
    return d + "Z"



# ===================================================================== engine
#
# A pose no longer walks bone chains. It says where each hand and foot should be;
# the engine works out shoulders and hips from the torso that was actually drawn
# (rotated, shifted or resized), grows one soft tapered limb to each target, and
# layers the result the way a plush is built:
#
#     legs (behind)  tail  side arms  torso  belly  head  props  feet  front arms  paws
#
# so a side arm grows from behind the body, a foot stands on whatever is under it,
# and a paw closes over the handle it holds.

GROUND = 238          # bottom of a standing foot
_SPECS = []
_T = None             # the torso drawn by this pose
_ANIMAL = "red_panda"
_PAD = "#FFFFFF"
_BIRD = False
_WRISTS = []
_DEFERRED = []
_PROPS = []
ARM_SLOT = "<!--arms-->"


def _b(key):
    return BUILD[_ANIMAL][key]


def _sk(key):
    return SKELETON[_ANIMAL][key]


def _world(lx, ly, T=None):
    """Torso-local point -> canvas, honouring the torso's rotation."""
    T = T or _T
    r = math.radians(T["rot"])
    c, s = math.cos(r), math.sin(r)
    return (T["cx"] + lx * c - ly * s, T["cy"] + lx * s + ly * c)


def _inside(p, T=None, k=0.92):
    T = T or _T
    r = math.radians(-T["rot"])
    dx, dy = p[0] - T["cx"], p[1] - T["cy"]
    lx = dx * math.cos(r) - dy * math.sin(r)
    ly = dx * math.sin(r) + dy * math.cos(r)
    return (lx / T["rx"]) ** 2 + (ly / T["ry"]) ** 2 < k * k


def _solid(head, fill, k=None):
    return f'{head} fill="{fill}" stroke="{INKS[_ANIMAL]}" stroke-width="{INNER}"/>'


def _limb(s, e, w0, w1, bend, fill, stroke=True, clean_root=False):
    """A plush limb: one soft tapered sausage with a gentle bend, not a bone chain.
    `bend` pushes the middle sideways (positive = to the limb's right).
    `clean_root` leaves the first third unstroked, so an arm laid over the body
    melts into it at the shoulder instead of showing a stitched cap."""
    (sx, sy), (ex, ey) = s, e
    dx, dy = ex - sx, ey - sy
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    # a quadratic Bezier whose midpoint is pushed `bend` sideways: smooth, no cusp,
    # so the inner edge of a short chubby limb never folds over itself
    cx_, cy_ = (sx + ex) / 2 + nx * bend * 2, (sy + ey) / 2 + ny * bend * 2
    n = 16
    pts, ws, tans = [], [], []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u * u * sx + 2 * u * t * cx_ + t * t * ex, u * u * sy + 2 * u * t * cy_ + t * t * ey))
        tans.append((2 * u * (cx_ - sx) + 2 * t * (ex - cx_), 2 * u * (cy_ - sy) + 2 * t * (ey - cy_)))
        ws.append((w0 + (w1 - w0) * t) * (1 + 0.05 * math.sin(math.pi * t)))
    d = _outline(pts, ws, tans)
    ang = math.degrees(math.atan2(dx, dy))
    if clean_root:
        k = len(pts) // 3
        open_d = _outline(pts[k:], ws[k:], tans[k:])
        open_d = open_d[:open_d.rindex("A")]          # drop the root cap and the close
        return (f'<path d="{d}" fill="{fill}"/>'
                f'<path d="{open_d}" fill="none" stroke="{INKS[_ANIMAL]}" stroke-width="{INNER}" '
                'stroke-linejoin="round" stroke-linecap="round"/>'), ang
    edge = f' stroke="{INKS[_ANIMAL]}" stroke-width="{INNER}" stroke-linejoin="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{edge}/>', ang


def _dark(hexcol):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.299 * r + 0.587 * g + 0.114 * b < 90


def _paw(x, y, a, fill, r, grip=False):
    """An open paw shows its beans, toes pointing down the arm. A gripping paw is a
    rounded fist with two knuckle creases, drawn over the handle it closes on."""
    ink = INKS[_ANIMAL]
    if grip:
        rot = 180 - a
        rim = ""
        if _dark(fill):     # a black paw on a dark handle needs a lighter edge to read
            rim = (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r * 1.02 - 2.6:.1f}" ry="{r * 0.92 - 2.6:.1f}" '
                   'fill="none" stroke="#8C8592" stroke-width="2.2"/>')
        return (f'<g transform="rotate({rot:.0f} {x:.1f} {y:.1f})">'
                + _solid(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r * 1.02:.1f}" ry="{r * 0.92:.1f}"', fill)
                + rim
                + "".join(f'<path d="M{x + dx * r:.1f} {y + r * 0.18:.1f}v{r * 0.55:.1f}" stroke="{ink}" '
                          f'stroke-width="2.4" stroke-linecap="round" opacity="0.55"/>' for dx in (-0.3, 0.3))
                + "</g>")
    rot = 180 - a
    return (f'<g transform="rotate({rot:.0f} {x:.1f} {y:.1f})">'
            + _solid(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r * 0.94:.1f}"', fill)
            + f'<ellipse cx="{x:.1f}" cy="{y + r * 0.2:.1f}" rx="{r * 0.5:.1f}" ry="{r * 0.4:.1f}" fill="{_PAD}"/>'
            + "".join(f'<circle cx="{x + dx * r:.1f}" cy="{y - r * 0.45:.1f}" r="{r * 0.21:.1f}" '
                      f'fill="{_PAD}"/>' for dx in (-0.46, 0, 0.46))
            + "</g>")


# -------------------------------------------------------------- pose verbs

def _arm(x, y, rot=0, fill=None, k=None, rx=None, ry=None, to=None, grip=False, front=None,
         side=None):
    """Ask for a hand at (x, y). `grip` closes the paw over a held prop; `front`
    forces the arm in front of the body (None = decide from where the hand is)."""
    hand = to or (x, y)
    _SPECS.append({"kind": "arm", "hand": hand, "fill": fill, "grip": grip, "front": front,
                   "side": side if side is not None else (-1 if hand[0] < 128 else 1)})
    return ""


def _leg(x, limb, k=None, y=206, rot=0, foot=None, sole=False):
    """Ask for a foot. Without `foot` it stands on the ground under the hip,
    swung by `rot` degrees for a stride."""
    _SPECS.append({"kind": "leg", "side": -1 if x < 128 else 1, "fill": limb, "rot": rot,
                   "foot": foot, "sole": sole})
    return ""


def _torso(fur, k=None, cx=128, cy=152, rx=None, ry=None, rot=0):
    global _T
    rx = rx if rx is not None else _b("torso")[0]
    ry = ry if ry is not None else _b("torso")[1]
    _T = {"cx": cx, "cy": cy, "rx": rx, "ry": ry, "rot": rot}
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    body = _solid(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"{t}', fur)
    if _ANIMAL == "panda":
        # the black yoke over a panda's shoulders, clipped to the body so it has no
        # cut ends — it just wraps round and runs into the arms
        cid = f"yoke-{cx}-{cy}-{rx}-{ry}-{rot}".replace(".", "_").replace("-", "_")
        body += (f'<defs><clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx - 1.6}" '
                 f'ry="{ry - 1.6}"{t}/></clipPath></defs>'
                 f'<g clip-path="url(#{cid})"><ellipse cx="{cx}" cy="{cy - ry * 0.98:.1f}" '
                 f'rx="{rx * 1.25:.1f}" ry="{ry * 0.62:.1f}" fill="#2F2A2C"{t}/></g>')
    return ARM_SLOT + body


def _belly(pad, cx=128, cy=158, rx=None, ry=None, rot=0):
    rx = rx if rx is not None else round(_b("torso")[0] * 0.58)
    ry = ry if ry is not None else round(_b("torso")[1] * 0.68)
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{pad}"{t}/>'


# ------------------------------------------------------------ the resolver

def _resolve():
    """Turn the pose's requests into drawn limbs, split into layers."""
    behind, arms, feet, front, paws = [], [], [], [], []
    T = _T
    fore = _sk("fore")
    Ln = sum(b[0] for b in fore)
    for sp in _SPECS:
        sign = sp["side"]
        if sp["kind"] == "arm":
            hx, hy = sp["hand"]
            sh_local = (sign * T["rx"] * 0.80, -T["ry"] * 0.36)
            S = _world(*sh_local)
            if hy < S[1] - 14:                      # raised: shoulder rides higher and inward
                S = _world(sign * T["rx"] * 0.70, -T["ry"] * 0.50)
            infront = sp["front"] if sp["front"] is not None else _inside((hx, hy))
            if _BIRD and sp["front"] is None:
                infront = True       # a wing lies over the body; behind it, it vanishes
            if _BIRD:
                art, paw = _wing_art(S, (hx, hy), sign, sp["fill"], sp["grip"])
            else:
                L = math.hypot(hx - S[0], hy - S[1]) or 1
                lmin, lmax = Ln * 0.72, Ln * 1.55
                if L > lmax:
                    hx, hy = S[0] + (hx - S[0]) / L * lmax, S[1] + (hy - S[1]) / L * lmax
                    L = lmax
                if not infront and L < lmin:        # tuck the root deeper, it is hidden anyway
                    S = (hx + (S[0] - hx) / L * lmin, hy + (S[1] - hy) / L * lmin)
                w0, w1 = fore[0][1] * 1.45, fore[1][1] * 1.3
                art, a = _limb(S, (hx, hy), w0, w1, 5 * sign, sp["fill"], clean_root=infront)
                paw = _paw(hx, hy, a, sp["fill"], max(_b("paw"), w1 * 0.58), sp["grip"])
            _WRISTS.append((hx, hy))
            if infront:
                front.append(art)
            else:
                arms.append(art)
            paws.append(paw)
        else:
            hip = _world(sign * T["rx"] * 0.40, T["ry"] * 0.55)
            fw, fh = _sk("foot") if not _BIRD else (0, 0)
            if not _BIRD:
                fw = fw * (0.9 if _ANIMAL == "rabbit" else 0.76)
                fh = fh * 1.12
            if sp["foot"]:
                fx, fy = sp["foot"]
            elif _BIRD:
                bottom = _world(sign * T["rx"] * 0.34, T["ry"])[1]
                r = math.radians(sp["rot"])
                fx, fy = hip[0] + math.sin(r) * 30, bottom + 12
            else:
                drop = GROUND - fh - hip[1]
                r = math.radians(sp["rot"])
                fx, fy = hip[0] + math.sin(r) * drop, hip[1] + math.cos(r) * drop
                fy = min(fy, GROUND - fh)
            if _BIRD:
                behind_art, foot_art = _owl_foot(hip, (fx, fy), sign, sp["sole"])
                behind.append(behind_art)
                feet.append(foot_art)
                continue
            femur = _sk("hind")[0][1]
            art, _ = _limb(hip, (fx, fy - fh * 0.35), femur * 1.5, femur * 1.22, -3 * sign, sp["fill"])
            behind.append(art)
            feet.append(_foot_art(fx, fy, fw, fh, sign, sp["fill"], sp["sole"]))
    return behind, arms, feet, front, paws


def _foot_art(cx, cy, fw, fh, sign, fill, sole):
    if sole:
        # a sitting plush shows its soles: an upright oval, big pad, three toe beans
        rx, ry = fw * 0.72, fw * 0.86
        return (_solid(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"', fill)
                + f'<ellipse cx="{cx:.1f}" cy="{cy + ry * 0.2:.1f}" rx="{rx * 0.55:.1f}" '
                  f'ry="{ry * 0.42:.1f}" fill="{_PAD}"/>'
                + "".join(f'<circle cx="{cx + dx * rx:.1f}" cy="{cy - ry * 0.45:.1f}" r="{rx * 0.19:.1f}" '
                          f'fill="{_PAD}"/>' for dx in (-0.5, 0, 0.5)))
    toe = fw * 0.18 * sign
    x = cx + toe
    return (_solid(f'<ellipse cx="{x:.1f}" cy="{cy:.1f}" rx="{fw:.1f}" ry="{fh:.1f}"', fill)
            + "".join(f'<circle cx="{x + dx * fw:.1f}" cy="{cy + fh * 0.18:.1f}" r="{fh * 0.2:.1f}" '
                      f'fill="{_PAD}"/>' for dx in (-0.42, 0, 0.42)))


def _wing_art(S, tip, sign, fill, grip):
    """A plush wing: short, broad at the shoulder, round at the tip, one inner
    feather curve. Never longer than the body is tall."""
    L = math.hypot(tip[0] - S[0], tip[1] - S[1]) or 1
    lmax = _T["ry"] * 0.95 + 8
    if L > lmax:
        tip = (S[0] + (tip[0] - S[0]) / L * lmax, S[1] + (tip[1] - S[1]) / L * lmax)
    art, a = _limb(S, tip, 34, 24, 7 * sign, fill, clean_root=True)
    r = math.radians(a)
    ux, uy = math.sin(r), math.cos(r)
    px, py = uy, -ux
    # one soft feather curve, well inside the wing near its tip
    c = (tip[0] - ux * 20, tip[1] - uy * 20)
    o = 5.5
    feather = (f'<path d="M{c[0] - px * o:.1f} {c[1] - py * o:.1f}Q{c[0] + ux * 7:.1f} {c[1] + uy * 7:.1f} '
               f'{c[0] + px * o:.1f} {c[1] + py * o:.1f}" fill="none" stroke="#6E6A72" '
               'stroke-width="2.4" stroke-linecap="round" opacity="0.6"/>')
    thumb = ""
    if grip:   # a little feather thumb folded over the handle
        tx, ty = tip[0] - ux * 4 - px * 7 * sign, tip[1] - uy * 4 - py * 7 * sign
        thumb = (f'<ellipse cx="{tx:.1f}" cy="{ty:.1f}" rx="7" ry="5" fill="{fill}" '
                 f'transform="rotate({-a:.0f} {tx:.1f} {ty:.1f})"/>'
                 f'<path d="M{tx - 5:.1f} {ty + 3:.1f}q5 4 10 0" fill="none" stroke="#6E6A72" '
                 'stroke-width="2.2" stroke-linecap="round" opacity="0.7"/>')
    return art + feather, thumb


def _mitten(x, y, s=1.0):
    """A plush owl foot: one flat yellow mitten with three rounded toes."""
    d = (f"M{x - 11 * s:.1f} {y - 3 * s:.1f}C{x - 15 * s:.1f} {y + 7 * s:.1f} {x - 12 * s:.1f} {y + 13 * s:.1f} "
         f"{x - 7 * s:.1f} {y + 12 * s:.1f}Q{x - 3.5 * s:.1f} {y + 15 * s:.1f} {x:.1f} {y + 12.5 * s:.1f}"
         f"Q{x + 3.5 * s:.1f} {y + 15 * s:.1f} {x + 7 * s:.1f} {y + 12 * s:.1f}C{x + 12 * s:.1f} {y + 13 * s:.1f} "
         f"{x + 15 * s:.1f} {y + 7 * s:.1f} {x + 11 * s:.1f} {y - 3 * s:.1f}Z")
    return _solid(f'<path d="{d}"', "#F2B630")


def _owl_foot(hip, target, sign, sole=False):
    """Owls keep their legs in the feathers. Near the body only a stub of shank
    shows; reaching further (a kick, a stride, a pedal) the feathered thigh comes
    out first, in body colour, and the yellow shank ends it."""
    bottom = _world(sign * _T["rx"] * 0.34, _T["ry"])[1]
    fx, fy = target
    if sole:
        return "", _mitten(fx, fy - 4, 1.2)
    out = []
    reach = math.hypot(fx - hip[0], fy - bottom)
    if fy > bottom + 16 or abs(fx - hip[0]) > 26:
        # the feathered thigh runs right down to the foot; no bare stick between
        thigh, _ = _limb(hip, (fx, fy - 2), 22, 15, -3 * sign, BODY[_ANIMAL][0])
        out.append(thigh)
    else:
        fy = bottom + 2      # feet tucked right under the feathers
    return "".join(out), _mitten(fx, fy)


def _head(art, x=128, y=74, s=0.5, rot=0):
    r = f" rotate({rot})" if rot else ""
    art = sticker(art, INKS[_ANIMAL], INNER / s)
    return f'<g transform="translate({x},{y}){r} scale({s}) translate(-128,-126)">{art}</g>'


def _prop(art):
    """A held thing: painted over the arms, under the paws that close on it."""
    _PROPS.append(art)
    return ""


def _held(art, grip, hand):
    """Move a prop drawn anywhere so its grip point sits in the hand."""
    dx, dy = hand[0] - grip[0], hand[1] - grip[1]
    return _prop(f'<g transform="translate({dx:.1f} {dy:.1f})">{art}</g>')


def _rot(p, ang, c):
    r = math.radians(ang)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(r) - y * math.sin(r), c[1] + x * math.sin(r) + y * math.cos(r))


def _ball(cx, cy, r, fill, detail):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="#D9D3E6" stroke-width="4"/>'
            f'<path d="M{cx - r + 3:.1f} {cy - 5:.1f}q{r - 3} 8 {2 * r - 6} 0M{cx - r + 3:.1f} {cy + 6:.1f}'
            f'q{r - 3} -8 {2 * r - 6} 0" fill="none" stroke="{detail}" stroke-width="3"/>')


def _speed(x=34, y=150, n=3, colour=LINE):
    return "".join(f'<path d="M{x} {y + i * 22}h{34 - i * 8}" stroke="{colour}" stroke-width="8" '
                   'stroke-linecap="round" fill="none"/>' for i in range(n))


# ---------------------------------------------------------------- props
# Each prop is drawn in its own coordinates and carries the point a paw holds.

def _racket(stringed=True, rx=26, ry=31, rot=28):
    c = (214, 84)
    art = (f'<g transform="rotate({rot} 214 84)"><ellipse cx="214" cy="84" rx="{rx}" ry="{ry}" '
           f'fill="#FFFCF8" stroke="{DARK}" stroke-width="8"/>'
           f'<path d="M196 74h36M196 90h36M206 58v52M222 58v52" stroke="{LINE}" stroke-width="4"/>'
           f'<rect x="208" y="112" width="12" height="34" rx="6" fill="{WOOD}"/></g>')
    return art, _rot((214, 134), rot, c)


def _paddle():
    art = ('<g transform="rotate(22 208 96)"><circle cx="208" cy="96" r="26" fill="#E4574C" '
           'stroke="#3A3335" stroke-width="5"/>'
           f'<rect x="200" y="120" width="16" height="30" rx="8" fill="{WOOD}"/></g>')
    return art, _rot((208, 138), 22, (208, 96))


def _bat():
    art = (f'<g transform="rotate(24 206 96)">'
           f'<rect x="196" y="34" width="24" height="86" rx="12" fill="{WOOD}"/>'
           f'<rect x="200" y="112" width="16" height="36" rx="8" fill="#A8814F"/></g>')
    return art, _rot((208, 134), 24, (206, 96))


def _cricket_bat(rot=196):
    """Held at the handle, blade raised over the shoulder — a batting stance."""
    art = (f'<g transform="rotate({rot} 208 148)">'
           f'<rect x="192" y="120" width="32" height="86" rx="8" fill="{WOOD}"/>'
           f'<rect x="202" y="72" width="12" height="52" rx="6" fill="#A8814F"/></g>')
    return art, _rot((208, 92), rot, (208, 148))


# ---------------------------------------------------------------- poses

def _pose_art(animal, name, head_art):
    global _PAD, _BIRD, _ANIMAL
    fur, pad, limb, k = BODY[animal][0], BODY[animal][1], BODY[animal][2], None
    _PAD, _BIRD, _ANIMAL = BEANS[animal], animal == "owl", animal
    tail = TAILS.get(animal, "")
    RX, RY = _b("torso")
    c, cy = 128, 152
    hang_l, hang_r = (c - RX - 12, cy + 22), (c + RX + 12, cy + 22)
    if animal == "owl":
        hang_l, hang_r = (c - RX - 20, cy + 12), (c + RX + 20, cy + 12)
    head = _head(head_art)

    def arm(p, **kw):
        return _arm(p[0], p[1], fill=limb, **kw)

    def leg(side, **kw):
        return _leg(64 if side < 0 else 192, limb, **kw)

    def std(extra_l=None, extra_r=None):
        """torso + belly + default legs; arms supplied by the pose."""
        return _torso(fur) + _belly(pad) + leg(-1) + leg(1)

    if name == "standing":
        return tail + arm(hang_l) + arm(hang_r) + std() + head

    if name == "sitting":
        T = dict(cy=172, rx=RX + 4, ry=RY + 2)
        return (tail + arm((c - RX - 14, 198)) + arm((c + RX + 14, 198))
                + _torso(fur, **T) + _belly(pad, cy=178, rx=round(RX * 0.6), ry=round(RY * 0.62))
                + leg(-1, foot=(c - 32, 222), sole=True) + leg(1, foot=(c + 32, 222), sole=True)
                + _head(head_art, y=92, s=0.56))

    if name == "waving":
        h = (c + RX + 20, cy - 54)
        return (tail + arm(hang_l) + arm(h) + std()
                + f'<g fill="none" stroke="{LINE}" stroke-width="8" stroke-linecap="round">'
                f'<path d="M{h[0] + 20} {h[1] - 30}a34 34 0 0 1 0 44"/></g>' + head)

    if name == "running":
        return (_speed() + tail
                + arm((c + RX + 18, cy - 30)) + arm((c - RX - 4, cy + 18))
                + _torso(fur, cx=134, rot=-12) + _belly(pad, cx=134, cy=158, rot=-12)
                + leg(-1, foot=(c - 46, GROUND - 12)) + leg(1, foot=(c + 48, GROUND - 26))
                + _head(head_art, x=138, y=72, rot=-10))

    if name == "jumping":
        return (tail + arm((c - RX - 16, cy - 56)) + arm((c + RX + 16, cy - 56))
                + _torso(fur, cy=146) + _belly(pad, cy=152)
                + leg(-1, foot=(c - 30, 214)) + leg(1, foot=(c + 30, 214))
                + f'<g fill="none" stroke="{LINE}" stroke-width="7" stroke-linecap="round">'
                '<path d="M74 244h30M152 244h30"/></g>' + _head(head_art, y=68))

    if name == "dancing":
        return (tail + arm((c - RX - 16, cy - 58)) + arm((c + RX + 24, cy + 24))
                + _torso(fur, cx=132, cy=160, rot=10) + _belly(pad, cx=132, cy=166, rot=10)
                + leg(-1, foot=(c - 22, GROUND - 12)) + leg(1, foot=(c + 54, 212))
                + '<path d="M40 92v-26l20-5v26" fill="none" stroke="#FF8FA9" stroke-width="7" '
                'stroke-linecap="round"/><circle cx="35" cy="93" r="7" fill="#FF8FA9"/>'
                '<circle cx="55" cy="88" r="7" fill="#FF8FA9"/>'
                '<path d="M214 78v-22" stroke="#7EC8E3" stroke-width="7" stroke-linecap="round"/>'
                '<circle cx="209" cy="79" r="7" fill="#7EC8E3"/>'
                + _head(head_art, x=132, y=82, rot=8))

    if name == "tennis":
        h = (c + RX + 16, cy - 8)
        art, g = _racket()
        return (tail + arm(hang_l) + arm(h, grip=True) + std() + head + _held(art, g, h)
                + '<circle cx="52" cy="70" r="14" fill="#D6E85B"/>'
                '<path d="M40 64a30 30 0 0 0 24 12" fill="none" stroke="#B9CC3F" stroke-width="3"/>')

    if name == "badminton":
        h = (c + RX + 16, cy - 12)
        art, g = _racket(rx=24, ry=30, rot=26)
        return (tail + arm(hang_l) + arm(h, grip=True) + std() + head + _held(art, g, h)
                + '<path d="M46 56 30 88h32z" fill="#FFFCF8" stroke="#D9D3E6" stroke-width="5" '
                'stroke-linejoin="round"/><circle cx="46" cy="52" r="10" fill="#FFD86B"/>')

    if name == "ping_pong":
        h = (c + RX + 16, cy - 6)
        art, g = _paddle()
        return (tail + arm(hang_l) + arm(h, grip=True) + std() + head + _held(art, g, h)
                + '<circle cx="52" cy="88" r="11" fill="#FFFCF8" stroke="#D9D3E6" stroke-width="4"/>')

    if name == "baseball":
        h = (c + RX + 12, cy - 12)
        art, g = _bat()
        return (tail + arm(hang_l) + arm(h, grip=True) + std() + head + _held(art, g, h)
                + _ball(50, 74, 16, "#FFFCF8", "#E4574C"))

    if name == "cricket":
        h = (c + RX + 12, cy - 4)
        art, g = _cricket_bat()
        return (tail + arm(hang_l) + arm(h, grip=True) + std() + head + _held(art, g, h)
                + _ball(46, 214, 16, "#C0392B", "#FFFCF8"))

    if name == "football":
        foot = (c - 50, GROUND - 22)
        return (tail + arm((c - RX - 16, cy + 8)) + arm((c + RX + 16, cy + 8))
                + _torso(fur) + _belly(pad) + leg(-1, foot=foot) + leg(1)
                + f'<circle cx="{foot[0] - 30}" cy="{foot[1] - 2}" r="22" fill="#FFFCF8" '
                'stroke="#3A3335" stroke-width="6"/>'
                f'<path d="m{foot[0] - 30} {foot[1] - 14} 10 7-4 12h-12l-4-12z" fill="#3A3335"/>' + head)

    if name == "basketball":
        h = (c + RX + 8, cy - 54)
        bx, by = h[0] + 8, h[1] - 32
        return (tail + arm(hang_l) + arm(h) + std() + head
                + f'<circle cx="{bx}" cy="{by}" r="28" fill="#E8873C"/>'
                f'<path d="M{bx - 28} {by}h56M{bx} {by - 28}v56M{bx - 20} {by - 20}c13 11 13 29 0 40'
                f'M{bx + 20} {by - 20}c-13 11-13 29 0 40" fill="none" stroke="#B5642A" stroke-width="4"/>')

    if name == "volleyball":
        hl, hr = (c - RX - 4, cy - 64), (c + RX + 4, cy - 64)
        return (tail + arm(hl) + arm(hr) + std() + head
                + f'<circle cx="{hr[0] + 4}" cy="{hr[1] - 32}" r="26" fill="#FFFCF8" stroke="#3F5BC0" '
                'stroke-width="6"/>'
                f'<path d="M{hr[0] - 14} {hr[1] - 50}c12 10 12 22 0 32M{hr[0] + 22} {hr[1] - 50}'
                f'c-12 10-12 22 0 32M{hr[0] - 22} {hr[1] - 32}h52" fill="none" stroke="#3F5BC0" '
                'stroke-width="5"/>')

    if name == "rugby":
        h = (c - RX - 8, cy + 14)
        return (tail + arm(h, grip=True) + arm(hang_r) + std() + head
                + f'<g transform="rotate(-22 {h[0] - 4} {h[1] + 2})"><ellipse cx="{h[0] - 4}" '
                f'cy="{h[1] + 2}" rx="32" ry="21" fill="#8A5A2B"/>'
                f'<path d="M{h[0] - 18} {h[1] + 2}h28M{h[0] - 10} {h[1] - 5}v14M{h[0] + 2} {h[1] - 5}v14" '
                'stroke="#FFFCF8" stroke-width="4.5" stroke-linecap="round"/></g>')

    if name == "golf":
        top, head_pt = (c + 16, cy + 22), (72, 232)
        def along(t):
            return (top[0] + (head_pt[0] - top[0]) * t, top[1] + (head_pt[1] - top[1]) * t)
        hr, hl = along(0.10), along(0.22)
        club = (f'<path d="M{top[0]:.1f} {top[1]:.1f}L{head_pt[0]} {head_pt[1]}" stroke="{WOOD}" '
                'stroke-width="9" stroke-linecap="round"/>'
                f'<path d="M{head_pt[0]} {head_pt[1] - 6}h-26v13h26z" fill="{DARK}"/>')
        return (tail + arm(hl, grip=True, front=True, side=-1) + arm(hr, grip=True, front=True, side=1)
                + _torso(fur) + _belly(pad) + leg(-1, rot=-6) + leg(1, rot=6) + head + _prop(club)
                + '<circle cx="34" cy="232" r="10" fill="#FFFCF8" stroke="#D9D3E6" stroke-width="4"/>')

    if name == "bowling":
        h = (c - RX - 14, cy + 36)
        return (tail + arm(h, grip=True) + arm(hang_r) + std() + head
                + f'<circle cx="{h[0] - 10}" cy="{h[1] + 10}" r="26" fill="{DARK}"/>'
                + "".join(f'<circle cx="{h[0] - 10 + dx}" cy="{h[1] + 10 + dy}" r="4.5" fill="#FFFCF8"/>'
                          for dx, dy in ((-8, -10), (6, -12), (-1, 4)))
                + '<path d="M214 178c8 0 12 8 12 18s-4 14-4 22 4 10 4 18h-24c0-8 4-10 4-18s-4-12-4-22'
                ' 4-18 12-18z" fill="#FFFCF8" stroke="#D9D3E6" stroke-width="5"/>'
                '<path d="M204 206h20" stroke="#E4574C" stroke-width="6"/>')

    if name == "hockey":
        hr = (c + RX + 6, cy - 6)
        B = (84, 230)
        hl = (hr[0] + (B[0] - hr[0]) * 0.36, hr[1] + (B[1] - hr[1]) * 0.36)
        stick = (f'<path d="M{hr[0] + 8} {hr[1] - 10}L{B[0]} {B[1]}h-30" fill="none" stroke="{WOOD}" '
                 'stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
        return (tail + arm(hl, grip=True, front=True, side=-1) + arm(hr, grip=True)
                + std() + head + _prop(stick) + f'<ellipse cx="38" cy="240" rx="18" ry="8" fill="{DARK}"/>')

    if name == "skiing":
        T = dict(cx=130, rot=-6)
        hl, hr = (c - RX - 18, cy + 16), (c + RX + 18, cy + 16)
        fl, fr = (c - 34, GROUND - 26), (c + 36, GROUND - 16)
        poles = "".join(f'<path d="M{x} {y - 10}L{x + dx} {GROUND + 6}" stroke="{DARK}" stroke-width="7" '
                        'stroke-linecap="round"/>' for (x, y), dx in ((hl, -16), (hr, 16)))
        skis = "".join(f'<rect x="{x - 44}" y="{y + 9}" width="88" height="12" rx="6" fill="#5B7BE8" '
                       f'transform="rotate(-6 {x} {y + 15})"/>' for x, y in (fl, fr))
        return (tail + arm(hl, grip=True) + arm(hr, grip=True)
                + _torso(fur, **T) + _belly(pad, cx=130, rot=-6)
                + leg(-1, foot=fl) + leg(1, foot=fr) + skis + head + _prop(poles))

    if name == "snowboarding":
        def top(x):
            return 222 - (x - 128) * math.tan(math.radians(10))
        fh = _sk("foot")[1] * 1.12
        fl, fr = (100, top(100) - fh + 2), (162, top(162) - fh + 2)
        return (tail + arm((c - RX - 24, cy - 28)) + arm((c + RX + 22, cy + 8))
                + _torso(fur, cx=130, cy=152, rot=-14) + _belly(pad, cx=130, cy=158, rot=-14)
                + leg(-1, foot=fl) + leg(1, foot=fr)
                + '<rect x="34" y="222" width="188" height="18" rx="9" '
                'transform="rotate(-10 128 231)" fill="#7EC8E3" stroke="#5B7BE8" stroke-width="4"/>'
                + _head(head_art, x=130, y=78, rot=-12))

    if name == "surfing":
        def top(x):
            return 210 - (x - 128) * math.tan(math.radians(8))
        fh = _sk("foot")[1] * 1.12
        fl, fr = (102, top(102) - fh + 3), (160, top(160) - fh + 3)
        return (tail + arm((c - RX - 26, cy - 22)) + arm((c + RX + 24, cy - 6))
                + _torso(fur, cx=130, cy=148, rot=-10) + _belly(pad, cx=130, cy=154, rot=-10)
                + leg(-1, foot=fl) + leg(1, foot=fr)
                + '<ellipse cx="128" cy="226" rx="94" ry="16" transform="rotate(-8 128 226)" '
                'fill="#FFD86B"/><path d="M48 236 208 214" stroke="#E8A93C" stroke-width="4"/>'
                '<g fill="none" stroke="#7EC8E3" stroke-width="9" stroke-linecap="round">'
                '<path d="M6 246q16-14 32 0t32 0"/><path d="M186 246q16-14 32 0t32 0"/></g>'
                + _head(head_art, x=130, y=76, rot=-8))

    if name == "skateboarding":
        fl, fr = (c - 30, 226 - _sk("foot")[1] * 1.12 + 2), (c + 34, 226 - _sk("foot")[1] * 1.12 + 2)
        return (tail + arm((c - RX - 24, cy - 10)) + arm((c + RX + 22, cy + 6))
                + _torso(fur, cx=132, cy=154, rot=-8) + _belly(pad, cx=132, cy=160, rot=-8)
                + leg(-1, foot=fl) + leg(1, foot=fr)
                + f'<rect x="46" y="226" width="164" height="14" rx="7" fill="{WOOD}"/>'
                f'<circle cx="82" cy="246" r="9" fill="{DARK}"/><circle cx="174" cy="246" r="9" fill="{DARK}"/>'
                + _head(head_art, x=134, y=78, rot=-6))

    if name == "ice_skating":
        fl, fr = (c - 30, GROUND - 16), (c + 44, GROUND - 26)
        fh = _sk("foot")[1] * 1.12
        blades = "".join(f'<path d="M{x - 22:.0f} {y + fh + 5:.0f}h44" stroke="{DARK}" stroke-width="6" '
                         'stroke-linecap="round"/>' for x, y in (fl, fr))
        return (tail + arm((c - RX - 26, cy - 14)) + arm((c + RX + 24, cy - 2))
                + _torso(fur, cx=130, rot=-8) + _belly(pad, cx=130, rot=-8)
                + leg(-1, foot=fl) + leg(1, foot=fr) + blades + _head(head_art, x=130, rot=-6))

    if name == "yoga":
        # tree pose: standing on one foot, the other sole at the knee, paws together
        return ('<rect x="40" y="228" width="176" height="16" rx="8" fill="#7EC8E3"/>'
                + tail + arm((c - 9, cy - 4), front=True) + arm((c + 9, cy - 4), front=True)
                + _torso(fur, cy=156) + _belly(pad, cy=162)
                + leg(-1, foot=(c - 8, 226 - _sk("foot")[1])) + leg(1, foot=(c + RX * 0.45, cy + 52), sole=True)
                + _head(head_art, y=78))

    if name == "boxing":
        # guard up and out in front of the shoulders, a white cuff where glove meets arm
        hl, hr = (c - RX + 4, cy - 6), (c + RX - 4, cy - 6)
        art = (tail + arm(hl, front=True) + arm(hr, front=True) + std() + head)
        _DEFERRED.append("".join(
            f'<circle cx="{x}" cy="{y + 2}" r="26" fill="#FFFFFF" stroke="{INKS[_ANIMAL]}" stroke-width="{INNER}"/>'
            f'<circle cx="{x}" cy="{y - 2}" r="24" fill="#E4574C" stroke="{INKS[_ANIMAL]}" stroke-width="{INNER}"/>'
            f'<path d="M{x - 20} {y + 2}a22 22 0 0 0 18 17" fill="none" stroke="#C0392B" stroke-width="5"/>'
            for x, y in (hl, hr)))
        return art

    if name == "karate":
        by = cy + 14
        cid = f"belt-{_ANIMAL}"
        belt = (f'<defs><clipPath id="{cid}"><ellipse cx="{c}" cy="{cy}" rx="{RX - 1.6}" ry="{RY - 1.6}"/>'
                f'</clipPath></defs><g clip-path="url(#{cid})">'
                f'<path d="M{c - RX} {by - 6}Q{c} {by + 4} {c + RX} {by - 6}v13Q{c} {by + 17} {c - RX} {by + 7}z" '
                f'fill="{DARK}"/></g>'
                f'<path d="M{c + 14} {by + 6}l6 26M{c + 6} {by + 8}l-2 24" stroke="{DARK}" stroke-width="8" '
                'stroke-linecap="round"/>')
        return (tail + arm((c - RX - 44, cy - 16), grip=True) + arm((c + RX + 4, cy + 14), grip=True)
                + _torso(fur) + _belly(pad) + belt
                + leg(-1, foot=(c - 50, GROUND - 12)) + leg(1, foot=(c + 50, GROUND - 12)) + head)

    if name == "weightlifting":
        # a deadlift: arms straight down in front, bar just above the feet
        y = cy + 56
        hl, hr = (c - RX + 10, y), (c + RX - 10, y)
        bar = (f'<rect x="{c - RX - 40}" y="{y - 6}" width="{2 * RX + 80}" height="12" rx="6" fill="#C9C3D6"/>'
               + "".join(f'<rect x="{x - 11}" y="{y - 30}" width="22" height="60" rx="9" fill="{DARK}"/>'
                         for x in (c - RX - 28, c + RX + 28)))
        return (tail + arm(hl, grip=True, front=True) + arm(hr, grip=True, front=True)
                + _torso(fur) + _belly(pad)
                + leg(-1, foot=(c - 40, GROUND - 12)) + leg(1, foot=(c + 40, GROUND - 12)) + head + _prop(bar))

    if name == "archery":
        hl, hr = (c - RX - 24, cy - 14), (c + 10, cy - 14)
        x, y = hl
        bow = (f'<path d="M{x + 10} {y - 62}Q{x - 34} {y} {x + 10} {y + 62}" fill="none" stroke="{WOOD}" '
               'stroke-width="9" stroke-linecap="round"/>'
               f'<path d="M{x + 10} {y - 62}L{hr[0]} {hr[1]}L{x + 10} {y + 62}" fill="none" '
               f'stroke="{LINE}" stroke-width="3.5"/>'
               f'<path d="M{hr[0]} {hr[1]}H{x - 34}" stroke="{DARK}" stroke-width="6" stroke-linecap="round"/>'
               f'<path d="m{x - 40} {y} 16-10v20z" fill="#E4574C"/>')
        return (tail + arm(hl, grip=True) + arm(hr, grip=True, front=True) + std() + head + _prop(bow))

    if name == "climbing":
        hr, hl = (206, cy - 54), (c - RX - 12, cy - 60)
        fl = (c - 44, 214)
        return (f'<path d="M206 8v240" stroke="{WOOD}" stroke-width="10" stroke-linecap="round"/>'
                + f'<circle cx="{hl[0] - 6}" cy="{hl[1] - 6}" r="12" fill="#6FBF7F"/>'
                f'<circle cx="{fl[0] - 6}" cy="{fl[1] + 12}" r="12" fill="#6FBF7F"/>'
                + tail + arm(hl, grip=True) + arm(hr, grip=True)
                + _torso(fur, cy=158, ry=RY + 4) + _belly(pad, cy=164)
                + leg(-1, foot=fl) + leg(1, foot=(c + 34, GROUND - 6)) + _head(head_art, y=76))

    if name == "rowing":
        hl, hr = (c - 4, cy + 10), (c + 18, cy + 16)
        oar = (f'<path d="M{c + 44} {cy + 30}L44 140" stroke="{WOOD}" stroke-width="9" stroke-linecap="round"/>'
               '<ellipse cx="36" cy="136" rx="20" ry="12" transform="rotate(22 36 136)" fill="#5B7BE8"/>')
        hull = ('<path d="M24 196h208l-18 34a14 14 0 0 1-12 8H54a14 14 0 0 1-12-8z" fill="#E4574C"/>'
                '<path d="M30 206h196" stroke="#FFFCF8" stroke-width="6" stroke-linecap="round"/>')
        return (tail + arm(hl, grip=True, front=True) + arm(hr, grip=True, front=True)
                + _torso(fur, cy=160, rot=-8) + _belly(pad, cy=166, rot=-8)
                + _head(head_art, y=84, rot=-6) + hull
                + '<g fill="none" stroke="#7EC8E3" stroke-width="9" stroke-linecap="round">'
                '<path d="M8 246q16-12 32 0t32 0"/><path d="M184 246q16-12 32 0t32 0"/></g>'
                + _prop(oar))

    if name == "fishing":
        h = (c + RX + 12, cy + 2)
        tip = (238, 40)
        rod = (f'<path d="M{h[0] - 6} {h[1] + 12}L{tip[0]} {tip[1]}" stroke="{WOOD}" stroke-width="8" '
               'stroke-linecap="round"/>'
               f'<path d="M{tip[0]} {tip[1]}v118" stroke="{LINE}" stroke-width="3"/>'
               f'<ellipse cx="{tip[0] - 4}" cy="{tip[1] + 130}" rx="10" ry="16" fill="#7EC8E3"/>'
               f'<path d="m{tip[0] - 4} {tip[1] + 144} -8 12h16z" fill="#7EC8E3"/>')
        return tail + arm(hang_l) + arm(h, grip=True) + std() + head + _prop(rod)

    if name == "cycling":
        bike = (f'<g fill="none" stroke="{DARK}" stroke-width="11" stroke-linecap="round">'
                '<circle cx="58" cy="204" r="34"/><circle cx="198" cy="204" r="34"/>'
                '<path d="M58 204h52l30-54M110 204l30-54M140 150h34M174 150v-18"/></g>'
                f'<rect x="88" y="168" width="34" height="12" rx="6" fill="{DARK}"/>'
                f'<circle cx="128" cy="204" r="12" fill="none" stroke="{DARK}" stroke-width="8"/>')
        return (bike + arm((172, 134), grip=True, side=1) + arm((164, 140), grip=True, side=1, front=False)
                + _torso(fur, cx=112, cy=140, rx=46, ry=42, rot=-12)
                + _belly(pad, cx=112, cy=146, rx=27, ry=25)
                + leg(1, foot=(142, 196)) + leg(-1, foot=(118, 214))
                + _head(head_art, x=112, y=80, s=0.48, rot=-10))

    if name == "swimming":
        return (arm((c - 50, cy + 2), front=True) + arm((c + 50, cy + 2), front=True)
                + _torso(fur, cy=158, ry=RY + 4) + _belly(pad, cy=164)
                + '<circle cx="128" cy="190" r="56" fill="none" stroke="#FF8FA9" stroke-width="24"/>'
                '<circle cx="128" cy="190" r="56" fill="none" stroke="#FFFCF8" stroke-width="24" '
                'stroke-dasharray="30 30" stroke-dashoffset="16"/>'
                '<g fill="none" stroke="#7EC8E3" stroke-width="8" stroke-linecap="round">'
                '<path d="M8 234q14-12 28 0t28 0"/><path d="M192 234q14-12 28 0t28 0"/></g>'
                + _head(head_art, y=88))

    if name == "holding":
        # the job pose: left arm relaxed, right paw wherever the tool is held
        return tail + arm(hang_l) + std() + head

    raise ValueError(name)


def pose(animal, name, head_art, grip=None, held=""):
    """Draw a pose. `grip` adds a right paw holding something at that point and
    `held` is the thing, drawn between the arm and the paw that closes on it."""
    global _DEFERRED, _WRISTS, _SPECS, _T, _PROPS
    _DEFERRED, _WRISTS, _SPECS, _T, _PROPS = [], [], [], None, []
    art = _pose_art(animal, name, head_art)
    if name == "holding":
        if grip:
            _arm(*grip, fill=BODY[animal][2], grip=True)
        else:
            _arm(128 + _b("torso")[0] + 12, 174, fill=BODY[animal][2])
    behind, arms, feet, front, paws = _resolve()
    art = art.replace(ARM_SLOT, "".join(arms), 1).replace(ARM_SLOT, "")
    return ("".join(behind) + art + "".join(feet) + "".join(front) + "".join(_PROPS) + held
            + "".join(paws) + "".join(_DEFERRED))


def standing(animal, head_art):
    return pose(animal, "standing", head_art)


def seated(animal, face, held, grips, owl_tilt=0):
    """The action layer: a seated body under a big head, arms reaching the prop."""
    global _DEFERRED, _WRISTS, _SPECS, _T, _PAD, _BIRD, _ANIMAL, _PROPS
    _DEFERRED, _WRISTS, _SPECS, _T, _PROPS = [], [], [], None, []
    _PAD, _BIRD, _ANIMAL = BEANS[animal], animal == "owl", animal
    fur, pad, limb = BODY[animal][:3]
    tail = TAILS.get(animal, "")
    # a seated tail curls round the hip, it does not reach up to the ears
    tail = f'<g transform="translate(40 58) scale(0.78)">{tail}</g>' if tail else ""
    torso = _torso(fur, cy=204, rx=60, ry=40) + _belly(pad, cy=212, rx=36, ry=25)
    for g in grips:
        _arm(*g, fill=limb, grip=True)
    if not grips:
        _arm(56, 226, fill=limb)
        _arm(200, 226, fill=limb)
    # soles peeking out under the seated body
    _leg(64, limb, foot=(92, 230), sole=True)
    _leg(192, limb, foot=(164, 230), sole=True)
    behind, arms, feet, front, paws = _resolve()
    torso = torso.replace(ARM_SLOT, "".join(arms))
    head = f'<g transform="translate(128,92) scale(0.62) translate(-128,-126)">{face}</g>'
    art = ("".join(behind) + tail + torso + "".join(feet) + head + "".join(front) + held
           + "".join(paws))
    # a touch smaller about the top of the canvas, so the seat never clips
    return f'<g transform="translate(7.7 4) scale(0.94)">{art}</g>'
