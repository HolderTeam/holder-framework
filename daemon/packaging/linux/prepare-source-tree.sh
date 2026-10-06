#!/usr/bin/env bash
# Makes a copy of daemon/ self-contained, the way the Debian source package needs it.
#
# A source package is built from daemon/ alone, so it cannot see the files the daemon's build reads
# from beside it in the repository: the HTTP contract (api/), the holderctl sources (cli/), the
# platform code holderd and holderctl share (common/) and the version (VERSION). This copies them
# into the daemon directory, where the CMake build looks when the ones beside it are out of reach.
#
# Used by the Launchpad upload and by the package build in CI, so both exercise the same layout.
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 REPOSITORY_ROOT DAEMON_DIR" >&2
  exit 2
fi
root="$1"
daemon="$2"

for directory in api cli common; do
  if [ ! -d "${root}/${directory}" ]; then
    echo "${root}/${directory} was not found; REPOSITORY_ROOT must be the framework repository." >&2
    exit 1
  fi
done
if [ ! -f "${root}/VERSION" ]; then
  echo "${root}/VERSION was not found." >&2
  exit 1
fi
if [ ! -f "${daemon}/CMakeLists.txt" ]; then
  echo "${daemon} does not look like the daemon directory (no CMakeLists.txt)." >&2
  exit 1
fi

for directory in api cli common; do
  rm -rf "${daemon:?}/${directory}"
  cp -a "${root}/${directory}" "${daemon}/${directory}"
done
cp "${root}/VERSION" "${daemon}/VERSION"
