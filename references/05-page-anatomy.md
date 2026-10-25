# 05 - Page anatomy (Windows Phone 8.1 core pages)

Units: points (pt) on a 360 x 740 screen, 4 px per pt. Status bar 28 pt at the top, navigation bar 40 pt at the bottom, so the page-only view is 360 x 664 (origin = top-left of the page area; the 28 pt status bar sits above it in screen coordinates, and the rendered view in the measurement set is 672 pt tall when the status bar is excluded and the nav bar is included below the page). Pixel position = 4 x (x, y + 28) for page coordinates.

**Text metrics.** Text boxes are positioned by their layout top. Text uses the font's NATURAL line height (win ascent 1.079 + descent 0.251 = 1.33 x size). All pitches below that are derived from line heights assume natural line height. Pitches marked "verified" were checked against rendered output and are authoritative. Baseline = top + 1.079 x size (the baseline columns in the recipes below were measured on rendered output and are quoted as measured).

## 1. Header and page skeleton

| Element | Spec |
|---|---|
| Caps line | y = 14, x = 16, Segoe-style Semibold 11.5, UPPERCASE, no tracking, white. Repeated on every page of an app. |
| Title | y = 24, x = 13, Semilight 48, white. Shown exactly as typed (normally lowercase). |
| Fixed header layer | rows 0..104; never scrolls |
| Content start | y = 108 (4 pt below the header layer), left margin 16 |
| Back hit area | (0, 0, 360, 90) |

Caps text and title baselines: caps 25.5, title about 72.5.

## 2. The page contract

A page is drawn at its natural height starting at y = 0; the content height is what it reports.

| Concern | Rule |
|---|---|
| Fixed header | Rows 0..104 are a separate layer on top and never scroll. The caps line (y 14) and the title (y 24, 48 pt) live in it. |
| Content start | 108. Pages that need less subtract: keypad -14, store search -8. |
| Scrolling | `scroll = clamp(0, content_h - view_h)`, where `content_h` includes the 108 header offset and `view_h` = 672 (a page of height <= 672 never scrolls). Items above y = 104 on screen are hard-clipped (no fade, no blur). |
| Hit mapping | `page_y(y) = y < 104 ? y : y + scroll`; header hits (back / pivot) are at y < 90 in screen coordinates so they keep working while scrolled. |
| Drag | After 8 pt of travel the touch is a scroll. Axis decision: < 12 pt travel = undecided; angle > 20 deg from horizontal = list scroll; flat and >= 18 pt = across (pivot swipe, only if the page is a pivot). Non-pivot pages: always list. |
| Overscroll | Content follows the finger at 0.4 x past either end. Pulled past the top, the list starts lower and black shows (title not repeated). |
| Fling | Velocity filter v = 0.4 v_old + 0.6 v_new (pt/ms); finger lifted after > 80 ms at rest gives 0; inside range v *= exp(-dt/350); at an edge v *= exp(-dt/35) and pos += (bound - pos)(1 - exp(-dt/110)); stop when v < 0.02 (in range) or v < 0.05 and distance < 0.5. See the motion document. |
| Fixed pages | Pages marked fixed never scroll or rubber-band. |
| Scrollbar | None. |
| Dialogs | None as such. Context menus (hold on a row) and in-place pickers are the only overlays; text entry uses the on-screen keyboard, which lifts the whole page view above the keyboard. |
| Back | Tap on the title/caps area (0,0,360,90) goes back; hardware/nav Back does the same. Back on a hub page closes the app (rows leave bottom-up). An open picker/menu is closed before navigating. The hub-title hit is registered after the pivot-next hit so the next title wins its own area. |
| Hub memory | Apps remember the last hub tab so Back from a sub page returns to the tab it came from. |

### Caps line text
The caps string is a per-app property stored UPPERCASE ("SETTINGS", "DIAGNOSTICS", ...). White, Semibold 11.5, no tracking.

