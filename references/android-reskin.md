# Reskinning an Android 7.x ROM in place (research notes)

Target: a LineageOS 14.1 / Android 7.1.2 device (example codename given as `<device>`), restyled toward a Metro-like look without rebuilding the ROM from source where possible.

Sources: LineageOS `cm-14.1` at HEAD (frameworks/base `eb7d3a89`, Settings `5f4a7353`) and AOSP `nougat-mr1-release`. A ROM built earlier than HEAD may differ slightly in line numbers.

Shorthand: FB = `https://github.com/LineageOS/android_frameworks_base/blob/cm-14.1`, SET = `https://github.com/LineageOS/android_packages_apps_Settings/blob/cm-14.1`, PMS = `FB/services/core/java/com/android/server/pm/PackageManagerService.java`.

## Scope and honesty

- This was researched from source reading. It has not been verified on a device except where a statement says so.
- Claims marked **UNVERIFIED** come from memory or inference and need a device test.
- A Metro look needs both resource changes (colors, dimens, styles, layouts, fonts, sounds, boot animation) and, for 3D turnstile or continuum transitions, code patches. Resources alone cannot produce those transitions (section 6).
- Tools assumed: apktool, `aapt` / `aapt2` from Android build-tools, `apksigner`, `zipalign`, `adb`, Magisk.

## 0. TL;DR

1. The framework-level look (Theme.DeviceDefault, switch, seekbar, dialog, animations) lives in `framework-res.apk`. Android 7.1 does not obviously support runtime resource overlays (RRO) for the `android` package. The PMS code skips it, and no caller of `idmap --scan` was found (F4).
2. SystemUI and Settings overlays through `/vendor/overlay` are supported by PMS (F1-F3). They are non-invasive, with no signature problem and no sharedUserId problem. This is the safest first lever.
3. Modified system APKs can be injected without the platform private key (F8-F9). On N, system-dir APKs get only their `AndroidManifest.xml` verified. Keep the original `META-INF/` and the byte-identical manifest, and swap `resources.arsc`, `res/` and `classes.dex`. If the ROM is signed with a private (non-public) platform key, re-signing is impossible and this is the only route for framework-res, Settings and SystemUI edits.
4. Biggest unknowns, answered by a device probe: whether `/vendor` is a symlink to `/system/vendor`, whether `/data` is FDE-encrypted (affects recovery and Magisk timing), and whether `/data/resource-cache/overlays.list` is ever created.

## 1. Findings from source reading

