# Windows Phone 8.1 Motion: Measured Specification

Measured timings, geometry and curves for Windows Phone 8.1 shell motion. Tags: **(inferred)** and **(unverified)** mark values that were not directly measured. Reference screen model: 360 x 740 pt. All `ms` values are at 100 % animation speed (as on a real device). A default of 75 % playback speed multiplies durations by 1.333.

## 1. Provenance of the numbers

Two kinds of data appear here and are labelled throughout: **measured** (frame-by-frame analysis of screen recordings of a reference build) and **SDK/firmware table** (official transition tables, with curves reconstructed).

| Source | What | Used for |
|---|---|---|
| A. 60 fps screen capture of a reference device (launch, return, a 4.9x slow-motion return, app list, list launch, Settings arrival) | frame-by-frame colour tracking of tiles | Start tile leave/return, app list, app entrance, pivots (measured) |
| B. Screen recording of Settings and an Office hub pivot drag | tab/pivot drag tracking | pivot spring and title travel (measured) |
| C. Firmware animation tables (angles, durations, scales, curve names, weights); exact curve formulas not available, rebuilt | named transitions table, turnstile 128 ms / 50 deg | SDK/firmware table |
| D. 30 fps third-party recording of notification-centre page changes | page-change timing in frames | row stagger ~ one frame, 3 frames long, black 2-3 frames (measured) |
| E. Older 30 fps recording of a reference device | Start leaves in 340 ms, 80 ms black | superseded by A |
| F. Static screenshot of the Settings hub | header metrics scaled to 360 pt | header 48 pt title, caps 14 pt down, first entry 108 down |
| G. Status bar | glyph proportions vs battery cell | status bar glyph sizing |

## 2. Measurement method

1. Record the reference clip at 60 fps and crop to the screen (506 px of screen = 360 pt, i.e. 1.405 px/pt; for the Office/Start capture the screen is 508 px wide). Extract every frame.
2. Tracking: de-duplicate frames (mean abs diff > 0.25). For each tile find its colour (tolerance 14-16 per channel; phone (255,112,0), office (254,73,0), here (10,63,151), pink (253,70,133), purple (128,54,160), iqiy (159,170,35)) inside a search box and record per frame: left edge x, right edge x, edge heights hL/hR (max over first/last k = max(2, run/12) columns), top, bottom. Edge heights give perspective depth; edges give turn angle.
3. Fit: time scale `MS = 1000/60/4.9` (the slow-motion clip is **4.9x** slower); eye distance `EYE = (740/2)/tan(17 deg)/360 * 508` (vertical FOV 34 deg on the 740-pt reference screen; = 3.4 screen widths); centre CX = 324 px. A 10-parameter model fitted by random-restart hill climbing (60,000 iterations), error on both edges for all tiles plus edge heights for Office and HERE. Result: **2.9 px rms on 215-px-wide tiles**.
4. Regression: the fitted formula is printed beside the measurement for comparison.
5. Re-measuring a clone: record every frame of the launch of Settings and return to Start (optionally at 5x slow motion), then report per tile "appears / settles / takes" in real ms (timestamps divided by 5 for slow motion; settle threshold mean diff < 6, appear threshold luminance > 6; 2-column grid boxes for a 360x700 area). Frames over 25 ms while moving count as dropped.
6. Unit conversions: capture 508 px = 360 pt (1.411 px/pt); 506 px = 360 pt (1.406); internal px/pt = 4.0.

## 3. Start tiles: coming back (arrival)

Measured (A, slow motion 4.9x, six tiles tracked; fit rms 2.9 px). For tile local time `u` in 0..1 over `life`:

- Life **186 ms** (fit 186.38).
- Angle (deg) = `69.8 * exp(-2.649 u) * (1-u)^0.165`, about the tile edge nearest the screen centre line, far side away. Plain-language checkpoint (earlier fit): from 65 deg: 38 after 35 ms, 22 after 70 ms, 8 after 105 ms, flat at end.
- Depth: hinge edge `0.182 * exp(-1.656 u) * (1-u)` eye-distances **behind** the screen (earlier fit: 0.2).
- Sideways offset (tile widths) = `(-0.476 exp(-7.157 u) + 0.193 exp(-0.849 u)) * sqrt(1-u)`: starts 0.28 left (earlier fit 0.3), overshoots ~0.1 (earlier 0.08) past place to the right about a third in (~60 ms, under the neighbour's edge), then glides home.
- Shade: darker while turned, about three quarters edge-on: `shade = (0.7 + 0.3 cos(angle)) * ramp(u/0.08)`.
- Opacity: tiles stay solid while turning, fading only the last stretch: `alpha = 1 for turn < 0.7, (1-turn)/0.3 after`.
- Stagger: each row starts **50 ms** after the one below; the left of two neighbours starts **51 ms** after the right; a small tile starts **33 ms** early with life x0.8; the top-left tile is last, +70 ms.
- Jitter (an added humanising touch, not measured): start +-6 ms, speed +-5 %, travel +-15 %.
- Eye: vertical FOV 34 deg; eye = 3.4 screen widths.

## 4. Start tiles: leaving (launch)

Measured (A, normal speed, 3 frames per tile at 60 fps):

- Tile turns on its **left** edge toward the viewer: **10, 25, 40 deg** over three frames (end angle 45 deg, quadratic `angle = -45 * turn^2`).
- Grows ~**10 %** (0.09 of eye distance closer).
- Swept left: 24 px of 508 on the left of the screen, 50 px on the right (`0.047` / `0.098` of screen width).
- Life **85 ms** per tile.
- Same stagger as return (50 / 51 / -33 ms), rows from the **bottom up**.
- Tapped tile alone: waits **80 ms**, then goes in **55 ms**.
- Whole launch (A at 60 fps): tiles out ~**270 ms**, tapped tile ~130 ms after, black **~110 ms**, app in **~300 ms** (a 350 ms value is used in the constants); closing: app out ~**250 ms**, black ~**150 ms**, tiles in from the bottom row ~**270 ms**.
- Older 30 fps recording (E): Start gone 8-9 frames (~270-300 ms) after it starts to leave, each tile 3-4 frames, black a few frames; an earlier note says "Start leaves in 340 ms, then 80 ms of black". **Conflict**: 340 vs ~270 ms and 80 vs 110 ms black; the 60 fps numbers are preferred.

## 5. Start <-> App list

- Page slide: two pages slide together, fast then settling, **~300 ms**; flick threshold **0.35 pt/ms**; nothing turns.
- List geometry (506 px = 360 pt): column 80 pt in, squares 45 pt, row pitch 55 pt, first square 17 pt below the status bar; a letter header is an accent-coloured outline with the letter in the lower left; an app is the tile colour with a glyph, name 13 pt right of the icon.
- Launch from list: rows leave **bottom first, ~23 ms apart**, each turning on its left edge; the tapped row alone takes ~**170 ms**, then is gone. Rule: rows of 55 pt vs tiles of 113 pt gives 23 ms; the tile rule can be reused unchanged by treating a row as a 110-wide small tile at x = 0.5 left.
- Scrolling (tuning, not measured): coast loses speed by a factor e every **380 ms**; overscroll follows at **0.35** of finger; spring omega **0.016/ms** (~quarter second, no bounce); max velocity 7 pt/ms, edge carry max 1.4.

## 6. App entrance and page turnstile

Measured (A, Settings arriving):

- Rows from the top, **28 ms** apart, each starts **50 pt** right of its place and turns in while sliding home in ~**190 ms**; remaining-distance fraction `(1-t)^4`; measured 1, 0.5, 0.31, 0.18, 0.055, 0.028, 0 at 0, 16, 50, 66, 100, 116, 150 ms.
- App name and title: same motion over **35 pt**, **200 ms**, not growing. Touch may cut it short after 60 ms.
- Page-to-page (D at 30 fps, plus A): rows of the old page leave from the **top**, the tapped row **last**, each ~1 frame apart (**33 ms**; firmware row feather 33), 3 frames long (**128 ms**, from the firmware TurnstileForwardOut 0.128 s; the SDK table gives 110), turning about the left edge to **50 deg** (firmware) while fading; screen black **2-3 frames** (~120 ms); new rows arrive from behind (**80 deg**, **180 ms**; a reference device's Settings: ~150); going back, both run bottom-up. An older note: rows 30 ms apart, black 80 ms, **~750 ms in all**.
- The title stays put; the list scrolls under cached drawing. Pull past end at **0.4** of finger, spring back.

## 7. Pivots

Measured (B, Office hub; title and rows tracked by left edge): the finger drags the tab across, with the next tab's rows already beside its grey title. On release (past ~**50 pt**, or flick > **0.3 pt/ms**): old rows are gone at once; the new tab (title plus rows together) glides home from where its title was: **272, 148, 71, 38, 17, 9 pt** left at 100 ms steps (e-fold ~150 ms). Spring omega **0.018/ms** (~quarter second, critically damped). The title strip moves one title-width per screen-width of tab movement; the next title lights up past halfway (over 60 pt); inactive title opacity 0.38. The app name does not move; the old title reappears at the right edge as the next one (tabs wrap).

## 8. Named transitions (SDK/firmware table)

Official SDK/firmware table; values were identical in two independent copies (13 rows verified equal). Fields: axis (0 = Y, 1 = X, 2 = Z), from_deg to_deg, pivot, from_scale to_scale, from_dy to_dy, from_alpha to_alpha, ms, curve (weight).

| name | axis | deg | pivot | scale | dy | alpha | ms | curve(weight) |
|---|---|---|---|---|---|---|---|---|
| turnstile-in | Y | -80 -> 0 | 0 | 1 | 0 | 1 | **350** | log(60) |
| turnstile-out | Y | 0 -> 50 | 0 | 1 | 0 | 1 -> 0 | **128** | exp(60) |
| swivel-in | X | -60 -> 0 | 0.5 | 1 | 0 | 0 -> 1 | 300 | log(200) |
| swivel-out | X | 0 -> 60 | 0.5 | 1 | 0 | 1 -> 0 | 199 | exp(60) |
| continuum-hide | X | 0 -> 80 | 0 | 1 | 0 -> 120 | 1 -> 0 | 120 | exp(60) |
| continuum-show | X | -50 -> 0 | 0 | 1.5 -> 1 | -60 -> 0 | 0 -> 1 | 350 | log(60) |
| readerboard-in | X | -45 -> 0 | 0 | 1 | 0 | 0 -> 1 | 166 | log(60) |
| readerboard-out | X | 0 -> 90 | 0 | 1 | 0 | 1 -> 0 | 166 | exp(60) |
| slide-up-fade-in | Y | 0 | - | 1 | 24 -> 0 | 0 -> 1 | 240 | log(150) |
| rotate-90 | Z | 90 -> 0 | 0.5 | 1 | 0 | 1 | 167 | scurve(7.5) |
| fade-in | - | 0 | - | 1 | 0 | 0 -> 1 | 350 | log(150) |
| fade-out | - | 0 | - | 1 | 0 | 1 -> 0 | 150 | exp(150) |
| tile-flip-notify | X | -180 -> 35 -> -6 -> 0 | 0.5 | 1 | 0 | 1 | **520** | overshoot |

Curve formulas (reconstructed, not read from firmware): `k = w/30`; exp: `(e^{k t}-1)/(e^{k}-1)`; log: `1-(e^{k(1-t)}-1)/(e^{k}-1)`; scurve: logistic `1/(1+e^{-w(t-0.5)})` normalised on [0,1]. Overshoot (live-tile notify flip): t < 0.367: -180 -> 35 via log(10); 0.367..0.833: 35 -> -6 via scurve(10); then -6 -> 0 linear. Also: toast swivel = **-45 deg about X to 0**; firmware row feather = **33 ms**.

## 9. Live tile (flip) and marquee

- Notify flip: spring to 180/0 deg in **520 ms**, damping 0.08, following the firmware overshoot -180 -> 35 -> -6 -> 0.
- Cadence (unverified, not measured): back stays 5-8 s; front 4-10 s; one tile at a time; small tiles do not flip.
- Long back lines marquee (tuning): rest 1200 ms at start, slide at 30 pt/s until the end shows, rest 1200 ms, restart.

## 10. Other timing constants (tuning, no measurement claimed)

| Constant | Value |
|---|---|
| Press tilt | 14 deg, lift 40, sink 0.045, in 70 / out 160 ms, ease out-quad |
| Peek hold / stay | 320 / 3000 ms |
| Edit mode | 180 ms |
| Status icon in / out | 150 / 70 ms |
| Toast | 4500 ms visible, 58 pt high, swivel -45 deg |
| Switcher | 260 ms, card scale 0.6, gap 18 |
| On-screen keyboard slide | 200 ms |
| Picker open / close | 250 / 200 ms |
| Toggle thumb | 130 ms OutCubic (SDK) |
| Dialog swing | 260 ms (SDK) |
| Loading dots | 2600 period, 1700 cross, 160 stagger |
| Key popup | letter redrawn larger in accent just above key |
| Animation speed default | 75 %, range 25-300 |
| Lock unlock slide | travel > 1/5 screen; exit 200 ms |

## 11. Unknowns and gaps

- Keyboard key-popup timing and tile flip timing from a real phone: (unverified), no measurement.
- Real haptic timing: (unverified).
- The original clips are not bundled; numbers cannot be re-derived from this document alone.
- Alternate figures to reconcile: 340 ms / 80 ms (older) vs 270 / 110 (current); SDK row-out 110 vs firmware 128; row stagger 33 (firmware) vs 28 (capture).

## Kit-ready constants

```json
{
 "tileReturn": {"lifeMs":186,"angleDeg0":69.8,"kAngle":2.649,"pAngle":0.165,"depth0":0.182,"kDepth":1.656,
   "dx":{"A":-0.476,"kA":7.157,"B":0.193,"kB":0.849,"fade":"sqrt(1-u)"},"rowMs":50,"leftMs":51,"smallEarlyMs":33,"smallLifeScale":0.8,
   "lastLateMs":70,"shade":"0.7+0.3*cos(angle)","alphaStartTurn":0.7,"fovDeg":34,"eyeScreenWidths":3.4,"fitRmsPx":2.9},
 "tileLeave": {"angleDeg":[10,25,40],"endDeg":45,"grow":0.09,"sweepLeft":0.047,"sweepRight":0.098,"lifeMs":85,"tappedWaitMs":80,"tappedLifeMs":55,"order":"bottom-up"},
 "launch": {"tilesOutMs":270,"blackMs":110,"appInMs":300,"appInCodeMs":350,"appOutMs":250,"backBlackMs":150,"tilesInMs":270},
 "appList": {"pageSlideMs":300,"listRowStaggerMs":23,"tappedAloneMs":170},
 "enter": {"staggerMs":28,"rowMs":190,"travelPt":50,"titleTravelPt":35,"titleMs":200,"remaining":[[0,1],[16,0.5],[50,0.31],[66,0.18],[100,0.055],[116,0.028],[150,0]]},
 "turnstile": {"rowOutMs":128,"rowInMs":180,"staggerMs":33,"gapMs":120,"outDeg":50,"inDeg":80},
 "pivot": {"switchPt":50,"flickPtPerMs":0.3,"springW":0.018,"lightPt":60,"glidePt":[[0,272],[100,148],[200,71],[300,38],[400,17],[500,9]],"inactiveOpacity":0.38},
 "transitions": {"turnstile-in":[350,"log",60],"turnstile-out":[128,"exp",60],"swivel-in":[300,"log",200],"swivel-out":[199,"exp",60],
   "continuum-hide":[120,"exp",60],"continuum-show":[350,"log",60],"readerboard-in":[166,"log",60],"readerboard-out":[166,"exp",60],
   "slide-up-fade-in":[240,"log",150],"rotate-90":[167,"scurve",7.5],"fade-in":[350,"log",150],"fade-out":[150,"exp",150],"tile-flip-notify":[520,"overshoot",0]},
 "curves": {"exp":"(e^(kt)-1)/(e^k-1)","log":"1-(e^(k(1-t))-1)/(e^k-1)","k":"w/30","scurve":"logistic w, normalised"},
 "toast": {"swivelDeg":-45,"visibleMs":4500},
 "marquee": {"restMs":1200,"speedPtPerSec":30},
 "speed": {"defaultPct":75,"min":25,"max":300}
}
```