### Pivot (tabs)
Title white 48 at x = 13; next title #616161 at `13 + W(title) + 16`; a third copy of the title follows so the strip is endless. Touch the next title (hit x from `16 + W + 8` to 360, y 0..90) or swipe flat >= 18 pt to slide; sliding behaviour is in the motion document. During the slide: caps band 0..32 is static; the title strip band 32..104 moves at a different rate (one title width per screen of tab travel); the body 104..H moves a full 360 per tab; the title nearest the middle is white, others #616161 (`alpha = 0.38 + 0.62 * light`, `light = clamp01((180 + 30 - |u - k| * 360) / 60)`).

Examples: settings "system | applications", diagnostics "tests | logs", phone "history | speed dial", store "top | categories | installed", devices "devices | services". Two-tab hubs alternate (A, B, A, ...).

### Vertical rhythm cheat-sheet (top of one item to the top of the next, pt)
| Item | Pitch | Notes |
|---|---|---|
| entry (title + detail) | 59 (verified) | title 25.5 / detail 12 at +31 |
| switch | 66 (verified) | |
| choice | 68 | |
| field (caption + value) | 52 (verified, 1-line value) = 20 + value block + 12; 71-72 with a 2-line value | |
| label + value pair (13 pt caption, 19 pt value) | 56 = 18 + 26 + 12 | natural line heights: caption 18, value 26, gap 12 |
| textbox | 76 (verified) = 22 + 38 + 16 | |
| picker (closed) | 82 (verified) = 24 + 40 + 18 | open adds `(n - 1) * 40 + 8` |
| slider block | 62 (brightness, audio, memory), 58 + text (haptics), 76 (key height) | |
| button | 52 | store button 46 |
| round-button row | 76 (button row 44 + gap); pairs 76 apart in x | |
| call history row | 62 (verified); messages thread 64 (verified); people row 48 (+52 per letter); store package row 76; devices row 54; service group header 36 | |
| paragraph note (14 pt) | natural height of 14 pt x lines + 18..20 | |
| page end padding | usually +20 (sometimes +10 / +24 / +60) | |

Left margin 16 for everything except: Wi-Fi list text at 58, app-list column at 80, speed-dial / keypad tiles at 16 and 0 (full-bleed keypad), pivot title at 13.

## 3. Page recipes (measured pages)

All x are left text origins (glyph ink starts about 0.5-2 pt to the right of x). Colours: W #fff, G #999. Pure-white pages (about, sensors) carry no tint. The cellular page capture is warm-tinted (x(1, 0.91, 0.85)) and its accent renders as (0,73,203) through that tint, i.e. #0050EF.

### 3.1 About (settings, page ABOUT)
Window y 0 = capture row 112. Blocks are label + value pairs at pitch 56 (assumes natural line height): `top_n = 108 + 56 n`; caption top = block top; value top = block top + 18; next block begins 12 pt after the value's 26 pt line.

| Element | Sample text | Font | Size | Col | x | top y |
|---|---|---|---|---|---|---|
| caps | SETTINGS | Semibold | 11.5 | W | 16 | 14 |
| title | about | Semilight | 48 | W | 13 | 24 |
| caption | Phone | Regular | 13 | G | 16 | 108 |
| value | Lumia 930 | Semilight | 19 | W | 16 | 126 |
| caption | Operating System | Regular | 13 | G | 16 | 164 |
| value | Windows Phone 8.1 | Semilight | 19 | W | 16 | 182 |
| caption | Version | Regular | 13 | G | 16 | 220 |
| value | 8.10.14219.341 | Semilight | 19 | W | 16 | 238 |
| caption | Shell | Regular | 13 | G | 16 | 276 |
| value | Start | Semilight | 19 | W | 16 | 294 |
| caption | Uptime | Regular | 13 | G | 16 | 332 |
| value | 0 hours, 25 mins | Semilight | 19 | W | 16 | 350 |

