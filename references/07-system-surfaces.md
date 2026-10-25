# 07 - Windows Phone 8.1 system surfaces

Measured specification of the shell-drawn system surfaces: status bar, navigation bar, lock screen, Action Center, toast, volume banner, app switcher, launch and close transitions, dialogs, on-screen keyboard and splash.

Conventions:

- Units are points on a **360 x 740 pt reference screen at 4 px/pt** (1440 x 2960 px).
- Text uses natural line height.
- Fonts are the Segoe UI family: Light, Semilight, Regular, Semibold.
- Default accent is cobalt `#0050EF`; every "accent" below follows the user accent.
- Items marked (unverified) or (inferred) were not directly measured.
- Easings named "expo ease-out" are exponential ease-out curves.

## 1. Layer order (bottom to top)

1. Black clear (`#000`)
2. Start tiles, wallpaper, badges, arrow button, app list, search, list menu
3. App switcher (black veil with alpha = switcher progress, plus app cards), or the foreground app / the app swinging out
4. "Loading..." text and dots
5. On-screen keyboard (slides)
6. Status bar (plus charging plug overlay)
7. Peek (held status bar, revealed by a clip)
8. Action Center (black dim over y 28..700, plus panel revealed by a clip, quick tiles as separate quads)
9. Boot splash (boot only)
10. Navigation bar (always above the Action Center, which stops at `H - 40`)
11. Key pop-up (enlarged pressed key)
12. Lock screen (plus plug); above navigation bar and status bar
13. Volume banner
14. Toast (swivel)
15. Modal dialog (black veil alpha 0.627 plus sheet)

## 2. Status bar

- Height **28 pt**, opaque black, always visible on Start and in apps. App area starts at y = 28, so apps are `740 - 28 - 40` = 672 pt tall. No auto-hide.
- Redrawn on the minute tick, power-state changes, network/Bluetooth changes and icon animation.

### 2.1 Derived metrics (W = 360)

| Metric | Formula | Value |
|---|---|---|
| `cell` (battery cell height; clock digits are as tall as the battery) | `round(W*0.032*2)/2` | 11.5 |
| `base` (shared baseline, all glyphs sit on it) | `(28 + cell)/2` | 19.75 |
| Left margin | - | 14 |
| Right edge | `W - 14` | 346 |

### 2.2 Left cluster (x starts at 14)

| # | Element | Geometry |
|---|---|---|
| 1 | Airplane mode | Vector airplane in a box `1.5*cell`, centre `(x + 0.8cell, base - 0.55cell)`; then x += `1.75cell + 8`. When shown, items 2-5 are absent. |
| 2 | Signal bars | 5 bars, total width `1.75*cell` (20.1), max height `1.15*cell` (13.2), `pitch = w/4.8`, `bar = 0.8*pitch`, bar i height `h*(0.2 + 0.2*i)`, bottoms on the baseline. Lit bars white, unlit white alpha 0.3. Lit count 0..5; not registered = 0 lit. Then x += `1.75cell + 5`. |
| 3 | Technology text (`4G`, `H+`, `3G`, `E`...) | Only when on mobile data and no Wi-Fi. Semibold, size `cell` (11.5), top y = `base - 1.12*size`. Pops in with the icon animation (2.5). After it, x += `3 + (textW + 3)*presence`. |
| 4 | Wi-Fi fan | Size `s = 1.15*cell` (13.2) when a link exists. Quarter fan whose corner is the bottom-right: 3 bands, each `0.115*s` thick, outer radii `1.0, 0.756, 0.513` of `s` (butt caps, arc from -180 to -90 deg about `(x + s, base)`), plus a dot of radius `0.115s` at `(cx - 0.115s, cy - 0.115s)`. Bands not reached by the signal are alpha 0.35. Then x += `s + 8`. |
| 5 | Data-activity arrow | Small up-left arrow in a box. On the bars' top-left (size `0.4*cell`) or on the Wi-Fi fan's top-left (`0.3*s`, offset `0.1*s` outward). Shown while the interface moved more than 300 bytes in the last 3 s. Shaft stroke `0.24*size`. |
| 6 | Bluetooth (when on) | Glyph box `1.25*cell`, centre `(x + 0.35s, base - s/2)`. White if a device is connected, otherwise grey 0.6. Blinks 1 s on / 1 s off while streaming. |

