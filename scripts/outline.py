#!/usr/bin/env python3
"""Die-cut sticker outline for the character layers.

`sticker(art, ink, w)` returns a silhouette pass followed by the art itself.
The silhouette is the same markup with every fill and stroke turned to `ink`
and every shape grown by `w` on all sides, so once the art is painted on top
only the outer contour shows: a single, even keyline around the whole figure,
props included. Internal overlaps stay clean because they are covered.

Growth is kept even in output units: inside a `scale(s)` group the stroke is
divided by s, so a head placed at half size still gets the same line as the
body it sits on.

Deliberately skipped in the silhouette:
  - anything translucent (blush, highlights) — it would print as a dark blob
  - hairline strokes below MIN_STROKE (whiskers, feather quills, racket strings)
  - clip-path groups and <defs> — their content already sits inside the head
"""

import re

MIN_STROKE = 5.0

# one keyline colour per character — a darker, warmer take on its own fur
INKS = {
    "red_panda": "#5A2412", "rabbit": "#6B5250", "panda": "#2E282A",
    "hamster": "#4A3E38", "raccoon": "#3A2C26", "owl": "#45434B",
}
_TAG = re.compile(r"<(/?)([a-zA-Z]+)((?:\s+[^\s=>/]+=\"[^\"]*\")*)\s*(/?)>")
_ATTR = re.compile(r'([^\s=]+)="([^"]*)"')
_SCALE = re.compile(r"scale\(\s*([-\d.]+)(?:[\s,]+([-\d.]+))?\s*\)")
_LEAVES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}


def _scale_of(transform):
    s = 1.0
    for m in _SCALE.finditer(transform or ""):
        sx = abs(float(m.group(1)))
        sy = abs(float(m.group(2))) if m.group(2) else sx
        s *= (sx + sy) / 2
    return s or 1.0


def _num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _translucent(attrs):
    for key in ("opacity", "fill-opacity"):
        if key in attrs and _num(attrs[key], 1) < 0.99:
            return True
    return False


def _fmt(attrs):
    return "".join(f' {k}="{v}"' for k, v in attrs.items())


def silhouette(art, ink, w):
    art = re.sub(r"<defs>.*?</defs>", "", art, flags=re.S)
    art = re.sub(r"<title[^>]*>.*?</title>", "", art, flags=re.S)
    art = re.sub(r'<g clip-path="[^"]*">.*?</g>', "", art, flags=re.S)

    out = []
    # inherited state: fill, stroke, stroke-width, cumulative scale, skip
    stack = [{"fill": "#000", "stroke": None, "sw": 1.0, "scale": 1.0, "skip": False}]

    for m in _TAG.finditer(art):
        closing, name, raw, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
        if closing:
            if name == "g":
                if not stack[-1]["skip"]:
                    out.append("</g>")
                if len(stack) > 1:
                    stack.pop()
            continue

        attrs = dict(_ATTR.findall(raw))
        ctx = stack[-1]
        fill = attrs.get("fill", ctx["fill"])
        stroke = attrs.get("stroke", ctx["stroke"])
        sw = _num(attrs.get("stroke-width"), ctx["sw"])

        if name == "g":
            scale = ctx["scale"] * _scale_of(attrs.get("transform"))
            # an inner keyline is always covered by this, wider, one
            skip = ctx["skip"] or _translucent(attrs) or attrs.get("class") == "outline"
            stack.append({"fill": fill, "stroke": stroke, "sw": sw, "scale": scale, "skip": skip})
            g = {k: v for k, v in attrs.items() if k == "transform"}
            if not skip:
                out.append(f"<g{_fmt(g)}>")
            if selfclose:
                stack.pop()
                if not skip:
                    out.append("</g>")
            continue

        if name not in _LEAVES or ctx["skip"] or _translucent(attrs):
            continue

        grow = 2 * w / ctx["scale"]
        has_fill = fill not in (None, "none", "transparent")
        has_stroke = stroke not in (None, "none") and sw > 0
        keep = {k: v for k, v in attrs.items()
                if k in ("d", "cx", "cy", "r", "rx", "ry", "x", "y", "width", "height",
                         "points", "x1", "y1", "x2", "y2", "transform", "stroke-linecap")}

        if has_fill:
            base = sw if has_stroke else 0.0
            keep.update({"fill": ink, "stroke": ink, "stroke-width": f"{base + grow:.1f}".replace(".0", "") if (base + grow) % 1 == 0 else f"{base + grow:.1f}",
                         "stroke-linejoin": "round"})
        elif has_stroke:
            if sw * ctx["scale"] < MIN_STROKE:
                continue
            keep.update({"fill": "none", "stroke": ink, "stroke-width": f"{sw + grow:.1f}",
                         "stroke-linejoin": "round"})
            keep.setdefault("stroke-linecap", attrs.get("stroke-linecap", "round"))
        else:
            continue
        out.append(f"<{name}{_fmt(keep)}/>")

    return "".join(out)


def sticker(art, ink, w):
    return f'<g class="outline">{silhouette(art, ink, w)}</g>{art}'
