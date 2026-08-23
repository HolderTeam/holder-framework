#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 CANDIDATE_DIR EXPECTED_VERSION EXPECTED_PUBLIC_KEY" >&2
  exit 2
fi

candidate_dir="$(realpath "$1")"
expected_version="$2"
expected_public_key="$(realpath "$3")"

if [ ! -f "${expected_public_key}" ] || [ -L "${expected_public_key}" ]; then
  echo "Expected public release key is missing: ${expected_public_key}" >&2
  exit 1
fi

signed_name="Holder-${expected_version}-x86_64.AppImage"
provenance_name="Holder-${expected_version}-provenance.json"
metadata_name="Holder-${expected_version}-signing-metadata.json"
public_key_name="Holder-linux-release-key.asc"
embedded_signature_name="Holder-${expected_version}-embedded-signature.asc"
checksums_name="Holder-${expected_version}-SHA256SUMS"

for filename in \
  "${signed_name}" \
  "${provenance_name}" \
  "${metadata_name}" \
  "${public_key_name}" \
  "${embedded_signature_name}" \
  "${checksums_name}" \
  "${checksums_name}.asc"; do
  if [ ! -f "${candidate_dir}/${filename}" ] || [ -L "${candidate_dir}/${filename}" ]; then
    echo "Signed candidate file is missing: ${filename}" >&2
    exit 1
  fi
done
if [ ! -x "${candidate_dir}/${signed_name}" ]; then
  echo "Signed AppImage is not executable." >&2
  exit 1
fi

(
  cd "${candidate_dir}"
  sha256sum -c "${checksums_name}"
)

validation_gnupg_home="$(mktemp -d)"
runtime_dir="$(mktemp -d)"
cleanup() {
  GNUPGHOME="${validation_gnupg_home}" gpgconf --kill gpg-agent >/dev/null 2>&1 || true
  rm -rf "${validation_gnupg_home}" "${runtime_dir}"
}
trap cleanup EXIT
chmod 0700 "${validation_gnupg_home}"

export GNUPGHOME="${validation_gnupg_home}"
if ! cmp -s "${expected_public_key}" "${candidate_dir}/${public_key_name}"; then
  echo "Candidate public key differs from the public key committed to holder-release." >&2
  exit 1
fi

mapfile -t expected_primary_fingerprints < <(
  gpg --batch --with-colons --show-keys "${expected_public_key}" |
    awk -F: '$1 == "pub" { want_fingerprint = 1; next }
      want_fingerprint && $1 == "fpr" { print toupper($10); want_fingerprint = 0 }'
)
if [ "${#expected_primary_fingerprints[@]}" -ne 1 ]; then
  echo "Committed public key must contain exactly one OpenPGP primary key." >&2
  exit 1
fi
expected_fingerprint="${expected_primary_fingerprints[0]}"

gpg --batch --quiet --import "${candidate_dir}/${public_key_name}"
mapfile -t public_primary_fingerprints < <(
  gpg --batch --with-colons --list-keys |
    awk -F: '$1 == "pub" { want_fingerprint = 1; next }
      want_fingerprint && $1 == "fpr" { print toupper($10); want_fingerprint = 0 }'
)
if [ "${#public_primary_fingerprints[@]}" -ne 1 ] ||
   [ "${public_primary_fingerprints[0]}" != "${expected_fingerprint}" ]; then
  echo "Candidate public key does not uniquely match the expected primary fingerprint." >&2
  exit 1
fi

gpg --batch --verify \
  "${candidate_dir}/${checksums_name}.asc" \
  "${candidate_dir}/${checksums_name}"

jq -e \
  --arg version "${expected_version}" \
  --arg fingerprint "${expected_fingerprint}" \
  '.appimage_version == $version and
   .signing_key_fingerprint == $fingerprint and
   (.staging.repository | type == "string" and length > 0) and
   (.staging.run_id | type == "string" and test("^[0-9]+$")) and
   (.signing_workflow.repository | type == "string" and length > 0) and
   (.signing_workflow.run_id | type == "string" and test("^[0-9]+$")) and
   (.signed_at | type == "string" and test("^[0-9]{4}-[0-9]{2}-[0-9]{2}T"))' \
  "${candidate_dir}/${metadata_name}" >/dev/null

extracted_signature="${runtime_dir}/embedded-signature.asc"
"${candidate_dir}/${signed_name}" --appimage-signature \
  > "${extracted_signature}"
cmp "${candidate_dir}/${embedded_signature_name}" "${extracted_signature}"
gpg --batch --list-packets "${extracted_signature}" >/dev/null

export XDG_DATA_HOME="${runtime_dir}/data"
export XDG_CONFIG_HOME="${runtime_dir}/config"
export XDG_CACHE_HOME="${runtime_dir}/cache"
export HOLDER_TEST_KEYSTORE_DIR="${runtime_dir}/keystore"
HOLDER_APPRUN_SMOKE_TEST=1 \
  timeout 90 "${candidate_dir}/${signed_name}" --appimage-extract-and-run

echo "Verified and smoke-tested signed Holder AppImage ${expected_version}."
