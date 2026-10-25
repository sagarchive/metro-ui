# Official guidelines and public evidence for Windows Phone 8 / 8.1 UI

Scope: Microsoft's own specifications plus public-web screenshots and reviews.
Convention: every fact carries a source tag such as `[S5]`; tags resolve to URLs in the Source index at the end of this file. "Measured" means read from the pixels of a published screenshot. "(unverified)" means recalled or inferred with no source fetched. Nothing is invented: where no source exists the gap is stated.

## 0. Read this first: version conflicts

The official design documentation covers **Windows Phone 8 (Silverlight, "vs.105")**. Microsoft never re-published a separate WP8.1 design library; the WP8.1 Runtime pages cover assets, XAML resources and APIs, not look and feel. Rule used throughout:

| Topic | WP7.x | WP8.0 (vs.105 docs) | WP8.1 (Runtime / Update 1) | Win10 Mobile | Applies to WP8.1 |
|---|---|---|---|---|---|
| Accent colours | 10 (plus brown 160,80,0 etc.) [S4] | 20 colours [S4] | same 20 (plus OEM extra) [S2]; WP8.1 apps read it through `SystemColorControlAccentColor` [S24] | user picks from a larger palette (not covered) | the 20 in S4 |
| Orange / Brown / Pink / Green values | Mango F09609, Brown A05000, Pink E671B8, Green 339933 [S4] | FA6800, 825A2C, F472D0, 60A917 [S4] | WP8 values | n/a | WP8 values |
| Fonts | Segoe WP | Segoe WP (plus Light / Semilight / Semibold) [S3] | Segoe WP still the phone UI face; XAML now lets you set "Segoe UI" and pick weights [S25]; Win10 type ramp pages describe Segoe UI | Segoe UI (UWP ramp) | Segoe WP family |
| Font size units | points in guides | XAML px values: 18.667 .. 186.667 [S3] | same values; Runtime guides quote points = px / 1.333 [S23] | UWP ramp 11-... px | S3 table |
| Tile templates | flip only | flip / iconic / cycle, small / medium / wide [S5][S9] | Runtime tiles: Small 71x71, Medium 150x150, Wide 310x150 (plus tiny 44x44) at scale 100% [S10]; WP8 templates still run | adds "large" etc. | S10 for new apps, S5-S8 for WP8-style |
| Start columns | 2 | 2 (third column added in GDR3 on big 1080p screens) [S31a] | third column available on all devices ("Show more tiles") [S31a][S29] | 3-4 columns | 2 or 3 |
| Back / Start / Search | hardware | hardware, capacitive allowed [S15] | may be on-screen; screenshot combo becomes Power + Volume up [S31a][S30] | on-screen | both |
| Settings structure | list | `system` / `applications` pivots [S26] | same two pivots plus an `extras & info` entry [S32 img 20, 35] | Win10 category grid (System, Devices, Network, Personalization...) [S32 img 20] | system / applications |
| Status bar height | 32 px | 32 px portrait, 72 px landscape (WVGA basis) [S14][S15] | unchanged in docs; expanded state shows carrier / battery % / date [S31b] | n/a | 32 (WVGA px) |

A screenshot labelled "Windows Phone 8.1 Update 2" on Wikimedia Commons (768x1280) shows a *categorised* Settings list with names Network+Wireless, Personalization, Accounts, System, Time+Language, Ease of access, Privacy, Update+Security, Extras (German UI). It is a transition frame (old list ghosted behind). This is the Win10-style structure, **not** the shipped 8.1 Update 1 structure; treat it as pre-release and not the target [S36].

## 1. Principles

- Themes: only colours (background Dark / Light plus accent) change with theme; fonts and control sizes never do [S1][S2]. Default = dark background plus blue (Cyan) accent; carriers and OEMs may add one extra accent [S1].
- Content over chrome: "foundation of the Windows Phone visual style is the lack of chrome elements ... typography bears more importance" [S13]. "Use content and typography for visual appeal, and never use visual elements that are purely decorative" [S11].
- Avoid in tiles: 3D type, gradients / bevels / shadows, rounded corners, black or white tile backgrounds, transparent background with colourful image [S11].
- Motion: two kinds - transitions (user triggered, "mental breadcrumb", big between apps, small within) and animations (local feedback, e.g. lock screen "hop") [S16]. Rules: all animations are part of one system; each serves a purpose and gets out of the way quickly; **2.5D not 3D**, no textures / lighting / extrusion; Tilt shows a flat surface; UI elements can push other elements; hardware and software can trigger them [S16].
- Easing: logarithmic for things entering (slide to an easy stop), exponential for things leaving (build tension then fly off), S-curve for larger moves when logarithmic feels jarring [S16]. No millisecond durations are given in the official doc (see section 7).
- Navigation: hub-and-spoke, hardware Back walks a back stack; no in-app Back / Close / Home buttons; no floating buttons - use the App Bar [S14][S13].
- Settings in apps: model on system settings; apply immediately (no OK / Done); avoid more than two pages; heading pattern `APPLICATION SETTINGS` over `<page name>` [S13].
- Tiles: avoid loud colours; do not use relative timestamps ("2 hours ago") on tiles - use absolute time, e.g. "14:00" [S5].

## 2. Typography

Official XAML values (WP8; carried to the WP8.1 XAML phone template - see conflict table) [S3]:

| Resource | Value |
|---|---|
| PhoneFontFamilyNormal | Segoe WP |
| PhoneFontFamilyLight | Segoe WP Light |
| PhoneFontFamilySemiLight | Segoe WP Semilight |
| PhoneFontFamilySemiBold | Segoe WP Semibold |
| PhoneFontSizeSmall | 18.667 |
| PhoneFontSizeNormal | 20 |
| PhoneFontSizeMedium | 22.667 |
| PhoneFontSizeMediumLarge | 25.333 |
| PhoneFontSizeLarge | 32 |
| PhoneFontSizeExtraLarge | 42.667 |
| PhoneFontSizeExtraExtraLarge | 72 |
| PhoneFontSizeHuge | 186.667 |

