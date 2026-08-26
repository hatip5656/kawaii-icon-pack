#!/usr/bin/env python3
"""Build preview/index.html.

The character tables read one row per icon code and one column per animal, so the
first column is the code you type and the row shows it drawn for every character.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "svg"
OUT = ROOT / "preview" / "index.html"

TINT = {
    "red_panda": "#FFF0E6",
    "rabbit": "#F4F1FB",
    "panda": "#F1F3F8",
    "hamster": "#FFF7E8",
    "raccoon": "#F2F3F7",
    "owl": "#F2EEFF",
}


def inline(path: Path, suffix: str) -> str:
    """Inline one SVG, namespacing ids so hundreds can share a document."""
    svg = path.read_text().strip()
    for ident in set(re.findall(r'id="([^"]+)"', svg)):
        new = f"{ident}-{suffix}"
        svg = svg.replace(f'id="{ident}"', f'id="{new}"')
        svg = svg.replace(f"url(#{ident})", f"url(#{new})")
        svg = svg.replace(f'aria-labelledby="{ident}"', f'aria-labelledby="{new}"')
    return re.sub(r'\swidth="\d+"\sheight="\d+"', "", svg, count=1)


def cell(path: Path, code: str, tint: str) -> str:
    return (f'<button class="cell" data-code="{code}" title="Copy {code}">'
            f'<span class="art" style="--tint:{tint}">{inline(path, code)}</span>'
            f'<code>{code}</code></button>')


def table(manifest, keys, folder, labels) -> str:
    """Rows are icon codes, columns are animals."""
    animals = list(manifest["animals"])
    head = "".join(
        f'<th class="col-head">{manifest["animals"][a]}<span>{a}</span></th>' for a in animals
    )
    rows = []
    for key in keys:
        cells = "".join(
            f'<td>{cell(SVG_DIR / folder / f"{key}_{a}.svg", f"{key}_{a}", TINT.get(a, "#F7F5FA"))}</td>'
            for a in animals
        )
        rows.append(
            f'<tr><th class="row-head"><b>{labels[key]}</b>'
            f'<code>{key}_&#123;animal&#125;</code></th>{cells}</tr>'
        )
    return (f'<div class="scroller"><table><thead><tr><th class="row-head">Icon code</th>{head}</tr>'
            f'</thead><tbody>{"".join(rows)}</tbody></table></div>')


def build() -> str:
    m = json.loads((ROOT / "icons.json").read_text())
    c = m["counts"]

    faces = table(m, m["expressions"], "characters",
                  {e: e.capitalize() for e in m["expressions"]})
    status = table(m, list(m["badges"]), "status",
                   {k: v.split(" /")[0] for k, v in m["badges"].items()})
    ratings = table(m, list(m["ratings"]), "characters", m["ratings"])
    paws = table(m, list(m["gestures"]), "paws", m["gestures"])
    frames = table(m, list(m["frames"]), "frames", m["frames"])
    extras = table(m, list(m["extras"]), "extras", m["extras"])
    actions = table(m, list(m["actions"]), "actions", m["actions"])
    bodies = table(m, list(m["bodies"]), "bodies", m["bodies"])
    jobs = table(m, list(m["jobs"]), "jobs", m["jobs"])
    badges = "".join(
        cell(SVG_DIR / "badges" / f"badge_{b}.svg", f"badge_{b}", "#FFFFFF") for b in m["badges"]
    )
    faced = {n[:-6] for n in m["ui"] if n.endswith("_plain")}
    ui_blocks = []
    for g in m["ui_groups"]:
        tiles = "".join(
            cell(SVG_DIR / "ui" / f"{n}.svg", n, "#FFFFFF")
            + (cell(SVG_DIR / "ui" / f"{n}_plain.svg", f"{n}_plain", "#FBF7FF") if n in faced else "")
            for n in g["icons"]
        )
        ui_blocks.append(f'<h3>{g["title"]} <span>{len(g["icons"])}</span></h3>'
                         f'<div class="grid">{tiles}</div>')
    ui = "".join(ui_blocks)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kawaii Animals — {m["total"]} icons</title>
<style>
  :root {{
    --ink: #3F3550; --muted: #8A7F9B; --page: #FFFCF8; --surface: #FFFFFF;
    --line: #EFE9F5; --accent: #E97A4E;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 40px 24px 80px; color: var(--ink);
    background: radial-gradient(1200px 600px at 50% -10%, #FFF1F6 0%, var(--page) 60%);
    font: 15px/1.5 ui-rounded, "SF Pro Rounded", Nunito, "Segoe UI", system-ui, sans-serif;
  }}
  .wrap {{ max-width: 1120px; margin: 0 auto; }}
  h1 {{ margin: 0 0 6px; font-size: 32px; letter-spacing: -0.5px; }}
  .lede {{ margin: 0 0 18px; color: var(--muted); }}
  .legend {{
    display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 18px;
    font-size: 12px; color: var(--muted); align-items: center;
  }}
  .legend code {{
    background: var(--surface); border: 1px solid var(--line);
    padding: 4px 9px; border-radius: 999px; color: var(--ink);
  }}
  #search {{
    width: 100%; padding: 12px 16px; font: inherit; color: var(--ink);
    background: var(--surface); border: 1px solid var(--line); border-radius: 14px;
  }}
  #search:focus {{ outline: 2px solid var(--accent); outline-offset: 1px; }}
  #count {{ font-size: 12px; color: var(--muted); min-height: 20px; padding-top: 4px; }}
  #nav {{
    position: sticky; top: 0; z-index: 5; display: flex; gap: 6px; flex-wrap: wrap;
    padding: 10px 0; margin-bottom: 4px;
    background: linear-gradient(var(--page) 70%, transparent);
  }}
  #nav a {{
    font-size: 12px; text-decoration: none; color: var(--muted);
    background: var(--surface); border: 1px solid var(--line);
    padding: 5px 12px; border-radius: 999px;
  }}
  #nav a:hover {{ color: var(--accent); border-color: var(--accent); }}
  h2 {{
    scroll-margin-top: 56px;
    margin: 40px 0 4px; font-size: 13px; text-transform: uppercase;
    letter-spacing: 0.12em; color: var(--muted);
  }}
  h2 + p {{ margin: 0 0 14px; font-size: 13px; color: var(--muted); }}
  h3 {{
    margin: 22px 0 8px; font-size: 12px; font-weight: 600; color: var(--ink);
    display: flex; align-items: center; gap: 8px;
  }}
  h3 span {{
    font-weight: 400; font-size: 11px; color: var(--muted);
    background: var(--surface); border: 1px solid var(--line);
    padding: 1px 8px; border-radius: 999px;
  }}
  .cell {{
    display: flex; flex-direction: column; align-items: center; gap: 6px; width: 100%;
    padding: 8px 4px; background: none; border: 0; border-radius: 12px;
    font: inherit; color: inherit; cursor: pointer; min-width: 0;
  }}
  .cell:hover {{ background: #FFF1E9; }}
  .cell code {{
    font: 10.5px/1.3 ui-monospace, SFMono-Regular, Menlo, monospace;
    color: var(--muted); overflow-wrap: anywhere; max-width: 100%;
  }}
  .cell:hover code {{ color: var(--accent); }}
  .art {{
    display: grid; place-items: center; width: 100%; aspect-ratio: 1;
    background: var(--tint); border-radius: 12px; padding: 8px;
  }}
  .art svg {{ display: block; width: 100%; height: auto; }}
  .scroller {{
    overflow-x: auto; background: var(--surface);
    border: 1px solid var(--line); border-radius: 18px;
  }}
  table {{ border-collapse: collapse; table-layout: fixed; width: 100%; min-width: 900px; }}
  td {{ padding: 4px; width: 148px; overflow: hidden; }}
  .col-head {{
    font-size: 13px; padding: 12px 4px 10px; border-bottom: 1px solid var(--line);
  }}
  .col-head span {{
    display: block; font-weight: 400; font-size: 10.5px; color: var(--muted);
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  }}
  thead .row-head {{
    font-size: 11px; text-transform: uppercase; letter-spacing: .1em; color: var(--muted);
    border-bottom: 1px solid var(--line); vertical-align: bottom; padding-bottom: 12px;
  }}
  .row-head {{
    position: sticky; left: 0; z-index: 1; background: var(--surface);
    text-align: left; padding: 10px 16px; width: 172px; white-space: nowrap;
  }}
  .row-head b {{ display: block; font-size: 14px; font-weight: 600; }}
  .row-head code {{
    font: 11px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--muted);
  }}
  tbody tr + tr th, tbody tr + tr td {{ border-top: 1px solid var(--line); }}
  .grid {{
    display: grid; gap: 6px; grid-template-columns: repeat(auto-fill, minmax(92px, 1fr));
    background: var(--surface); border: 1px solid var(--line); border-radius: 18px; padding: 12px;
  }}
  .grid .art {{ padding: 14px; }}
  .dim {{ opacity: 0.1; }}
  #toast {{
    position: fixed; left: 50%; bottom: 28px; transform: translate(-50%, 14px);
    background: var(--ink); color: #fff; padding: 10px 18px; border-radius: 999px;
    font-size: 13px; opacity: 0; pointer-events: none; transition: .18s;
  }}
  #toast.on {{ opacity: 1; transform: translate(-50%, 0); }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Kawaii Animals</h1>
  <p class="lede">{c["characters"]} faces &middot; {c["paws"]} paw gestures &middot;
     {c["jobs"]} jobs &middot; {c["bodies"]} bodies &middot; {c["actions"]} actions &middot; {c["extras"]} accessories &middot; {c["frames"]} compositions &middot; {c["status"]} status avatars &middot; {c["badges"]} badges
     &middot; {c["ui"]} kawaii UI icons. Click any icon to copy its code.</p>
  <div class="legend">
    <span>Naming:</span>
    <code>&lt;expression&gt;_&lt;animal&gt;</code>
    <code>&lt;status&gt;_&lt;animal&gt;</code>
    <code>badge_&lt;status&gt;</code>
    <code>&lt;ui_name&gt;</code>
  </div>
  <input id="search" type="search" placeholder="Filter by code — try rabbit, sleepy, online, cart">
  <div id="count"></div>
  <nav id="nav">
    <a href="#expressions">Expressions</a>
    <a href="#ratings">Rating faces</a>
    <a href="#paws">Paw gestures</a>
    <a href="#bodies">Full bodies</a>
    <a href="#jobs">Occupations</a>
    <a href="#actions">Doing things</a>
    <a href="#extras">Accessories</a>
    <a href="#frames">Compositions</a>
    <a href="#status">Status avatars</a>
    <a href="#badges">Badges</a>
    <a href="#ui">UI icons</a>
  </nav>

  <h2 id="expressions">Expressions</h2>
  <p>Swap <code>&#123;animal&#125;</code> for any character in the columns.</p>
  {faces}

  <h2 id="ratings">Rating faces</h2>
  <p>A calibrated five-step scale per character — drop straight into a feedback widget.
     The plain circle versions live in the UI section.</p>
  {ratings}

  <h2 id="paws">Paw gestures</h2>
  <p>Every gesture in each character's own colours — and as a wing for the owl, which
     does not have paws. The monochrome line versions live in the UI section.</p>
  {paws}

  <h2 id="bodies">Full bodies</h2>
  <p>The whole character, not just the face. Limb colour is a species detail — the
     panda's arms and legs are black, the owl has wings and talons, and the red panda
     gets its ringed tail at full size.</p>
  {bodies}

  <h2 id="jobs">Occupations</h2>
  <p>Each job is headwear + uniform + tool over the standing body, so the set is a data
     table rather than 43 separate drawings.</p>
  {jobs}

  <h2 id="actions">Doing things</h2>
  <p>Verbs. The face sits above, the prop below, and the paws grip it — with one accent
     element in each character's own colour.</p>
  {actions}

  <h2 id="extras">Accessories &amp; snacks</h2>
  <p>The same face dressed for the occasion — and one signature food per character,
     because a panda with bamboo is not the same animal as a rabbit with a carrot.</p>
  {extras}

  <h2 id="frames">Compositions</h2>
  <p>The characters placed into container shapes, for bubbles, stickers and empty states.</p>
  {frames}

  <h2 id="status">Status avatars</h2>
  <p>The happy face with a status badge in the corner.</p>
  {status}

  <h2 id="badges">Status badges</h2>
  <p>Character-independent — drop one over any avatar yourself.</p>
  <div class="grid">{badges}</div>

  <h2 id="ui">UI icons</h2>
  <p>Kawaii too — faces on the objects, paws for every gesture. Monochrome, 24px grid,
     inherits <code>currentColor</code>. Faced icons are followed by their
     <code>_plain</code> twin (tinted), for 16px chrome where the eyes turn to mush.</p>
  {ui}
</div>
<div id="toast"></div>
<script>
  const cells = [...document.querySelectorAll(".cell")];
  const rows = [...document.querySelectorAll("tbody tr")];
  const toast = document.getElementById("toast");
  const count = document.getElementById("count");
  let timer;

  function flash(text) {{
    toast.textContent = text;
    toast.classList.add("on");
    clearTimeout(timer);
    timer = setTimeout(() => toast.classList.remove("on"), 1400);
  }}

  // navigator.clipboard needs a secure context, which file:// is not — so fall
  // back to the legacy path and keep this page a plain double-click-to-open file.
  async function copy(text) {{
    try {{
      if (navigator.clipboard && window.isSecureContext) {{
        await navigator.clipboard.writeText(text);
        return true;
      }}
    }} catch {{}}
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;top:-1000px;opacity:0";
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try {{ ok = document.execCommand("copy"); }} catch {{}}
    document.body.removeChild(ta);
    return ok;
  }}

  for (const cell of cells) {{
    cell.addEventListener("click", async () => {{
      const code = cell.dataset.code;
      flash(await copy(code) ? `Copied ${{code}}` : code);
    }});
  }}

  document.getElementById("search").addEventListener("input", (e) => {{
    const q = e.target.value.trim().toLowerCase();
    let hits = 0;
    for (const cell of cells) {{
      const match = !q || cell.dataset.code.includes(q);
      cell.classList.toggle("dim", !match);
      if (match) hits++;
    }}
    for (const row of rows) {{
      const any = [...row.querySelectorAll(".cell")].some((c) => !c.classList.contains("dim"));
      row.querySelector(".row-head").classList.toggle("dim", !any);
    }}
    count.textContent = q ? `${{hits}} of ${{cells.length}} icons match` : "";
  }});
</script>
</body>
</html>
"""


