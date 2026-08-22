#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 APPDIR ELF_TARGET..." >&2
  exit 2
fi

appdir="$(readlink -f "$1")"
shift
multiarch="$(gcc -print-multiarch)"
library_dir="${appdir}/usr/lib"

for command_name in file lddtree patchelf; do
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "Missing runtime bundling tool: ${command_name}" >&2
    exit 1
  fi
done

install -d "${library_dir}"

is_host_glibc_component() {
  case "$1" in
    ld-linux*.so*|libBrokenLocale.so*|libanl.so*|libc.so*|libdl.so*|libm.so*|libnss_*.so*|libpthread.so*|libresolv.so*|librt.so*|libthread_db.so*|libutil.so*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

copy_library() {
  local source_path="$1"
  local source_name
  local destination

  source_name="$(basename "${source_path}")"
  if is_host_glibc_component "${source_name}"; then
    return
  fi

  case "${source_path}" in
    "${appdir}"/*)
      return
      ;;
  esac

  destination="${library_dir}/${source_name}"
  if [ -e "${destination}" ]; then
    if ! cmp -s "${source_path}" "${destination}"; then
      echo "Conflicting libraries share the name ${source_name}:" >&2
      echo "  ${source_path}" >&2
      echo "  ${destination}" >&2
      exit 1
    fi
    return
  fi

  install -m 0755 -D "$(readlink -f "${source_path}")" "${destination}"
}

export LD_LIBRARY_PATH="${appdir}/usr/lib/${multiarch}:${appdir}/usr/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"

for target in "$@"; do
  if [ ! -f "${target}" ]; then
    echo "ELF dependency target does not exist: ${target}" >&2
    exit 1
  fi
  if ! file "${target}" | grep -q 'ELF'; then
    continue
  fi

  while IFS= read -r dependency; do
    if [ -f "${dependency}" ]; then
      copy_library "${dependency}"
    fi
  done < <(lddtree -l "${target}")
done

for executable in \
  "${appdir}/usr/bin/holder-desktop" \
  "${appdir}/usr/bin/holderd" \
  "${appdir}/usr/bin/holderctl"; do
  patchelf \
    --set-rpath "\$ORIGIN/../lib:\$ORIGIN/../lib/${multiarch}" \
    "${executable}"
done

echo "Bundled shared libraries:"
find "${library_dir}" -maxdepth 1 -type f -printf '%f\n' | sort
