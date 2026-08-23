#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 INPUT_DIR EXPECTED_VERSION WORK_DIR" >&2
  exit 2
fi

input_dir="$(realpath "$1")"
expected_version="$2"
work_dir="$3"

semver_pattern='^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$'
if ! [[ "${expected_version}" =~ ${semver_pattern} ]]; then
  echo "Expected version is not semantic versioning: ${expected_version}" >&2
  exit 1
fi

if [ -e "${work_dir}" ]; then
  echo "Verification work directory already exists: ${work_dir}" >&2
  exit 1
fi
install -d "${work_dir}"
work_dir="$(realpath "${work_dir}")"

appimage_name="Holder-${expected_version}-x86_64.AppImage"
appdir_archive_name="Holder-${expected_version}-x86_64.AppDir.tar.gz"
provenance_name="Holder-${expected_version}-provenance.json"
checksums_name="Holder-${expected_version}-SHA256SUMS"

require_regular_file() {
  local path="$1"
  if [ ! -f "${path}" ] || [ -L "${path}" ]; then
    echo "Required regular file is missing: ${path}" >&2
    exit 1
  fi
}

require_regular_file "${input_dir}/${appimage_name}"
require_regular_file "${input_dir}/${appdir_archive_name}"
require_regular_file "${input_dir}/${provenance_name}"
require_regular_file "${input_dir}/${checksums_name}"

mapfile -t checksum_entries < <(awk '{print $2}' "${input_dir}/${checksums_name}")
if [ "${#checksum_entries[@]}" -ne 2 ] ||
   [ "${checksum_entries[0]}" != "${appimage_name}" ] ||
   [ "${checksum_entries[1]}" != "${appdir_archive_name}" ]; then
  echo "Staging checksum manifest does not contain exactly the expected AppImage and AppDir archive." >&2
  cat "${input_dir}/${checksums_name}" >&2
  exit 1
fi

(
  cd "${input_dir}"
  sha256sum -c "${checksums_name}"
)

archive_listing="$(mktemp)"
trap 'rm -f "${archive_listing}"' EXIT
tar -tzf "${input_dir}/${appdir_archive_name}" > "${archive_listing}"
while IFS= read -r entry; do
  case "${entry}" in
    Holder.AppDir | Holder.AppDir/*) ;;
    *)
      echo "Unexpected path in AppDir archive: ${entry}" >&2
      exit 1
      ;;
  esac
  case "/${entry}/" in
    *'/../'* | *'/./'*)
      echo "Unsafe path in AppDir archive: ${entry}" >&2
      exit 1
      ;;
  esac
done < "${archive_listing}"

tar -C "${work_dir}" -xzf "${input_dir}/${appdir_archive_name}"
appdir="${work_dir}/Holder.AppDir"
internal_provenance="${appdir}/usr/share/holder/release/holder-appimage-provenance.json"

if [ ! -x "${appdir}/AppRun" ]; then
  echo "The verified AppDir has no executable AppRun." >&2
  exit 1
fi
for executable in holder-desktop holderd holderctl; do
  if [ ! -x "${appdir}/usr/bin/${executable}" ]; then
    echo "The verified AppDir is missing usr/bin/${executable}." >&2
    exit 1
  fi
done
require_regular_file "${internal_provenance}"

if ! cmp -s "${input_dir}/${provenance_name}" "${internal_provenance}"; then
  echo "External provenance does not match the provenance embedded in the AppDir." >&2
  exit 1
fi

jq -e --arg version "${expected_version}" '
  .appimage_version == $version and
  (.desktop.repository | type == "string" and length > 0) and
  (.desktop.run_id | type == "string" and test("^[0-9]+$")) and
  (.desktop.version | type == "string" and length > 0) and
  (.desktop.commit | type == "string" and test("^[0-9a-fA-F]{40}$")) and
  (.backend.repository | type == "string" and length > 0) and
  (.backend.run_id | type == "string" and test("^[0-9]+$")) and
  (.backend.version | type == "string" and length > 0) and
  (.backend.commit | type == "string" and test("^[0-9a-fA-F]{40}$")) and
  (.backend.api_version | type == "string" and test("^[0-9]+\\.[0-9]+$"))
' "${internal_provenance}" >/dev/null

while IFS= read -r -d '' link; do
  target="$(readlink "${link}")"
  if [[ "${target}" = /* ]]; then
    echo "Absolute symlink in verified AppDir: ${link} -> ${target}" >&2
    exit 1
  fi
  resolved="$(realpath -m "$(dirname "${link}")/${target}")"
  case "${resolved}" in
    "${appdir}" | "${appdir}"/*) ;;
    *)
      echo "Symlink escapes verified AppDir: ${link} -> ${target}" >&2
      exit 1
      ;;
  esac
done < <(find "${appdir}" -type l -print0)

cp "${input_dir}/${provenance_name}" "${work_dir}/provenance.json"

cat > "${work_dir}/verified.env" <<EOF
APPIMAGE_VERSION=${expected_version}
APPIMAGE_NAME=${appimage_name}
EOF

echo "Verified staged Holder AppImage ${expected_version}."