# --------------------------------------------------------------- README sheets
#
# GitHub cannot embed the interactive preview, but it does render SVG images, so
# the pack ships flat contact sheets the README can show inline. Icons are
# inlined as <g transform> rather than nested <svg>, which GitHub's sanitiser
# handles far more reliably.

SHEETS_DIR = ROOT / "preview" / "sheets"
INK = "#3F3550"

SAMPLE = {
    "characters": 42, "ui": 48, "paws": 30, "bodies": 24, "jobs": 24,
    "actions": 24, "status": 18, "extras": 18, "frames": 12, "badges": 10,
}

HERO = [
    "characters/happy_red_panda", "characters/love_rabbit", "characters/cool_panda",
    "characters/sleepy_hamster", "characters/wink_raccoon", "characters/laughing_owl",
    "paws/wave_rabbit", "paws/heart_hands_panda", "paws/thumbs_up_raccoon",
    "paws/peace_hamster", "paws/high_five_red_panda", "paws/grab_owl",
    "bodies/running_rabbit", "bodies/skateboarding_raccoon", "jobs/chef_panda",
    "jobs/astronaut_owl", "actions/celebrating_red_panda", "frames/hug_hamster",
    "status/online_rabbit", "status/busy_panda", "extras/party_hat_raccoon",
    "ui/heart", "ui/star", "ui/search", "ui/bell", "ui/cloud", "ui/rocket", "ui/paw",
]


