# Staging
Builds and stages Holder release candidates

For a whole-framework RC or production release, use one
[framework release manifest](docs/framework-release-manifest.md) across Linux,
Windows and macOS. It pins one core SDK revision/configuration, product version
and each platform's component runs and source commits. Release manifests require
Release backend/core artifacts and release Meson desktop artifacts.
Normal development staging continues to follow latest-green.

## Windows

The `Staging / Windows` workflow assembles the two Windows build outputs into a release-candidate layout:

- `holder-desktop-windows` from `HolderTeam/holder-desktop`
- `holder-daemon-windows-backend` from core's downstream integration run

The desktop is the program the installer's shortcuts start (`bin\holder-desktop.exe`); it starts its own
backend with `holderctl ensure`. There is no launcher.

Run it manually from:

https://github.com/HolderTeam/holder-framework/actions/workflows/staging-windows-stage.yml

By default, staging resolves core's latest-green SDK and selects successful
desktop and core daemon-integration runs on main. All selected
artifacts must be unexpired. An explicit core tag/SHA and component run IDs
support reproducible staging. Desktop installer metadata is checked out at the
selected desktop run's commit. A backend built against another core revision
is rejected.

The staged directory and installed package preserve `core-build.json` and
`release/holder-core-provenance.json`; `release-candidate.json` records the
core SDK asset checksum and publication. `backend_run_commit` identifies the
workflow run revision (the core revision when selecting a core integration run).

The normal workflow uploads two artifacts:

- `Holder-windows-staged`: unsigned canonical staging directory for release signing.
- `Holder-windows-test-signed-installer`: self-signed installer for trusted manual testing.

Set `sign_test_installer=false` to validate an unsigned branch build without
using the protected signing environment. This still assembles the staged
directory and builds, installs and smoke-tests the unsigned installer.

The self-signed tester installer is only for internal validation. It is not the release signing path. To test it on a clean Windows machine, import the included `Holder-windows-test-signing.cer` into the trusted certificate store only if the fingerprint matches `Holder-windows-test-signing-fingerprint.txt`.

The workflow needs a protected GitHub environment named `windows-staging` with access limited to `main` and these environment secrets:

- `WINDOWS_TEST_SIGNING_PFX`: base64 encoded test signing PFX.
- `WINDOWS_TEST_SIGNING_PFX_PASSWORD`: PFX export password.

If the artifact downloads need cross-repository authentication, add a repository secret named `HOLDER_CI_ARTIFACT_TOKEN` with read-only access to the build artifacts.

## Linux AppImage

The Linux AppImage workflow combines the native Ubuntu 24.04 artifacts from
`holder-desktop` and `holder-daemon`, bundles their GTK/GIO runtime, and uploads
both an AppImage and its assembled AppDir:

https://github.com/HolderTeam/holder-framework/actions/workflows/staging-linux-appimage-stage.yml

All workflow inputs are optional. Development staging resolves core's
`latest-green` SDK once and selects the newest successful desktop main artifact
and core main `daemon-integration.yml` artifact that are still downloadable.
Core's integration run contains the daemon package built and tested against
that published SDK. Staging rejects a backend whose recorded core revision
differs from the selected SDK, including while a newer downstream check is
still running. Retry after that check passes; it does not silently use older core.

Run IDs, repositories, branches, `core_ref` (tag or full SHA), and the AppImage
version can be overridden for compatibility testing. Set `backend_repository`
to `HolderTeam/holder-daemon` to select artifacts from daemon's `ci.yml` instead.
An explicit older core selection needs a backend run built against that revision.

For an RC or release, commit a JSON manifest to this repository and supply its
relative path through `release_manifest`. The manifest controls the version,
repositories, immutable component runs and core commit; leave run ID, product
version and `core_ref` overrides at their defaults. For example:

```json
{
  "appimage_version": "0.2.1-rc.1",
  "core": {"commit": "<full core SHA>", "build_type": "RelWithDebInfo"},
  "desktop": {
    "repository": "HolderTeam/holder-desktop",
    "run_id": "<successful desktop run ID>",
    "commit": "<full desktop SHA>"
  },
  "backend": {
    "repository": "HolderTeam/holder-core",
    "run_id": "<successful daemon integration run ID>",
    "commit": "<full daemon SHA>"
  }
}
```

Every component commit and the core build configuration are checked against
the extracted artifacts. Development daemon artifacts use `RelWithDebInfo`;
production artifacts use daemon's `core_build_type=Release` workflow input and
distinct `-release` artifact names.
Component Actions artifacts expire, so stage the pinned candidate while they
are available. Signing and promotion use that staged AppImage afterwards.

Desktop and daemon package versions do not have to be identical. The workflow
uses the compatibility metadata published in their artifacts instead: the daemon
declares one API version and the desktop declares the supported API range. A
stable AppImage version will not accept prerelease component builds.

The `Holder-linux-appimage-staged` artifact contains:

- `Holder-<version>-x86_64.AppImage`
- A matching AppDir archive for inspection and debugging
- SHA-256 checksums and component/core provenance, including the SDK asset digest

The AppDir and final AppImage retain daemon's original `core-build.json` and
`holder-core-provenance.json`. The external product provenance also includes
the same core selection. A supplied framework release manifest is bundled in
`usr/share/holder/release/holder-framework-release.json`.

`AppRun` sets up the bundled runtime (library, GTK and schema paths) and starts the
desktop. The desktop starts its own backend with `holderctl ensure` (the one in the
AppImage's `usr/bin`): it uses an already-running compatible daemon when there is one,
and otherwise starts the bundled `holderd` with `--idle-exit 60`, so the daemon stops
by itself shortly after the window closes. `AppRun` no longer owns or stops a daemon. With
`HOLDER_APPRUN_SMOKE_TEST=1` it starts the bundled daemon the same way, checks it is healthy
within the API range the desktop was built for, stops the daemon it started and exits (CI and
the release verification use this).

## Mac

macOS staging uses the same latest-green selection and rejects mismatched
backend SDKs. Artifact runs must be successful and unexpired, and desktop
packaging metadata comes from the selected run's exact source commit. Core
provenance is retained in `Holder.app/Contents/Resources/core-build.json`,
`release/holder-core-provenance.json` and the release-candidate metadata.
Explicit core and component run overrides support reproducible staging.

Homebrew's GTK is built without the macOS accessibility bridge (AccessKit), so staging rebuilds the
`libgtk-4` library from Homebrew's source version with `-Daccesskit=enabled`, using checksum-pinned
AccessKit C 0.18.0, before bundling (`staging/scripts/build-macos-accessible-gtk.sh`). Staging fails if the
final bundle's GTK no longer depends on AccessKit, and records the versions in `gtk-accessibility-build.json`.
Before a release, try a staged app with VoiceOver: a linked bridge does not mean every Holder interaction is accessible.

How to manually test a prerelease development version of Holder, aka a "staged copy".

1. Go to the Mac OS staged app action:

https://github.com/HolderTeam/holder-framework/actions/workflows/staging-macos-stage.yml

2. Click on the latest (or your target) successful run.

3. Look under Artifacts

4. Click the Download button.

5. Open the Terminal (Applications/Utility).

6. Get to where you downloaded the asset. E.g.

	cd ~/Downloads

7. Check the artifact has all the files it needs:

  codesign --verify --deep --strict --verbose=2 Holder.app

8. For local test only, remove quarantine:

  xattr -dr com.apple.quarantine Holder.app

9. Open it:

  open Holder.app
