# Kawaii UI — full system spec

The pack as it stands is a **character set**. To build websites with it, it needs a
second, larger layer: functional UI icons, plus the contract and tooling that let
either layer drop into any project.

```
kawaii-icon-pack
├── ui/          302 functional icons   kawaii, currentColor, 24px grid       ← 251 built
├── characters/  354 animal icons       multicolour, fixed palette, 256px     ← 130 built
├── scenes/       16 empty-state illustrations                                 ← blocked (see Part 6.1)
└── assets/       26 favicons, OG templates, loaders, patterns, ribbons        ← missing
```

**Status (v0.9.0):** 506 icons built. The five bases were redrawn from species
anatomy (ringed tail, cheek pouches, cleft lip, round skull, head tilt) so the
characters read as different animals rather than one face in five palettes. — the whole ★ UI subset plus 12 extras, the
character layer as it stood, sprites, a React wrapper and a searchable preview.
Decisions 2–4 in Part 6 are settled; decision 1 still blocks the scenes.

**The two layers must not share a contract.** UI icons are monochrome and inherit
`currentColor` so a button can recolour them; characters are multicolour and fixed.
Packs that blur this are the ones nobody can theme. Everything below assumes the split.

★ = the v1.0 subset. Ship those first; the rest is long-tail.

---

# Part 1 — UI icons (302)

Line style, 24 × 24 grid, 2px rounded stroke, `stroke="currentColor"`, `fill="none"`.
Solid variants for the ~120 marked ★ (a filled state for active tabs and selected items).

## 1.1 Navigation & layout — 28

★home · ★menu · ★close · ★chevron-up · ★chevron-down · ★chevron-left · ★chevron-right ·
★arrow-up · ★arrow-down · ★arrow-left · ★arrow-right · ★external-link · chevrons-left ·
chevrons-right · ★refresh · expand · minimize · fullscreen · sidebar-left · sidebar-right ·
★grid-view · ★list-view · columns · dashboard · ★more-horizontal · more-vertical ·
drag-handle · anchor

## 1.2 Actions — 38

★search · ★filter · sort-asc · sort-desc · ★plus · minus · ★edit · ★trash · save · ★copy ·
duplicate · paste · ★download · ★upload · ★share · print · undo · redo · sync · ★settings ·
sliders · ★check · ★x · ★send · ★attach · ★link · unlink · pin · archive · restore · ★lock ·
unlock · ★eye · ★eye-off · zoom-in · zoom-out · select-all · scissors

## 1.3 Forms & input — 20

★checkbox-on · ★checkbox-off · checkbox-indeterminate · ★radio-on · ★radio-off ·
★toggle-on · ★toggle-off · ★caret-down · text-cursor · password-dots · asterisk-required ·
★field-valid · ★field-error · dropzone · color-picker · slider-handle · stepper ·
★clear-input · ★calendar-input · clock-input

## 1.4 Status & feedback — 16

★info · ★check-circle · ★alert-triangle · ★x-circle · ★help-circle · ★spinner-ring ·
spinner-dots · spinner-bars · progress-circle · ★bell · bell-off · flag · shield-check ·
shield-alert · badge-verified · badge-new

## 1.5 User & account — 18

★user · ★users · user-add · user-remove · user-check · ★avatar-placeholder · id-card ·
★login · ★logout · key · fingerprint · crown-role · team · building-org · contact-book ·
permissions-shield · profile-edit · switch-account

## 1.6 Commerce — 30

★cart · ★cart-add · cart-remove · bag · basket · ★tag · ★discount-percent · coupon · gift ·
wallet · ★credit-card · banknote · coin · receipt · invoice · ★truck-shipping · ★package ·
delivered · return · store · barcode · qr-code · ★heart-wishlist · compare · ★star-filled ·
★star-half · ★star-empty · secure-payment · subscription · ★checkout

## 1.7 Communication — 22

★mail · mail-open · mail-unread · ★inbox · ★send-message · ★chat · chat-dots · ★comment ·
★reply · forward · ★phone · phone-call · phone-off · ★video · video-off · ★mic · ★mic-off ·
headset · ★at-sign · hashtag · megaphone · thread

## 1.8 Media — 24

★play · ★pause · stop · ★skip-next · ★skip-prev · rewind · fast-forward · ★volume-high ·
volume-low · ★volume-mute · ★image · image-add · gallery · ★camera · film · music-note ·
playlist · live-dot · subtitles · picture-in-picture · shuffle · repeat · record · cast

## 1.9 Files & data — 24

★file · file-add · ★file-text · file-pdf · file-image · file-video · file-zip · file-code ·
★folder · folder-open · folder-add · ★cloud · ★cloud-upload · cloud-download · cloud-off ·
database · server · hard-drive · ★chart-bar · chart-line · chart-pie · ★table · export · import

## 1.10 Text & editor — 18

