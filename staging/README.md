# holder-staging
Builds and stages Holder release candidates


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

7. Check the artifect has all the files it needs:

  codesign --verify --deep --strict --verbose=2 Holder.app

8. For local test only, remove quarantine:

  xattr -dr com.apple.quarantine Holder.app

9. Open it:

  open Holder.app
