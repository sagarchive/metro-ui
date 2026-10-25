# Windows Phone theme resources and widget metrics

Reference values for a Windows Phone 8 / 8.1 style interface: theme tokens, type roles, accent palette, widget geometry and motion constants. The official WP8 XAML resources are expressed in 480-wide pixels; the widget metrics below are expressed in points on a 360 x 740 pt reference screen (4.0 px per pt at 1440 x 2960). Items marked (unverified) or (inferred) are not confirmed by a primary source.

## 0. Units: 480-wide px to pt

Official WP8 XAML sizes are in 480-wide px. To convert to pt on a 360-wide screen, multiply by 0.75 (360 / 480). Both columns are given where an official value exists.

| Resource | Official px (480 wide) | pt (x 0.75) |
|---|---|---|
| PhoneFontSizeSmall | 18.667 | 14 |
| PhoneFontSizeNormal | 20 | 15 |
| PhoneFontSizeMedium | 22.667 | 17 |
| PhoneFontSizeMediumLarge | 25.333 | 19 |
| PhoneFontSizeLarge | 32 | 24 |
| PhoneFontSizeExtraLarge | 42.667 | 32 |
| PhoneFontSizeExtraExtraLarge | 72 | 54 |
| PhoneFontSizeHuge | 186.667 | 140 |
| PhoneMargin / PhoneHorizontalMargin | 12 | 9 |
| Page gutter (12 + 12) (inferred) | 24 | 18 |
| PhoneBorderThickness / PhoneStrokeThickness | 3 | 2.25 |
| Status bar (portrait) | 32 | 24 |
| App bar | 72 | 54 |
| App bar icon button | 48 x 48 | 36 x 36 |
| App bar glyph | 26 x 26 | 19.5 x 19.5 |

The widget metrics in sections 2-4 are already in pt and are not converted again. Some of them differ from a plain x 0.75 conversion of the official px values (for example a 16 pt page margin versus 9 pt for PhoneMargin, or an 80 pt app bar versus 54 pt); treat the official table as the specification of the platform and this document's widget table as a tuned, larger-format layout.

## 1. Theme tokens

| Token | Value | Notes |
|---|---|---|
| Page background | `#000000` | black |
| Foreground | white | default body size 15 px |
| Margin | 16 pt | corresponds to 20 px on a 450 px-wide reference |
| Grey (details, captions) | `#999999` (153,153,153) = 0.60 | |
| Dim (next pivot titles) | `#616161` (97,97,97) = 0.38 | opacity 0.38 + 0.62 x light-up |
| Slider / progress track | `#383838` (56,56,56) = 0.22 | |
| Seek bar buffered | `#555555` (85,85,85) | |
| Toggle off-track | none drawn (black) in the primary set; 0.2 grey in the alternate set | see section 5 |
| App bar background | `#1F1F1F` (31,31,31), height 80 | |
| Dialog panel | `#1F1F1F` | |
| Text box fill | idle `#C7C7C7` (199) = 0.78, focused `#FFFFFF`; text black; 2 px border in the same colour | |
| Menu dim | rgba(0,0,0,184) = 0.72 alpha; white band; black text 24 pt Semilight | |
| Disabled button text | `#666666` | |
| Combo border | `#999999`, 2 px | |
| Accent default | cobalt `#0050EF` | |
| Dark / light | Dark theme only in this metric set. Light theme values: (unverified) | |

### Accent palette (20)

| # | Name | Hex |
|---|---|---|
| 1 | lime | `#A4C400` |
| 2 | green | `#60A917` |
| 3 | emerald | `#008A00` |
| 4 | teal | `#00ABA9` |
| 5 | cyan | `#1BA1E2` |
| 6 | cobalt | `#0050EF` |
| 7 | indigo | `#6A00FF` |
| 8 | violet | `#AA00FF` |
| 9 | pink | `#F472D0` |
| 10 | magenta | `#D80073` |
| 11 | crimson | `#A20025` |
| 12 | red | `#E51400` |
| 13 | orange | `#FA6800` |
| 14 | amber | `#F0A30A` |
| 15 | yellow | `#E3C800` |
| 16 | brown | `#825A2C` |
| 17 | olive | `#6D8764` |
| 18 | steel | `#647687` |
| 19 | mauve | `#76608A` |
| 20 | taupe | `#87794E` |

