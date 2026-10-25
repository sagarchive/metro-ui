---
name: metro-ui
description: Build Windows Phone 8.1 ("Metro", Lumia) UI that is pixel-, colour-, type- and motion-faithful: Start tiles, Settings pages, toggles, pickers, sliders, call/message lists, keyboard, Action Center, lock screen, toasts, app bar, page transitions, and custom icons. Use whenever the user asks for Windows Phone, WP8/8.1, Metro, Lumia, Segoe UI Light, live tiles, or a flat black-and-accent phone UI. Never use Material, iOS, rounded or shadowed styling.
---

# metro-ui: Windows Phone 8.1

**Geometry.** 1 CSS px = 1 pt. Phone screen **360 x 740** = status bar 28 + app area 672 + nav bar 40. A *page-only* view (no bars) is **360 x 664**. Capture at device-scale-factor 4: screen PNG 1440x2960, page PNG 1440x2656.
Every number comes from measured data (`references/`). Do not guess; read the file for the surface you build.

## Prerequisites (for the render/score loop)
Docker with the `metro-capture` image: `docker build -t metro-capture harness/`. Output paths must live under `$HOME` (VM mounts). Set `DOCKER_HOST` if you use Colima. Python 3 + Pillow for `scripts/compare.py`.

## Workflow
1. Pick the surface, read its reference file (index below). Constants are in each file's final "Kit-ready constants" JSON.
2. Start from this skeleton (header is absolutely positioned; `.m-body` starts at y=108):
```html
<link rel="stylesheet" href="kit/metro.css"><script src="kit/metro.js" defer></script>
<div class="m-page">                      <!-- 360x664; use .m-screen (360x740) for a full phone with bars -->
  <div class="m-caps">Settings</div>      <!-- app name, rendered UPPERCASE 11.5 semibold -->
  <div class="m-title">display</div>      <!-- shown exactly as typed; titles are normally lowercase -->
  <div class="m-body">
    <div class="m-switch"><div class="t">OpenTone</div><div class="s">Off</div><div class="m-toggle"></div></div>   <!-- add .on to .m-toggle -->
    <div class="m-slider" data-value="50"><div class="m-caption">Screen brightness</div><div class="pct">50%</div>
      <div class="track"><div class="fill"></div><div class="thumb"></div></div></div>
    <div class="m-picker"><div class="m-caption">Timeout</div><div class="box">1 minute</div></div>
    <div class="m-pair"><div class="m-caption">Phone</div><div class="v">Lumia 930</div></div>
    <div class="m-entry"><div class="t">Wi-Fi</div><div class="d">Not connected</div></div>
  </div>
</div>
```
Pivot: `<div class="m-title">system<span class="next">applications</span></div>` (next title is `#616161`, clipped at the right edge; `data-pivot-group` / `data-pivot` in `kit/metro.js` add tap-to-switch).
Keypad: `.m-num` (dialled number, Light 42), `.m-who` (contact, accent 14), `.m-keypad > .m-key` x12 (`<b>digit</b><i>LETTERS</i>`, keys `#333`, 2 pt gaps, full-bleed), `.m-obtn` (phone-style outlined button: 1.5 pt `#666`, 46 tall; different from the 2 pt white `.m-button`).
Lists: `.m-call` (round icon, name, time, detail), `.m-thread` (name, time, ellipsised preview), `.m-bar` (full-width action bar). Mark accent text with `.hot`. Round shapes: only `.m-dot` and the 44 pt ring.
3. Capture: `sh scripts/capture.sh page.html out.png 360 664 4` (page) or `... 360 740 4` (screen). **Look at the PNG.**
4. Lint: `python3 scripts/audit.py page.html`.
5. Score against a reference spec: `python3 scripts/spec_check.py out.png evals/specs/<name>.json` (per-band dy/dx in CSS px). Fix every band with |dy| or |dx| > 1.
6. Icons: see `references/icon-design.md`; build with `scripts/icon.py`. Do not paste third-party icon fonts.

## Hard rules (the look)
- Background `#000`, text `#fff`, secondary `#999`, inactive pivot title `#616161` (40 % opacity), chrome/app bar `#1F1F1F`. Dark theme only unless the user asks for light (`references/12-sdk80-official-theme.md`).
- **Square corners, no shadows, no gradients, no blur.** Only 2 pt white outlines.
- One accent, default `#0050EF` (cobalt). The 20-colour palette is in `references/01-official-guidelines.md`. Accent = ON toggle fill, slider fill, tiles, missed/failed status text, selected items.
- Fonts: Segoe UI Light/Semilight (titles, values), Regular (body, captions), Semibold (app-name caps line). `kit/metro.css` falls back to Selawik (OFL, metric-compatible).
- **Never set `line-height`.** Use the font's natural line height; every pitch in the references was measured with it (e.g. label-value pair = 18 + 26 + 12 = 56). `scripts/audit.py` flags it.
- Left margin 16 (title at x=13). Page header: caps at y=14, title at y=24 (48 pt Semilight), content from y=108.
- Start: no clock block. Tiles small 49.5 / medium 106 / wide 219x106, gutter 7, margin 14, label bottom-left 13 pt.
- Switch row: title 21 Semilight + "On"/"Off" 13 grey + rectangular 54x24 toggle at right (thumb jumps, no slide). The title must stay on one line.
- Touch feedback is a 3D tilt (14 deg, 70 ms in / 160 ms out), not a ripple. Page changes are turnstile (rows out top-down 128 ms, in 180 ms, 33 ms stagger). `Metro.turnstile(rows, "out"|"in", cb)` in `kit/metro.js`.
- Settings entries are white Semilight + grey detail, **not** accent-coloured link lists. Action Center is a slim row of quick-action tiles (`#1F1F1F` off, accent on) plus a notification list.

## Anti-patterns
Wrong scale (it is 360 pt at DSF 4, not 450 / 3.2). A clock on Start. A large tile size. Rounded cards. Material switches. Forcing titles to lowercase in CSS (write the string as it should appear). Wrapping switch titles. Colour-shifted screenshots as colour truth.

## References (read on demand)
| Need | File |
|---|---|
| Official palette, type ramp, guidance | 01-official-guidelines.md, sources.md |
| Start, tiles, live-tile flip, app list | 03-start-and-tiles.md |
| Controls: toggle, slider, textbox, picker, button, menu | 04-controls.md |
| Page anatomy, pitches, page recipes | 05-page-anatomy.md |
| Motion: pages / shell / measured curves | 06a / 06b / 06c |
| Status bar, nav bar, lock, Action Center, toast, volume, switcher, dialog, keyboard | 07-system-surfaces.md |
| Icons (grammar, redesign procedure) | icon-design.md, 08-iconography.md |
| Sound and haptics | 09-sound-haptics.md |
| SDK theme resources (sizes x 0.75 = pt) | 10-sdk-theme-and-widgets.md, 12-sdk80-official-theme.md |
| Evals, briefs, specs | evals/evals.json |
| Known unknowns | 11-statements-of-fact.md |
| Android: reskin a real ROM | android-reskin.md |

## Fonts and licensing
Segoe UI is proprietary: reference it only via `local()`; never copy it into a deliverable. `kit/fonts/` holds Selawik (SIL OFL 1.1).