Text styles [S3]: `PhoneTextBlockBase` = Normal family, Normal size (20), Foreground PhoneForegroundBrush, Margin PhoneHorizontalMargin (12,0). Title1 = SemiLight 72; Title2 = SemiLight 32; Title3 = SemiLight 22.667; Large = SemiLight 32; ExtraLarge = SemiLight 42.667; GroupHeader = SemiLight 32 + PhoneSubtleBrush; Small = 18.667 + PhoneSubtleBrush; Subtle = Normal + PhoneSubtleBrush; Contrast = SemiBold + PhoneContrastForegroundBrush; Accent = SemiBold + PhoneAccentBrush; Huge = Light 186.667.

Other typographic facts:
- Minimum font size on the platform: **15 pt** [S13]. 20 px = 15 pt, i.e. the px values above are points x 1.333 [S23].
- Segoe WP is not fixed-width; tile character counts are approximate; there is no automatic wrapping in tile templates, truncation is encouraged [S6].
- WP8.1 TextBlock additions: CharacterSpacing, MaxLines, OpticalMarginAlignment (default ON, so remove manual left-edge nudges), TextTrimming CharacterEllipsis / Clip, default TextWrapping changes from NoWrap to WrapWholeWords, IsColorFontEnabled (colour emoji) [S25].
- Pivot header text: maximum one or two words; pivot header height is fixed [S19]. Menu item text is lowercased automatically; 14-20 characters maximum [S11][S12].
- Observed (not official): page titles in 8.1 are very large Segoe WP Light / Semilight lowercase ("system", "start+theme", "people", "xbox music") with a small UPPERCASE app / section label above ("SETTINGS", "PHOTOS"); the pivot's inactive headers are drawn at about 50% grey (measured #808080 in a Microsoft 8.1 marketing screenshot); dark-theme body text is white, secondary labels light grey about #C1C1C1 (thin text, so the peak value understates).

## 3. Colour and themes

### 3.1 The 20 accent colours (official table image, read visually) [S4]

| # | Name | RGB | Hex | Note |
|---|---|---|---|---|
| 1 | Lime | 164,196,0 | #A4C400 | |
| 2 | Green | 96,169,23 | #60A917 | WP7.5: 339933 |
| 3 | Emerald | 0,138,0 | #008A00 | |
| 4 | Teal | 0,171,169 | #00ABA9 | WP7.5 called it Viridian |
| 5 | Cyan | 27,161,226 | #1BA1E2 | WP7.5 "Blue"; the default accent |
| 6 | Cobalt | 0,80,239 | #0050EF | |
| 7 | Indigo | 106,0,255 | #6A00FF | |
| 8 | Violet | 170,0,255 | #AA00FF | WP7.5 "Purple" |
| 9 | Pink | 244,141,208 (table) | #F472D0 | the table's RGB column says 141 but hex F472D0 = 244,114,208; hex is consistent with the swatch, treat hex as correct |
| 10 | Magenta | 216,0,115 | #D80073 | |
| 11 | Crimson | 162,0,37 | #A20025 | |
| 12 | Red | 229,20,0 | #E51400 | |
| 13 | Orange | 250,104,0 | #FA6800 | WP7.5 "Mango" F09609 |
| 14 | Amber | 240,163,10 | #F0A30A | |
| 15 | Yellow | 227,200,0 | #E3C800 | |
| 16 | Brown | 130,90,44 | #825A2C | WP7.5: A05000 |
| 17 | Olive | 109,135,100 | #6D8764 | |
| 18 | Steel | 100,118,135 | #647687 | |
| 19 | Mauve | 118,96,138 | #76608A | |
| 20 | Sienna | 160,82,45 | #A0522D | |

Warning: a popular third-party blog list (grade C) has Pink F47D02-ish, Yellow D8C100 and Sienna 7A3B3F - all disagree with the official table; use the table above. Windows Phone 8 also allows one carrier / OEM accent not in the table [S1][S2].

