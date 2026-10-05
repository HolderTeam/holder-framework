# Coding-agent instructions

This repository contains the Python HTTP client for a running holder-daemon.
holder-kit is a separate offline library; do not add native bindings here.

The high-level API has not been designed. Keep this initial experiment confined
to project tooling and the low-level generated client in `src/holder/generated`.
Do not hand-edit generated files. Use `python scripts/generate.py` to regenerate
and `python scripts/generate.py --check` to verify them.

`openapi/openapi.yaml` is a verbatim snapshot of holder-daemon's contract.
Fix contract errors in holder-daemon first (it lives in `daemon/` of the holder-framework
repository), test there, then refresh the snapshot with
`python scripts/generate.py --source ../holder-framework/daemon/openapi.yaml`.
Do not duplicate domain logic owned by the daemon or holder-core.