bold · italic · underline · strikethrough · ★list-bullet · ★list-ordered · quote ·
★code-inline · code-block · heading · align-left · align-center · align-right ·
align-justify · insert-link · insert-image · insert-emoji · insert-table

## 1.11 Time & scheduling — 12

★clock · ★calendar · calendar-add · calendar-check · calendar-x · timer · stopwatch ·
alarm · ★history · hourglass · schedule · recurring

## 1.12 Location & travel — 14

★map-pin · map · compass · ★globe · route · car · plane · train · bike · walk · hotel-bed ·
ticket · luggage · flag-destination

## 1.13 Weather — 12

sun · moon · cloud · cloud-sun · rain · storm · snow · wind · fog · humidity ·
thermometer · sunrise

*Skip this whole group unless you're building weather or travel sites.*

## 1.14 Theme & accessibility — 8

★light-mode · ★dark-mode · contrast · ★language · accessibility · text-size · rtl · cookie

## 1.15 Utility & delight — 18

★heart · ★star · ★bookmark · ★thumbs-up · thumbs-down · fire · ★sparkles · lightbulb ·
rocket · trophy · target · puzzle · wrench · bug · terminal · plug · leaf-eco · ★paw

`paw` is the brand tie-in — the one glyph that links the UI layer to the animals.

## 1.16 Brand marks — 16 (ship separately)

facebook · instagram · x · linkedin · youtube · tiktok · github · discord · whatsapp ·
telegram · pinterest · reddit · twitch · slack · apple · google

**These are trademarks.** They cannot be restyled into your kawaii look, cannot be
relicensed MIT, and each owner's brand guidelines govern their use. Ship them as an
optional `@kawaii-icon-pack/brands` package so your main package's licence stays clean.

---

# Part 2 — Characters (354, of which 130 built)