| # | Finding | Source |
|---|---------|--------|
| F1 | PMS scans `/vendor/overlay` (and `/vendor/overlay/<ro.boot.vendor.overlay.theme>`) before any app, with `PARSE_TRUSTED_OVERLAY`. `/system/vendor/overlay` is NOT scanned by name. It works only if `/vendor` resolves to `/system/vendor`. | PMS #L2386-L2399 |
| F2 | Overlay trust = directory location only. `createIdmapForPackagePairLI` refuses only if `!opkg.mTrustedOverlay`. No signature check. | PMS #L6773-L6778 |
| F3 | The only overlay manifest attributes are `<overlay android:targetPackage android:priority>`, priority 0..9999. There is no `isStatic` and no OMS in 7.1, so every overlay is static and boot-time. Priority order is `mOverlayPriority` ascending, and the last wins. | FB/core/java/android/content/pm/PackageParser.java#L1807-L1827 ; PMS #L6795-L6808 |
| F4 | PMS excludes target `"android"` from its idmap path ("handled by native layers"). Native `AssetManager` reads `/data/resource-cache/overlays.list` (`addSystemOverlays`). No caller of `idmap --scan` was found in nougat-mr1 `ZygoteInit.java`, `Resources.java`, `app_main.cpp`, `AndroidRuntime.cpp`, `init.rc` or installd. A Lineage commit message says the scan "is executed as a part of the pre-loading in ZygoteInit", but that code is absent in N. Conclusion: framework-res RRO is probably dormant on N. UNVERIFIED (code search was rate-limited; only 6 files checked). | PMS #L9174-L9177 ; FB/libs/androidfw/AssetManager.cpp#L636-L664,L776-L820 ; FB commit `0fbb6081` |
| F5 | The idmap maps target resource to overlay resource BY (type, name), for every resource type, including file-based ones (layout, drawable, anim, xml). Only names present in both are mapped. The overlay must have a single package group. All entries of one type must land on one overlay type id. The idmap stores the CRC of both `resources.arsc` files and is regenerated when stale. | FB/libs/androidfw/ResourceTypes.cpp#L6619-L6725 ; FB/cmds/idmap/create.cpp#L75-L131 |
| F6 | Runtime lookup translates only the requested target entry id into the overlay entry (`getEntry`). Reference VALUES inside overlay resources are not remapped. A reference from an overlay value to an overlay-only resource therefore resolves wrongly or fails. Inferred from reading the code, needs a test. | ResourceTypes.cpp#L6019-L6035 |
| F7 | Config selection is across target and overlay entries. An overlay entry wins only if its config is better than the target's best match, or exactly equal (`currentTypeIsOverlay && compare==0`). The overlay must provide the same qualifier folders (`-xxhdpi-v4`, `-v21`, `-land`) as the target for each replaced name. | ResourceTypes.cpp#L6093-L6104 |
| F8 | System-dir APKs on N: with v1 (JAR) signing only, PMS verifies only the `AndroidManifest.xml` entry digest and extracts the certs. Other entries are not integrity-checked, and rollback protection is ignored. A typical Lineage-based ROM Settings APK is v1-signed only (no APK Signing Block). Check whether the signing cert is the public AOSP/Lineage test platform key. If it is a private key, it is unavailable and re-signing is impossible. | FB/core/java/android/content/pm/PackageParser.java#L1206-L1330 |
| F9 | A system package whose cert changes is accepted ("signature changed; retaining data"), unless it has a sharedUser whose recorded certs differ. Then scanning throws `INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES` and the package is not installed. Settings is `android.uid.system` + `coreApp`. SystemUI is `android.uid.systemui` + `coreApp` + platform cert. framework-res (`android`) is `android.uid.system` + `coreApp`. A re-signed Settings or SystemUI would vanish. | PMS #L7317-L7360,#L8505-L8560 ; FB/packages/SystemUI/AndroidManifest.xml#L21-L23 ; FB/core/res/AndroidManifest.xml |
| F10 | Some Lineage 14.1 device trees have no vendor image (BoardConfig lists system/boot/recovery/persist/userdata/cache only), so `/vendor` may not exist as a partition. Check the device's `BoardConfig.mk`, `fstab` and `device.mk` (the latter carries `DEVICE_PACKAGE_OVERLAYS`). | the device tree's `cm-14.1` branch |
| F11 | Magisk module `system/` is merged into the real `/system`. Files for `/vendor` go under `system/vendor`, and Magisk handles separate-partition vs not. A `.replace` file replaces a folder. `disable`, `remove` and `skip_mount` marker files exist. Safe mode (volume-down at the right moment) disables modules. `magisk --remove-modules` works over adb. Minimum Magisk Android is 6.0. | Magisk `docs/guides.md`, `docs/faq.md`, `docs/changes.md` |
| F12 | Fonts: `Typeface.java` reads `/system/etc/fonts.xml`. The default family is `sans-serif` (Roboto, weights 100-900). Aliases exist, e.g. `tahoma`, `verdana`. Selawik (Segoe UI metric-compatible) is SIL OFL-1.1 (github.com/microsoft/Selawik). | FB/graphics/java/android/graphics/Typeface.java#L76,L329,L407 ; FB/data/fonts/fonts.xml |
| F13 | Boot animation search order: `/oem/media/bootanimation.zip`, then `/system/media/bootanimation.zip`, plus an encrypted variant. `desc.txt` format is `W H FPS` then `p|c loops pause folder [color]`. UI sound effects load from `/system/media/audio/ui/` per `xml/audio_assets` (framework-res). Lock/unlock/low-battery sound paths are defaults in SettingsProvider `defaults.xml`. | FB/cmds/bootanimation/BootAnimation.cpp#L65-L67,L325-L329 ; FB/services/core/java/com/android/server/audio/AudioService.java#L283,L2632-L2670 ; FB/packages/SettingsProvider/res/values/defaults.xml#L72-L83 |
| F14 | Framework timing config: `config_shortAnimTime=200`, `config_mediumAnimTime=400`, `config_longAnimTime=500`, `config_activityShortDur=150`, `config_activityDefaultDur=220`. | FB/core/res/res/values/config.xml#L121-L131 |
| F15 | There is no CM Theme Engine hook in PMS (no theme grep hits), so the old CM themes route is unavailable. UNVERIFIED beyond PMS. | PMS grep |
| F16 | Lineage 14.1 base is AOSP `android-7.1.2_r36`. Blobs come from a community vendor repo branch `cm-14.1` for the device's vendor, and the kernel from the device's `cm-14.1` kernel repo. | `LineageOS/android` `default.xml` ; Lineage wiki device data |
| F17 | Settings themes extend framework themes: `Theme.SettingsBase` -> `@android:style/Theme.DeviceDefault.Settings`. Alert dialogs extend `Theme.DeviceDefault.Settings.Dialog.Alert`. Dashboard tile text uses `TextAppearance.TileTitle`. A decoded Settings APK has a `public.xml` (thousands of ids) which can pin overlay ids. | SET/res/values/themes.xml |
| F18 | When decoding Settings with apktool, keep `AndroidManifest.xml` and `apktool.yml` along with `res/` and `smali/`, or the tree is not rebuildable. Settings typically has a single `classes.dex` (a few MB) and a large stored `resources.arsc` (tens of MB). Android build-tools 33.x (aapt, aapt2, apksigner, zipalign, d8) and apktool 3.x were used for planning. | local inspection |

