#!/bin/sh
# probe-device.sh - READ-ONLY probes for the an Android 7.x (LineageOS 14.1 class) ROM before reskinning it.
#
# What it does: runs only read commands over adb (getprop, ls, cat, mount, dumpsys, logcat -d,
# stat, and `su -c <read-only command>` when root is granted). It never writes to the device,
# never installs, never reboots, never touches the lock screen or any PIN.
# Prerequisite: phone connected, USB debugging authorised by the user (do NOT try to unlock it).
#
# Usage:  scripts/probe-device.sh [-s SERIAL] [-o OUTDIR]
#   -s SERIAL  adb serial (else the only attached device is used)
#   -o OUTDIR  also tee the output into OUTDIR/probe-<timestamp>.txt (local Mac path only)
#
# Each section prints "### name" then raw output. Compare with the checklist in
# references/android-rom-research.md section 9 ("What the probe must answer").

ADB="adb"
OUTDIR=""
while getopts "s:o:" opt; do
  case "$opt" in
    s) ADB="adb -s $OPTARG" ;;
    o) OUTDIR="$OPTARG" ;;
    *) echo "usage: $0 [-s SERIAL] [-o OUTDIR]" >&2; exit 2 ;;
  esac
done

if ! $ADB get-state >/dev/null 2>&1; then
  echo "No authorised adb device (get-state failed). Connect the phone; do not unlock it for me." >&2
  exit 1
fi

run() { # run a device shell command, never fail the script
  $ADB shell "$@" 2>&1 | tr -d '\r'
}
# Root probe: only ever pass read-only commands here.
rootrun() {
  $ADB shell "su -c '$*'" 2>&1 | tr -d '\r'
}
section() { printf '\n### %s\n' "$1"; }

