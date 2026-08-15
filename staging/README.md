# holder-staging
Builds and stages Holder release candidates

## Windows

The Windows staged package workflow assembles the three Windows build outputs into a release-candidate layout:

- `holder-desktop-windows` from `HolderTeam/holder-desktop`
- `holder-daemon-windows-backend` from `HolderTeam/holder-daemon`
- `holder-launcher-windows` from `HolderTeam/holder-launcher`

Run it manually from:

https://github.com/HolderTeam/holder-staging/actions/workflows/windows-stage.yml

Use the successful workflow run IDs from the three input repositories. The desktop repo currently uses `master`; the daemon and launcher repos use `main`.

The workflow uploads two artifacts:

- `Holder-windows-staged`: unsigned canonical staging directory for release signing.
- `Holder-windows-test-signed-installer`: self-signed installer for trusted manual testing.

The self-signed tester installer is only for internal validation. It is not the release signing path. To test it on a clean Windows machine, import the included `Holder-windows-test-signing.cer` into the trusted certificate store only if the fingerprint matches `Holder-windows-test-signing-fingerprint.txt`.

The workflow needs a protected GitHub environment named `windows-staging` with access limited to `main` and these environment secrets:

- `WINDOWS_TEST_SIGNING_PFX`: base64 encoded test signing PFX.
- `WINDOWS_TEST_SIGNING_PFX_PASSWORD`: PFX export password.

If the artifact downloads need cross-repository authentication, add a repository secret named `HOLDER_CI_ARTIFACT_TOKEN` with read-only access to the build artifacts.

## Mac

How to manually test a prerelease development version of Holder, aka a "staged copy".

1. Go to the Mac OS staged app action:

https://github.com/HolderTeam/holder-staging/actions/workflows/macos-stage.yml

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
