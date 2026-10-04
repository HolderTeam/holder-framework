# Holder Framework

**Your knowledge belongs to you.**

Holder Framework turns your knowledge into something you can own, inspect, automate and build upon.

Holder Framework is a complete, local-first knowledge system: a set of open tools for storing, organising, connecting and working with your information without surrendering control of it to somebody else's platform.

It provides the services and interfaces that make Holder available to applications, scripts and people across different operating systems. Desktop clients, command-line tools and other software can all work with the same local knowledge through a stable OpenAPI interface, while your data remains in formats and repositories you control.

Holder Core provides the underlying algorithms, data structures and formats. Holder Framework builds on that foundation to provide the running system around them: the Holder daemon, `holderctl`, application lifecycle support, packaging and the machinery used to build and release Holder across platforms.

The goal is not simply to make another notes application. It is to provide a durable personal computing foundation for knowledge: open, interoperable, automatable and yours.

## Layout

- `staging/` - assembles and checks per-platform build artifacts from the component repositories (workflows: `staging-*-stage.yml`).
- `release/` - signing keys, scripts and documentation for release signing and promotion (workflows: `sign-*` and `promote-*`).
- `.github/workflows/` - all workflows live here, as GitHub requires.

This repository is not the Holder source-code repository. The source is split across other repositories, such as holder-daemon (backend, CLI and core functionality), holder-desktop (GTK desktop application) and holder-launcher (launcher). See the HolderTeam GitHub organisation for the complete source.

## Windows development builds

The `Promote Windows dev build` workflow can publish a self-signed Windows tester installer from a successful Windows staging run of this repository.

This is for prerelease testing only. It does not replace the final Windows signing path.

## Linux AppImage release candidates

The `Sign Linux AppImage release candidate` workflow verifies and signs one exact
successful AppImage staging run of this repository. It emits a tested,
OpenPGP-signed candidate with checksums, provenance, and a GitHub artifact
attestation; it does not publish a GitHub release.

The protected-environment setup and verification process are documented in
[`release/docs/linux-appimage-signing.md`](release/docs/linux-appimage-signing.md).

After signing, `Promote Linux AppImage to release` verifies one exact signing
run and adds the AppImage, checksum manifest, manifest signature, and public
key to the draft for that exact version tag. An existing published prerelease
can also receive the assets when `allow_published_prerelease` is explicitly
enabled. Existing release titles and descriptions are never edited by the workflow.