Caps baseline 25.5 (ink 17.0-25.5); title baseline 72.5. Caption/value baselines are top + 1.079 x size (caption +14.0, value +38.5 from block top) (inferred from natural metrics). Earlier measurements of this page used a 53 pt pitch (1.2 x size line height); that figure is superseded by the natural-height value 56.

Status and navigation bars (outside the page): status y 0..28; navigation bar y 700..740 with back arrow, a centred 17 pt Semilight label and a search glyph.

### 3.2 Cellular + SIM (settings)
| Element | Text | Font | Size | Col | x | top y | baseline (pred) | measured |
|---|---|---|---|---|---|---|---|---|
| caps / title | SETTINGS / cellular + SIM | as above | 11.5 / 48 | W | 16 / 13 | 14 / 24 | 25.5 / 72 | 25.5 / ~72.5 |
| switch title | Data connection | Semilight | 21 | W | 16 | 108 | 129 | merged with toggle ink |
| switch state | On | Regular | 13 | G | 16 | 134 | 147.0 | 147.0 |
| toggle | (ON) | - | 54x24, thumb 12x26 | accent | 290 | 112 | y 111..137 | bbox 290-344 x 111-137 (exact) |
| field caption | Mobile data | Regular | 13 | G | 16 | 174 | 187.0 | 187.0 |
| field value | Connected | Regular | 16 | W | 16 | 192 | 208.0 | 208.2 |
| field caption | Network | Regular | 13 | G | 16 | 226 | 239.0 | 239.0 |
| field value | Carrier, 4G | Regular | 16 | W | 16 | 244 | 260 | ink 248-263.8 |
| field caption | Registration | Regular | 13 | G | 16 | 278 | 291 | 291.4 (g descender) |
| field value | Registered, home network | Regular | 16 | W | 16 | 296 | 312 | ink 300-315.8 |
| entry title | access point | Semilight | 25.5 | W | 16 | 330 | 355.5 | 356.1 (p descender) |
| entry detail | internet | Regular | 12 | G | 16 | 361 | 373 | 375.4 incl. g descender |

Field pitch 52 (verified: 208 to 260), switch pitch 66 (verified: 108 to 174), entry at 174 + 52 x 3 = 330. Baseline error across 6 checked baselines <= 0.6 pt. The separator in the network value renders as a bullet in the capture and as ", " in some builds (unverified which is canonical).

### 3.3 Sensors (diagnostics app, page SENSORS)
Caps DIAGNOSTICS, title sensors. 9 fields; tops: 108, 160, 212, 264 (the charger value wraps to 2 lines: block H = 39, so next = 264 + 20 + 39 + 12 = 335), 335, 387, 439, 491, 543.

| Top | Caption | Value (white 16 Regular at top + 18) |
|---|---|---|
| 108 | Battery | 47 %, Discharging |
| 160 | Cell | 3.854 V, -186 mA now, -67 mA average |
| 212 | Battery temperature | 36.8 C |
| 264 | Charger | Charging (Fast), input limit 525 mA, charge / 450 mA (2 lines, measured line pitch 19.2) |
| 335 | Heat: battery | 36.8 C |
| 387 | Processor clocks | little 1499 MHz, big 400 MHz, cores 0-4 |
| 439 | GPU clock | 260 MHz |
| 491 | Light: lux, colour K, red green blue clear | 44 5144 27 51 50 50 |
| 543 | Accelerometer: x y z | 56 -11 -4139 |

Caption: Regular 13 #999, x = 16, baseline top + 13. Verified (measured baseline / predicted): Cell caption 173.0 / 173; title 72.2 / 72; charger line 2 317.2 / 317.2; accelerometer value 577.0 / 577; accelerometer caption 556 + 2.6 descender = 558.6 vs ink 559.0. All errors <= 0.4 pt. The 19.2 wrapped line pitch is the measured value; it does not equal the natural line height of 16 pt text (21.3), so treat multi-line value pitches as (unverified) outside this capture. Content height = 543 + 52 + 10 = 605 (< 672, the page does not scroll). The page refreshes every 1000 ms.

