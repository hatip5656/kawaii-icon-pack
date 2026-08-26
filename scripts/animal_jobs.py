#!/usr/bin/env python3
"""Occupations, built on the standing body.

Each job is a row of data — headwear, uniform, tool — not a bespoke drawing, so the
set stays consistent and a new job costs one line. Coordinates assume the body pose:
head centred at (128, 74) spanning y 28-120, torso y 116-212, right paw near (200, 150).
"""

WHITE, LINE, DARK, WOOD = "#FFFFFF", "#E4E0F0", "#5A5560", "#C9A87C"
STEEL, GOLD, RED, TEAL = "#B9C0CC", "#FFD86B", "#E4574C", "#6FBFB8"


# ----------------------------------------------------------------- headwear
def hat(kind):
    if kind == "cap":
        return ('<path d="M92 48a36 30 0 0 1 72 0z" fill="#3B4A6B"/>'
                '<path d="M88 44h80v12H88z" fill="#313E5A"/>'
                '<path d="M164 46h34a6 6 0 0 1 0 12h-34z" fill="#313E5A"/>')
    if kind == "cap_red":
        return hat("cap").replace("#3B4A6B", "#E4574C").replace("#313E5A", "#C0392B")
    if kind == "cap_blue":
        return hat("cap").replace("#3B4A6B", "#5B7BE8").replace("#313E5A", "#3F5BC0")
    if kind == "cap_green":
        return hat("cap").replace("#3B4A6B", "#4F8A5B").replace("#313E5A", "#3D6E48")
    if kind == "toque":
        return ('<g fill="#FFFFFF" stroke="#E4E0F0" stroke-width="4">'
                '<circle cx="104" cy="28" r="21"/><circle cx="152" cy="28" r="21"/>'
                '<circle cx="128" cy="20" r="25"/>'
                '<rect x="96" y="36" width="64" height="22" rx="9"/></g>')
    if kind == "hardhat":
        return ('<path d="M92 50a36 32 0 0 1 72 0z" fill="#FFC24A"/>'
                '<rect x="78" y="46" width="100" height="11" rx="5" fill="#FFC24A"/>'
                '<path d="M128 20v30" stroke="#E8A93C" stroke-width="7" stroke-linecap="round"/>')
    if kind == "fire_helmet":
        return ('<path d="M92 50a36 32 0 0 1 72 0z" fill="#E4574C"/>'
                '<path d="M74 46h108l10 14H64z" fill="#C0392B"/>'
                '<path d="M128 22l10 22h-20z" fill="#FFD86B"/>')
    if kind == "grad_cap":
        return ('<path d="m128 16 66 26-66 26-66-26z" fill="#3A3335"/>'
                '<path d="M102 56v16c0 9 52 9 52 0V56" fill="#3A3335"/>'
                '<path d="M194 42v28" stroke="#FFD86B" stroke-width="5"/>'
                '<circle cx="194" cy="74" r="7" fill="#FFD86B"/>')
    if kind == "beret":
        return ('<ellipse cx="126" cy="42" rx="46" ry="20" fill="#E4574C"/>'
                '<circle cx="154" cy="26" r="8" fill="#C0392B"/>')
    if kind == "scrub_cap":
        return ('<path d="M92 52a36 30 0 0 1 72 0z" fill="#6FBFB8"/>'
                '<rect x="86" y="48" width="84" height="11" rx="5" fill="#5AA9A2"/>')
    if kind == "nurse_cap":
        return ('<path d="m98 50 18-24h24l18 24z" fill="#FFFFFF" stroke="#E4E0F0" stroke-width="4"/>'
                '<path d="M128 32v14M121 39h14" stroke="#E4574C" stroke-width="5" stroke-linecap="round"/>')
    if kind == "straw_hat":
        return ('<ellipse cx="128" cy="50" rx="64" ry="15" fill="#E8C88A"/>'
                '<path d="M100 48a28 26 0 0 1 56 0z" fill="#E8C88A"/>'
                '<rect x="99" y="40" width="58" height="9" rx="4" fill="#C9A87C"/>')
    if kind == "sailor_cap":
        return ('<path d="M94 48a34 28 0 0 1 68 0z" fill="#FFFFFF" stroke="#E4E0F0" stroke-width="4"/>'
                '<rect x="90" y="44" width="76" height="12" rx="5" fill="#3B4A6B"/>')
    if kind == "pilot_cap":
        return (hat("cap").replace("#3B4A6B", "#25324B").replace("#313E5A", "#18233A")
                + '<path d="M128 32l7 10h-14z" fill="#FFD86B"/>')
    if kind == "space_helmet":
        return ('<circle cx="128" cy="74" r="70" fill="#CFE6F5" fill-opacity="0.45" '
                'stroke="#AECFE6" stroke-width="7"/>'
                '<path d="M92 40a52 52 0 0 1 26-14" fill="none" stroke="#FFFFFF" stroke-width="8" '
                'stroke-linecap="round" opacity="0.8"/>')
    if kind == "welding_mask":
        return ('<path d="M86 34h84v58c0 12-19 22-42 22s-42-10-42-22z" fill="#4F5B6B"/>'
                '<rect x="100" y="58" width="56" height="18" rx="4" fill="#2C333D"/>')
    if kind == "top_hat":
        return ('<rect x="98" y="8" width="60" height="44" rx="5" fill="#3A3335"/>'
                '<rect x="80" y="46" width="96" height="11" rx="5" fill="#3A3335"/>'
                '<rect x="98" y="36" width="60" height="11" fill="#E4574C"/>')
    if kind == "detective_hat":
        return ('<ellipse cx="128" cy="48" rx="58" ry="13" fill="#8A7A6B"/>'
                '<path d="M102 46a26 24 0 0 1 52 0z" fill="#8A7A6B"/>'
                '<rect x="101" y="38" width="54" height="9" rx="4" fill="#6B5D50"/>')
    if kind == "wig":
        return ('<g fill="#FFFCF8" stroke="#E4E0F0" stroke-width="4">'
                '<ellipse cx="128" cy="40" rx="48" ry="27"/>'
                '<circle cx="86" cy="64" r="19"/><circle cx="170" cy="64" r="19"/>'
                '<circle cx="82" cy="90" r="16"/><circle cx="174" cy="90" r="16"/></g>')
    if kind == "mask":
        return ('<path d="M94 88h68v20c0 15-15 24-34 24s-34-9-34-24z" fill="#9BD7E8"/>'
                '<path d="M94 96H80M162 96h14" stroke="#9BD7E8" stroke-width="6" stroke-linecap="round"/>')
    return ""


