#!/usr/bin/env bash
set -euo pipefail

APK="${1:-}"
adb_cmd() {
  if [[ -n "${ANDROID_SERIAL:-}" ]]; then
    adb -s "$ANDROID_SERIAL" "$@"
  else
    adb "$@"
  fi
}

state="$(adb_cmd get-state 2>/dev/null || true)"
if [[ "$state" != "device" ]]; then
  echo "No authorized USB ADB device detected. Unlock NetHunter, enable USB debugging, and accept the host key." >&2
  adb devices -l >&2 || true
  exit 2
fi

echo "Device: $(adb_cmd shell getprop ro.product.model | tr -d '\r')"
echo "Android: $(adb_cmd shell getprop ro.build.version.release | tr -d '\r')"

if [[ -n "$APK" ]]; then
  test -f "$APK" || { echo "APK not found: $APK" >&2; exit 1; }
  adb_cmd install -r "$APK"
fi

package="com.kali.nethunter.mcpchat"
if ! adb_cmd shell pm path "$package" >/dev/null 2>&1; then
  echo "KaliYAI package is not installed: $package" >&2
  exit 3
fi

echo "KaliYAI package: installed"
echo "USB preflight: ready"