### 2.3 Right cluster

- Clock `HH:MM`, 24-hour. Regular, size `1.3*cell` = **14.95**, right-aligned at x = 346, baseline on `base`.
- Battery sits to the left of the clock:

| Part | Value |
|---|---|
| Body width `bw` | `round(1.95*cell)` = 22 |
| Outline `line` | `max(1, round(0.085*cell))` = 1 |
| `gap` | 1 |
| Nub width | `round(0.16cell)` = 2 |
| Nub height | `0.56cell`, rect at `y = base - 0.78cell`, `x = bx + bw + gap` |
| `bx` | `right - clockW - 0.9*cell - (bw + gap + nubW)` (clock-to-battery gap `0.9cell` = 10.35) |
| Outline | Stroked rect `bx..bx+bw`, height `cell`, top `base - cell`, white, square caps |
| Fill | Inset `line + gap`; width `(bw - 2*inset)*pct/100`; **white**, **red `rgb(.898, .078, 0)` = #E51400 at 15% or below** |

- Charging indicator: white boxy plug glyph (prongs `0.13cell` wide, `0.18cell` apart, `0.32cell` tall; body `0.58cell` square; cord `0.18cell` wide, `0.32cell` tall) with a 1.4 pt black halo, centred on the battery. It **blinks**: hard visible/invisible toggle every 1000 ms; solid when full.

### 2.4 Icon animation

- Glyphs that are absent take no space. Icons **grow from their centre** (scale `0.25 + 0.75*t` plus alpha `t`) in **150 ms** and leave in **70 ms**; neighbours slide to close or open the gap.
- The technology text waits 70 ms for the Wi-Fi fan to leave; the activity arrow waits 70 ms.

### 2.5 Measurement cross-check

Measured on a 4 px/pt capture: signal glyph left edge at 14 pt; clock right edge at about 344.7 pt (formula 346); battery with plug at 276..298.6 pt. All consistent with the formulas above.

### 2.6 Peek (status bar held)

- Finger rests on y <= 40 for **320 ms** (fires at >= 290 ms) without moving. A taller row (**peek height = 28 + 22 = 50 pt**) is revealed by a clip; `peek` goes 0 to 1 in **180 ms**.
- Second line at `y = base + 5`, size `1.05*cell`:
  - at x = 14: operator name, or "No SIM", "No service", "Searching...", "airplane mode";
  - battery `NN%` under the battery at `bx`;
  - date `d/m` under the clock.
- Stays **3000 ms** after lift, then `peek` goes to 0 in **220 ms**. Light haptic tick on activation.

## 3. Navigation bar

- Height **40 pt**, black, always visible. It sits above everything except lock screen, toast, volume banner, dialog and key pop-up.
- Three equal cells of `W/3 = 120 pt`; icon centres at `cx = 60, 180, 300`, `cy = 20`.

| Cell | Button | Drawing |
|---|---|---|
| Left | **Back** | Left arrow vector in a 20 pt box. Shaft from `+0.8u` to `-0.75u` (u = 10), arrow head at the left end, stroke `max(1.2, 20*0.07)` = 1.4, square caps. |
| Centre | **Start** | The Windows logo glyph, centred in an 80 x 40 box. (The reference capture used a text label in this slot; the real device draws the Windows logo. Logo drawing size is (unverified); text-slot size was Semilight 17 pt.) |
| Right | **Search** | Magnifier (lens plus handle) vector in a 20 pt box. While the keyboard is up it becomes the keyboard glyph U+E144 (Segoe UI Symbol, 24 pt). |