Measured confirmation: Steel accent (#647687) renders as #657688 in a 1080p screenshot of tiles and the Action Center quick-action "on" state [S31b] (JPEG error +-1).

Measured anomaly: Microsoft's own 8.1 marketing screenshots (432x768, 2014 blog [S27]) show the "cyan" accent as **#00BCF2**, not #1BA1E2 (tile fills, toggle fill, "end call" button #00BCF2; Cortana ring dark variant #00546D). Either those are renders using an OEM cyan or the official "Cyan" was retuned; Update 1 screenshots show a similar bright blue [S32]. Treat #00BCF2 as the observed on-device look of "cyan" in 8.1 mock / marketing frames and #1BA1E2 as the SDK constant. Which one a given implementation should use is (unverified).

### 3.2 Theme resources
Names (brushes plus colours, all backed by a colour of the same name) [S3]: PhoneAccent, PhoneForeground, PhoneBackground, PhoneContrastBackground, PhoneContrastForeground, PhoneDisabled, PhoneSubtle, Transparent, PhoneSemitransparent, PhoneChrome ("used to match the application bar colour"; colour = "status bar and application bar"), TextBox set (PhoneTextBox, TextCaret, TextBoxForeground, TextBoxEditBackground, TextBoxEditBorder, TextBoxReadOnly, TextBoxSelectionForeground), RadioCheckBox set (RadioCheckBox, ...Disabled, ...Check, ...CheckDisabled, ...Pressed, ...PressedBorder). Visibility / Opacity switches: PhoneDarkThemeVisibility / Opacity (1 in dark, 0 in light) and PhoneLightTheme* [S3].

**The official pages do not print the hex values** of Dark / Light PhoneBackground / Foreground / Chrome / Disabled / Subtle / TextBox; they live in `ThemeResources.xaml` in the Windows Phone SDK v8.0 `Design` folder [S2], which ships inside the 1.7 GB SDK ISO [S35]. Values that could be grounded:

| Item | Value | Evidence |
|---|---|---|
| Dark background | #000000 | measured on all dark screenshots |
| Dark foreground | #FFFFFF | measured on titles / value text |
| Chrome (app bar / keyboard backdrop / off quick-action tile) | #1F1F1F | measured: app bar in marketing screenshots (#191919 with a gradient edge in one), Action Center "off" tile in a 1080p capture [S31b], keyboard well in a Word Flow crop [S31c] |
| Keyboard key fill | #474747 | measured in a Word Flow screenshot [S31c] |
| Dialer key / in-call button fill | #505050 | measured in a Skype dialer marketing frame [S27] |
| Cortana search box (light grey) / mic button | #D2D2D2 / #505050 | measured in a Cortana home frame [S27] |
| Action Center bottom grab-handle bar | accent x 0.69 (#46525E for Steel) | measured [S31b] |
| Toggle outline "off/on" greys | #ADADAD thumb outline | measured in a Wi-Fi Sense settings frame [S27] |
| WP7-era Dark: Disabled 808080, Subtle 999999, TextBox BFBFBF, Border CCCCCC, Inactive 666666; Light: Disabled / Inactive CCCCCC, Subtle 999999, TextBox BFBFBF, Border 999999 | WP7 emulator dump, **grade C, not WP8.1**; the blog also calls the dark background 1F1F1F, which is its own App.xaml override | [S37] |
| Light-theme values for PhoneBackground / Foreground | White / Black | [S37] (WP7), consistent with the platform; the WP8.1 light theme was measured in a Facebook app screenshot [S31b]: white page, dark text, #3B5998-like header (app-specific) |

Not found anywhere: official text-hierarchy opacity values (e.g. Subtle = 0.5 white). Do not cite a number for those; use the measured peaks above only as lower bounds.

### 3.3 Backgrounds, Start background photo
- Panorama / hub backgrounds: single image preferred; JPEG; between 480x800 and 1024x800 for no-scale; use dark, soft, low contrast; overlay a semi-transparent black / white rectangle to protect legibility [S18].
- Lock screen: static image; keep logo / text small, slightly transparent, text related to the image; provide a default image; notification text is drawn as white pixels, quick-status icons must be white plus alpha ("watermark") and show the primary-tile count beside them [S17].
- WP8.1 Start background: Settings > Start + theme > "choose photo" (opens Photo Hub: camera roll plus accounts) or the built-in Backgrounds gallery; pinch to zoom and drag to crop; tiles become transparent and the photo shows through and "shifts when scrolling to create a sense of depth" (parallax) [S28][S33]. Colour-logo tiles (e.g. Facebook, Xbox Games) and hub tiles (People) stay opaque [S31a]. Without a photo, tiles use the accent [S33].
- Measured effect in a 1080p capture [S31a]: the photo is visible through every tile as if the tile were a window; each tile still shows its own icon / label in white; opaque tiles keep their own fixed colour (Messaging etc. are see-through, Facebook blue, Office orange, Xbox green, camera purple, people tile red / transparent mosaic).

## 4. Layout and grid

Official constants (WP8):
- Screen: "the full 480 x 800 pixels" of app space when the status bar is hidden [S15]. Resolutions named in the lock-screen doc: WVGA 480x800, WXGA 768x1280, HD720p 720x1280 [S17]; the WP8.1 emulator list adds 720p 4.7", 1080p 5.5" / 6", qHD 5" [S34].
- Status bar: 32 px high in portrait, 72 px wide in landscape (WVGA px), always opaque to the screen edge, only the clock visible by default; double-tap / tap reveals indicators for about 8 seconds [S11][S14][S15]. Indicator order left to right: signal, data, call forwarding, roaming, wifi, Bluetooth, ringer, input, battery, clock [S11].
- App bar: fixed 72 px (portrait height / landscape width); icon buttons 48x48 with a white 26x26 glyph centred inside a circle drawn by the OS; up to 4 buttons; menu <= 5 items; opacity recommended 0, 0.5, 1 (at 1.0 the page is resized, below 1.0 the bar overlays) [S11][S12]. Mini mode shrinks the bar [S12]. Measured cross-check: the bar in a marketing screenshot is 63 px of 768 at 0.9 scale = 70 epx (about 72) and filled #1F1F1F [S27].
- Margins / thickness [S3]: PhoneMargin 12; PhoneHorizontalMargin 12,0; PhoneVerticalMargin 0,12; PhoneTouchTargetOverhang 12; PhoneTouchTargetLargeOverhang 12,20; PhoneBorderThickness 3; PhoneStrokeThickness 3; PhoneTextBoxInnerMargin 1,2; PhonePasswordBoxInnerMargin 3,2. The "24 px page gutter" (12 + 12) is the common WP8 content margin - (unverified) as a documented number; the templates compose it from the 12 px resources.
- Touch: ideal target 9 mm square (about 90 px on a 262-dpi device); minimum 7 mm (use only if width >= 15 mm); minimum visual size 4.2 mm; visuals under the target must keep >= 4.5 mm and 2 mm spacing; four simultaneous touches, a touch >= 7 mm wide counts if edges are >= 3.5 mm apart [S13][S14].
- Ad control: 480x80 default [S13] (not UI chrome but a layout constant).
- Orientation: portrait default; Start is always portrait; Panorama is portrait only; status and app bars stay on the same side in landscape [S14][S15][S18].
- WP8.1 Runtime XAML default page margin of 19 px (hub / pivot templates): (unverified), recalled from the Visual Studio template.

### 4.1 Start grid (WP8.1) - measured, not official
Source: a 1080x1920 capture of a 3-column "show more tiles" layout in a 8.1 review [S31a]:
- left / right margin 31 px / 32 px; column gap and row gap 25-26 px; small tile 148x148; medium 322x322 (= 2 small + 1 gap); wide 669x322 (measured 31..699); first tile top at y = 117 below the status icons; vertical pitch of small rows 174 px.
- Convert to dp by dividing by the device scale. The Runtime docs say Windows Phone 1080p assets use scale-240 [S10]; the older WP8 stack called 1080p 225%. Dividing by 2.4 gives margin 12.9, gap 10.7, small 61.7, medium 134; by 2.25 gives 13.8, 11.4, 65.8, 143. Neither gives round numbers, so treat the *ratios* as the invariant: gap / small = 0.17, margin / small = 0.21, medium = 2 x small + gap.
- Marketing frames (432x768, scale 0.9 of 480 wide if the screen is 480 epx wide, (unverified)) [S27]: margins 19 / 19, gap 6-7, small 60, medium 127 px: gap / small = 0.11 (tighter than the device capture). These are earlier-build renders; prefer the device capture.

## 5. Tiles

### 5.1 Official sizes
- WP8 doc: three sizes small / medium / wide, wide optional; small and medium required; all tiles begin as medium; the user may resize any time [S5]. Double-width tiles were reserved for Microsoft and partners in the 7.x text of S11, but WP8 allows wide for apps via the manifest [S5].
- WP8 template character counts: Iconic: Medium title 19; Wide title 39, WideContent1-3 33 each. Flip: Medium Title / BackTitle 19, BackContent 3 lines x 13; Wide Title / BackTitle 39, WideBackContent 3 lines x 27. Cycle: Medium 19, Wide 39. Small: no text [S6][S7][S8].
- Iconic images: SmallIconImage max 110x110 (best fit 70x110); IconImage max 202x202 (best fit 130x202); pad vertically with transparency to full height, crop tight horizontally [S6]. The Cycle template cycles 1-9 images [S9].
- WP8.1 Runtime asset table [S10] (phone-relevant, px at scale-100 / 140 / 240; asset / padding / logo):

| Manifest property | scale-100 | scale-140 | scale-240 |
|---|---|---|---|
| Square71x71Logo (Start small) | 71x71, pad 19,19, logo 32x32 | 99x99, pad 27, logo 45 | 170x170, pad 46, logo 77 |
| Square150x150Logo (medium) | 150x150, pad 45, logo 60 | 210x210, pad 63, logo 84 | 360x360, pad 108, logo 144 |
| Wide310x150Logo | 310x150, pad 125,45, logo 60 | 434x210, pad 175,63, logo 84 | 744x360, pad 300,108, logo 144 |
| Square44x44Logo (All apps list) | 44, pad 6, logo 32 | 62, pad 9, logo 44 | 106, pad 15, logo 76 |
| Package Logo | 50, pad 9, logo 32 | 70, pad 12, logo 46 | 120, pad 20, logo 80 |

  Also: tiny 44x44 (phone) used in search results and the Apps list; no medium-vs-wide default on phone (pinned as medium); images <= 1024x1024 px, <= 200 KB; scale values supported through the manifest on phone: 100, 140, 240 (others in practice 120, 160, 180, 200, 220, 300, 400); supply scale-240 at minimum [S10]. 150 / 71 = 2.11 and 310 = 2 x 150 + 10 imply a 10 px gap at scale-100 (derived).
- Derived 2-column math at scale-100 (from S10): wide = 2 medium + 10 px; medium = 2 small + 8 px (150 = 71 + 71 + 8). Hence the tile gutter is about 8-10 px at 100% on phone; this is consistent only roughly with the 3-column device capture (11 dp).
- Tile art rules: a transparent tile background shows the theme accent; the foreground icon must be white; avoid black / white fills [S11]. The counter always uses the user's accent, fixed system font / size [S11]. Absolute not relative times [S5].
- App name label bottom-left in white; icon centred (measured in all Start screenshots; official statement: "keep the same vertical placement of the logo in both medium and wide tiles ... include the app name at the bottom of the Tile" [S5]).

### 5.2 Live tile behaviours observed (screenshots)
Flip / people mosaic (People tile 3x3 sub-squares of 107 px at 1080p, measured), weather tile (opaque dark with moon / cloud art, uppercase city, big temperature), calendar tile (event text left, big day number bottom-right "Mon 14"), mail tile (envelope plus count right-aligned bold large), Cortana tile (ring icon, wide) [S31a].

## 6. Controls

- **Toggle switch** (WP8 / 8.1): rendered as a two-state slider: wide rectangular outline, accent-coloured fill that occupies the left portion when On, white (dark theme) / grey (light theme) vertical thumb at the right end when On and at the left when Off; label above in subtle grey and the state word "On / Off" in large type to the left. Seen in screenshots: Wi-Fi Sense settings (fill #00BCF2, thumb white, outline white) [S27]; a light-theme Facebook app (outline #A0A0A0-grey, fill app blue, thumb outlined grey; size about 200x100 px on 1080p = about 83x42 dp at 2.4) [S31b]; Ease of Access settings (Off: white thumb at left, empty outline) [S26]. Official text for the control is only the generic ToggleButton guideline; no pixel spec found. Platform-guide rule: do not put Slider / ToggleButton / Map inside a Pivot [S19].
- **Checkbox / RadioButton**: square white outline 3 px with accent / foreground tick (measured outlines in Update 1 screenshots and Cortana onboarding screens [S32][S31b]); brushes listed in S3.
- **Buttons**: rectangular, 3 px border (PhoneBorderThickness), text centred lowercase ("sync now", "choose photo", "edit info") (measured) [S3].
- **Slider** (ease of access text size), measured: thin track, filled portion in accent (red there), white rectangular thumb, 4 tick segments [S26].
- **TextBox**: light / white fill with black text in dark theme; caret; PhoneTextBox* brushes [S3]; Cortana's input is light grey #D2D2D2 with a #505050 mic square (measured) [S27].
- **App bar**: see section 4; ellipsis "..." at right; icon buttons 48x48 circle outlines; the menu is a lowercase text list that slides up from under the icons [S12]. Measured look: dark #1F1F1F bar, white circle-outlined icons [S27].
- **Pivot**: header strip with 2-3 titles visible, active white, inactive about 50% grey, pages wrap cyclically; <= 4 pivot pages recommended in the control doc, <= 6 in the app-tab doc (the docs disagree - [S19] vs [S20]); no edit boxes or panning controls inside; header height fixed [S19]. Seen: calendar week view ("this week" white, "next wee" grey; small uppercase "MAY 2014" label above) [S27].
- **Panorama / Hub**: long horizontal canvas; layers (background image slowest, panorama title slow, section titles, sections at finger speed); <= 5 sections; wraps; portrait only; app bar mode minimized; background 480x800..1024x800 [S18]. In WP8.1 the **Hub** control replaces Panorama [S38]. Seen: huge lowercase title "xbox music" over a photo background, section label "COLLECTION" uppercase small, list of lowercase links in rows about 40 px tall, next section clipped at the right edge [S27]; the People hub [S27].
- **Dialog / MessageBox**: official page not retrieved; the Back button cancels popups / MessageBox automatically [S14]. Appearance (unverified): full-width dark panel, uppercase title, buttons at the bottom.
- **Progress**: determinate / indeterminate system progress integrated in the status bar (dots running along the top) [S11]; scroll indicators fade in on pan, fade out 1 s after the gesture ends, overlay on the right / bottom edge, not touchable [S11].
- **Toast (WP8 push)**: opaque bar in accent colour at the top of the screen, small app icon at left, one bold title line plus one normal subtitle line, truncated, displayed 10 seconds, tap launches the app [S11]. WP8.1 replaces this with "banners" configurable in notifications+actions (On: Banners, Sounds, Vibrations per app) [S32 img 25][S29].

## 7. Motion and transitions

Official statements available [S16]: Turnstile is the example in the navigation matrix (four entry directions; "two or four directions"); Panoramic Entrance animation; Tilt on touch (flat, no depth); edit-box resize is animated; lock-screen "hop"; app bar menu animates; screen rotation plays transition animations [S15]. Names known from the WP7/8 Toolkit and WinRT (swivel, turnstile, continuum, slide, roll) are real, but **no official source gave durations, delays or Bezier values**; do not invent. Recalled values, (unverified): turnstile about 350 ms in / 250 ms out, row stagger about 50 ms, tilt 0.1-0.2 s.

WP8.1 Runtime: the continuum transition is exposed as `ContinuumNavigationTransitionInfo` for phone apps; `CommonNavigationTransitionInfo` and `SlideNavigationTransitionInfo` also exist; starting with Windows 8.1, theme transitions honour the Ease of Access "turn off unnecessary animations" setting [S46].

Observed (screenshots, not durations): the lock screen clock rotates / swings during unlock (a Microsoft frame shows a big white 3-D-rotated clock "10:36" over a blurred raindrop photo with the date "Tuesday September 29" on the swing path; this frame may be Windows 10 Mobile era, era (unverified)).

## 8. System surfaces catalogue (WP8.1, Update 1 unless noted)

For each surface: structure, then evidence.

### 8.1 Start
- Tiles in 2 columns (default on small screens) or 3 columns ("Show more Tiles" toggle in Settings > start+theme; the setting is a switch under the text "You can change the size and number of tiles available on your start screen." with a mini-phone wireframe showing 2 small + 1 medium + wide layout) [S29][S31a]; Start is always portrait [S15].
- Tile sizes: small / medium / wide; resize via long-press then the arrow button at the tile corner (mechanism (unverified)) [S5 for user resizing].
- Background photo with transparent tiles and parallax (see 3.3). Update 1 adds folders on Start and Apps Corner (kid mode) [S40].
- "All apps" arrow at the bottom right of Start in 8.x (unverified) - swipe left to the list.
- Evidence: Update 1 Start screenshots [S32], 1080p Start captures [S31a], marketing Start frames [S27].

### 8.2 All apps list and jump list
Alphabetical list: search magnifier circle at top-left (46-px circle outline, measured [S32]), then rows: 44-px accent-filled square icon (white glyph) + app name in Segoe WP Semilight about 20 px; letter headers are accent-outlined squares containing the lowercase letter (tap opens the jump list = grid of letters; unavailable letters dim) [S32 img 18]. Tiny logo asset 44x44 (scale-100) [S10].

### 8.3 Settings (top-level structure)
- Page pattern: tiny uppercase `SETTINGS` label, then the page title in huge lowercase Light type with pivot overflow to the right (`system applications`), single-column list rows with a 20 px title and a 12-13 px grey subtitle under it giving the current state (e.g. "start+theme / cyan", "ringtones+sounds / Nokia Tune", "email+accounts / set up email, contacts and others", "lock screen / screen timeout: 1 minute", "notifications+actions / manage action centre", "WiFi / <ssid>, WiFi Sense turned on", "flight mode / turned off", "Bluetooth / turned off", "mobile+SIM / no SIM", "NFC / turned on", "internet sharing") [S32 img 20]. Further items seen in the same list (Update 1, device dependent): display, battery saver, VPN, About, phone update, glance screen (device specific), Extras & info (OEM) [S32 imgs 21-26, 29, 34, 35].
- `system` pivot lists (2013 article): Email+Accounts, Ease of Access, Lock Screen under System; Phone, Internet Explorer, People, Photos+camera under Applications [S26]. The `applications` pivot = per-app settings (Phone, Messaging, Mail, Internet Explorer, Store, Photos+camera, People, Xbox, Games, ...) [S26][S29].
- start+theme page: intro sentence ("Change your phone's background and accent colour to suit your mood today, this week or all month."), then two combo boxes: `Background` (dark | light) and `Accent colour` (swatch + name), then a 120-px square start-background preview with a `choose photo` button and (8.1 final) `remove`; below, the toggle `Show more Tiles` (On / Off). The accent picker is a full-screen list of colour swatch + name (20 names) [S32 img 30][S29]. Backgrounds gallery page: `CHOOSE PICTURE` / `backgrounds`, 4-column grid of 215-px (1080p) square thumbnails with a 3-px accent frame and 36-px gutter (measured loosely from a screenshot [S29]).
- notifications+actions page: `Choose your quick actions` row of four (WP8.1 GA, per [S31b]) or five (Update 1) square outline buttons (about 130x130 on 1080p), then the checkbox `Show notifications in action center when my phone is locked`, explanatory text, then one row per app: coloured square icon + app name + state line "On: Banners, Sounds, Vibrations" [S32 img 25][S31b][S29].
- lock screen page: Background (choose background combo), `Show artist when playing music` toggle, notifications: `Choose an app to show detailed status` (combo), `Choose apps to show quick status` (row of 5 outlined squares, + to add), `Screen times out after` combo, `Password` toggle [S32 img 32]. Glance screen: Glance screen combo (peek / ...), "Select notifications and other content", toggles Date, Detailed status notification, Quick status notifications, Background photo [S32 img 34].
- extras & info (OEM): `EXTRAS & INFO` / `Lumia Denim`, policies link, list of installed OEM extras with versions, RAM etc. [S32 img 35].
- Toggles use a label-above / value-below layout (Subtle label, big "On", switch at right) (measured, Wi-Fi Sense [S27]).

### 8.4 Action Center (new in 8.1)
- Opened by swiping down from the top edge; a short pull shows the quick-action row, a long pull shows everything [S29][S31b][S41]. Pulling down also reveals extra status text: battery %, date, carrier name; the status bar no longer auto-hides [S31b].
- Quick actions: a row of tiles flush to the screen edges, **4 per row** in 8.1 GA ([S31b]: "direct access to four different shortcuts"; [S41] says four, e.g. Wi-Fi, Bluetooth, Flight / Airplane, Rotation lock; defaults vary by OEM e.g. brightness, camera) and **5 per row** in Update 1 (Wi-Fi, Bluetooth, Flight mode, Rotation lock, Automatic brightness [S32 img 19]) [S31b][S41]. The user chooses which in notifications+actions; settings has no scroll for more than five [S31b].
- On state = accent fill; off state = #1F1F1F with white glyph + uppercase 12-px label bottom-left; the name of the Wi-Fi network replaces the "WI-FI" label when connected; Bluetooth shows "NOT CONNECTED" or the device name (measured / seen [S29][S27][S31b]).
- Measured geometry in a 1080x1920 capture [S31b]: tiles 257 px wide x 157 px tall, 17 px gap, first tile at x = 0 (edge to edge, 4 x 257 + 3 x 17 = 1079), top at y = 189 below a status area that is taller (carrier text added); a row `X CLEAR ALL` (left) and gear `ALL SETTINGS` (right) at about y = 437 in uppercase 13-px type; notification groups below; a bottom grab-handle bar 56 px high filled with the dark accent (accent x 0.69) holding a short white dash. In a 432-px marketing frame: 4 tiles 103 px (= 114 epx at 0.9) wide, gap 6; 70 px tall [S27]. Treat the two as different builds.
- Notification cards: group header = 40x40 accent-filled app icon + app name in 26-px Light type; below, each item: bold sender / title line (white), grey preview line, right-aligned time ("12:49p"); swipe an item sideways to dismiss; swipe on a group dismisses the app group; `clear all` also clears live tile counts [S31b]. Empty state: `No notifications` in large Light grey (#A0A0A0 peak).
- A German-UI 360x600 screenshot shows 4 quick tiles (EXTERNE ANZEIGE / ORTUNG / wifi / BLUETOOTH), `ALLE EINSTELLUNGEN`, `Keine Benachrichtigungen`, and a lime accent bar at the bottom [S36].

### 8.5 Notification banners / toasts (WP8.1)
A banner appears at the top (slides down, accent-or-dark bar with app icon, bold title, message), with a per-app toggle "Banners / Sounds / Vibrations" in notifications+actions; official WP8 toast: accent bar, 10 s, icon left, bold title + subtitle [S11][S32 img 25]. No screenshot of an 8.1 banner was obtained; exact colours are (unverified).

### 8.6 Lock screen
- Components: full-bleed background photo (system or app-provided e.g. Bing / lock-screen apps), large light clock + date at bottom-left, optional detailed status line (white text from the chosen app's tile), up to 5 quick-status icons with counts, status bar icons at the top [S17][S32 img 33][S27].
- Clock / date look: time `12:05` in Segoe WP Light at about 36% of screen width (about 130 px tall on a 510x960 crop = 14% of height), date `Monday` / `29 February` in two lines in regular weight about 1/3 the clock height, left aligned with an 8% margin, about 8% above the nav buttons (measured by eye [S32 img 33]).
- Unlock: swipe up with the clock / photo sliding (the physical "hop" hint is the official animation example) [S16].
- Glance screen (Lumia only): black screen with time / date / notification peek; settings page described in 8.3 [S32 img 34].
- Notifications on lock: toggle in notifications+actions ("Show notifications in action center when my phone is locked") [S32 img 25]. 8.1 adds an open API so apps can change the lock screen theme / animation [S27][S30].

### 8.7 Cortana (8.1, beta)
- Launch: Search button (tap), long-press = listening; also a tile. Home screen: Cortana ring icon top-left, BETA label top-right (grey small caps), music-note (identify song) and hamburger (menu) icons top-right; greeting text in accent colour, large Light ("Hi Darrin! How can I help you?" with the ring centred in the marketing frame; in the device capture "Here's the latest in Business News." in dimmed accent); below, curated cards (news items with 177x177 thumbnails, headline 26-px, source / time grey); links `see more news`, `hide this news` in accent; bottom input: light grey #D2D2D2 text box "ask me anything" + #505050 mic square occupying the right 20% (measured) [S27][S31b][S32 img 49].
- Notebook menu: `CORTANA'S NOTEBOOK` uppercase small, then a list in large Light lowercase: interests, remind me, quiet hours, inner circle, places, music searches, settings (measured row pitch about 65 px at 0.9 scale) [S27].
- Dialog pattern: small ring (about 56 px at 432 scale) top-left, prompts in accent, then white underlined editable fields (dotted underline) with `remind` / `cancel` buttons (#333333-ish dark grey boxes). Typing allowed, results silent; the Cortana ring animates [S27][S30].
- Onboarding: `Cortana` title, long paragraph, two outlined buttons `not now, thanks` and `sure`, then interest pickers with checkboxes "1 of 4" and `skip` [S32 imgs 12, 47].

### 8.8 Keyboard (Word Flow)
- Layout (portrait): suggestion strip on top (3 candidates; bold first = current / best; emoji can be a suggestion item), 4 rows of dark keys (#474747, 1-2 px gaps on #1F1F1F): q-p; a-l; shift + z-m + backspace; `&123`, smiley (emoji), `,`, space, `.`, enter; below the keyboard an app-defined toolbar row (messaging: attach, mic, ...) and the app bar dots [S31c] (measured on a 395x450 crop: key rows about 56 px tall, letter keys about 36 px wide, pitch about 39.5 px; the text field shows white input with an underlined composing word).
- Shape Writing: trace a path over letters (new in WP8.1); candidates appear in the strip; emoji suggested after a word or swipe; autocorrect suggestions hidden above about 45 wpm; one-hand tap about 41 wpm, shape about 51, two-hand about 60 (reviewer's test) [S31c]. New caret: tap between words to place it [S42].
- The numbers / symbols layer: digit row on top (1-0), symbols in 3 rows [S32].
- Lower-case labels, square keys without corner radius (measured).

### 8.9 Volume panel, app switcher, navigation buttons
- Volume: pressing a hardware volume key shows an overlay at the top of the screen with a ringer on / off toggle and, if media plays, Previous / Next transport controls [S15]. In 8.1 volume has separate sliders (ringer + notifications vs media / apps) [S27][S43]. No pixel spec; appearance (unverified).
- App switcher: long-press Back opens a card carousel of running apps (WP8-style stacked app cards); 8.1 adds "swipe the card down to close" one at a time [S31a]; a small X button also exists at the top-right of the focused card [S44, grade C]. Visual spec not captured.
- Back / Start / Search: hardware or capacitive in WP8; in 8.1 may be on-screen with Search, Start, Back keys [S30][S31a]; an Update 1 render shows the on-screen bar glyph row `<-`, Windows flag, magnifier at the bottom, black bar about 72 px (measured); apps can hide them and users bring them back with an upward swipe (leak) [S45].
- Steering buttons stay on the same edge as the app bar [S12].

### 8.10 Phone dialer / in-call
- Dialer (Update 1 [S32 img 43]): number display at the top in large Light type with a circled backspace icon at right ("No SIM" label above in uppercase small), 3x4 keypad of #505050-like squares with 2-px black gaps; digit in about 34-px Light and small letters "ABC" at the lower-right of each key; bottom row: accent `call` button 2/3 width + `save` 1/3 width dark key with a disk icon.
- In-call (Skype-upgrade marketing frame [S27]): contact photo top about 65% of the screen, elapsed timer "00:32" in small accent at top-left, name large Light white, number small; below, a 3-column grid of #505050 buttons with white glyph and lowercase label (speaker, mute, add call / hold, Skype, bluetooth), last row an accent `end call` button spanning two columns and a keypad button; grid gaps 6 px at 0.9 scale.

### 8.11 People, Messaging, Photos, Calendar, Mail, Store patterns
- People hub [S27][S32]: giant lowercase `people` hub title, panorama sections: `what's new` feed cards with speech-bubble count badges (dark grey rectangle with tail, 2 / +), `CONTACTS` list sorted with an accent-outlined letter header (`a`), contact rows with a 38-px square avatar (grey placeholder) and name in 20-px; app bar: `+` and search circles and dots.
- Messaging thread [S32 img 17]: header `WINDOWS PHONE` uppercase small, speech bubbles (received = accent-filled rounded rectangle with tail, sent = grey), bottom text box and icons, app bar dots.
- Photos (`all albums favourites` pivot with a `May 2014` accent date header, 4-column square grid with about 6 px gaps) [S27]. Calendar week view: this week / next week pivot, 2-column day grid with temperature + weather glyph, events coloured by calendar, mini-month at bottom-right [S27]. Mail: pivot `all unread flagged urgent`, rows with accent subject line, grey preview, time; app bar `+ select sync search` icons.
- Store [S32]: `Store` big title with search pivot to the right, 2-column grid of app tiles with price / rating beneath each, vertical pivot dots.
- Alarms: `ALARMS` / `all` pivot, row with time, name and toggle switch at right, `+` in the app bar [S32 img 45].
- Data Sense [S27]: pivot `overview usage`, donut chart with two accents, outlined `set limit` button, footnote in grey, app bar with a single gear.

### 8.12 Status bar in 8.1
Icons left (signal bars, data type "LTE", do-not-disturb moon, notification glyph), battery + clock at right in 20-px Light; measured height about 70-80 px at 1080p (about 32 dp at 2.4) in a 1080p Start capture [S31a]; the pulled-down state adds the carrier ("Verizon Wireless"), battery %, and date [S31b][S11].

## 9. Gaps
Official durations and easing curves; official hex values of PhoneChrome / Subtle / Disabled in WP8.1; toggle-switch pixel geometry; a dialog / MessageBox screenshot; app switcher visuals; volume overlay visuals; the 8.1 banner / toast look; Hub / Pivot header exact font sizes (the Runtime pages only say "Page header 56 pt" / "Subheader 26.667" for the Windows 8.1 type ramp [S23], which is Windows, not Phone); WP8.1 letter-spacing; tile corner and press-tilt angle. The SDK ISO on archive.org (1.7 GB, [S35]) and the 940 MB 8.1 Update ISO [S34] would contain `ThemeResources.xaml` and icon assets and are the route to closing the colour gaps. The 1.1 MB `windowsphone81sdkupdate1.exe` is only a bootstrapper.

## Kit-ready constants

```json
{
  "meta": {"platform": "WindowsPhone8.1", "units": "px at WVGA 480x800 unless noted", "confidence": "see tags"},
  "accents": {
    "lime": "#A4C400", "green": "#60A917", "emerald": "#008A00", "teal": "#00ABA9",
    "cyan": "#1BA1E2", "cobalt": "#0050EF", "indigo": "#6A00FF", "violet": "#AA00FF",
    "pink": "#F472D0", "magenta": "#D80073", "crimson": "#A20025", "red": "#E51400",
    "orange": "#FA6800", "amber": "#F0A30A", "yellow": "#E3C800", "brown": "#825A2C",
    "olive": "#6D8764", "steel": "#647687", "mauve": "#76608A", "sienna": "#A0522D",
    "_source": "S4 official table image; default accent cyan",
    "_observed_8_1_cyan_in_marketing_frames": "#00BCF2"
  },
  "theme": {
    "dark": {"background": "#000000", "foreground": "#FFFFFF", "chrome": "#1F1F1F", "keyboardKey": "#474747", "inactiveHeader": "#808080"},
    "light": {"background": "#FFFFFF", "foreground": "#000000"},
    "_note": "dark values measured from screenshots, light values from a WP7 emulator dump; official ThemeResources.xaml hex not retrieved"
  },
  "fonts": {"normal": "Segoe WP", "light": "Segoe WP Light", "semilight": "Segoe WP Semilight", "semibold": "Segoe WP Semibold"},
  "fontSizes": {"small": 18.667, "normal": 20, "medium": 22.667, "mediumLarge": 25.333, "large": 32, "extraLarge": 42.667, "extraExtraLarge": 72, "huge": 186.667, "minimumPt": 15},
  "margins": {"phoneMargin": 12, "horizontal": [12, 0], "vertical": [0, 12], "touchOverhang": 12, "touchLargeOverhang": [12, 20], "borderThickness": 3, "strokeThickness": 3},
  "chrome": {"statusBarPortrait": 32, "statusBarLandscape": 72, "appBarHeight": 72, "appBarIcon": 48, "appBarGlyph": 26, "appBarMaxButtons": 4, "appBarMaxMenuItems": 5, "appBarOpacities": [0, 0.5, 1]},
  "touch": {"idealMm": 9, "minMm": 7, "minVisualMm": 4.2, "minSpacingMm": 2},
  "tiles100pct": {"small": [71, 71], "medium": [150, 150], "wide": [310, 150], "tiny": [44, 44], "scales": [100, 140, 240], "assetScale240": {"small": 170, "medium": 360, "wide": [744, 360]}},
  "tilesWp8": {"iconic": {"iconMax": [202, 202], "smallIconMax": [110, 110]}, "chars": {"mediumTitle": 19, "wideTitle": 39, "iconicWideLine": 33}},
  "startGrid1080pMeasured": {"screen": [1080, 1920], "margin": 31, "gap": 25.5, "small": 148, "medium": 322, "wide": 669, "firstTileTop": 117, "ratios": {"gapOverSmall": 0.17, "mediumEquals": "2*small+gap"}},
  "actionCenter": {"quickActionsPerRow": {"8.1GA": 4, "8.1Update1": 5}, "onFill": "accent", "offFill": "#1F1F1F", "handleBarFill": "accent*0.69", "measured1080p": {"tile": [257, 157], "gap": 17, "top": 189, "handleBarHeight": 56}},
  "toast": {"seconds": 10, "background": "accent", "lines": 2},
  "scrollIndicatorFadeSeconds": 1,
  "statusBarRevealSeconds": 8,
  "panorama": {"maxSections": 5, "bgImage": [[480, 800], [1024, 800]]},
  "pivot": {"maxPagesControlDoc": 4, "maxPagesAppTabDoc": 6, "headerWords": 2},
  "motion": {"easing": {"enter": "logarithmic", "exit": "exponential", "large": "scurve"}, "dimension": "2.5D", "durationsMs": null, "_note": "no official durations found"},
  "wordflow": {"tapOneHandWpm": 41, "shapeOneHandWpm": 51, "twoHandWpm": 60, "suggestionHiddenAboveWpm": 45, "_src": "S31c"}
}
```

## Source index
[S1]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202878(v=vs.105)
[S2]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/ff402557(v=vs.105)
[S3]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/ff769552(v=vs.105)
[S4]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202878(v=vs.105) (accent colour table image on the theme page)
[S5]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/jj662929(v=vs.105)
[S6]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/jj662924(v=vs.105)
[S7]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/jj662925(v=vs.105)
[S8]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/jj662923(v=vs.105)
[S9]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/jj662926(v=vs.105)
[S10]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh781198(v=win.10)
[S11]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202884(v=vs.105)
[S12]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/ff431813(v=vs.105)
[S13]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202889(v=vs.105)
[S14]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202911(v=vs.105)
[S15]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202905(v=vs.105)
[S16]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202871(v=vs.105)
[S17]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/jj662927(v=vs.105)
[S18]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202912(v=vs.105)
[S19]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202919(v=vs.105)
[S20]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh202890(v=vs.105)
[S23]: https://learn.microsoft.com/en-us/previous-versions/windows/apps/dn518235(v=win.10)
[S24]: https://learn.microsoft.com/en-us/archive/blogs/thunbrynt/windows-phone-8-1-for-developerstheme-resources
[S25]: https://learn.microsoft.com/en-us/archive/blogs/thunbrynt/windows-phone-8-1-for-developerstype-and-text-handling
[S26]: https://blogs.windows.com/windowsexperience/2013/02/13/8-hidden-windows-phone-8-settings-youll-actually-use/
[S27]: http://blogs.windows.com/windowsexperience/2014/04/02/cortana-yes-and-many-many-other-great-features-coming-in-windows-phone-8-1/
[S28]: https://blogs.windows.com/devices/2014/04/29/deep-dive-windows-phone-8-1-start-screen-backgrounds/
[S29]: https://newatlas.com/tips-getting-started-windows-phone-81/31828/
[S30]: https://www.gsmarena.com/windows_phone_81_is_official_here_are_the_new_features-news-8198.php
[S31a]: https://www.anandtech.com/show/7940/windows-phone-81-review (archive: https://web.archive.org/web/20201126232122/https://www.anandtech.com/show/7940/windows-phone-81-review)
[S31b]: https://www.anandtech.com/show/7940/windows-phone-81-review/2 (archive: https://web.archive.org/web/20220124034858/https://www.anandtech.com/show/7940/windows-phone-81-review/2)
[S31c]: https://www.anandtech.com/show/7940/windows-phone-81-review/3 (archive: https://web.archive.org/web/20201028183004/https://www.anandtech.com/show/7940/windows-phone-81-review/3)
[S32]: https://www.neowin.net/news/in-pictures-comparing-windows-phone-81-and-windows-10-mobile-side-by-side/ (archive: https://web.archive.org/web/20201108132118/https://www.neowin.net/news/in-pictures-comparing-windows-phone-81-and-windows-10-mobile-side-by-side/)
[S33]: https://en.wikipedia.org/wiki/Windows_Phone
[S34]: https://www.microsoft.com/en-in/download/details.aspx?id=43719
[S35]: https://archive.org/details/wpsdk8
[S36]: Wikimedia Commons, "Windows Phone 8.1 Update 2 Einstellungen" and "Benachrichtigungszentrale" (search commons.wikimedia.org)
[S37]: https://nicksnettravels.builttoroam.com/?p=461
[S38]: https://learn.microsoft.com/en-us/archive/blogs/the_pythic_coder/getting-started-hubs-vs-pivots
[S39]: https://learn.microsoft.com/en-us/uwp/API/windows.ui.xaml.media.animation.navigationtransitioninfo?view=winrt-22621
[S40]: https://www.techradar.com/reviews/phones/windows-phone-8-1-1239375/review (archive: https://web.archive.org/web/20201205090313/https://www.techradar.com/reviews/phones/windows-phone-8-1-1239375/review)
[S41]: https://www.windowscentral.com/notification-center-windows-phone-81-reveal
[S42]: https://windowscentral.com/new-word-flow-keyboard-caret-windows-phone-81
[S43]: https://www.theverge.com/2014/2/11/5400660/windows-phone-8-1-features-leaked (archive: https://web.archive.org/web/20210203220048/https://www.theverge.com/2014/2/11/5400660/windows-phone-8-1-features-leaked)
[S44]: https://www.expertreviews.co.uk/node/1400643
[S45]: https://www.theverge.com/2014/2/11/5400660/windows-phone-8-1-features-leaked
[S46]: https://msdn.microsoft.com/library/hh452701(v=win.10)
