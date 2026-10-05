# holderctl

The command line client for the Holder daemon. `holderctl` talks to a running `holderd` over its HTTP API,
and `holderctl ensure` makes sure a compatible daemon is running (see
[`daemon/docs/ensure.md`](../daemon/docs/ensure.md)); client applications call that rather than starting a
daemon themselves.

## Layout

- `src/holderctl.cpp` - the entry point and command dispatch.
- `src/commands/` - one file per group of commands (`card`, `project`, `sync`, `ensure`, ...).

## Building

`holderctl` is built together with the daemon, by the CMake project in [`daemon/`](../daemon/), because it
links the same Holder Core library and shares its version:

```sh
cd daemon
./make.sh build Debug     # builds holderd and holderctl into daemon/build
```

The command tests live with the daemon's tests in `daemon/tests/` (`HolderCtl*_test.cpp`,
`MilestoneDateTime_test.cpp`), because they compile these sources and run against a real `holderd`.

## Shared code

The few platform files that `holderd` and `holderctl` both need are in [`common/`](../common/).