# ------------------------------------------------------------------ uniform
def uniform(kind):
    if kind == "coat":
        return ('<path d="M100 122a54 48 0 0 0-26 42v48h28l10-88zM156 122a54 48 0 0 1 26 42v48h-28'
                'l-10-88z" fill="#FFFFFF" stroke="#E4E0F0" stroke-width="4"/>')
    if kind.startswith("apron"):
        colour = {"apron": "#E4574C", "apron_blue": "#5B7BE8", "apron_brown": "#A8814F",
                  "apron_green": "#4F8A5B"}[kind]
        return (f'<path d="M100 140h56v42a28 28 0 0 1-56 0z" fill="{colour}"/>'
                f'<path d="M112 140v-14h32v14" fill="none" stroke="{colour}" stroke-width="7"/>')
    if kind == "vest":
        return ('<path d="M98 124 88 212h26l8-84zM158 124l10 88h-26l-8-84z" fill="#FFE24A"/>'
                '<path d="M92 172h72" stroke="#FFFFFF" stroke-width="9"/>')
    if kind == "scrubs":
        return ('<path d="M128 116a54 48 0 0 0-54 48v48h108v-48a54 48 0 0 0-54-48z" fill="#6FBFB8"/>'
                '<path d="M110 118 128 142l18-24" fill="none" stroke="#5AA9A2" stroke-width="6"/>')
    if kind == "tie":
        return ('<path d="m128 116-12 12 12 44 12-44z" fill="#E4574C"/>'
                '<path d="m118 114 10 10 10-10" fill="none" stroke="#FFFFFF" stroke-width="6"/>')
    return ""


