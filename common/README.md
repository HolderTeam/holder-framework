# common

Platform code shared by the daemon (`holderd`) and the command line client (`holderctl`), which are built by
the CMake project in [`daemon/`](../daemon/). It has no dependency on the rest of the daemon, only on the
standard library and Boost, and no dependency on Holder Core.

## Contents

- `src/platform/BaseDir.*` and `Paths.*` - where Holder keeps its data, configuration and cache, per platform.
  These give `holderctl` and the daemon the same answer, so they find each other's files.
- `src/platform/DetachedProcess.*` - starts a program so that it keeps running after the caller exits (its
  own session on POSIX, its own process group without a console window on Windows), through Boost.Process.
  `holderctl ensure` uses it to start the daemon.

Headers keep their `platform/...` include paths, so `#include "platform/Paths.h"` works in both programs.

Code that only one of the two programs uses stays with that program.

## Debian source package

A Debian source package is built from `daemon/` alone. Its workflow copies `cli/` and `common/` into `daemon/`
first, and the CMake build uses those copies when the directories beside `daemon/` are not there. The copies
are ignored by Git (`daemon/.gitignore`).
