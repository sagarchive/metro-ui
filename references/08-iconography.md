# 08 - Iconography: glyph system, status glyphs, round-button glyphs, MDL2 codepoints

Measurement and design specification for Windows Phone 8.1 style iconography.
Tags: **(inferred)** = deduced from measurement or the public MDL2 chart; **(unverified)** = not confirmed.
Units: points (pt) on a 360 x 740 pt logical reference screen; reference captures are 1440x2960 px = 4.0 px/pt (px / 4.0 = pt).
Icons themselves are designed per the grammar in `references/icon-design.md`; this document gives the measurements and recipes that grammar builds on. No particular icon set is a deliverable here.

## 1. Glyph style rules

| Rule | Value |
|---|---|
| Colour | White (`#FFFFFF`) on the tile/page; a tile glyph in reference screenshots looks very slightly warm/off-white (inferred); draw pure white |
| App icon authoring format | white on transparent; SVG, or 256 px raster |
| Tile glyph is ONE white shape | A full-colour icon is reduced: single-colour icon = its own shape; plate+picture icon = the picture only (pixel distance from plate colour); otherwise an outline with lighter parts more solid |
| Tile glyph normalised | Cut out and scaled to fill the square so every glyph is the same size regardless of source margin; stored as a 192x192 8-bit alpha mask |
| Line glyph stroke (shell vector icons) | `line_width = max(1.2, s*0.07)`, square caps, mitre joins; icon box `s`, half-extent `u = s/2` |
| Line glyph stroke (status-area / quick-action icons) | `max(1.3, s*0.08..0.09)` (Wi-Fi 0.09, Bluetooth 0.085, torch/brightness 0.08, rotation 0.09) |
| Round-button glyph (primary recipe) | drawn in a ~20-pt box about (0,0); stroke 2 pt, ROUND cap, ROUND join; ring 2.2 pt, diameter 44 |
| Round-button glyph (symbol-font variant) | box `size=18` (s=9), pen 2 pt, ROUND cap/join; ring 2.2 pt |
| Solid vs outline | Glyphs are either 2-pt strokes (add, cancel, back, delete...) or small solid fills (people, keypad dots, "more" dots r=1.6) - never gradients, never shadows |
| Nav bar glyphs | back arrow and search at size 20; keyboard glyph = symbol U+E144 at 24 |
| Pressed state | ring fills with the accent colour; glyph stays white |
| Disabled / unlit | signal bars not reached stay drawn at alpha 0.30; Wi-Fi bands not reached at alpha 0.35 |

## 2. Quick-action glyph proportions (measured)

Quick-action glyphs (airplane, battery, Bluetooth, brightness, camera, do-not-disturb, hotspot, location, rotation lock, search, settings, sharing, VPN, Wi-Fi) share one measured rule (inferred): bold strokes of ~8-12 px on ~70-90 px canvases = ~11-13 % of glyph size; ends are rounded or square-flat (never pointed); no gradients; one tone, with at most one reduced-alpha (~53 %) element, e.g. a partially filled battery cell. Draw them as vectors using the stroke rules in section 1; design each per `references/icon-design.md`.

Specific vector recipes (half-extent `u`, in units of the icon box):

| Glyph | Construction |
|---|---|
| gear | 8 square teeth, outer radius 0.95u, root 0.7u, hole 0.3u, even-odd fill |
| search | lens centre (0.28u, -0.28u) radius 0.52u; handle to (-0.74u, 0.74u) |
| smiley | circle 0.78u, eyes r 0.10u at (+-0.28u, -0.20u), smile arc r 0.48u |
| brightness | centre disc 0.35u + 8 rays spanning 0.52u-0.82u |
| rotation | arc r 0.82u plus padlock |
| other shell glyphs | terminal, folder, globe, chart, pencil, store, back, shift, shift-on, backspace, enter, Wi-Fi, Bluetooth, torch, plug are drawn in the same line grammar (square caps, mitre joins) |

## 3. Segoe MDL2 Assets - codepoints used

Family "Segoe MDL2 Assets". All codepoints below are in the font's private-use area; none are in the base Segoe UI face. The E1xx codes are the legacy Segoe UI Symbol positions (Win8 / WP8) that MDL2 keeps. Meanings are from the public MDL2 chart (inferred).

