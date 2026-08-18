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