### 3.4 App list (Start-adjacent app list; no header)
Same palette and fonts as the core pages.

| Element | Geometry | Style |
|---|---|---|
| status bar | y -28..0 (list y measured from the status-bar bottom, same as page origin) | |
| search round button | 31 x 31 at left 35.5 (centre x = 51), top 12 | ring 2 pt white, circle radius c - 1.5; magnifier lens r6 at (c + 2, c - 2), handle to (c - 8, c + 8) |
| letter header ("a", "b", "c") | 45 x 45 square at x = 80, 1.5 pt accent outline (rect inset .75, size 43.5); letter lowercase Semilight 27 **accent** at (84, top + 7) | y0 = 17 + 55 i |
| app row | accent-filled 45 x 45 at x = 80; white glyph 25 pt (centred); name Semilight 22 white at x = 80 + 45 + 13 = 138, top = row_top + 7; max width = 360 - 80 - 8 minus tile; ellipsis "..." | row pitch 55 |
| first item top | 17 | rows: header 17, apps 72 / 127 / 182, header 237, app 292, header 347, apps 402 / 457 / 512 / 567 / 622 |
| scroll | time constant 380 ms, resist 0.35, max v 7 pt/ms, edge v 1.4, spring w 0.016/ms | differs from the core page scroll constants |

Verified: tile tops measured 72.0, 127.0, 182.0, 237.0, 292.0, 347.0 (error 0.0), tile x 80.0-125.0 (45 wide), header square same box (outline), search circle top 12.5 (predicted 12). Label x: 552 px = 138 pt.

## 4. Other pages (layouts not checked against captures)
Offsets are relative to the page y after the header (108 unless noted). Line-height-derived pitches here assume natural line height unless stated.

### Settings hub, "system | applications"
12-14 entry rows from y = 108 at pitch 59: theme, display, Wi-Fi, Bluetooth, cellular + SIM, ringtones + sounds, haptics, notifications + actions, battery saver, processor, virtual memory, graphics, date + region, about; end +20. Second tab: keyboard, performance, diagnostics.

Display page: slider (caption "Screen brightness") at 108, +62; switch rows pitch 66; three pickers (82 closed).

Wi-Fi list: two switches (66 each), status 13.5 accent, then per network: glyph 30 at (14, y + 8); SSID Semilight 22 at x = 58, detail Regular 12.5 at (58, y + 29), padlock at (35, y + 30); pitch 60, hit (0, y - 4, 360, 56); "search again" Semilight 19 accent at y + 8; trailing +72.

Bluetooth: Status switch, 14 pt paragraph, devices Semilight 26 + state 14 at y + 34, pitch 70.

Theme page: caption 13.5 at 108; box at 128 (h 42); "Start screen columns" caption at +62; three 36-high buttons, gap 8, label Regular 13 at (+10, +9); background photo entry at +60 below them.

Accents page: 4 swatches across, gap 10, side 74.5, pitch 84.5; selected swatch = 3 pt white inset stroke; each row a turnstile strip.

### Phone
History tab: keypad bar rect (16, 108, 328, 44) #212121, 3 x 3 dots r 1.6 at pitch 6 around (38, 130), label "keypad" Regular 15 at (62, 120); list starts 168; per call 62 (verified): round call button at (38, y + 2) (ring 44), name Semilight 24 at x = 74, "when" Regular 13 #999 right-aligned at (344 - W, y + 6), detail Regular 12.5 at (74, y + 31), missed = accent.

Speed dial: 2-across tiles h 112, gap 8, side 160; "plus" tile #212121 with 32 pt cross (2 pt stroke).

Keypad page: number Light 34 (26 if > 13 digits) at y = header - 14; keys 3 x 4, gap 2, key height 84; bottom outline buttons h 46 at `view_h - 60`.