- Colour: white. **While pressed the icon turns accent**; there is no background plate. Light tap haptic on touch down, no sound.

### 3.1 Behaviour

| Input | Result |
|---|---|
| Tap Start | Return to Start. On Start itself: close menu, then end edit mode, then return the list page to Start, then scroll to top. |
| Tap Back | Back to the app. On Start: closes menu / search / edit mode / list page. Closes the Action Center first if open. |
| Tap Search | Opens search (toggle). If the keyboard is up, hides the keyboard. |
| Long press (**450 ms**) Back | Switch to the next app (strong haptic). |
| Long press Start | Open the app switcher. |
| Long press Search | Toggle the keyboard. |

### 3.2 Boot reveal

Icons start `NAV_H + 20 = 60 pt` below their rest position and rise to 0, clipped to their cell. Delays 700 / 1050 / 1400 ms for Back / Start / Search, duration **480 ms** each, expo ease-out.

## 4. Lock screen

- Full-screen layer, 360 x 740.
- **Background**: with no photo, a vertical gradient from black (0-25%) to `accent*0.5` (100%). With a photo (cover-cropped), a black gradient overlay: alpha 0.25 at 0%, 0 at 15% and 55%, **0.5 at 100%**.
- Status row at the top (same as status bar, without the peek details).

| Element | Font | Position |
|---|---|---|
| Clock `HH:MM` | Segoe UI **Light 92 pt**, white | x = 16, top y = `H - 268` = 472 |
| Day (`%A`, full weekday) | Semilight **30** | x = 20, y = `H - 156` = 584 |
| Date (month name and day, e.g. "March 5") | Semilight 30 | x = 20, y = `H - 120` = 620 |

- No notification rows and no PIN keypad on the lock screen itself; the screen is swipe-to-unlock. The charging plug blinks over it.

### 4.1 Unlock gesture

- Finger drags the lock layer up, following 1:1 (`lock_y = min(0, y - y0)`, never below rest).
- On release, if travel > `H/5` = **148 pt** and the gesture was not cancelled: unlocked. `lock_y` goes to `-H` over **200 ms** ease-out, light tap haptic, unlock sound.
- Tap without moving: bounce. `lock_y = -26`, then back to 0 over **320 ms** (hints the gesture).
- Short drag: returns to 0 in **220 ms**.

### 4.2 Locking

