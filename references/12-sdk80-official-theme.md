# 12 - Official WP8 SDK theme values (from wpsdkv80_enu1.iso)

Source: `packages/MobileTools/wpsdkcore/WPSDK_en.cab` -> `WPDT_DESIGN_{DARK,LIGHT}_THEMERESOURCES_XAML` and `..._SYSTEM_WINDOWS_XAML` (full control templates, e.g. ToggleSwitch, Slider, Pivot). Copies: `references/sdk8-xaml/` (Microsoft copyright, local reference only, do not redistribute). The ISO is the **Windows Phone SDK 8.0** (not 8.1) but 8.1 kept these resources. It also holds Segoe WP fonts (`FONTS_SEGOEWP_*_TTF` in the same cab) for local testing only.

## Unit conversion
WP8 XAML units are WVGA px (480 wide). Our reference is 360 pt wide, so **pt = xaml x 0.75** (measured phone references also scale this way: body 20 -> 15, value 25.333 -> 19).

| Resource | XAML | pt (x0.75) | measured pages |
|---|---|---|---|
| PhoneFontSizeSmall | 18.667 | 14 | 13-14 |
| PhoneFontSizeNormal | 20 | 15 | 15 |
| PhoneFontSizeMedium | 22.667 | 17 | 17 |
| PhoneFontSizeMediumLarge | 25.333 | 19 | 19 (about value) |
| PhoneFontSizeLarge | 32 | 24 | 24 (menu/name) |
| PhoneFontSizeExtraLarge | 42.667 | 32 | 30-34 |
| PhoneFontSizeExtraExtraLarge (title1) | 72 | 54 | **48** (measured pages smaller) |
| PivotHeaderFontSize | 72 | 54 | 48 |
| PivotTitleFontSize | 22.667 | 17 | 11.5 caps (differs) |
| PanoramaItemHeaderFontSize | 66 | 49.5 | - |
| LongListSelectorGroupHeader | 29.333 | 22 | 22/27 |
| LetterTile font | 42.667 | 32 | 27 |
| JumpListString / Alphabet | 26.667 / 48 | 20 / 36 | - |
| EmptyListHeader | 32 | 24 | - |
| PivotItemMargin | 12,28,12,0 | 9,21,9,0 | - |
| PhoneMargin / HorizontalMargin | 12 | 9 | 16 (page margin 24 px -> 18 pt on a real phone) |
| PhoneBorderThickness / StrokeThickness | 3 | 2.25 | 2 |
| TouchTargetOverhang | 12 | 9 | - |
| TextBoxInnerMargin | 1,2 | - | - |
Where measured pages and the SDK disagree, the measured pages win for matching `evals/specs/`; SDK wins when the aim is a faithful WP8.1 phone.

## Dark theme colours (ARGB)
Foreground #FFFFFF; Background #000000; Chrome (app bar, dialogs) **#1F1F1F**; Subtle / MidContrast #99FFFFFF (=#999 on black); LowContrast #73FFFFFF; Disabled #66FFFFFF; Inactive #33FFFFFF; InverseInactive #CCCCCC; ProgressBarBackground #19FFFFFF; TextBox (idle fill) #BFFFFFFF (=#BFBFBF on black; measured pages #C7C7C7); TextBox edit background #FFFFFF with accent border; TextBox read-only #77000000; Semitransparent #AA000000; Border #BFFFFFFF; PivotUnselectedItemOpacity **0.4**; RadioCheckBox: transparent fill, white border, pressed = accent.
Light theme: see `sdk8-xaml/wpdt_design_light_themeresources_xaml.xaml` (fg #000, bg #FFF).

## Fonts
Segoe WP (Regular), Segoe WP Light, Segoe WP SemiLight, Segoe WP Semibold, Segoe WP Bold, Segoe WP Black. Text style defaults: PhoneTextBlockBase = Segoe WP 20 px; Title1 72 Light; Title2 32 SemiLight; Title3 22.667; GroupHeader 32 Light; Subtle = #99FFFFFF.

## Where to look for control geometry
`sdk8-xaml/wpdt_design_dark_system_windows_xaml.xaml` (55 KB): templates for Button, CheckBox, RadioButton, ToggleSwitch, Slider, ProgressBar, TextBox, ListPicker, ContextMenu, Pivot, Panorama. Grep by `x:Key` or `TargetType`.