def _inner(path: Path, suffix: str):
    """(drawing, viewBox size) with ids namespaced and the title dropped.

    Layers do not share a canvas — characters are 256, UI glyphs are 24 — so the
    box has to be read per icon or the small ones end up as dots.
    """
    svg = path.read_text()
    root = svg[svg.index("<svg"):svg.index(">", svg.index("<svg"))]
    box = re.search(r'viewBox="([\d.\s-]+)"', svg).group(1).split()
    size = max(float(box[2]), float(box[3]))

    # The UI layer sets fill/stroke on the root <svg>; drop those and the line
    # icons render as solid black blobs, so they move onto the wrapper.
    carried = ("fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin",
               "stroke-miterlimit", "fill-rule", "clip-rule", "opacity", "color")
    attrs = " ".join(f'{k}="{v}"' for k, v in re.findall(r'([\w-]+)="([^"]*)"', root)
                     if k in carried)

    body = svg[svg.index(">", svg.index("<svg")) + 1:svg.rindex("</svg>")]
    body = re.sub(r"<title.*?</title>", "", body, flags=re.S)
    for ident in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{ident}"', f'id="{ident}-{suffix}"')
        body = body.replace(f"url(#{ident})", f"url(#{ident}-{suffix})")
    return body.strip(), size, attrs