# -------------------------------------------------------------------- tools
def tool(kind):
    if kind == "stethoscope":
        return ('<path d="M108 118c0 34 18 52 38 52s38-18 38-52" fill="none" stroke="#5A5560" '
                'stroke-width="7"/><circle cx="184" cy="180" r="15" fill="#5A5560"/>'
                '<circle cx="184" cy="180" r="7" fill="#B9C0CC"/>')
    if kind == "clipboard":
        return ('<rect x="176" y="132" width="56" height="72" rx="8" fill="#FFFFFF" '
                'stroke="#C9A87C" stroke-width="6"/><rect x="192" y="124" width="24" height="14" '
                'rx="6" fill="#C9A87C"/><path d="M188 156h32M188 174h22" stroke="#D9D3E6" '
                'stroke-width="6" stroke-linecap="round"/>')
    if kind == "syringe":
        return ('<g transform="rotate(38 204 156)"><rect x="190" y="120" width="26" height="60" '
                'rx="5" fill="#FFFFFF" stroke="#B9C0CC" stroke-width="5"/>'
                '<rect x="196" y="104" width="14" height="18" rx="4" fill="#B9C0CC"/>'
                '<path d="M203 180v22" stroke="#B9C0CC" stroke-width="6" stroke-linecap="round"/></g>')
    if kind == "pill_bottle":
        return ('<rect x="182" y="146" width="48" height="62" rx="8" fill="#FFB6A8"/>'
                '<rect x="186" y="132" width="40" height="18" rx="6" fill="#E4574C"/>'
                '<path d="M206 166v22M195 177h22" stroke="#FFFFFF" stroke-width="7" '
                'stroke-linecap="round"/>')
    if kind == "hose":
        return ('<path d="M196 148c34 0 40 30 14 46" fill="none" stroke="#FFC24A" stroke-width="12" '
                'stroke-linecap="round"/><path d="M204 190h32l-6 20h-26z" fill="#5A5560"/>')
    if kind == "badge":
        return ('<path d="M204 128 236 142v26c0 20-16 30-32 36-16-6-32-16-32-36v-26z" '
                'fill="#FFD86B" stroke="#E8A93C" stroke-width="5"/>'
                '<path d="m204 148 5 11 12 1-9 9 3 12-11-6-11 6 3-12-9-9 12-1z" fill="#FFFFFF"/>')
    if kind == "medkit":
        return ('<rect x="176" y="150" width="66" height="52" rx="8" fill="#FFFFFF" '
                'stroke="#E4574C" stroke-width="6"/><path d="M209 162v28M195 176h28" '
                'stroke="#E4574C" stroke-width="8" stroke-linecap="round"/>')
    if kind == "float":
        return ('<circle cx="204" cy="176" r="34" fill="none" stroke="#FF8FA9" stroke-width="18"/>'
                '<circle cx="204" cy="176" r="34" fill="none" stroke="#FFFFFF" stroke-width="18" '
                'stroke-dasharray="18 18" stroke-dashoffset="9"/>')
    if kind == "book":
        return ('<path d="M170 148c16-10 42-12 62-8v58c-20-4-46-2-62 8z" fill="#5B7BE8"/>'
                '<path d="M170 148v58" stroke="#3F5BC0" stroke-width="5"/>')
    if kind == "flask":
        return ('<path d="M196 128h20v30l24 46a8 8 0 0 1-7 12h-54a8 8 0 0 1-7-12l24-46z" '
                'fill="#CFE6F5" stroke="#8FBBD9" stroke-width="5"/>'
                '<path d="M180 186h56l12 18a8 8 0 0 1-7 12h-66a8 8 0 0 1-7-12z" fill="#6FBFB8"/>')
    if kind == "wrench":
        return ('<g transform="rotate(35 204 164)"><path d="M196 120a20 20 0 1 0 16 30v54a10 10 0 0 0 '
                '20 0v-54a20 20 0 0 0-16-30z" fill="#B9C0CC" stroke="#8E96A6" stroke-width="4"/></g>')
    if kind == "hammer":
        return ('<g transform="rotate(28 204 160)"><rect x="180" y="118" width="52" height="26" rx="6" '
                'fill="#B9C0CC"/><rect x="199" y="140" width="14" height="70" rx="6" fill="#C9A87C"/></g>')
    if kind == "saw":
        return ('<g transform="rotate(-24 202 166)"><path d="M168 148h72v20h-72z" fill="#B9C0CC"/>'
                '<path d="M168 168h72l-6 10h-6l-6-10h-6l-6 10h-6l-6-10h-6l-6 10h-6l-6-10h-6l-6 10h-6z" '
                'fill="#8E96A6"/><rect x="234" y="140" width="16" height="36" rx="8" fill="#C9A87C"/></g>')
    if kind == "bulb":
        return ('<circle cx="204" cy="152" r="28" fill="#FFE24A"/>'
                '<rect x="192" y="178" width="24" height="18" rx="5" fill="#B9C0CC"/>'
                '<path d="M186 128 176 118M222 128l10-10M204 118v-14" stroke="#FFC24A" '
                'stroke-width="6" stroke-linecap="round"/>')
    if kind == "roller":
        return ('<rect x="172" y="128" width="66" height="24" rx="8" fill="#5B7BE8"/>'
                '<path d="M205 152v18h-14v40" fill="none" stroke="#B9C0CC" stroke-width="8" '
                'stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "mop":
        return ('<path d="M204 128v56" stroke="#C9A87C" stroke-width="10" stroke-linecap="round"/>'
                '<path d="M178 184h52l-8 34h-36z" fill="#9BD7E8"/>'
                '<path d="M188 190v26M204 190v26M220 190v26" stroke="#7EC8E3" stroke-width="5"/>')
    if kind == "torch":
        return ('<path d="M176 196 214 150" stroke="#5A5560" stroke-width="12" stroke-linecap="round"/>'
                '<path d="M214 150c14-8 22-2 22-2s-4 14-18 16z" fill="#FFC24A"/>'
                '<circle cx="228" cy="152" r="9" fill="#FFE24A"/>')
    if kind == "palette":
        return ('<ellipse cx="204" cy="168" rx="42" ry="32" fill="#FFFFFF" stroke="#D9D3E6" '
                'stroke-width="6"/><circle cx="222" cy="178" r="9" fill="#FFFCF8" stroke="#D9D3E6" '
                'stroke-width="4"/>'
                '<circle cx="186" cy="156" r="8" fill="#E4574C"/><circle cx="206" cy="150" r="8" '
                'fill="#5B7BE8"/><circle cx="222" cy="160" r="8" fill="#FFD86B"/>'
                '<circle cx="186" cy="180" r="8" fill="#6FBF7F"/>')
    if kind == "guitar":
        return ('<g transform="rotate(28 196 172)"><ellipse cx="196" cy="186" rx="34" ry="40" '
                'fill="#C9A87C"/><circle cx="196" cy="186" r="12" fill="#8A5A2B"/>'
                '<rect x="188" y="106" width="16" height="52" rx="5" fill="#8A5A2B"/></g>')
    if kind == "camera":
        return ('<rect x="166" y="146" width="76" height="52" rx="10" fill="#5A5560"/>'
                '<path d="m190 146 6-12h20l6 12z" fill="#5A5560"/>'
                '<circle cx="204" cy="172" r="18" fill="#CFE6F5" stroke="#3A3335" stroke-width="6"/>')
    if kind == "notepad":
        return ('<rect x="176" y="140" width="56" height="66" rx="7" fill="#FFFFFF" '
                'stroke="#D9D3E6" stroke-width="6"/>'
                '<path d="M188 162h32M188 180h22" stroke="#D9D3E6" stroke-width="6" '
                'stroke-linecap="round"/>'
                '<path d="m236 128-8 26 22-18z" fill="#FFD86B"/>')
    if kind == "laptop":
        return ('<rect x="168" y="140" width="72" height="46" rx="6" fill="#FFFFFF" '
                'stroke="#B9C0CC" stroke-width="6"/><path d="M160 190h88l-6 12h-76z" fill="#B9C0CC"/>'
                '<path d="M182 156h20M182 170h34" stroke="#7EC8E3" stroke-width="5" '
                'stroke-linecap="round"/>')
    if kind == "gavel":
        return ('<g transform="rotate(-32 204 156)"><rect x="176" y="128" width="56" height="30" '
                'rx="8" fill="#C9A87C"/><rect x="197" y="156" width="14" height="56" rx="7" '
                'fill="#A8814F"/></g>')
    if kind == "briefcase":
        return ('<rect x="168" y="152" width="76" height="56" rx="8" fill="#8A5A2B"/>'
                '<path d="M190 152v-12h32v12" fill="none" stroke="#8A5A2B" stroke-width="7"/>'
                '<rect x="168" y="174" width="76" height="10" fill="#6B4520"/>')
    if kind == "tray":
        return ('<ellipse cx="206" cy="146" rx="46" ry="14" fill="#B9C0CC"/>'
                '<rect x="188" y="120" width="16" height="26" rx="5" fill="#FFFFFF" '
                'stroke="#D9D3E6" stroke-width="4"/><circle cx="220" cy="134" r="11" fill="#FF8FA9"/>')
    if kind == "rolling_pin":
        return ('<g transform="rotate(-20 204 168)"><rect x="166" y="152" width="76" height="26" '
                'rx="13" fill="#E8C88A"/><rect x="150" y="160" width="20" height="10" rx="5" '
                'fill="#C9A87C"/><rect x="238" y="160" width="20" height="10" rx="5" fill="#C9A87C"/></g>')
    if kind == "cup":
        return ('<path d="M172 148h58v34a29 29 0 0 1-58 0z" fill="#FFFFFF" stroke="#D9D3E6" '
                'stroke-width="6"/><path d="M230 158h12a15 15 0 0 1 0 30h-12" fill="none" '
                'stroke="#D9D3E6" stroke-width="6"/><rect x="176" y="162" width="50" height="12" '
                'fill="#A8814F"/>')
    if kind == "pitchfork":
        return ('<path d="M204 132v76" stroke="#C9A87C" stroke-width="10" stroke-linecap="round"/>'
                '<path d="M180 132v-26M204 132v-30M228 132v-26" stroke="#B9C0CC" stroke-width="8" '
                'stroke-linecap="round"/><path d="M176 132h56" stroke="#B9C0CC" stroke-width="8"/>')
    if kind == "cleaver":
        return ('<g transform="rotate(24 204 160)"><rect x="172" y="126" width="66" height="44" '
                'rx="5" fill="#B9C0CC"/><rect x="196" y="170" width="16" height="42" rx="7" '
                'fill="#3A3335"/></g>')
    if kind == "box":
        return ('<rect x="170" y="152" width="72" height="56" rx="5" fill="#F0E2CC" '
                'stroke="#C9A87C" stroke-width="5"/><path d="M170 176h72" stroke="#C9A87C" '
                'stroke-width="5"/><rect x="198" y="152" width="16" height="56" fill="#C9A87C" '
                'opacity="0.7"/>')
    if kind == "wheel":
        return ('<circle cx="206" cy="168" r="38" fill="none" stroke="#3A3335" stroke-width="12"/>'
                '<circle cx="206" cy="168" r="10" fill="#3A3335"/>'
                '<path d="M206 158v-20M198 176l-18 14M214 176l18 14" stroke="#3A3335" '
                'stroke-width="8" stroke-linecap="round"/>')
    if kind == "anchor":
        return ('<circle cx="206" cy="130" r="11" fill="none" stroke="#B9C0CC" stroke-width="7"/>'
                '<path d="M206 142v66M182 156h48" stroke="#B9C0CC" stroke-width="8" '
                'stroke-linecap="round"/>'
                '<path d="M172 182c0 18 15 28 34 28s34-10 34-28" fill="none" stroke="#B9C0CC" '
                'stroke-width="8" stroke-linecap="round"/>')
    if kind == "magnifier":
        return ('<circle cx="200" cy="152" r="32" fill="#FFFFFF" fill-opacity="0.6" '
                'stroke="#5A5560" stroke-width="10"/>'
                '<path d="m224 176 24 24" stroke="#5A5560" stroke-width="12" stroke-linecap="round"/>')
    if kind == "pointer":
        return ('<path d="M186 208 232 122" stroke="#C9A87C" stroke-width="9" stroke-linecap="round"/>'
                '<circle cx="234" cy="118" r="9" fill="#E4574C"/>')
    if kind == "wand":
        return ('<g transform="rotate(24 204 162)">'
                '<rect x="196" y="118" width="16" height="88" rx="8" fill="#3A3335"/>'
                '<rect x="196" y="118" width="16" height="22" rx="8" fill="#FFFCF8"/></g>'
                '<path d="M238 108q2 14 16 16-14 2-16 16-2-14-16-16 14-2 16-16z" fill="#FFD86B"/>')
    if kind == "mirror":
        return ('<g transform="rotate(34 204 160)">'
                '<circle cx="204" cy="126" r="17" fill="#CFE6F5" stroke="#B9C0CC" stroke-width="5"/>'
                '<rect x="197" y="140" width="14" height="66" rx="7" fill="#B9C0CC"/></g>')
    if kind == "wings":
        return ('<path d="M164 158h84M170 148l-16 10 16 10M242 148l16 10-16 10" fill="none" '
                'stroke="#FFD86B" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "scalpel":
        return ('<g transform="rotate(38 204 160)"><path d="M198 116h14v44h-14z" fill="#CFE6F5"/>'
                '<rect x="196" y="160" width="18" height="48" rx="6" fill="#B9C0CC"/></g>')
    return ""


# ----------------------------------------------------------------- backdrop
def backdrop(kind):
    """Drawn behind the whole body, so the character stands in front of it."""
    if kind == "shelf":
        spines = []
        for row, y in enumerate((30, 82)):
            for i, c in enumerate(("#E4574C", "#5B7BE8", "#4F8A5B", "#FFD86B",
                                   "#9C8AD1", "#E8912B")):
                x = 40 + i * 30 + (10 if row else 0)
                spines.append(f'<rect x="{x}" y="{y + (6 if i % 2 else 0)}" width="20" '
                              f'height="{40 - (6 if i % 2 else 0)}" rx="3" fill="{c}"/>')
        return ('<rect x="24" y="16" width="208" height="128" rx="8" fill="#A8814F"/>'
                + "".join(spines)
                + '<rect x="24" y="72" width="208" height="10" fill="#8A6A44"/>'
                '<rect x="24" y="128" width="208" height="12" fill="#8A6A44"/>')
    if kind == "board":
        return ('<rect x="24" y="16" width="208" height="124" rx="9" fill="#C9A87C"/>'
                '<rect x="34" y="26" width="188" height="104" rx="5" fill="#3E5B4A"/>'
                '<path d="M48 50h62M48 74h100M48 98h74" stroke="#FFFCF8" stroke-width="7" '
                'stroke-linecap="round" opacity="0.85"/>'
                '<rect x="24" y="140" width="208" height="11" rx="5" fill="#A8814F"/>'
                '<rect x="180" y="142" width="22" height="7" rx="3" fill="#FFFCF8"/>')
    return ""


# ---------------------------------------------------------------- the table
JOBS = {
    # healthcare
    "doctor": ("Doctor", None, "coat", "stethoscope"),
    "nurse": ("Nurse", "nurse_cap", "coat", "clipboard"),
    "surgeon": ("Surgeon", "scrub_cap+mask", "scrubs", "scalpel"),
    "dentist": ("Dentist", "scrub_cap+mask", "coat", "mirror"),
    "vet": ("Vet", None, "coat", "syringe"),
    "pharmacist": ("Pharmacist", None, "coat", "pill_bottle"),
    # emergency and public service
    "firefighter": ("Firefighter", "fire_helmet", "vest", "hose"),
    "police": ("Police officer", "cap", None, "badge"),
    "paramedic": ("Paramedic", "cap_red", "vest", "medkit"),
    "lifeguard": ("Lifeguard", "cap_red", None, "float"),
    # education and science
    "teacher": ("Teacher", None, "tie", "pointer", "board"),
    "professor": ("Professor", "grad_cap", None, "book"),
    "scientist": ("Scientist", None, "coat", "flask"),
    "librarian": ("Librarian", None, None, "book", "shelf"),
    "astronaut": ("Astronaut", "space_helmet", None, "wings"),
    # food
    "chef": ("Chef", "toque", "apron", "cleaver"),
    "baker": ("Baker", "toque", "apron_brown", "rolling_pin"),
    "barista": ("Barista", None, "apron_green", "cup"),
    "waiter": ("Waiter", None, "tie", "tray"),
    "butcher": ("Butcher", None, "apron", "cleaver"),
    "farmer": ("Farmer", "straw_hat", "apron_green", "pitchfork"),
    # trades
    "builder": ("Builder", "hardhat", "vest", "hammer"),
    "carpenter": ("Carpenter", None, "apron_brown", "saw"),
    "plumber": ("Plumber", "cap_blue", "apron_blue", "wrench"),
    "electrician": ("Electrician", "hardhat", "vest", "bulb"),
    "mechanic": ("Mechanic", "cap", "apron_blue", "wrench"),
    "decorator": ("Decorator", "cap", "vest", "roller"),
    "welder": ("Welder", "welding_mask", "vest", "torch"),
    "cleaner": ("Cleaner", None, "apron_blue", "mop"),
    # creative and office
    "artist": ("Artist", "beret", "apron", "palette"),
    "musician": ("Musician", None, None, "guitar"),
    "photographer": ("Photographer", "cap", None, "camera"),
    "writer": ("Writer", None, None, "notepad"),
    "developer": ("Developer", None, None, "laptop"),
    "lawyer": ("Lawyer", None, "tie", "gavel"),
    "judge": ("Judge", "wig", "tie", "gavel"),
    "businessperson": ("Businessperson", None, "tie", "briefcase"),
    "detective": ("Detective", "detective_hat", None, "magnifier"),
    "magician": ("Magician", "top_hat", "tie", "wand"),
    # transport
    "pilot": ("Pilot", "pilot_cap", "tie", "wings"),
    "sailor": ("Sailor", "sailor_cap", None, "anchor"),
    "driver": ("Driver", "cap", None, "wheel"),
    "courier": ("Courier", "cap_green", "vest", "box"),
}
JOB_ORDER = list(JOBS)
JOB_LABELS = {k: v[0] for k, v in JOBS.items()}


def outfit(job):
    """(behind, under-head, over-everything) — a backdrop, the uniform, then hat and tool."""
    row = JOBS[job]
    _, head, body, held = row[:4]
    behind = backdrop(row[4]) if len(row) > 4 else ""
    worn = "".join(hat(h) for h in (head or "").split("+") if h)
    return behind, uniform(body or ""), worn + tool(held or "")
