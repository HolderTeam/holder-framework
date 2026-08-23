#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "Usage: $0 VERIFIED_DIR OUTPUT_DIR APPIMAGETOOL RUNTIME_FILE EXPECTED_PUBLIC_KEY STAGING_REPOSITORY STAGING_RUN_ID RELEASE_REPOSITORY RELEASE_RUN_ID" >&2
  exit 2
fi

verified_dir="$(realpath "$1")"
output_dir="$2"
appimagetool="$(realpath "$3")"
runtime_file="$(realpath "$4")"
expected_public_key="$(realpath "$5")"
staging_repository="$6"
staging_run_id="$7"
release_repository="$8"
release_run_id="$9"

: "${HOLDER_GPG_SIGNING_KEY_B64:?HOLDER_GPG_SIGNING_KEY_B64 is required}"
: "${HOLDER_GPG_SIGNING_PASSPHRASE:?HOLDER_GPG_SIGNING_PASSPHRASE is required}"

if ! [[ "${staging_run_id}" =~ ^[0-9]+$ ]] || ! [[ "${release_run_id}" =~ ^[0-9]+$ ]]; then
  echo "Staging and release run IDs must be numeric." >&2
  exit 1
fi
if [ ! -x "${appimagetool}" ]; then
  echo "appimagetool is not executable: ${appimagetool}" >&2
  exit 1
fi
if [ ! -f "${runtime_file}" ] || [ -L "${runtime_file}" ]; then
  echo "Pinned AppImage runtime is missing: ${runtime_file}" >&2
  exit 1
fi
if [ ! -f "${expected_public_key}" ] || [ -L "${expected_public_key}" ]; then
  echo "Expected public release key is missing: ${expected_public_key}" >&2
  exit 1
fi
if [ -e "${output_dir}" ]; then
  echo "Candidate output directory already exists: ${output_dir}" >&2
  exit 1
fi
install -d "${output_dir}"
output_dir="$(realpath "${output_dir}")"

# shellcheck disable=SC1090
source "${verified_dir}/verified.env"
appdir="${verified_dir}/Holder.AppDir"
provenance="${verified_dir}/provenance.json"

for required_path in "${appdir}/AppRun" "${provenance}"; do
  if [ ! -e "${required_path}" ]; then
    echo "Verified signing input is missing: ${required_path}" >&2
    exit 1
  fi
done

signed_name="Holder-${APPIMAGE_VERSION}-x86_64.AppImage"
provenance_name="Holder-${APPIMAGE_VERSION}-provenance.json"
metadata_name="Holder-${APPIMAGE_VERSION}-signing-metadata.json"
public_key_name="Holder-linux-release-key.asc"
embedded_signature_name="Holder-${APPIMAGE_VERSION}-embedded-signature.asc"
checksums_name="Holder-${APPIMAGE_VERSION}-SHA256SUMS"

key_file="$(mktemp)"
export GNUPGHOME="$(mktemp -d)"
chmod 0700 "${GNUPGHOME}"

cleanup() {
  gpgconf --kill gpg-agent >/dev/null 2>&1 || true
  rm -f "${key_file}"
  rm -rf "${GNUPGHOME}"
}
trap cleanup EXIT

mapfile -t expected_primary_fingerprints < <(
  gpg --batch --with-colons --show-keys "${expected_public_key}" |
    awk -F: '$1 == "pub" { want_fingerprint = 1; next }
      want_fingerprint && $1 == "fpr" { print toupper($10); want_fingerprint = 0 }'
)
if [ "${#expected_primary_fingerprints[@]}" -ne 1 ]; then
  echo "Committed public key must contain exactly one OpenPGP primary key." >&2
  exit 1
fi
fingerprint="${expected_primary_fingerprints[0]}"
if ! [[ "${fingerprint}" =~ ^([0-9A-F]{40}|[0-9A-F]{64})$ ]]; then
  echo "Committed public key does not contain a full OpenPGP fingerprint." >&2
  exit 1
fi

printf '%s' "${HOLDER_GPG_SIGNING_KEY_B64}" | base64 --decode > "${key_file}"
gpg --batch --quiet --import "${expected_public_key}"
gpg --batch --quiet --import "${key_file}"

mapfile -t imported_primary_fingerprints < <(
  gpg --batch --with-colons --list-secret-keys |
    awk -F: '$1 == "sec" { want_fingerprint = 1; next }
      want_fingerprint && $1 == "fpr" { print toupper($10); want_fingerprint = 0 }'
)
if [ "${#imported_primary_fingerprints[@]}" -ne 1 ] ||
   [ "${imported_primary_fingerprints[0]}" != "${fingerprint}" ]; then
  echo "Imported secret key does not uniquely match the configured primary fingerprint." >&2
  printf 'Imported primary fingerprints: %s\n' "${imported_primary_fingerprints[*]:-none}" >&2
  exit 1
fi

ARCH=x86_64 \
VERSION="${APPIMAGE_VERSION}" \
APPIMAGE_EXTRACT_AND_RUN=1 \
APPIMAGETOOL_SIGN_PASSPHRASE="${HOLDER_GPG_SIGNING_PASSPHRASE}" \
  "${appimagetool}" \
    --runtime-file "${runtime_file}" \
    --comp zstd \
    --sign \
    --sign-key "${fingerprint}" \
    "${appdir}" \
    "${output_dir}/${signed_name}"
chmod 0755 "${output_dir}/${signed_name}"

"${output_dir}/${signed_name}" --appimage-signature \
  > "${output_dir}/${embedded_signature_name}"
if ! grep -q '^-----BEGIN PGP SIGNATURE-----$' "${output_dir}/${embedded_signature_name}"; then
  echo "The resulting AppImage does not expose an embedded OpenPGP signature." >&2
  exit 1
fi

cp "${provenance}" "${output_dir}/${provenance_name}"
cp "${expected_public_key}" "${output_dir}/${public_key_name}"

jq -n \
  --arg version "${APPIMAGE_VERSION}" \
  --arg fingerprint "${fingerprint}" \
  --arg staging_repository "${staging_repository}" \
  --arg staging_run_id "${staging_run_id}" \
  --arg release_repository "${release_repository}" \
  --arg release_run_id "${release_run_id}" \
  --arg signed_at "$(date --utc +'%Y-%m-%dT%H:%M:%SZ')" \
  '{
    appimage_version: $version,
    signing_key_fingerprint: $fingerprint,
    staging: {
      repository: $staging_repository,
      run_id: $staging_run_id
    },
    signing_workflow: {
      repository: $release_repository,
      run_id: $release_run_id
    },
    signed_at: $signed_at
  }' > "${output_dir}/${metadata_name}"

(
  cd "${output_dir}"
  sha256sum "${signed_name}" > "${checksums_name}"
)

printf '%s' "${HOLDER_GPG_SIGNING_PASSPHRASE}" |
  gpg --batch --yes --pinentry-mode loopback --passphrase-fd 0 \
    --local-user "${fingerprint}" \
    --armor --detach-sign \
    --output "${output_dir}/${checksums_name}.asc" \
    "${output_dir}/${checksums_name}"

echo "Created signed Holder AppImage candidate ${APPIMAGE_VERSION}."