The official WP8 table lists Sienna `#A0522D` as the 20th accent; the widget set uses taupe `#87794E` in that slot. Warning red `#E51400` is also used for low battery and error states, with amber for caution.

Accent is used for: toggle fill, slider and progress fill, pressed round-button fill, selection background, checked checkbox/radio fill, selected list-item text, pressed push-button background, loading dots, combo selection.

## 2. Fonts (role map)

| Role | Face | Size (pt) |
|---|---|---|
| Page title | Semilight | **48**, at (margin - 3, 24) |
| App name ("caps") line | Semibold, UPPERCASE | **11.5**, y = 14 |
| Entry title | Semilight | 25.5 |
| Entry detail | Regular, grey | 12, y + 31 |
| Toggle title | Semilight | 25.5 (alternate switch row: 21) |
| On/Off caption | Regular, grey | 12 (alternate: 13) |
| Slider caption / value | Regular 13 grey / Semibold 14 white | |
| Section caption | Regular 13, grey | |
| Body text | Regular | 15 |
| Textbox caption / input | Regular 13 grey / 17 px | |
| Round button label | Regular | 11.5 |
| Menu item | Semilight | 24 |
| Dialog title / body | Semibold 20 / Regular 15 | |
| Seek timestamps | Semilight | 12 |
| Checkbox / radio / combo input | 17 px; lists and combo popup 22 px; tab bar 28 px (`#616161`) | |

Font families:

| Weight | Family |
|---|---|
| Light | Segoe UI Light (phone: Segoe WP Light) |
| Semilight | Segoe UI Semilight (phone: Segoe WP Semilight) |
| Regular | Segoe UI (phone: Segoe WP) |
| Semibold | Segoe UI Semibold (phone: Segoe WP Semibold) |
| Symbols | Segoe MDL2 Assets, Segoe UI Symbol |

Open fallbacks (Selawik, Open Sans) can stand in where Segoe is unavailable. Bold exists in the Segoe family but no role above uses it. Text sizes are in points of a 360-wide coordinate space, so 1 pt = 1 CSS px at 360 px wide.

## 3. Widget geometry (pt unless noted)

