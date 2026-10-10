#!/usr/bin/env bash
# Print the cache key for a staged Linux holderd. Daemon CI saves under it and Python / Check
# restores from it, so both must compute it here. Git tree IDs cover every file that feeds the
# build, including the caste submodule's commit; the core commit covers a new core SDK.
set -euo pipefail

build_type=$1
core_commit=$2

inputs=$(git rev-parse \
  HEAD:daemon \
  HEAD:api \
  HEAD:common \
  HEAD:cli \
  HEAD:VERSION \
  HEAD:.gitmodules \
  HEAD:.github/actions/linux-daemon-deps \
  HEAD:.github/actions/linux-daemon-build)

printf 'linux-daemon-ubuntu-24.04-%s-%s-%s\n' \
  "$build_type" "$core_commit" "$(sha256sum <<< "$inputs" | cut -c1-16)"
