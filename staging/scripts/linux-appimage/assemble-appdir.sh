#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 DESKTOP_ROOT BACKEND_ROOT APPDIR APPIMAGE_VERSION" >&2
  exit 2
fi

desktop_root="$(readlink -f "$1")"
backend_root="$(readlink -f "$2")"
appdir="$(readlink -m "$3")"
appimage_version="$4"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
multiarch="$(gcc -print-multiarch)"

require_file() {
  if [ ! -f "$1" ]; then
    echo "Required file is missing: $1" >&2
    exit 1
  fi
}

require_dir() {
  if [ ! -d "$1" ]; then
    echo "Required directory is missing: $1" >&2
    exit 1
  fi
}

for executable in holder-desktop holderd holderctl; do
  if [ "${executable}" = "holder-desktop" ]; then
    test -x "${desktop_root}/usr/bin/${executable}"
  else
    test -x "${backend_root}/usr/bin/${executable}"
  fi
done

require_file "${desktop_root}/release/holder-desktop-daemon-api.json"
require_file "${backend_root}/release/holder-daemon-api-version.txt"

install -d "${appdir}/usr" "${appdir}/usr/share/holder/release"
cp -a "${desktop_root}/usr/." "${appdir}/usr/"

while IFS= read -r relative_path; do
  if [ -e "${appdir}/usr/${relative_path}" ] && \
     ! cmp -s "${backend_root}/usr/${relative_path}" "${appdir}/usr/${relative_path}"; then
    echo "Desktop/backend artifact collision: usr/${relative_path}" >&2
    exit 1
  fi
done < <(cd "${backend_root}/usr" && find . -type f -printf '%P\n' | sort)
cp -a "${backend_root}/usr/." "${appdir}/usr/"

cp -a "${desktop_root}/release/." "${appdir}/usr/share/holder/release/"
cp -a "${backend_root}/release/." "${appdir}/usr/share/holder/release/"
printf '%s\n' "${appimage_version}" \
  > "${appdir}/usr/share/holder/release/holder-appimage-version.txt"
jq -er '.daemon_api.minimum' \
  "${desktop_root}/release/holder-desktop-daemon-api.json" \
  > "${appdir}/usr/share/holder/release/holder-desktop-daemon-api-minimum.txt"
jq -er '.daemon_api.maximum_exclusive' \
  "${desktop_root}/release/holder-desktop-daemon-api.json" \
  > "${appdir}/usr/share/holder/release/holder-desktop-daemon-api-maximum-exclusive.txt"

gio_modules_source="/usr/lib/${multiarch}/gio/modules"
pixbuf_loaders_source="/usr/lib/${multiarch}/gdk-pixbuf-2.0/2.10.0/loaders"
gtk_runtime_source="/usr/lib/${multiarch}/gtk-4.0"
enchant_modules_source="/usr/lib/${multiarch}/enchant-2"

require_dir "${gio_modules_source}"
require_dir "${pixbuf_loaders_source}"
require_dir "${gtk_runtime_source}"
require_dir "${gtk_runtime_source}/4.0.0/immodules"
require_dir "${enchant_modules_source}"
require_dir /usr/share/glib-2.0/schemas
require_dir /usr/share/icons/Adwaita
require_dir /usr/share/icons/hicolor
require_dir /usr/share/gtksourceview-5
require_dir /usr/share/hunspell

install -d \
  "${appdir}/usr/lib/${multiarch}/gio/modules" \
  "${appdir}/usr/lib/${multiarch}/gdk-pixbuf-2.0/2.10.0/loaders" \
  "${appdir}/usr/lib/${multiarch}/gtk-4.0" \
  "${appdir}/usr/lib/${multiarch}/enchant-2" \
  "${appdir}/usr/share/glib-2.0/schemas" \
  "${appdir}/usr/share/icons" \
  "${appdir}/usr/share/hunspell"

cp -a "${gio_modules_source}/." \
  "${appdir}/usr/lib/${multiarch}/gio/modules/"
cp -a "${pixbuf_loaders_source}/." \
  "${appdir}/usr/lib/${multiarch}/gdk-pixbuf-2.0/2.10.0/loaders/"
cp -a "${gtk_runtime_source}/." \
  "${appdir}/usr/lib/${multiarch}/gtk-4.0/"
cp -a "${enchant_modules_source}/." \
  "${appdir}/usr/lib/${multiarch}/enchant-2/"