The animal layer, unchanged from the previous spec. Detail per expression is in
[the expression table](#21-expressions) below.

## 2.1 Expressions — 42 per animal × 5 (14 built, 28 missing)

**Built (14):** happy · neutral · sad · crying · angry · surprised · sleepy · love ·
wink · laughing · cool · confused · shy · sick

**Tier 1 (14):** grin (toothy) · content (calm closed smile) · tear (single) ·
sobbing (waterfall) · rage (red tint + steam) · annoyed (half-lidded) · smug ·
thinking (side-glance + dots) · worried · scared (tiny pupils) · pleading (glossy eyes) ·
bored · tongue-out · joy (laughing-crying)

**Tier 2 (14):** relieved · silly · kiss · starstruck · dizzy (spirals) · nauseous ·
mask · yawning · skeptical · eyeroll · zipped · party · dreaming · bandage

Needs ~20 new primitives first: 7 eye types (half-lidded, side-glance, rolled-up,
tiny-pupil, glossy, star, spiral), 6 mouths (toothy grin, tongue-out, pucker, yawn,
zipper, shouting), 9 overlays (waterfall tears, steam, face tint, thought dots, sigh
puff, mask, party hat, dream cloud, plaster). `mask`, `party`, `bandage` and `dreaming`
sit *on* the face and need per-animal anchors — the owl has a beak where the mask goes.

## 2.2 Status badges — 24 (10 built, 14 missing)

**Built:** online · away · busy · offline · typing · notification · muted · verified ·
locked · star

**Tier 1:** success (green check, distinct from blue verified) · error · warning ·
loading · meeting · call · camera-off (completes the a/v pair with muted) ·
screen-share · live

**Tier 2:** vacation · commuting · lunch · pinned · crown

## 2.3 Composed avatars — 120

Every animal × every badge. Consider pairing each status with a fitting mood
(`away` → sleepy, `vacation` → content) instead of always `happy` — same file count,
far more character.

---

# Part 3 — Scenes / empty states (16)

Full illustrations using the animals. This is what actually makes a pack *feel* like a
design system — every site needs these and nobody has them on hand.

1. `404` — animal with a map, lost
2. `500` — animal with unplugged cable
3. `no-results` — animal with magnifying glass
4. `empty-cart` — animal in an empty basket
5. `empty-inbox` — animal asleep on a mailbox
6. `no-messages` — animal with a paper plane
7. `offline` — animal with a disconnected cloud
8. `success` — animal celebrating with confetti
9. `payment-failed` — animal with a broken card
10. `access-denied` — animal with a padlock
11. `maintenance` — animal with a wrench
12. `coming-soon` — animal with a calendar
13. `welcome` — animal waving (onboarding step 1)
14. `subscribe` — animal with an envelope
15. `cookie-consent` — animal with a cookie
16. `thank-you` — animal with a heart

Each needs a body, not just a face — see the mascot decision in Part 6.

---

# Part 4 — Web assets (26)

| Group | Items |
| --- | --- |
| Favicons (6) | 16, 32, 180 apple-touch, 512 maskable, `.ico`, `site.webmanifest` |
| OG / social (3) | 1200×630 templates: default, article, product |
| Loaders (4) | hamster in a wheel, blinking owl, bouncing panda, plain ring — CSS + Lottie |
| Cursors (2) | default paw, pointer paw |
| Patterns (4) | paws, clouds, confetti, dots — seamless SVG tiles for section backgrounds |
| Dividers (3) | wave, blob, scallop — section separators |
| Ribbons (6) | new, sale, pro, beta, sold-out, free |
| Logo lockups (2) | horizontal, stacked — mark + wordmark |

---

# Part 5 — The contract and the tooling

This is the part that makes a pack *handy*. A 120-icon set with great DX beats an
800-icon set you can't search. None of it exists yet.

## 5.1 Geometric contract (UI layer)

| Rule | Value |
| --- | --- |
| Grid | 24 × 24, 2px safe padding |
| Stroke | 2px, `round` caps and joins, no scaling on resize |
| Colour | `stroke="currentColor"`, never a hardcoded hex |
| Optical sizes | 16 / 20 / 24 / 32 — 16px redrawn at 1.5px stroke, not scaled down |
| Corner radius | 2px minimum, matching the characters' soft feel |
| Variants | line (all 302) + solid (the 120 ★) |

## 5.2 Distribution

1. ★ `@kawaii-icon-pack/react` — one component per icon, tree-shakeable, `size`/`color`/`strokeWidth` props
2. ★ SVG sprite — `<use href="sprite.svg#search">`, one request
3. ★ Raw SVG files + `icons.json` manifest (already the shape we have)
4. `@kawaii-icon-pack/vue`, `@kawaii-icon-pack/svelte` — same generator, different template
5. Web components — framework-free `<kawaii-icon name="search">`
6. PNG exports — 16/24/32/48/64/128/256/512 for non-SVG pipelines
7. Icon font — legacy email and CMS templates
8. Tailwind plugin — `<i class="i-kawaii-search">`
9. Figma library — the designer half of the handoff
10. ★ Docs site — searchable grid, click to copy SVG / JSX / class name

## 5.3 Quality gates (build these once, they pay forever)

- Contact sheet render on every build (we have this — `scripts/contact_sheet.py`)
- Grid-conformance check: every path inside the 24px box, stroke width exactly 2
- No hardcoded colours in the `ui/` layer (a grep test in CI)
- Visual diff between releases so a regenerated icon can't silently change
- Bundle-size budget per icon (< 1 KB)

---

# Part 6 — Decisions

1. **Mascot or emoji?** ✅ **Resolved — bodies are in.** `standing_<animal>` exists with
   species-correct limbs, so Part 3's scenes are unblocked. Remaining poses: sitting,
   waving, sleeping curled, running, peeking, thumbs-up, clapping, heart-hands, facepalm.
2. **Package name.** ✅ Renamed to `kawaii-icon-pack`.
3. **Kawaii treatment for UI icons?** ✅ **Reversed — the UI layer is kawaii too.**
   Faces on 26 object icons, the whole gesture family drawn as paws, 2.2px stroke.
   My earlier "keep it calm" call was wrong for this pack: the motto is kawaii, and a
   neutral UI set made the product feel like two unrelated halves. Cost: faces need
   ~20px, so each faced icon ships a `_plain` twin for 16px chrome.
4. **Brand marks in or out?** ✅ Out. Ship separately if ever (Part 1.16).

---

# Totals and phasing

| Layer | Built | Full |
| --- | --- | --- |
| UI icons (line) | 251 | 302 |
| UI icons (solid variants) | 4 | 120 |
| Brand marks | 0 | 16 |
| Character faces | 95 | 210 |
| Paw gestures | 50 | 50 |
| Compositions | 20 | 20 |
| Accessories & snacks | 30 | 30 |
| Actions (verbs) | 60 | 60 |
| Full bodies | 5 | 50 |
| Status badges | 10 | 24 |
| Composed avatars | 50 | 120 |
| Scenes | 0 | 16 |
| Web assets | 0 | 26 |
| **Total** | **571** | **1049** |

## Phasing

| Phase | Contents | Assets |
| --- | --- | --- |
| **v1.0** | 120 ★ UI icons + the 130 characters we have + 6 scenes (404, 500, no-results, empty-cart, success, welcome) + favicon/OG + React + sprite + docs site | ~265 |
| ✅ **v0.2.0** | 132 UI icons, 130 characters, 2 sprites, React wrapper, searchable preview. Missing from v1.0: the 6 scenes, favicon/OG set, standalone docs site. | 262 |
| **v1.1** | Remaining 182 UI icons, solid variants | +302 |
| **v1.2** | Character tiers 1–2 (28 expressions, 14 badges) | +224 |
| **v1.3** | Remaining scenes, patterns, loaders, Vue/Svelte, Figma | +43 |

**v1.0 is the honest goal.** 120 UI icons cover the overwhelming majority of what a
website actually renders, and paired with the character layer and a docs site it is
already a pack someone would install. The other 570 assets are what you add once real
usage tells you which gaps hurt.
