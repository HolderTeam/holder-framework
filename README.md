# Holder Framework

**Your knowledge belongs to you.**

Holder Framework turns your knowledge into something you can own, inspect, automate and build upon.

Holder Framework is a complete, local-first knowledge system: a set of open tools for storing, organising, connecting and working with your information without surrendering control of it to somebody else's platform.

It provides the services and interfaces that make Holder available to applications, scripts and people across different operating systems. Desktop clients, command-line tools and other software can all work with the same local knowledge through a stable OpenAPI interface, while your data remains in formats and repositories you control.

Holder Core provides the underlying algorithms, data structures and formats. Holder Framework builds on that foundation to provide the running system around them: the Holder daemon, `holderctl`, application lifecycle support, packaging and the machinery used to build and release Holder across platforms.

The goal is not simply to make another notes application. It is to provide a durable personal computing foundation for knowledge: open, interoperable, automatable and yours.

## Getting Holder

Download Holder for Windows, macOS or Linux from [holder.team](https://holder.team/), or from the [releases page](https://github.com/HolderTeam/holder-framework/releases).

## In this repository

- [`launcher/`](launcher/) - the launcher that starts the Holder backend and opens the desktop app.
- [`staging/`](staging/) - assembles and checks build artifacts for each platform.
- [`python/`](python/) - an experimental Python client for the Holder daemon's HTTP API.
- [`release/`](release/) - signing, verification and publishing of releases.

## Licence

Holder Framework is free software, licensed under the GNU General Public License, version 3. See [LICENSE](LICENSE).