while IFS= read -r schema_file; do
  schema_name="$(basename "${schema_file}")"
  if [ ! -e "${appdir}/usr/share/glib-2.0/schemas/${schema_name}" ]; then
    cp -a "${schema_file}" "${appdir}/usr/share/glib-2.0/schemas/"
  fi
done < <(
  find /usr/share/glib-2.0/schemas -maxdepth 1 -type f \
    \( -name '*.gschema.xml' -o -name '*.enums.xml' -o -name '*.gschema.override' \) \
    | sort
)
cp -a /usr/share/icons/Adwaita "${appdir}/usr/share/icons/"
cp -a --update=none /usr/share/icons/hicolor/. "${appdir}/usr/share/icons/hicolor/"
cp -a /usr/share/gtksourceview-5 "${appdir}/usr/share/"

if [ -d /usr/share/enchant-2 ]; then
  cp -a /usr/share/enchant-2 "${appdir}/usr/share/"
else
  install -d "${appdir}/usr/share/enchant-2"
fi
if [ -d /usr/share/mime ]; then
  cp -a /usr/share/mime "${appdir}/usr/share/"
fi

dictionary_count=0
for dictionary in /usr/share/hunspell/en_GB.* /usr/share/hunspell/en_US.*; do
  if [ -f "${dictionary}" ]; then
    cp -a "${dictionary}" "${appdir}/usr/share/hunspell/"
    dictionary_count=$((dictionary_count + 1))
  fi
done
if [ "${dictionary_count}" -eq 0 ]; then
  echo "No basic English Hunspell dictionaries were found." >&2
  exit 1
fi

glib-compile-schemas "${appdir}/usr/share/glib-2.0/schemas"
gio-querymodules "${appdir}/usr/lib/${multiarch}/gio/modules"

pixbuf_query="$(pkg-config --variable=gdk_pixbuf_query_loaders gdk-pixbuf-2.0)"
if [ ! -x "${pixbuf_query}" ]; then
  echo "GDK Pixbuf loader query tool was not found: ${pixbuf_query}" >&2
  exit 1
fi
mapfile -t pixbuf_loaders < <(
  find "${appdir}/usr/lib/${multiarch}/gdk-pixbuf-2.0/2.10.0/loaders" \
    -maxdepth 1 -type f -name '*.so' | sort
)
if [ "${#pixbuf_loaders[@]}" -eq 0 ]; then
  echo "No GDK Pixbuf loaders were copied." >&2
  exit 1
fi
"${pixbuf_query}" "${pixbuf_loaders[@]}" \
  | sed "s#${appdir}#@APPDIR@#g" \
  > "${appdir}/usr/lib/${multiarch}/gdk-pixbuf-2.0/2.10.0/loaders.cache.in"

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f -t "${appdir}/usr/share/icons/hicolor"
  gtk-update-icon-cache -f -t "${appdir}/usr/share/icons/Adwaita"
fi

install -m 0755 "${script_dir}/AppRun" "${appdir}/AppRun"
install -m 0644 \
  "${appdir}/usr/share/applications/team.holder.Holder.desktop" \
  "${appdir}/team.holder.Holder.desktop"
install -m 0644 \
  "${appdir}/usr/share/icons/hicolor/512x512/apps/team.holder.Holder.png" \
  "${appdir}/team.holder.Holder.png"
ln -sfn team.holder.Holder.png "${appdir}/.DirIcon"

mapfile -t plugin_targets < <(
  find \
    "${appdir}/usr/lib/${multiarch}/gio/modules" \
    "${appdir}/usr/lib/${multiarch}/gdk-pixbuf-2.0/2.10.0/loaders" \
    "${appdir}/usr/lib/${multiarch}/gtk-4.0" \
    "${appdir}/usr/lib/${multiarch}/enchant-2" \
    -type f -name '*.so' | sort
)
bash "${script_dir}/bundle-runtime.sh" \
  "${appdir}" \
  "${appdir}/usr/bin/holder-desktop" \
  "${appdir}/usr/bin/holderd" \
  "${appdir}/usr/bin/holderctl" \
  "${plugin_targets[@]}"

(
  cd "${appdir}"
  find . \( -type f -o -type l \) \
    ! -path './usr/share/holder/release/holder-appimage-manifest.txt' \
    | sed 's#^\./##' \
    | sort \
    > usr/share/holder/release/holder-appimage-manifest.txt
)