Call page: name Light 40 (30 if > 12 chars) at y - 6; status Semilight 26 accent; answer/decline h 54.

### Messages
"messaging": header, round "new" button at (38, 108); list from 184, pitch 64 (verified): name Semilight 24, time Regular 12.5 #999 right-aligned at y + 12, last line Regular 13.5 at y + 31. Thread: bubbles; compose = textbox + send round button at x = 322.

### Contacts
"people": round add at 108, list from 184; letter block (+6, 42 square, +52); name rows pitch 48 (Semilight 24 at y + 6). Card: name Light 34 at y - 8; entries; E-mail / Note fields; edit/delete round buttons pitch 76.

### Devices / services
Row: title Semilight 22 white at y, detail Regular 12.5 at y + 28 (grey; amber #F0A30A = missing; red #E51400 = crashed), pitch 54; group header Semibold 13 accent "running (n)" at y + 8, +36.

### Store
Search textbox at header - 8; spotlight tile accent 328 x 150 with caps Semibold 10.5 at (30, y + 14), title Light 30 at y + 66, blurb 13 at y + 112; section heading Semilight 24 (+2) with caption 12 #999 (+22) (+4); package rows pitch 76; category tiles 3 across, gap 10, cell 102.67 square, count 11 top-right, label 13.5 at `y + cell - 44`; detail: tile 96 at (16, y), text column x = 126.

## 5. Page-change anatomy (what the user sees)
Forward (tap a row): rows of the old page leave top-to-bottom, the tapped row last; 120 ms of black; rows of the new page arrive top-to-bottom. Back: both pages bottom-up. Launch: Start gives way, then the app's first page arrives row by row ("entrance"). Close: rows leave bottom-up. A row is the horizontal strip between consecutive tappable tops (full-width targets >= 90% of width, > 8 pt apart); the header strip is row 0. Timings and curves are in the motion document.

## Kit-ready constants
```json
{
 "screen":{"w":360,"h":740,"px_per_pt":4,"status_h":28,"nav_h":40,"page_view_h":664,"app_h":672},
 "page":{"header_h":104,"content_top":108,"margin":16,"overscroll_k":0.4,"page_end_pad":20,"hit_back":[0,0,360,90]},
 "header":{"caps":{"y":14,"x":16,"size":11.5,"weight":"semibold","case":"upper"},"title":{"y":24,"x":13,"size":48,"weight":"semilight","case":"as typed"}},
 "pivot":{"titleX":13,"nextGap":16,"nextColor":"#616161","caps_h":32,"drag_axis":{"undecided_len":12,"flat_deg":20,"across_len":18}},
 "pitch":{"entry":59,"switch":66,"choice":68,"field":"20+H+12","field1Line":52,"labelValuePair":56,"textbox":76,"pickerClosed":82,"button":52,"roundRow":76,"call":62,"thread":64,"people":48,"storeRow":76,"deviceRow":54,"appListRow":55,"note":"pitches assume natural line height (1.33 x size)"},
 "appList":{"left":80,"icon":45,"rowH":55,"top":17,"label":{"x":138,"dy":7,"size":22},"letter":{"size":27,"dx":4,"dy":7,"stroke":1.5},"search":{"d":31,"cx":51,"top":12}},
 "recipes":{
  "about":{"firstTop":108,"pitch":56,"captionH":18,"valueH":26,"gap":12,"valueDy":18,"captionSize":13,"valueSize":19,"valueFont":"semilight"},
  "cellular":{"switchTop":108,"fieldTops":[174,226,278],"entryTop":330},
  "sensors":{"fieldTops":[108,160,212,264,335,387,439,491,543],"wrappedPitch":71}
 },
 "verification":{"about_err_pt":0.2,"networking_err_pt":0.6,"sensors_err_pt":0.4,"appList_err_pt":0.0}
}
```
