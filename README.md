# Holder Releases

Publishes Holder release assets for distribution.

## Note

This repository contains the release and distribution machinery for Holder. It is not the Holder source-code repository.

Holder is split across several repositories:

holder-daemon - backend, CLI and core functionality
holder-desktop - GTK desktop application
holder-launcher - launcher
holder-staging - build artifact staging

See the HolderTeam GitHub organisation for the complete source.

## Windows development builds

The `Promote Windows dev build` workflow can publish a self-signed Windows tester installer from a successful `HolderTeam/holder-staging` Windows staging run.

This is for prerelease testing only. It does not replace the final Windows signing path.

## Linux AppImage release candidates

The `Sign Linux AppImage release candidate` workflow verifies and signs one exact
successful `HolderTeam/holder-staging` AppImage run. It emits a tested,
OpenPGP-signed candidate with checksums, provenance, and a GitHub artifact
attestation; it does not publish a GitHub release.

The protected-environment setup and verification process are documented in
[`docs/linux-appimage-signing.md`](docs/linux-appimage-signing.md).

After signing, `Promote Linux AppImage to draft release` verifies one exact
signing run and adds the AppImage, checksum manifest, manifest signature, and
public key to the draft for that exact version tag. Existing release titles and
descriptions are never edited by the workflow.
