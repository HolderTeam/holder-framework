# Release

Signing, promotion and publishing of Holder release assets.

The workflows are in `.github/workflows/` (`sign-*` and `promote-*`), as GitHub requires. This directory holds what they use:

- `docs/` - how release signing and verification work.
- `keys/` - the public signing key that releases are checked against.
- `scripts/` - the helpers the workflows call to verify and sign artifacts.

## Windows development builds

The `Promote Windows dev build` workflow can publish a self-signed Windows tester installer from a successful Windows staging run of this repository.

This is for prerelease testing only. It does not replace the final Windows signing path.

## Linux AppImage release candidates

The `Sign Linux AppImage release candidate` workflow verifies and signs one exact
successful AppImage staging run of this repository. It emits a tested,
OpenPGP-signed candidate with checksums, provenance, and a GitHub artifact
attestation; it does not publish a GitHub release.

The protected-environment setup and verification process are documented in
[`docs/linux-appimage-signing.md`](docs/linux-appimage-signing.md).

After signing, `Promote Linux AppImage to release` verifies one exact signing
run and adds the AppImage, checksum manifest, manifest signature, and public
key to the draft for that exact version tag. An existing published prerelease
can also receive the assets when `allow_published_prerelease` is explicitly
enabled. Existing release titles and descriptions are never edited by the workflow.