| Widget | Geometry |
|---|---|
| Page header | height **108** (an alternate constant of 104 also appears; use 108); caps line at y 14, title top at y 24; hit area top 90 |
| Pivot titles | height 108; next title at x = margin - 3 + width + 16; non-current titles opacity 0.38; light-up past half way (crossing +-30 over 60); switch distance 50 pt, flick velocity 0.3 pt/ms, spring w 0.018/ms; caps height 32 |
| Page list | margins L 16, R 16, bottom 24, spacing 0; default space 16; text +12 after; section: gap 10 above, 6 below; slider +8; textbox +16; button +12 |
| Entry | height **59** with detail, **45** without; title 25.5 Semilight; detail at y + 31 (alternate: pitch 59, hit rect 57 high from y - 2) |
| Toggle row | height **59**; switch frame at x = w - 54, y = 8: 2 pt white stroke rect (x+1, y+1, 52, 22); accent fill (x+4, y+4, 46 x pos, 16); thumb white 12 x 26 at x + 1 + 40 x pos, y - 1; animation 130 ms OutCubic. Alternate switch row: pitch 66, title 21 pt, switch at y + 4, off-track fill 0.2 grey, thumb at x + 1 / x + 41 |
| Slider | height **56** + 8 gap; caption 13 grey; value right-aligned 14 Semibold; track y = 34, h 4 (`#383838`); thumb white 10 x 18 at fill - 5, y = track - 7; haptic tick on press. Alternate: hit height 46, track y + 24, value at x + w - 42, same thumb |
| Seek bar | height 46; times 12 Semilight above; track y 28, h 4; thumb 10 x 18 (12 x 22 while scrubbing), opaque white; buffered bar `#555555` |
| Text box | caption 13 grey, 4 gap, field height **40** (alternate: 38, caption gap 22); on-screen keyboard raised on tap |
| Button | primary variant: transparent background, radius 4, padding 6 x 14, min height 26, 16 px text, pressed = accent background. Alternate (outlined) variant: height 40, 2 pt white outline, filled white with black text when down, label 14.5 Semibold |
| Round button | 68 x 74 (68 x 52 with no label); ring d 44 at top 4; ring stroke 2.2 pt; glyph box 18 (alternate 20); label 11.5 at d + 7 |
| App bar | height **80**, background `#1F1F1F`, margins L/R 16, top 2, bottom 4, buttons centred with stretch on both sides |
| Hold menu | dim 0.72, white band, row **50**, band padding 16 (8 + 8), text 24 Semilight at x = margin, y = top + 16 + i x 50 |
| Dialog | panel `#1F1F1F` full width from top; margins L/R 24 (margin + 8), top 40, bottom 20, spacing 12; title 20 Semibold; buttons min height 40, spacing 12 (buttons may carry a 2 px solid white border, transparent fill); swings down (-90 deg to 0) in 260 ms OutCubic; page dims; haptic tap on show |
| Loading dots | height 8; 5 dots 3 x 3 in accent at y + 3; period 2600 ms; dot i starts at i x 160 ms; each crosses in 1700 ms along x = w x (0.5 + 0.5 x (0.25u + 0.75u^3)), u = 2k - 1 |
| Progress bar | 4 px accent bar on `#383838`; height 12 (28 with caption); glide 320 ms OutCubic; indeterminate value shows dots |
| Checkbox / radio | 22 x 22, 2 px white border, checked = accent fill; radio radius 13; spacing 12 |
| Scroll | body follows finger; overscroll resistance 0.4; fling friction e-fold **350 ms** (alternate 380 ms); overscroll pull-back e-fold 110 ms with fling damped e-fold 35 ms |
| Press lean (tilt) | tilt 14 deg, lift 40, sink 0.045, in 70 ms, out 160 ms, ease 1 - (1 - t)^2 |
| Gestures | slop 8 pt; hold 500 ms; pivot drag only if within 20 deg over 18 pt |
| Live tiles | up to 3 text lines plus a count; small tiles stay still |
| Navigation animation | turnstile rows: row-out 110 ms, row-in 180 ms, stagger 33 ms, gap 120 ms, turn-in 80 deg, turn-out 50 deg, field of view 34 deg; first-page entrance: stagger 28, row 190, title 200 over 35 pt (rows travel 50 pt), hold 60 |

All durations are at 100 % animation speed. A default speed of 75 % plays them at 133 % duration; selectable speeds are 50 / 75 / 100 / 125 / 150 / 200 %.

## 4. Conventions

- Pages are 360 pt wide; apps do not draw status or navigation bars.
- One finger, one owner: tap versus drag is decided at 8 pt; hold is 500 ms.
- The small "caps" line over a page title is the application name in uppercase.
- Loading: first frames are black; the entrance begins after the first rendered frames (up to 1.5 s).

## 5. Metric variants (primary versus alternate values)

Two sets of values exist for several widgets. The primary set is used in the widget table above; use it unless matching the alternate look.