probe() {
  echo "probe-device.sh  $(date '+%Y-%m-%d %H:%M:%S')  host=$(uname -n)"

  section "01 identity / version props"
  run 'for p in ro.product.model ro.product.device ro.product.board ro.build.version.release ro.build.version.sdk ro.build.version.security_patch ro.build.id ro.build.display.id ro.build.fingerprint ro.build.tags ro.build.type ro.build.user ro.build.host ro.build.date ro.cm.version ro.lineage.version ro.lineage.build.version ro.modversion ro.product.cpu.abi ro.product.cpu.abilist ro.sf.lcd_density ro.boot.verifiedbootstate ro.boot.flash.locked ro.secure ro.debuggable ro.crypto.state ro.crypto.type ro.boot.vendor.overlay.theme sys.boot_completed; do echo "$p=$(getprop $p)"; done'

  section "02 root / su / magisk"
  run 'id; which su; ls -l /sbin/su /system/xbin/su /system/bin/su 2>&1 | head'
  rootrun 'id; getenforce; magisk -v; magisk -V'

  section "03 vendor overlay dirs (does /vendor exist, is it a symlink, is there /vendor/overlay)"
  run 'ls -ld /vendor /system/vendor /vendor/overlay /system/vendor/overlay /oem /oem/overlay 2>&1'
  run 'ls -la /vendor/ 2>&1 | head -30'
  run 'ls -laR /vendor/overlay /system/vendor/overlay 2>&1 | head -40'
  run 'ls -ld /system/vendor/* 2>&1 | head -30'

  section "04 mount table / partitions"
  run 'cat /proc/mounts | grep -E " /(system|vendor|data|cache|persist|firmware|oem|sbin|odm)( |/)" '
  run 'grep -E "magisk|vendor|overlay" /proc/mounts | head -40'
  run 'df -h /system /data /cache 2>&1'
  run 'ls -l /dev/block/bootdevice/by-name/ 2>&1 | head -80'

  section "05 package manager view: Settings / SystemUI / framework-res"
  run 'pm path com.android.settings; pm path com.android.systemui; pm path android'
  run 'dumpsys package com.android.settings | grep -i -E "codePath|resourcePath|resourceDirs|sharedUser|userId=|versionCode|flags=|pkgFlags|privateFlags|timeStamp|lastUpdate|signatures|overlay|dataDir" | head -30'
  run 'dumpsys package com.android.systemui | grep -i -E "codePath|resourcePath|resourceDirs|sharedUser|userId=|versionCode|pkgFlags|privateFlags|timeStamp|signatures|overlay" | head -30'
  run 'dumpsys package android | grep -i -E "codePath|resourcePath|sharedUser|userId=|pkgFlags|signatures|overlay" | head -20'
  run 'pm list packages -f | grep -i -E "overlay|theme|metro" '
  run 'dumpsys package shared-users | grep -i -A6 -E "SharedUser.*(android.uid.system|android.uid.systemui)" | head -50'

  section "06 apk file paths + sizes"
  run 'ls -l /system/framework/framework-res.apk /system/priv-app/Settings/ /system/priv-app/SystemUI/ /system/priv-app/*/ 2>&1 | head -120'
  run 'ls -l /system/framework/ | head -60'

  section "07 odex / oat presence (dexpreopt?)"
  run 'ls -lR /system/priv-app/Settings/oat /system/priv-app/SystemUI/oat 2>&1 | head -20'
  run 'ls -l /system/framework/arm/ 2>&1 | head -20'
  run 'ls -l /data/dalvik-cache/ 2>&1 | head; ls /data/dalvik-cache/arm 2>&1 | grep -i -E "Settings|SystemUI|framework-res" | head'
  rootrun 'ls -l /data/dalvik-cache/arm 2>&1 | grep -i -E "Settings|SystemUI|framework" | head'

  section "08 resource-cache (framework RRO mechanism: overlays.list / idmap files)"
  rootrun 'ls -laZ /data/resource-cache 2>&1 | head -40; cat /data/resource-cache/overlays.list 2>&1 | head'
  run 'ls -l /system/bin/idmap /system/bin/installd 2>&1'

  section "09 magisk modules (names, props, what each module mounts)"
  rootrun 'ls -la /data/adb/modules 2>&1'
  rootrun 'for d in /data/adb/modules/*; do echo "== $d"; ls -a $d; cat $d/module.prop 2>/dev/null; done'
  rootrun 'ls -la /data/adb/post-fs-data.d /data/adb/service.d 2>&1'
  rootrun 'find /data/adb/modules -maxdepth 4 -path "*/system/*" 2>/dev/null | head -80'

  section "10 fonts"
  run 'ls -l /system/fonts | head -80'
  run 'ls -l /system/etc/fonts.xml /system/etc/system_fonts.xml /system/etc/fallback_fonts.xml 2>&1'
  run 'head -40 /system/etc/fonts.xml 2>&1'

  section "11 boot animation / media / sounds"
  run 'ls -l /system/media/bootanimation.zip /oem/media/bootanimation.zip /data/local/bootanimation.zip /system/media/bootanimation-encrypted.zip 2>&1'
  run 'ls /system/media /system/media/audio /system/media/audio/ui 2>&1 | head -80'
  run 'getprop | grep -i -E "bootanim|bootanimation|init.svc.bootanim"'

  section "12 display / animation settings (read only)"
  run 'wm size; wm density'
  run 'for k in window_animation_scale transition_animation_scale animator_duration_scale; do echo "$k=$(settings get global $k)"; done'
  run 'settings get system font_scale; settings get secure lockscreen.disabled 2>&1 | head -1'
  run 'getprop | grep -E "^\[(persist\.sys|persist\.sys\.|ro\.config|debug\.sf|ro\.sf)" | head -40'

  section "13 selinux + sepolicy hints for module-injected files"
  run 'getenforce; ls -ldZ /system/priv-app/Settings /data/resource-cache /data/adb 2>&1'

  section "14 logcat (dump only): overlay/idmap/package-scan messages from this boot"
  run 'logcat -d -b main,system 2>&1 | grep -i -E "idmap|Overlay added|overlay not trusted|resource-cache|signatures do not match|Signature mismatch|signature changed|Failed to generate idmap|PackageManager.*(Settings|SystemUI)" | tail -60'
  run 'getprop sys.boot_completed; getprop init.svc.zygote; getprop ro.runtime.firstboot; getprop dalvik.vm.dex2oat-filter; getprop ro.dalvik.vm.native.bridge'

  section "15 zygote / system health (boot loop detection signals)"
  run 'ps | grep -E "zygote|system_server|systemui" | head; uptime 2>&1; cat /proc/uptime'
  run 'ls -l /data/system/packages.xml /data/system/packages.list 2>&1'
  rootrun 'grep -A3 -E "shared-user name=\"android.uid.(system|systemui)\"" /data/system/packages.xml | head -20'

  section "16 backups checklist helpers (sizes only)"
  run 'ls -l /dev/block/bootdevice/by-name/ 2>&1 | grep -E " (boot|recovery|system|persist|modemst1|modemst2|fsg|misc|logo|oem|cache|userdata|metadata|bluetooth|dsp|modem|sbl1|aboot|rpm|tz|hyp|ddr|cid|clogo|utags|utagsBackup|padA|padB|frp|keystore|DDR|apdp|msadp|dip|devinfo|limits|mdtp|sec|pad)$"'
  echo
  echo "### done"
}

if [ -n "$OUTDIR" ]; then
  mkdir -p "$OUTDIR" || exit 1
  OUT="$OUTDIR/probe-$(date +%Y%m%d-%H%M%S).txt"
  probe 2>&1 | tee "$OUT"
  echo "saved: $OUT" >&2
else
  probe 2>&1
fi