The ROM builder can be identified from the ROM's own `ro.build.host`, `ro.build.user` and `ro.build.fingerprint`. Private self-generated platform keys are common in community builds.

## 2. Topic notes (A to F)

### A. Static RRO on 7.1

- Location: `/vendor/overlay/*.apk`. Manifest: `<manifest package="x.overlay.settings"><overlay android:targetPackage="com.android.settings" android:priority="10"/><application android:hasCode="false"/></manifest>`. Only the `<overlay>` tag is parsed by PackageParser (F3).
- Overlayable types: all types by name (F5), including layout, drawable, anim, animator, color, dimen, bool, integer, array, style, string, xml and raw (file-based entries are just path strings). Limits:
  - (a) no new names are reachable (F5);
  - (b) overlay values cannot reference overlay-only resources (F6): use inline literals, or reference `@android:` and target names;
  - (c) match the target's qualifier folders (F7);
  - (d) ids in overlay layouts must equal the target's, so pin them with a generated `public.xml` copied from the target. This is a recipe to be tested, UNVERIFIED;
  - (e) `<style parent=>` replacement is plausible, because the whole bag is replaced. UNVERIFIED;
  - (f) a framework target is probably dormant (F4).
- Compiler: use `aapt` v1 from build-tools (what apktool calls with `--use-aapt1`, or call it directly). Command shape: `aapt package -f -M AndroidManifest.xml -S res -I android.jar -I framework-res.apk --min-sdk-version 25 --target-sdk-version 25 -F out.apk`. For references to private framework attrs, add the device's `framework-res.apk` via `-I`. `aapt2` also works with `--min-sdk-version 25`, but verify that the output has no sparse or compact entries (UNVERIFIED). Do not use flags that alter ids (`-x`, `--auto-add-overlay`).
- Signing: not required for validity (F2), but an unsigned APK is rejected at parse (no certs). Sign with any key via `apksigner sign --v1-signing-enabled true --v2-signing-enabled false`.
- Magisk shipping: module path `system/vendor/overlay/<name>.apk`. If the device has no `/vendor` symlink (UNVERIFIED), put the module at `system/vendor/overlay` and also verify `/proc/mounts`. Magisk adds new dirs and files into the real tree (F11). Mounting happens at post-fs-data, before the zygote, so PMS sees it.
- Hot test: a reboot is not strictly needed. Magisk mounts are bind mounts, so overwriting the module file in place keeps the same inode, then `su -c 'stop; start'` restarts the framework. A new inode needs a reboot. UNVERIFIED. With FDE, Magisk only mounts after the PIN is entered. Check `ro.crypto.state`.
- Framework RRO experiment (reversible, small): a Magisk `post-fs-data.sh` that runs `/system/bin/idmap --scan android /system/framework/framework-res.apk /data/resource-cache /vendor/overlay` (usage in FB/cmds/idmap/idmap.cpp), then `restorecon -R /data/resource-cache`. It would reproduce the missing zygote step. Success is shown by logcat "Overlay added: targetPath=..." (AssetManager.cpp#L286) and a visible change. UNVERIFIED.

### B. Rebuild and replace system APKs

- Keep the original APK zip. Replace only `resources.arsc`, `res/**`, `classes.dex` (and, if needed, `lib/`, `assets/`). Keep `META-INF/*` and `AndroidManifest.xml` byte-identical (F8). Any manifest edit (new activity, permission, `android:theme`) breaks it. Manifest changes would need the platform key, which is impossible for a private-key ROM.
- Resource-id stability: the manifest and compiled dex reference ids. Rebuild the arsc with apktool using the decoded `public.xml`, then diff `aapt dump resources` of old and new for identical ids. framework-res also has private ids baked into framework.jar's `R`, so any id drift is fatal. For framework-res, prefer editing resource values and files without adding or removing resources.
- Install: Magisk module `system/priv-app/Settings/Settings.apk` replaces the file. The `oat/arm/*.odex` stays in place. If `classes.dex` is unchanged, the odex remains valid. If it changed, ART falls back to a /data dexopt, with a slower first boot. UNVERIFIED (check whether the system is dexpreopted).
- Scanning: PMS compares the file mtime and re-parses. Cert checks pass as in F8-F9.
- Survives dexopt: yes, because dexopt writes to `/data/dalvik-cache` and never mutates the APK.
- What breaks if you re-sign: F9. Settings and SystemUI disappear (black or empty UI). The module can be disabled to recover.
- smali edits: decode with apktool, edit smali, rebuild `classes.dex` only, and inject it (apktool's full rebuild output is not used for the manifest or signature).

### C. Source build

- Base: `repo init -u https://github.com/LineageOS/android.git -b cm-14.1`, then `breakfast <device>` (F16). The device tree pulls kernel, SoC common repos and other dependencies. Blobs come from the community vendor repo.
- Requirements (UNVERIFIED estimates): Ubuntu 16.04 (a container is fine), OpenJDK 8, 16+ GB RAM, 8+ cores, 250-300 GB SSD. Sync takes 1-2 h, the first build 2-4 h on 16 vCPU, about $1-3 per build on a rented VM.
- Key point: a new build signed with new platform keys cannot be dirty-flashed over the current /data (F9, shared users). Plan a wipe or backup/restore. Source-level changes: edit `frameworks/base/core/res`, `packages/SystemUI`, `packages/apps/Settings`, device overlays, `services` for AppTransition, etc.
- Compared to A/B: the highest payoff, with no id or manifest constraints, but the highest effort and a wipe.

### D. Xposed / runtime hooks

- Official Xposed for SDK 25 exists as `xposed-v88.x-sdk25-<arch>`. A v89 SDK 25 Magisk module was NOT confirmed. UNVERIFIED.
- EdXposed and LSPosed need Android 8.1 or higher, so they are not options on N. Xposed on N replaces `app_process`, ART and framework jars, which is a higher risk of bootloop than resources.
- Use only for behaviour that resources cannot change, preferably after the smali route is tried.

### E. Quick wins (no code)

| Item | How |
|------|-----|
| Font | Magisk `system/fonts/Selawik-*.ttf` plus replacement `system/etc/fonts.xml` (family `sans-serif`, weights 300/400/600/700). F12. Fonts are cached per process, so reboot. A bad font file can bootloop (Safe Mode recovers). |
| Boot animation | `system/media/bootanimation.zip` (stored zip, no compression; half-resolution is fine). F13. |
| Sounds | Replace files in `system/media/audio/ui/` (Lock, Unlock, Effect_Tick, KeypressStandard, etc.), notifications, ringtones, alarms. Paths in F13. Keep the filenames. |
| Animation timing | SystemUI/Settings configs via RRO. Framework `config_*AnimTime` needs the framework route (F4/B). Global scales via `settings put global window_animation_scale 1.0` etc. (device side). |
| Density / DPI | `wm density N` is reversible (`wm density reset`). Persisted by `ro.sf.lcd_density` (build.prop, via resetprop). |
| Nav bar / QS | SystemUI `quick_settings_num_columns` (3), `quick_settings_num_rows`, `quick_settings_tiles_default` (`wifi,cell,battery,dnd,flashlight,rotation,bt,airplane`), `config_maxNotificationIcons`. |
| Accent colors | Framework `colorAccent`, `colorPrimary` need framework-res. Settings/SystemUI-level colors via RRO. |
| Wallpaper | User choice, or a `config_defaultWallpaper`-type drawable in framework-res (UNVERIFIED name). |

### F. Recovery / rollback

Back up first (run these yourself on the device):
- Pull boot (the Magisk-patched and the stock images), recovery, `persist`, and the modem calibration partitions (`modemst1`, `modemst2`, `fsg` on Qualcomm devices; these hold IMEI and calibration data). Example, from `su`: `dd if=/dev/block/bootdevice/by-name/persist of=/sdcard/persist.img`. List partitions with `ls -l /dev/block/bootdevice/by-name`.
- Full `system` image: `dd if=/dev/block/bootdevice/by-name/system of=/sdcard/system.img`. Optional because the changes are systemless, but it gives full restore.
- A custom-recovery (TWRP or Lineage recovery) backup of system, data and boot.
- Keep a copy of the stock `Settings.apk`, `SystemUI.apk` and `framework-res.apk` pulled from the device.

Rollback ladder (try in order):

1. Boot loop or black screen: hold volume-down early in boot for Magisk Safe Mode (disables all modules, F11). Timing is device-specific. This needs no PIN and no /data access.
2. If adb is up: `adb shell magisk --remove-modules` (reboots), or `adb shell su -c 'touch /data/adb/modules/<id>/disable'` then reboot.
3. Recovery: `fastboot boot <recovery.img>`, then `adb shell`. If `/data` is FDE with a PIN, Lineage recovery may not mount it (UNVERIFIED). TWRP can decrypt with the PIN on supported devices. Then `touch /data/adb/modules/<id>/disable` or `rm -rf /data/adb/modules/<id>`.
4. Overlay-only breakage: delete `/data/adb/modules/<id>/system/vendor/overlay/*.apk`. If PMS has recorded a bad overlay in `packages.xml` it self-heals on the next scan.
5. Last resort: flash the stock `system` image and `boot` with fastboot or recovery, or wipe `/data`.

Boot-loop detection: `adb wait-for-device; adb shell getprop sys.boot_completed` stays empty or 0; `getprop init.svc.zygote` flips between running and restarting; `adb logcat -b all -d | grep -i -E "FATAL|AndroidRuntime|PackageManager|idmap"`.

Before touching anything: install a trivial module with a `disable`-friendly layout, and save the stock APK copies.

## 3. Approach ranking

| Approach | Feasibility | Payoff | Risk | Effort | Reversible |
|----------|-------------|--------|------|--------|------------|
| E quick wins (font, bootanim, sounds, density) | High | Medium | Low | Low | Yes, remove module |
| A1 RRO for SystemUI + Settings (`/vendor/overlay`) | High (F1-F3) | Medium-High (colors, dims, styles, layouts with same ids) | Low | Medium | Yes |
| A2 framework RRO via manual `idmap --scan` | Unknown | High if it works | Low | Low to test | Yes |
| B1 inject rebuilt framework-res arsc (original META-INF) | Medium (id stability) | High (global theme, anims) | Medium-High: a bad arsc can bootloop before UI | Medium-High | Yes, Safe Mode |
| B2 smali patch of SystemUI/Settings (dex only) | Medium | High (behaviour) | Medium | High | Yes |
| D Xposed | Low-Medium | Medium | High | Medium | Mostly |
| C Source build | High but heavy | Highest | Medium, wipe required | Highest | Via backup |

## 4. Recommended phased plan

| Phase | Work | Acceptance | Rollback |
|-------|------|------------|----------|
| 0 | Backup and probe: run a read-only device probe (see section 9) and save stock APK copies. | Every probe section produces output, backups exist. | Not needed. |
| 1 | Quick-win Magisk module (font + boot animation + one sound). | New font in Settings; new boot animation on next reboot. | Safe Mode or `disable`. |
| 2 | Pipeline proof with a SystemUI RRO: change one color and `quick_settings_num_columns` to 4, placed in `system/vendor/overlay`. | Logcat shows the overlay added, QS grid has 4 columns, `dumpsys package com.android.systemui` shows `resourceDirs`. | Delete the module. |
| 3 | Settings RRO: `Theme.Settings`, text appearances, dashboard layouts and preference layouts, with pinned ids and mirrored qualifier folders. | Settings opens, scrolls and toggles, and shows the new style. | Delete the module. |
| 4 | Framework: first test A2 (`idmap --scan`). If dormant, use B1 with a minimal change (colors and one anim), checking id diffs. | Boot completes and switch/dialog/seekbar change. | Safe Mode. |
| 5 | SystemUI structure: layouts that keep ids and classes; then smali patches for notification-shade behaviour. | Per widget. | Disable module. |
| 6 | Xposed (optional) or a source build when the resource and smali route is exhausted. | Per feature. | Backup / restore. |

## 5. Resource names that matter

### Framework (framework-res)

- Themes: `Theme.Material`, `Theme.Material.Light`, `Theme.DeviceDefault`, `Theme.DeviceDefault.Light`, `Theme.DeviceDefault.Settings`, `Theme.DeviceDefault.Settings.Dialog.Alert`, `Theme.DeviceDefault.Dialog`, `Theme.DeviceDefault.Dialog.Alert`, `Theme.DeviceDefault.Light.Dialog.Alert`, `Theme.DeviceDefault.DialogWhenLarge`, `Theme.Material.Settings`, `Theme.Material.Dialog.Alert`.
- Widget styles: `Widget.Material.CompoundButton.Switch` (items: `track=@drawable/switch_track_material`, `thumb=@drawable/switch_thumb_material_anim`, `switchTextAppearance`, `textOn`, `textOff`, `showText`), `Widget.DeviceDefault.CompoundButton.Switch`, `Widget.Material.CompoundButton.CheckBox`, `.RadioButton`, `Widget.Material.SeekBar` (`progressDrawable=@drawable/seekbar_track_material`, `thumb=@drawable/seekbar_thumb_material_anim`, `splitTrack`), `Widget.Material.ProgressBar*`, `Widget.Material.Button*` (`textAllCaps`), `Widget.Material.EditText`, `Widget.Material.ActionBar*`, `Widget.Material.ListView`, `AlertDialog.Material`, `Widget.Material.ButtonBar.AlertDialog`.
- Drawables: `switch_track_material`, `switch_thumb_material_anim`, `seekbar_track_material`, `seekbar_thumb_material_anim`, `btn_check_material_anim`, `btn_radio_material_anim`, `btn_checkbox_checked_mtrl`, `btn_checkbox_unchecked_mtrl`, `btn_default_material`, `dialog_background_material`, `popup_background_material`, `list_divider_material`, `item_background_material`, `edit_text_material`, `control_background_32dp_material`, `control_background_40dp_material`, `progress_horizontal_material`, `progress_indeterminate_*_material`, `ic_ab_back_material`, `spinner_background_material`, `ratingbar_*_material`, `number_picker_divider_material`.
- Layouts: `alert_dialog_material`, `alert_dialog_title_material`, `alert_dialog_button_bar_material`, `select_dialog_*_material`, `date_picker_material`, `time_picker_material`, `preference_material`, `preference_category_material`, `preference_list_content_material`, `preference_widget_switch`, `notification_template_material_base`, `notification_material_action*`, `global_actions_item` (power menu), `transient_notification` (toast), `screen_simple`, `action_bar_title_item`.
- Activity/window anims (style `Animation.Activity`; `Animation.Material.Activity` is the theme default): `activityOpenEnterAnimation=@anim/activity_open_enter`, `activityOpenExitAnimation=@anim/activity_open_exit`, `activityCloseEnterAnimation=@anim/activity_close_enter`, `activityCloseExitAnimation=@anim/activity_close_exit`, `taskOpenEnter/Exit` (`task_open_enter/exit`), `taskCloseEnter/Exit`, `taskToFront*`, `taskToBack*`, `wallpaper*`, `launchTaskBehindTarget/Source`, `fragmentOpenEnter/ExitAnimation` etc. (`@animator/fragment_*`). Others: `Animation.Dialog` (`dialog_enter/exit`), `Animation.Material.Dialog` and `.Popup` (`popup_enter_material/exit`), `Animation.Toast`, `Animation.InputMethod`, `Animation.LockScreen`, `Animation.OptionsPanel`, `Animation.Translucent`, plus `recent_enter/exit`, `app_starting_exit`, `screen_rotate_*`.
- Config: `config_shortAnimTime` 200, `config_mediumAnimTime` 400, `config_longAnimTime` 500, `config_activityShortDur` 150, `config_activityDefaultDur` 220, `config_longPressOnPowerBehavior`, `config_globalActionsKeyTimeout`. Fonts: styles use `@string/font_family_*_material` (body_1, title, headline, etc.); `fonts.xml` is a file (section 2E).
- Colors: `colors_material.xml` (`accent_material_dark/light`, `primary_material_*`, `background_material_*`), `colors.xml` (`system_error`, etc.). Theme attrs: `colorAccent`, `colorPrimary`, `colorPrimaryDark`, `colorControlActivated`, `colorControlNormal`, `colorBackground`, `textColorPrimary`, `windowBackground`.

### Settings (LineageOS 14.1, package `com.android.settings`)

- Themes: `Theme.SettingsBase`, `Theme.Settings`, `Theme.SubSettings`, `Theme.ActionBar`, `Theme.ActionBar.SubSettings`, `ThemeOverlay.SwitchBar.Settings`, `ThemeOverlay.SwitchBar.SubSettings`, `Theme.DialogWhenLarge`, `Theme.AlertDialog`, `Theme.SubSettingsDialogWhenLarge`, `PreferenceTheme`, `Theme.CryptKeeper`, `FallbackHome`. Ids come from the build's own `public.xml`, so read them from your decoded APK.
- Layouts (about 400 in the decoded APK): `dashboard`, `dashboard_category`, `dashboard_tile`, `dashboard_container`, `dashboard_container_header`, `dashboard_spacer`, `preference`, `preference_material_settings`, `preference_material`, `preference_category`, `preference_category_material`, `preference_icon`, `preference_widget_switch`, `preference_widget_switch_compat`, `preference_widget_checkbox`, `preference_widget_radiobutton`, `preference_widget_settings`, `preference_dialog_seekbar_material`, `preference_volume_slider`, `preference_dropdown_material`, `preference_list_fragment`, `preference_recyclerview`, `horizontal_preference`, `headerless_preference_category`, `preference_progress_category`. Dashboard tile ids: `@+id/dashboard_tile`, `@android:id/icon`, `title`, `summary`, with dims `dashboard_tile_minimum_height`, `dashboard_tile_image_size`, `dashboard_tile_image_margin_start/end`, drawable `selectable_card`.
- Drawables: `abc_switch_thumb_material`, `abc_switch_track_mtrl_alpha`, `abc_btn_switch_to_on_mtrl_*`, `preference_list_divider_material`, `switchbar_background`, `notification_tile_bg`, `tile_icon_*`. Colors: `abc_tint_switch_thumb`, `abc_tint_switch_track`, `abc_tint_seek_thumb`, `switch_thumb_material_dark/light`. Anims: `suw_slide_*`, `confirm_credential_*`, `fab_elevation`.
- Dashboard categories XML: `xml/dashboard_categories` (UNVERIFIED name); preference screens are in `res/xml` (over a hundred files).

### SystemUI (`com.android.systemui`)

- Layouts: `status_bar`, `status_bar_expanded` (the notification shade), `super_status_bar`, `status_bar_notification_row`, `status_bar_no_notifications`, `status_bar_notification_dismiss_all`, `signal_cluster_view`, `system_icons`, `keyguard_status_bar`, `keyguard_bottom_area`, `qs_panel`, `qs_tile_layout`, `qs_paged_tile_layout`, `qs_paged_page`, `qs_tile_label`, `qs_detail*`, `qs_customize_*`, `quick_status_bar_expanded_header`, `quick_settings_footer`, `quick_settings_brightness_dialog`, `recents`, `recents_task_view`, `recents_task_view_header`, `recents_empty`, `recents_grid_task_view`, `volume_dialog`, `volume_dialog_row`, `navigation_bar`, `navigation_layout`, `global_screenshot`, `zen_mode_panel`, `brightness_mirror`.
- Keyguard module (`packages/Keyguard`, compiled into SystemUI): `keyguard_host_view`, `keyguard_status_view`, `keyguard_pin_view`, `keyguard_pattern_view`, `keyguard_password_view`, `keyguard_num_pad_key`, `keyguard_message_area`, `keyguard_bouncer`, `keyguard_status_area`, `keyguard_sim_pin_view`.
- Values: `config.xml` (`quick_settings_num_columns`, `quick_settings_num_rows`, `quick_settings_tiles_default`, `config_maxNotificationIcons`, `recents_*_duration`, `heads_up_notification_decay`, `config_recents_use_hardware_layers`), `colors.xml` (`system_bar_background_opaque`, `notification_panel_solid_background`, `qs_text`, `qs_tile_divider`, `qs_subhead`, `status_bar_clock_color`, `notification_shade_background_color`, `notification_material_background_color`, `recents_task_bar_*`, `batterymeter_*`), `dimens.xml` (hundreds of dimens: `status_bar_icon_size`, `navigation_bar_size`, `notification_panel_width`, `qs_peek_height`, `volume_dialog_*`), `styles.xml`, plus Lineage extras `cm_*.xml`.
- Drawables: `stat_sys_*` (wifi_signal_, signal_, data_fully_connected_*, airplane_mode, alarm, bluetooth, dnd, location, hotspot, ringer_*), `ic_qs_*` (wifi_, signal_, bluetooth_*, dnd_*, ringer_*, brightness, cast, nfc, night_display, profiles, volume_panel, caffeine, heads_up, usb_tether, adb), `ic_sysbar_*` (back, home, recent, menu, ime), `ic_volume_*`, `volume_dialog_background`, `qs_background_primary`, `qs_tile_background`, `qs_detail_background`, `qs_customizer_background`, `notification_material_bg`, `notification_guts_bg`, `recents_*`, `ic_close`, `keyguard_overflow_number_background`.

## 6. What resources cannot do, and alternatives

| Need | Why resources fail | Alternative |
|------|--------------------|-------------|
| Turnstile and continuum animations (3D flip, staggered tiles) | Activity and window anims are 2D `<set>` Animation resources applied by WindowManager `AppTransition`. No rotateY or camera perspective in XML. | Patch `AppTransition.loadAnimation` in `services.jar` (smali, B2) with a custom Animation; or a source build (C); or an Xposed hook (D). In-app transitions are only per-app. |
| Notification shade layout, tile order, pivot headers | `PhoneStatusBar`/`QSPanel` code expects fixed ids and classes. | Keep ids and classes in the layout RRO; reorder by smali/source for structure. |
| Lowercase titles and live-tile behaviour | `textAllCaps` can only turn caps off, not lowercase. Live tiles are launcher code. | Rewrite English strings programmatically in the arsc (care with format specifiers), or patch `AllCapsTransformationMethod`. Live tiles need a custom launcher. |
| Lock screen swipe and clock behaviour | `KeyguardViewMediator` and `NotificationPanelView` logic. | Smali or source. |
| Power menu behaviour | `GlobalActions` (policy) code. Look is restyleable via `global_actions_item` plus the dialog theme. | Smali or source for behaviour. |
| Adding new views, IDs or manifest components | The manifest is frozen (F8-F9) and idmap hides overlay-only names (F5-F6). | Source build, or inject new smali classes (dex only, no manifest). |
| New permissions or components | Needs the platform key. | Source build with own keys (wipe, F9). |
| Framework themes if A2 is dormant | F4. | B1 or source build. |

## 7. Caveats and what to test first

1. Overlay config precedence (F7): an overlay `drawable/` entry loses to the target's `drawable-xxhdpi-v4`. Mirror all folders.
2. Pin ids with `public.xml` copied from the decoded target (F17), but do not rely on it before testing (F6).
3. FDE: with a PIN-encrypted `/data`, modules mount only after unlock, and Lineage recovery may not mount `/data`. Check `ro.crypto.*`.
4. All sources here are `cm-14.1` HEAD, not necessarily the exact tree your ROM was built from.

## 8. Tooling summary

| Task | Tool |
|------|------|
| Decode / rebuild resources and smali | apktool (keep `public.xml`, `AndroidManifest.xml`, `apktool.yml`) |
| Compile overlay APKs | `aapt` (v1) or `aapt2` from Android build-tools |
| Inspect APKs and ids | `aapt dump badging`, `aapt dump resources`, `aapt dump xmltree` |
| Align / sign | `zipalign`, `apksigner` (v1 only for overlays) |
| Deploy and debug | `adb`, `fastboot`, `logcat` |
| Systemless delivery | Magisk module (`system/` tree, `disable` / `remove` markers) |

## 9. What a device probe must answer

- Is `/vendor` a symlink to `/system/vendor`, and does `/vendor/overlay` exist?
- Does `/data/resource-cache/overlays.list` exist, and is `/system/bin/idmap` present?
- Is the system dexpreopted (`oat/arm/*.odex`)?
- Which fonts, boot animation and sound paths exist?
- Does `su` work, and which Magisk modules and version are installed?
- Is `/data` encrypted, and what do `ro.build.tags` / host / user / fingerprint say about the builder and signing keys?
- What are the shared-user records for `android.uid.system` and `android.uid.systemui` (`/data/system/packages.xml`)?