def sheet(paths, cols: int, cell: int = 128, pad: float = 0.86) -> str:
    rows = -(-len(paths) // cols)
    parts = []
    for i, path in enumerate(paths):
        art, size, attrs = _inner(path, str(i))
        scale = cell * pad / size
        ox = (i % cols) * cell + (cell - size * scale) / 2
        oy = (i // cols) * cell + (cell - size * scale) / 2
        head = f'transform="translate({ox:.4g} {oy:.4g}) scale({scale:.4g})"'
        parts.append(f'<g {head}{" " + attrs if attrs else ""}>{art}</g>')
    body = "".join(parts)
    w, h = cols * cell, rows * cell
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">'
            f'<rect width="100%" height="100%" fill="#FFFCF8" rx="16"/>'
            f'<g color="{INK}">{body}</g></svg>\n')


def spread(items, n):
    """n items sampled evenly across the list, so a sheet shows the whole range."""
    if len(items) <= n:
        return items
    step = len(items) / n
    return [items[int(i * step)] for i in range(n)]


def build_sheets() -> None:
    SHEETS_DIR.mkdir(parents=True, exist_ok=True)
    written = []

    hero = [SVG_DIR / f"{name}.svg" for name in HERO]
    missing = [p for p in hero if not p.exists()]
    if missing:
        raise SystemExit(f"hero sheet references missing icons: {missing}")
    (SHEETS_DIR / "hero.svg").write_text(sheet(hero, cols=7))
    written.append("hero")

    for layer, n in SAMPLE.items():
        paths = spread(sorted((SVG_DIR / layer).glob("*.svg")), n)
        cols = 10 if layer in ("ui", "badges") else 6
        (SHEETS_DIR / f"{layer}.svg").write_text(sheet(paths, cols=cols))
        written.append(layer)

    total = sum((SHEETS_DIR / f"{n}.svg").stat().st_size for n in written)
    print(f"wrote {len(written)} README sheets ({total // 1024} KB total)")


if __name__ == "__main__":
    OUT.write_text(build())
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
    build_sheets()