- Screen off locks the device; when the screen turns on the lock layer is at rest. A lock sound plays when the screen goes dark.
- Default idle sleep **60 s** (inferred as a default; the phone's setting is user adjustable).
- The power key only toggles the screen.
- Touches on the lock layer are swallowed; nothing underneath responds.

## 5. Action Center

### 5.1 Opening and closing

- Open by pulling down from the status bar: touch down with `y <= 28 + 12 = 40`.
- While the finger moves: `shade_h = clamp(h0 + (y - y0), 0, 700)`; maximum height `H - NAV_H` = **700**.
- Release rule: if it was mostly closed, it opens when drag dy > 40; if it was open, it stays open when dy > -40 (closing needs an upward drag of more than 40 pt).
- Settle: **260 ms** expo ease-out.
- Also closes by tapping the bottom bar (y >= 700 - 16 - 14 = 670), Back, ALL SETTINGS, or Search.

### 5.2 Rendering

- The panel does **not translate**. Contents stay fixed at the top while a clip of height `shade_h - 16` reveals them, with the 16 pt accent bar riding the bottom edge.
- A black veil over y 28..700 with alpha `0.6 * shade_h/700`. Panel background is opaque black.

### 5.3 Layout, top to bottom

| Region | Geometry |
|---|---|
| Status row with details line | y 0..50 (same as peek) |
| Quick actions | **4 columns x 2 rows**; side margin 4; gap 3; tile `w = (W - 8 - 9)/4` = 85.75; `h = round(0.66*w)` = 57; `x = 4 + col*(w + 3)`; `y = 50 + row*(h + 3)` |
| Links row | `y = row2.y + h + 12` = 179. "CLEAR ALL" left: close-x icon 10 pt at x = 19, text Semibold 10 at x = 32. "ALL SETTINGS" right: Semibold 10 right-aligned to `W - 14`, gear icon 12 pt placed 12 pt left of the text. Hit area y in [links - 8, links + 26]; left half = clear, right half = settings. |
| Notification list | Starts at `links + 46`. Empty state: "No notifications", Light 21, at (14, links + 44). |
| Bottom handle | Accent bar 16 pt tall, full width, at `y = 684`; white pill 28 x 3 centred. |

### 5.4 Quick-action tile

- Flat rectangle, no corner radius.
- **On = accent fill; off = `#1F1F1F` (0.122 grey)**; empty slot `#121212` (0.07 grey).
- Glyph in the top-left, 18 pt box centred at (17, 17) (8 pt inset). Label Semibold **7.6 pt**, UPPERCASE, at x = 7, top y = `h - 15`, width `w - 10`.
- Unavailable hardware: whole tile at white alpha 0.3.
- Default order (row-major): WI-FI, MOBILE DATA, BLUETOOTH, AIRPLANE MODE, ROTATION LOCK, FLASHLIGHT, BRIGHTNESS NN%, ALL SETTINGS.
- Available actions: Wi-Fi, mobile data, Bluetooth, airplane, rotation, flashlight, location, brightness, settings, vibrate, none.
- Brightness is always drawn "on" and cycles 25 -> 50 -> 75 -> 100 -> 25 per tap; label e.g. "BRIGHTNESS 50%".
- Press feedback: same tilt as Start tiles but **scale 0.97**, tilt 14 deg, in **70 ms** / out **160 ms**; tilt sign negated relative to Start tiles.
- Haptics: clear and settings = tick; toggles = tap/click (airplane and vibrate use click).

### 5.5 Notifications

- Maximum 12, newest first, **grouped by app**.
- Group header: accent square 28 x 28 at (14, y) with the app initial in Semibold 17 white; app name Semilight **22** at x = 52; then advance 40.
- Per item:
  - title Semibold **14.5** at x = 14, width `W - 28 - whenW - 12`;
  - time right-aligned, Regular 13.5 (`HH:MM` if today, otherwise short weekday); advance 21;
  - body Regular 13.5, grey 0.62, single line (advance 19) or, when **tapped**, expanded to all wrapped lines (width `W - 28`);
  - item gap +12; group gap +10.
- Tap toggles expand/collapse. CLEAR ALL empties the list with no animation. Swipe-to-dismiss was not observed (unverified for the real device).
- List is clipped between `links + 30` and `700 - 16 - 4`.

## 6. Toast (notification banner)

- Full width x **58 pt** at y = 0 (covers the status bar), **accent colour**, white text.
  - Title Semibold **15** at (16, 9).
  - Text Regular **13** at (16, 31), width `W - 32`, ellipsised.
- Animation is the Windows Phone "message toast show" swivel: rotation about the **top edge (X axis)** from **-45 deg to 0** while alpha goes 0 to 1 (`angle = -45*(1 - t)`, `alpha = t`).
  - In: **300 ms** expo ease-out.
  - Hold: **4500 ms**.
  - Out: **199 ms**, reverse swivel.
- Tapping it (y < 58 while visible) dismisses at once.
- On entry: notification sound and strong haptic. The notification stays listed in the Action Center.

## 7. Volume banner

- Hardware volume keys are handled by the shell. The banner drops from the top: `volume_y` from `-banner_h` to 0 in **140 ms** ease-out; it hides after **2000 ms** (**4000 ms** with media) by moving up in **180 ms**.
- Height `banner_h = 58 + (media ? 74 : 0) + 44`. Background `#1F1F1F` (0.12 grey).

| Element | Spec |
|---|---|
| Level text `NN/30` | Semilight 26, white, at (16, 8) |
| Caption | Regular 12, grey 0.6, at (108, 20): "ringer + notifications", "vibrate" (level 0), or "media + apps" |
| Level bar | y = `58 - 9` = 49, x 16..W-16, 3 pt tall; track `#404040`; fill accent at `level/30` |
| Media row (74 pt, when media plays) | Title Semibold 14.5 (y + 10); artist Regular 12.5 grey 0.62 (y + 31); three 46 pt buttons right-aligned (previous / play-pause / next; white glyphs: triangles plus bar; pause = two 5 x 18 bars) |
| Output row (44 pt) | 1 pt `#333` divider; music icon 16 at x = 25; device name Regular 13.5 at x = 40; "change >" in accent Semibold 13.5, right-aligned, when more than one output exists; tap selects the next output |

- Keys control media volume while audio plays, otherwise ringer volume. Reaching zero on the ringer gives a tap haptic; each ringer step plays a short "pip" sound.

## 8. App switcher

- Open: long press (**450 ms**) on the Start button. Closes by tapping outside the cards, any navigation button, or picking a card.
- `switch_t` goes 0 to 1 over **260 ms** expo ease-out. Black veil with alpha `t` over the whole screen. Apps become **cards**: newest at centre, older to the **left** (card 0 = newest; x offset `(switch_x - i)*pitch`).

### 8.1 Card geometry

| Parameter | Value |
|---|---|
| Scale | `sc = 1 + (0.6 - 1)*t`; at rest **0.6** |
| Card size | 216 x 403.2 pt |
| Card gap | 18 |
| Pitch | `W*sc + 18` = 234 |
| x | `W/2 + (switch_x - i)*pitch - sc*W/2` |
| y | `28 + (672 - sc*672)/2 - 10*t` (= 152.4 at t = 1) |
| Max cards | 8 |
| Projection | Flat 2D scaling; no 3D tilt or perspective (angle 0) |
| Opacity | Cards fade in from Start (alpha = t); fully opaque when the switcher opens over an app |

- Card title: app name, Semilight 15 white, at card `x`, `y = card bottom + 8`, width 216, alpha `t`.

### 8.2 Gestures

- **Horizontal drag** moves along the row; past either end it rubber-bands at 0.35x. On release it lands on `round(switch_x + v*170)` clamped, using a critically damped spring `k = 0.014/ms` seeded by finger speed (`v = vx/pitch`).
- **Vertical drag** (decided at the first move when mostly vertical and started on a card): the card follows the finger up 1:1 and down at 0.15x.
  - **Close** if `drop < -90 pt` or on a fling (`vy < -0.7 pt/ms` and lift within 90 ms). The card flies off at `max(-vy, 2.2) pt/ms` over `clamp((H + drop)/speed, 90..240)` ms, linear, with alpha `1 + drop/300`. Click haptic on close.
  - Otherwise the card returns in **260 ms**.
- **Pick**: the tapped card grows back to full size (`switch_t` to 0, `switch_x` to `i`, **260 ms**) with no turnstile. Tap haptic.

## 9. App launch and close transitions

| Event | Visual |
|---|---|
| Tap tile / row | Start's tiles turnstile out (bottom rows first, tapped tile last); about 110 ms of black; the app swings in from behind around its left edge (80 deg to 0, **350 ms**). For first-party apps that animate their own content, the app is uncovered at the end of the turnstile and animates its own rows. |
| "Loading..." (slow apps, up to 4 s) | After Start has left: "Loading..." Semilight 20 white at x = 20, y = `28 + (740 - 68)/2` = 364. Five accent 3 x 3 pt dots cross the screen at y = `364 - 12`, each delayed **160 ms**, period **2600 ms**, travel 1700 ms. |
| App closes / Start tapped | App swings away (rotate about the left edge, Y axis, 0 to 80 deg, alpha to 0, **250 ms**), 150 ms black, then tiles turnstile back in. |
| Switcher pick | Card scales to full size (section 8). |
| Left-edge swipe | Touch down at `x <= 18`, travel > 56 pt to the right: the app is closed (no drag-following animation). |

## 10. Dialog sheet (modal)

- Slides down from the top: `dialog_y` from `-h` to 0 in **260 ms** ease-out; closes upward in **170 ms**.
- Black veil alpha **0.627** over everything. Panel `#1F1F1F`, full width. Margins `pad = 24`.

| Element | Spec |
|---|---|
| Title | Semibold 20, at y = 40 |
| Body | Regular 15, wrapped at `W - 48`, at `y = 40 + 28 + 12` = 80 |
| Buttons | 40 pt tall, **2 pt white outline, transparent fill**, Regular 15 label centred; two buttons side by side with a 12 pt gap (stacked if a label does not fit) |
| Height | `btn_y + 40 + 20` |
| Dismiss | Tapping the veil below the sheet |

## 11. Boot splash

- Black screen with a centred mark, centred horizontally and vertically on 360 x 740 pt. Mark size and artwork for the real device are (unverified); the reference capture used a 56 pt Light wordmark in white.
- Sequence: once the system is ready, navigation icons rise (section 3.2); at **+2200 ms** the **lock screen drops from the top** (`lock_y` from `-H` to 0, **750 ms** ease-out), covering the splash. The splash is removed when that animation ends and the notification chime plays.

## 12. On-screen keyboard

### 12.1 Geometry (W = 360, key height K = 56 default; adjustable range 42..72)

- `KEY_GAP = 3` ("the gap is the border"). Keyboard height `3 + 4*K` = **227 pt**.
- Positioned at `y = H - 40 - kb_h*slide`; `slide` goes 0 to 1 in **200 ms** expo ease-out. It overlays the app (the app is lifted as needed).
- Key rect: `y = 3 + row*K`, `h = K - 3` = 53.

**Letters layout**

- Row 1 `qwertyuiop`: available width `W - 11*3` = 327, each key **32.7**, `x = 3 + i*35.7`.
- Rows 2-4 use a centred grid: base cell `unit = (W - 33)/10` = 32.7; row start `x0 = 3 + (10 - cols)*(unit + 3)/2`.

| Row | Content | Notes |
|---|---|---|
| 2 | `asdfghjkl` (9 cells) | x0 = 20.85, each 32.7 |
| 3 | shift, `zxcvbnm`, backspace (9 cells) | Shift and backspace **absorb the side margins**: shift x = 3, w = `32.7 + (x0 - 3)` = 50.55; backspace right edge at `W - 3` |
| 4 | `&123` (1), smiley (1), `,` (1), space (4 = 139.8), `.` (1), enter (1) (9 cells) | `&123` and enter absorb the margins; smiley, comma and period align under Z, X, M |

**Symbols page (`&123`)**

- Row 1: `1234567890`.
- Row 2: `@ # $ % & * - + ( )`.
- Row 3: `! " ' : ; / ? _ =` plus backspace (weight 1.5); key width = 327/10.5 = 31.14, backspace 46.7.
- Bottom row: same as letters, with `abc` in place of `&123`.

**Emoji page**

- 3 rows x 8 emoji (24 total), key width `(360 - 27)/8` = 41.6, glyph 24 pt.
- Bottom row: `abc` (1.5), space (4), backspace (1.5), enter (1.5).
- Emoji set: 😀😂😍😊😭😎🤔😅👍👎🙏👏❤🔥🎉✨😡😢😴😘😁💯✅👋 (set is a sample; the real device's set is (unverified)).

**Cursor dot**

- Dot at `x = 1.5*pitch + 1.5` where `pitch = (W - 3)/10`, giving **55.05**, `y = kb_h - K - 1.5`: black disc radius 10 with an accent dot of radius **3.5**. Touch target radius 14 (28 pt diameter).
- Hold **450 ms** (or drag off it) to enter cursor-move mode: keys hidden, panel `#141414` with "move cursor" in Regular 16, grey 0.55, centred. Every 10 pt of horizontal travel = one Left/Right step; every 18 pt vertical = one Up/Down step; clamp +/-32 horizontal and +/-16 vertical steps per event; silent. Lifting restores the keys.

### 12.2 Colours and type

- Background black.
- **Letter keys (single-character labels including digits and symbols): `#333333` (0.2 grey).**
- **Function keys (shift, `&123`, space, enter, backspace, smiley, word labels): `#1F1F1F` (0.12 grey).**
- Latched shift = accent. **Pressed key = accent fill** with white label.
- Labels white, Regular **20 pt** for single letters (uppercase when shift is active), **13 pt** for word keys (`&123`, space...), 24 pt for emoji. Icons in an 18 pt box (shift, shift-on filled, backspace, enter, smiley). Corner radius 0.

### 12.3 Key pop-up and hit testing

- Key pop-up appears only for single-character, non-space keys: accent rectangle `(key.w + 16) x (K + 10)`, white Regular **34** letter centred, placed centred above the key with its bottom edge at the key's top (`y = kbTop + key.y - h`), clamped to the screen. No pop-up for function keys.
- Touch targets cover the gaps: a touch within `|dx|, |dy| < 0.6` of a key (normalised by half size plus gap/2) selects it; otherwise the nearest key by distance with a **next-letter prefix bias** (`score -= 0.5 * P(next letter | typed prefix)`, from a word list of about 100 words; letters page only) (inferred; the real prediction model is (unverified)).
- Sliding to another key before lifting selects that key. A key fires on **lift**; the pressed state shows on touch down.
- Backspace repeat: after **450 ms**, then every **60 ms**.
- Shift applies to one key then releases (no caps lock observed).

### 12.4 Sound and haptics

- Key sounds in three classes: letters, space, function (shift / backspace / enter / page / emoji). Played on **touch down** (and on sliding to a new key) at ring volume.
- Haptic: 7 ms pulse at level 0.28.

## 13. Gesture summary

| Gesture | Where | Result |
|---|---|---|
| Tap tile / row | Start / list | Launch |
| Long press (450 ms) tile | Start | Edit mode |
| Long press row | List | Context menu |
| Vertical drag | Start / list | Scroll (fling) |
| Horizontal drag (< 20 deg, >= 18 pt) | Start / list | Page between Start and list |
| Drag down from status bar (touch y <= 40) | Anywhere unlocked | Action Center |
| Hold status bar 320 ms | Anywhere | Peek |
| Swipe up | Lock screen | Unlock if > 148 pt |
| Swipe right from left edge (x <= 18, > 56 pt) | In app | Close app |
| Back / Start / Search tap | Navigation bar | Section 3.1 |
| Back / Start / Search long press 450 ms | Navigation bar | Next app / switcher / keyboard |
| Hold cursor dot 450 ms | Keyboard | Cursor-move mode |
| Swipe up on card (> 90 pt or fling) | Switcher | Close app |
| Tap toast | Banner | Dismiss |
| Power key | Hardware | Screen on/off |
| Volume keys | Hardware | Volume banner |

Touch priority, highest first: dialog, volume banner, toast, lock screen, switcher, Action Center, status-bar pull, navigation bar, keyboard, search, Start, edge-close, app.

## Kit-ready constants

```json
{
  "screen": {"w": 360, "h": 740, "pxPerPt": 4},
  "statusBar": {"h": 28, "cellFormula": "round(W*0.032*2)/2", "cell@360": 11.5, "baseline": 19.75,
    "marginX": 14, "clockPt": 14.95, "clockFont": "Regular", "clockFmt": "HH:mm", "signalW": "1.75*cell",
    "signalH": "1.15*cell", "bars": 5, "barH": "0.2+0.2*i", "unlitAlpha": 0.3, "wifiS": "1.15*cell",
    "wifiBands": [1.0, 0.756, 0.513], "wifiBandW": 0.115, "battery": {"w": "round(1.95*cell)", "lowPct": 15, "lowColor": "#E51400"},
    "iconInMs": 150, "iconOutMs": 70, "peekH": 50, "peekHoldMs": 320, "peekStayMs": 3000},
  "navBar": {"h": 40, "iconBox": 20, "startGlyph": "windows-logo", "pressedColor": "accent",
    "longPressMs": 450, "bootRiseMs": 480, "bootDelaysMs": [700, 1050, 1400]},
  "lock": {"clockPt": 92, "clockFont": "Light", "clockXY": [16, "H-268"], "dayPt": 30, "dayY": "H-156", "dateY": "H-120",
    "unlockDistFrac": 0.2, "unlockMs": 200, "tapBounce": -26, "tapBounceMs": 320, "cancelMs": 220,
    "shadeStops": [[0, 0.25], [0.15, 0], [0.55, 0], [1, 0.5]], "idleSleepS": 60},
  "shade": {"openFromY": 40, "maxH": 700, "settleMs": 260, "dimAlpha": 0.6, "side": 4, "gap": 3, "top": 50,
    "tileW": "(W-17)/4", "tileH": "round(0.66*w)", "onColor": "accent", "offColor": "#1F1F1F", "emptyColor": "#121212",
    "labelPt": 7.6, "labelFont": "Semibold", "handleH": 16, "linksY": "top+2*tileH+3+12", "openThresholdPt": 40,
    "maxNotes": 12, "noteTitlePt": 14.5, "noteBodyPt": 13.5, "appHeaderPt": 22, "press": {"tilt": 14, "scale": 0.97}},
  "toast": {"h": 58, "swivelDeg": -45, "inMs": 300, "holdMs": 4500, "outMs": 199, "titlePt": 15, "textPt": 13, "bg": "accent"},
  "volume": {"h": 58, "mediaH": 74, "outputH": 44, "inMs": 140, "outMs": 180, "holdMs": 2000, "holdMediaMs": 4000,
    "max": 30, "bg": "#1F1F1F", "barY": 49, "barH": 3},
  "switcher": {"cardScale": 0.6, "gap": 18, "openMs": 260, "dropClosePt": -90, "flingV": -0.7, "springK": 0.014,
    "maxCards": 8, "yShift": -10, "titlePt": 15},
  "dialog": {"bg": "#1F1F1F", "veilAlpha": 0.627, "pad": 24, "titlePt": 20, "bodyPt": 15, "btnH": 40, "btnGap": 12,
    "btnStroke": 2, "inMs": 260, "outMs": 170},
  "keyboard": {"keyH": 56, "gap": 3, "h": "3+4*keyH", "slideMs": 200, "letterColor": "#333333", "funcColor": "#1F1F1F",
    "pressedColor": "accent", "letterPt": 20, "wordPt": 13, "popPt": 34, "popPad": [16, 10], "dotX": 55.05,
    "dotR": [10, 3.5], "dotTargetR": 14, "cursorHoldMs": 450, "cursorStep": [10, 18],
    "repeatDelayMs": 450, "repeatMs": 60, "emojiCols": 8, "prefixBias": 0.5},
  "splash": {"pt": 56, "font": "Light", "lockDropMs": 750, "lockDropDelayMs": 2200},
  "loading": {"textPt": 20, "x": 20, "dotPx": 3, "dots": 5, "dotDelayMs": 160, "periodMs": 2600, "travelMs": 1700},
  "edgeGesture": {"edge": 18, "swipe": 56, "slop": 8, "longPressMs": 450}
}
```
