#!/bin/bash
# Build the Homebrew-selected GTK version with the macOS accessibility bridge.
# The output is isolated; the staging runner installs its dylibs into its GTK keg.
set -euo pipefail

work_dir="${1:?usage: build-macos-accessible-gtk.sh WORK_DIR}"
mkdir -p "${work_dir}"
work_dir="$(cd "${work_dir}" && pwd)"
runtime_prefix="${work_dir}/runtime"

brew info --json=v2 gtk4 > "${work_dir}/gtk-formula.json"
python3 - "${work_dir}/gtk-formula.json" "${work_dir}/gtk-source.env" <<'PY'
import json
import shlex
import subprocess
import sys

formula = json.load(open(sys.argv[1]))["formulae"][0]
version = subprocess.check_output(["pkg-config", "--modversion", "gtk4"], text=True).strip()
if version != formula["versions"]["stable"]:
    raise SystemExit("Installed GTK does not match the current Homebrew source; update GTK first")
source = formula["urls"]["stable"]
with open(sys.argv[2], "w") as output:
    for key, value in {"gtk_version": version, "gtk_url": source["url"],
                       "gtk_sha256": source["checksum"]}.items():
        output.write(f"{key}={shlex.quote(value)}\n")
PY
gtk_version='' gtk_url='' gtk_sha256=''
# Generated above from Homebrew's formula metadata, with shell-quoted values.
# shellcheck disable=SC1091
source "${work_dir}/gtk-source.env"

download_verified() {
  local url="$1" checksum="$2" destination="$3"
  curl --fail --location --show-error "${url}" --output "${destination}"
  printf '%s  %s\n' "${checksum}" "${destination}" | shasum -a 256 --check
}

# GTK 4.24 uses the accesskit-c-0.18 pkg-config API. A future GTK API change
# deliberately fails configuration instead of silently disabling accessibility.
download_verified \
  "https://github.com/AccessKit/accesskit-c/archive/refs/tags/0.18.0.tar.gz" \
  "71465b15724cfbe7d54fb27e82e86c6935f922c40703615972c4e79fdce48b40" \
  "${work_dir}/accesskit.tar.gz"
tar -xzf "${work_dir}/accesskit.tar.gz" -C "${work_dir}"
meson setup "${work_dir}/accesskit-build" "${work_dir}/accesskit-c-0.18.0" \
  --prefix "${runtime_prefix}" --libdir lib --buildtype release --default-library shared
meson compile -C "${work_dir}/accesskit-build"
meson install -C "${work_dir}/accesskit-build"

download_verified "${gtk_url}" "${gtk_sha256}" "${work_dir}/gtk.tar.xz"
tar -xJf "${work_dir}/gtk.tar.xz" -C "${work_dir}"
gettext_prefix="$(brew --prefix gettext)"
export PKG_CONFIG_PATH="${runtime_prefix}/lib/pkgconfig:${gettext_prefix}/lib/pkgconfig:${PKG_CONFIG_PATH:-}"
meson setup "${work_dir}/gtk-build" "${work_dir}/gtk-${gtk_version}" \
  --prefix "${runtime_prefix}" --libdir lib --buildtype release \
  -Daccesskit=enabled -Dmacos-backend=true -Dx11-backend=false \
  -Dintrospection=disabled -Ddocumentation=false -Dman-pages=false \
  -Dbuild-tests=false -Dbuild-testsuite=false -Dbuild-examples=false -Dbuild-demos=false \
  -Dmedia-gstreamer=disabled -Dvulkan=disabled
meson compile -C "${work_dir}/gtk-build" gtk-4

cp -a "${work_dir}/gtk-build/gtk/"libgtk-4*.dylib "${runtime_prefix}/lib/"
mkdir -p "${runtime_prefix}/share/licenses/accesskit-c"
cp "${work_dir}/accesskit-c-0.18.0/"LICENSE* "${runtime_prefix}/share/licenses/accesskit-c/"

python3 - "${runtime_prefix}/gtk-accessibility-build.json" "${gtk_version}" "${gtk_url}" "${gtk_sha256}" <<'PY'
import json
import sys

with open(sys.argv[1], "w") as output:
    json.dump({"gtk": {"version": sys.argv[2], "source_url": sys.argv[3], "sha256": sys.argv[4]},
               "accesskit_c": {"version": "0.18.0", "sha256":
                               "71465b15724cfbe7d54fb27e82e86c6935f922c40703615972c4e79fdce48b40"},
               "gtk_accesskit": "enabled"}, output, indent=2)
    output.write("\n")
PY

# A linked AccessKit dylib proves the backend was compiled in, unlike the
# backend-name strings which GTK includes even when that backend is disabled.
otool -L "${runtime_prefix}/lib/libgtk-4.1.dylib" | grep -F 'libaccesskit-c-0.18'