| U+ | Meaning | Use | Draw size |
|---|---|---|---|
| E13A | phone handset | tile "phone" | box `s*1.1` |
| E125 | people / contacts | tile | s*1.1 |
| E13B | message / chat bubble | tile | s*1.1 |
| E119 | mail / envelope | tile | s*1.1 |
| E142 | music | tile | s*1.1 |
| E114 | camera | tile | s*1.1 |
| E163 | calendar | tile | s*1.1 |
| E14D | store (shopping bag) | tile | s*1.1 |
| E128 | map / pin | tile | s*1.1 |
| E144 | on-screen keyboard (shown in nav bar while keyboard is up) | nav bar | 24 pt |
| E711 | Cancel (X) - browser "stop loading" | browser chrome | 16 pt / 13 pt |
| E72C | Refresh - reload | browser chrome, round button | 16 pt / 18 pt |
| E724 | Send | round button | 18 pt |
| E768 | Play | media round button | 18 pt |
| E769 | Pause | media round button | 18 pt |
| E892 | Previous track | media round button | 18 pt |
| E893 | Next track | media round button | 18 pt |
| E8EE | Repeat (all) | media round button | 18 pt |
| E896 | Download (save offline) | media round button | 18 pt |
| E73E | Check mark (saved) | media round button | 18 pt |
| E81C | History / replay | media round button | 18 pt |
| EC4F | Music note (now playing) | media round button | 18 pt |

Placement: lay out the glyph, take its **ink extents**, and centre the *ink* box on (cx, cy). Never centre by advance width.

Font stacks:
- Symbol stack for buttons: `["Segoe MDL2 Assets", "Segoe UI Symbol", "sans-serif"]`.
- A round button treats its content as a symbol when any character is in U+E000-F8FF or U+2500-2BFF, then sizes it 18 pt in the symbol font; otherwise it shows 16 pt Semibold text.
- Tile stack: `"Segoe UI Symbol, Segoe MDL2 Assets, Noto Sans Symbols, sans-serif"`.

## 4. App-bar / round-button glyphs and how each is drawn

Round button = ring (d=44, 2.2 pt white outline, centred at x; ring top 4 pt below widget top) + glyph + optional 11.5-pt Regular lower-case label 3 pt under the ring. Widget 68 wide x 74 tall (52 if no label). Hit rect: `cx-34, y-4, 68, d+26 (or d+8 without label)`.

Primary glyph list, coordinates in pt from centre, stroke 2 (ring 2.2):

| Name | Construction |
|---|---|
| call | handset: arc r13 centred (0,9) from -0.72pi..-0.28pi, plus two filled 5.5x5 end-pads at (-10.5,-3.6) and (5,-3.6), whole thing rotated -45 deg |
| message | speech-bubble outline: (-9,-7)-(9,-7)-(9,4)-(-2,4)-(-7,9)-(-7,4)-(-9,4) closed |
| add | plus, arms +-8 |
| save | 16x16 square outline, filled 8x5 top tab at (-4,-8), outlined 9x7 label at (-4.5,1) |
| edit | pencil parallelogram (-8,8) (-7,3) (4,-8) (8,-4) (-3,7) closed |
| delete | bin: lid line y=-5 x+-8, handle (-3..3, -8..-5), body trapezoid (-6,-5)-(-5,9)-(5,9)-(6,-5) |
| send | paper-plane: (-9,-8) (9,0) (-9,8) (-6,0) closed |
| cancel | X, arms +-7 |
| back | arrow: shaft (8,0)-(-8,0), head (-2,-6)-(-8,0)-(-2,6) |
| refresh | arc r8 from -0.2pi to 1.35pi, arrowhead (8,-8)-(7,-2.5)-(2,-4.5) |
| people | filled circle r4 at (0,-4.5) + filled upper half-disc r8.5 centred (0,9) |
| keypad | 3x3 grid of filled r1.8 dots, pitch 7 |

Parametric glyph set (box `size`, `s = size/2`): add, save, edit, delete, send, cancel, check, back, refresh, search, call, message, more, share, settings, play, pause. Geometry:

| Name | Construction |
|---|---|
| check | (-s,0) -> (-s/3,0.7s) -> (s,-0.7s) |
| more | three dots r1.6 at x = -0.8s, 0, 0.8s |
| share | 3 nodes r0.25s at (0.7s,-0.7s), (-0.7s,0), (0.7s,0.7s) joined by lines |
| settings | concentric circles r0.4s and 0.85s |
| play | triangle (-0.5s,-0.8s) (0.8s,0) (-0.5s,0.8s) closed |
| pause | two bars 0.4s x 1.6s at x = -0.6s and +0.2s |

## 5. Status-bar glyph rules