| # | Item | Primary | Alternate | Note |
|---|---|---|---|---|
| 1 | Header height | 108 | 104 | the 104 constant is inconsistent with the 108 first-entry offset; use 108 |
| 2 | Toggle row | 59 high, title 25.5, On/Off 12, switch y = 8 | pitch 66, title 21, On/Off 13 at y + 26, switch y + 4 | primary looks like an entry row; alternate is a separate style |
| 3 | Toggle off-track | none | 0.2 grey fill (46 x 16 at +4, +4) | |
| 4 | Slider | widget 56, track y 34 | hit 46, track y + 24, value at x + w - 42 | right-aligned versus fixed offset |
| 5 | Text box | height 40, caption gap 4 | height 38, field at +22 | |
| 6 | Button | borderless, pressed = accent | outlined 2 pt, 40 high, pressed = white | the outlined style matches the stock phone button |
| 7 | Round-button glyph box | 18 | 20 (path coordinates to +-10) | |
| 8 | Row-out duration | 110 ms | 128 ms | |
| 9 | Overscroll resistance | 0.4 | 0.35 | |
| 10 | Scroll friction e-fold | 350 ms | 380 ms | |
| 11 | Bottom bar height | 80 (app bar) | navigation bar 40, status bar 28 | different elements |
| 12 | Default window | 360 x 740 | 360 x 640 | |
| 13 | Dialog buttons | plain, no border, min height 40 | 2 px solid white border, transparent, 40 high | otherwise identical panel, margins and fonts |
| 14 | Splash font | n/a | Light face, size 56 | |
| 15 | Navigation transition table | 13 rows | 13 rows | identical values |

## Kit-ready constants

```json
{
 "theme": {"bg":"#000000","fg":"#FFFFFF","grey":"#999999","dim":"#616161","track":"#383838","appBar":"#1F1F1F","dialog":"#1F1F1F",
  "inputIdle":"#C7C7C7","inputFocus":"#FFFFFF","menuDim":0.72,"accentDefault":"#0050EF","mode":"dark-only","margin":16},
 "type": {"title":["SemiLight",48],"caps":["SemiBold",11.5],"entryTitle":["SemiLight",25.5],"entryDetail":["Regular",12],
  "caption":["Regular",13],"sliderValue":["SemiBold",14],"body":["Regular",15],"menuItem":["SemiLight",24],"dialogTitle":["SemiBold",20],"roundLabel":["Regular",11.5]},
 "widgets": {"header":108,"entry":{"h":59,"hNoDetail":45},"toggleRow":{"h":59,"switch":{"w":54,"frame":[52,22],"fill":[46,16],"thumb":[12,26],"travel":40,"y":8,"ms":130}},
  "slider":{"h":56,"trackY":34,"trackH":4,"thumb":[10,18]},"seek":{"h":46,"trackY":28,"thumb":[10,18],"thumbDrag":[12,22]},
  "textbox":{"h":40,"altH":38},"button":{"h":40,"stroke":2},"roundButton":{"w":68,"h":74,"ring":44},"appBar":80,"menuRow":50,"menuPad":16,
  "dialog":{"padX":24,"padTop":40,"padBottom":20,"gap":12,"ms":260},"dots":{"count":5,"period":2600,"cross":1700,"stagger":160,"size":3,"h":8},
  "progress":{"h":4,"ms":320},"checkbox":22},
 "motion": {"tilt":{"deg":14,"lift":40,"sink":0.045,"inMs":70,"outMs":160},"slop":8,"holdMs":500,"overscroll":0.4,"flingTauMs":350,
  "speedDefaultPct":75,"fovDeg":34,"rowStaggerMs":33,"gapMs":120,"rowInMs":180,"rowOutMs":[110,128],"turnInDeg":80,"turnOutDeg":50},
 "accents": {"lime":"a4c400","green":"60a917","emerald":"008a00","teal":"00aba9","cyan":"1ba1e2","cobalt":"0050ef","indigo":"6a00ff","violet":"aa00ff","pink":"f472d0","magenta":"d80073","crimson":"a20025","red":"e51400","orange":"fa6800","amber":"f0a30a","yellow":"e3c800","brown":"825a2c","olive":"6d8764","steel":"647687","mauve":"76608a","taupe":"87794e"}
}
```