- Heights: status bar 28 pt, nav bar 40 pt. Status icons grow in 150 ms, leave in 70 ms.
- All status glyphs share one baseline. Proportions are measured off a Windows Phone 8.1 status bar against the battery cell height `cell`: signal 1.15 high x 1.75 wide, Wi-Fi 1.15 square.
- **Signal**: five bars, pitch `w/4.8`, bar width `0.8*pitch`, heights `h*(0.2+0.2*i)`; lit alpha 1.0, unlit 0.3.
- **Wi-Fi**: quarter-fan anchored bottom-right; 3 bands each 0.115*s wide, outer radii 1.0, 0.756, 0.513 of s, butt caps, plus a dot r0.115s tucked into the corner; unreached bands alpha 0.35. Bands light at about -60 / -72 / -82 dBm (device-specific thresholds).
- **Battery**: line = max(1, round(cell*0.085)), gap = same, body width = round(cell*1.95) (aspect ~1.95), nub w = round(cell*0.16), nub h = round(cell*0.38) (drawn up to 0.56*cell tall), inner fill inset = line+gap; fill white, **red `#E51400` (0.898, 0.078, 0.0) at <= 15 %**. Charging: plug glyph centred with prongs above the top line and cord through the bottom line, gaps cut in the outline (the canonical Windows Phone app-bar plug).
- **Data-network arrow**: square of side s, shaft + head, stroke 0.24*s, butt caps, mitre joins.
- Layout agrees with reference screenshots: signal bars at far left, Wi-Fi fan next, battery + clock right, no carrier text.

## 6. Tile icon sizing

- Symbol-font tile glyph size = `s*1.1` where `s` is the glyph box. Box value per tile size: (unverified) - see the tile geometry document.
- Custom app glyphs: 192x192 8-bit alpha mask, scaled to box `s`.
- App-list row icon square: 45 pt, row pitch 55, left column x=80, first square 17 pt below the status bar; letters are an accent outline with the letter in its lower-left.
- Round buttons on Start / list: diameter 31 pt, search button centre x=51. Edit-mode badge 32 pt.

## 7. Creating a new icon consistently

DO
1. Draw on a 20x20 (round-button) or 24x24 grid centred on the origin; stroke 2 pt (= 10 % of box), ROUND caps/joins for app-bar icons; SQUARE caps / MITRE joins for shell line glyphs (stroke `max(1.2, 0.07*size)`).
2. Pure white only; use alpha 0.3-0.35 for "off/unlit" portions; accent fill only for the pressed ring.
3. Prefer MDL2 codepoints (section 3) when a glyph exists; centre by ink extents; 18 pt inside a 44-pt ring, 1.1x box on a tile.
4. Reduce any imported art to one white silhouette and normalise it to fill the square.
5. Keep geometry rectilinear / angular with few curves (Metro "pictogram" feel); at most 1 solid + 1 outline element.

DON'T
- No gradients, drop shadows, bevels, multi-colour, or rounded-rect plates behind the glyph.
- No hairlines thinner than 1.5 pt at 360-pt scale; no text inside glyphs except letters in app-list squares.
- Do not centre on advance width; do not mix 2-pt round strokes and mitre square-capped strokes in one toolbar.

## 8. Licensing note

| Asset class | Note |
|---|---|
| Segoe MDL2 Assets, Segoe UI | Proprietary Microsoft fonts, licensed for design / development / testing on Microsoft platforms; no redistribution rights. Do not bundle in a kit; reference by family name only |
| Selawik (Segoe UI metric-compatible) | SIL OFL 1.1 (from public knowledge); safe fallback |
| Reference imagery (wallpapers, ripped glyphs, sound kits) | Microsoft / Nokia derived; do not ship |

## Kit-ready constants

```json
{
 "iconography": {
  "glyphColor": "#FFFFFF", "unlitAlpha": {"signal": 0.30, "wifi": 0.35},
  "roundButton": {"ringDiameter": 44, "ringStroke": 2.2, "glyphBox": 20, "glyphStroke": 2, "cap": "round", "join": "round",
                  "symbolGlyphSize": 18, "widget": [68, 74], "widgetNoLabel": [68, 52], "labelPt": 11.5, "labelGap": 3, "pressedFill": "accent"},
  "shellLineGlyph": {"strokeMinPt": 1.2, "strokeFactor": 0.07, "cap": "square", "join": "miter"},
  "tileSymbolFontScale": 1.1, "tileGlyphMaskPx": 192,
  "bars": {"statusH": 28, "navH": 40, "navGlyphPt": 20, "kbdGlyphPt": 24},
  "appList": {"icon": 45, "rowPitch": 55, "left": 80, "top": 17},
  "status": {"signalBars": 5, "signalHeights": [0.2,0.4,0.6,0.8,1.0], "wifiBandOuter": [1.0,0.756,0.513], "wifiBandWidth": 0.115,
             "battery": {"aspect": 1.95, "lineFactor": 0.085, "nubW": 0.16, "nubH": 0.38, "lowRed": "#E51400", "lowAt": 15}},
  "mdl2": {"phone":"E13A","people":"E125","message":"E13B","mail":"E119","music":"E142","camera":"E114","calendar":"E163",
           "store":"E14D","map":"E128","keyboard":"E144","cancel":"E711","refresh":"E72C","send":"E724","play":"E768","pause":"E769",
           "prev":"E892","next":"E893","repeat":"E8EE","download":"E896","check":"E73E","history":"E81C","musicNote":"EC4F"},
  "symbolFontStack": ["Segoe MDL2 Assets","Segoe UI Symbol","sans-serif"]
 }
}
```
