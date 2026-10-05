# `holderctl ensure`: make sure a daemon is running

`holderctl ensure` checks that a compatible Holder daemon is running and starts one if it
is not. It is the one place that knows how to do this, so a client application does not
need its own copy of the logic: it runs `holderctl ensure --json` as a child process,
reads one JSON object from standard output, and acts on the exit status.

It is idempotent. Running it when a compatible daemon is already up changes nothing.

```sh
holderctl ensure --json --api-min 0.1 --api-max-exclusive 1.0
```

## What it does

1. Looks for a running daemon: the info file (`holder.json`, see [CLIENTS.md](../../api/docs/CLIENTS.md)),
   a live process, and a successful `GET /health`.
2. If one is healthy, checks its API version against the range the caller supports. That
   decides the result; nothing is started or stopped.
3. If none is healthy (and `--no-start` was not given), starts one:
   - **service**: `systemctl --user start holder-daemon.service`. Chosen automatically on
     Linux when that unit is installed, the caller did not name a daemon, and the program
     is not running inside an AppImage (which brings its own `holderd`).
   - **spawned**: runs a `holderd` it finds, detached from the caller.
4. Waits for the daemon to become healthy, then reports.

A spawned daemon is started in its own session (POSIX) or process group without a console
window (Windows), so it keeps running when `holderctl` and the client exit. Its standard
output and error are appended to `holderd-start.log` in the Holder cache directory
(`~/.cache/holder` on Linux).

**By default the daemon keeps running after the client exits.** Nothing in `ensure` stops it;
stop one you started with `SIGTERM` (the PID is in the result). To have a spawned daemon stop
by itself when it is no longer used, pass `--idle-exit SECONDS` (see [idle-exit.md](idle-exit.md)).

## `holderctl start`: a daemon that stays

`holderctl start` is for a person, or a script, that wants a daemon running and staying running: it
is `ensure` without `--idle-exit`, and it takes the same options except that one. A daemon it starts
runs until it is stopped; the output says so and names the process to end.

It differs from `ensure` in one case. If the daemon already running was started to stop itself when
idle (by a client that used `ensure --idle-exit`, such as the desktop app), `start` does not claim
success: it exits with status 15 and error code `ephemeral`, leaves that daemon alone, and says how
long it will wait before stopping. Stop that daemon and run `start` again to get one that stays. (`ensure`
itself accepts such a daemon, because a client that asked for one only needs it to be running now.)

```sh
holderctl start             # human-readable
holderctl start --json      # the same JSON as ensure, plus exit status 15 above
```

## Options

| Option | Meaning |
| --- | --- |
| `--json` | Print one JSON object on standard output (see below). |
| `--api-min VERSION` | Lowest daemon API version the caller supports (inclusive). |
| `--api-max-exclusive VERSION` | First daemon API version the caller does not support. |
| `--no-start` | Only check; never start a daemon. |
| `--timeout SECONDS` | How long to wait for a started daemon to become healthy (default 60, at most 3600). |
| `--mode auto\|service\|spawn` | How to start a daemon (default `auto`). |
| `--daemon PATH` | The `holderd` to start. Implies spawning. |
| `--daemon-arg ARG` | An argument for `holderd`; repeat for several. |
| `--workdir PATH` | Working directory for a spawned `holderd`. |
| `--idle-exit SECONDS` | Start a spawned `holderd` with `--idle-exit`, so it stops itself after this long without activity (1 to 86400). Not used for the systemd service, or when a compatible daemon is already running. |

Options that take a value also accept `--option=value`.

API versions are dot-separated numbers such as `0.1`, compared numerically (`0.9` is below
`0.10`; `1` equals `1.0`). A caller states the versions it supports itself, so the same
command works for any client. With no bounds, any daemon is accepted. When a bound is given
and the daemon reports no usable version, the daemon is treated as incompatible.

Without `--daemon`, a spawned daemon is looked for beside the `holderctl` that is running
(installed layouts keep both in the same `bin` directory), then on `PATH`. Its working
directory is `../share/holder-daemon` relative to it when that exists, otherwise its own
directory, which is where the daemon looks for its resources.

## Result

With `--json`, standard output is exactly one JSON object, for success and for failure, and
the exit status matches `exit_code`. The one exception is invalid options (exit status 2):
standard output is then empty and the usual `holderctl` JSON error
(`{"ok": false, "error": {"code": "usage", "message": ...}}`) is written to standard error.
Without `--json`, a short summary is printed (failures go to standard error).

Success:

```json
{
  "ok": true,
  "state": "started",
  "started": true,
  "mode": "spawned",
  "exit_code": 0,
  "elapsed_ms": 105,
  "daemon": {
    "pid": 330887,
    "url": "http://127.0.0.1:46507",
    "api_version": "0.1",
    "server_version": "0.2.1"
  },
  "spawned_pid": 330887,
  "idle_exit_seconds": 30,
  "log": "/home/user/.cache/holder/holderd-start.log"
}
```

Failure:

```json
{
  "ok": false,
  "state": "failed",
  "started": false,
  "exit_code": 10,
  "elapsed_ms": 4,
  "daemon": { "pid": 330887, "url": "http://127.0.0.1:46507", "api_version": "0.1", "server_version": "0.2.1" },
  "error": {
    "code": "api_incompatible",
    "message": "the daemon API version 0.1 is older than the minimum supported 99"
  }
}
```

| Field | Meaning |
| --- | --- |
| `state` | `running` (already up), `started` (this call started it) or `failed`. |
| `mode` | `existing`, `service` or `spawned`. Absent on failure when nothing was started. |
| `daemon` | The daemon that was found or started. Also present when it is running but incompatible. |
| `spawned_pid` | The `holderd` this call started, if any, including when it never became healthy. |
| `idle_exit_seconds` | Present when this call started the daemon with `--idle-exit`. |
| `daemon.idle_exit_seconds` | Present when the daemon, however it was started, will stop itself after this many seconds without activity. Absent for a daemon that stays running. |
| `log` | The start log, when a daemon was spawned. |
| `error` | `code` and a human-readable `message`, on failure only. |

## Exit status

| Code | `error.code` | Meaning |
| --- | --- | --- |
| 0 | | A compatible daemon is running. |
| 2 | `usage` | Invalid options. |
| 10 | `api_incompatible` | The running daemon's API version is outside the supported range. The daemon is left running. |
| 11 | `not_running` | No daemon is running and `--no-start` was given. |
| 12 | `start_failed` | The daemon could not be started, or exited before becoming healthy. |
| 13 | `timeout` | A started daemon did not become healthy in time. It is left running; `spawned_pid` identifies it. |
| 14 | `daemon_not_found` | No `holderd` was found. |
| 15 | `ephemeral` | `holderctl start` only: the running daemon was started with `--idle-exit` and will stop itself. It is left running. |

## Notes for client authors

- Run it as a hidden child process and read standard output. On Windows, start the child with
  `CREATE_NO_WINDOW`: tested with GLib 2.90, GLib's spawn functions (`g_spawn_async`,
  `g_spawn_sync` and `GSubprocess`) show a console window for a console program run from a GUI
  program, while `CreateProcess` with `CREATE_NO_WINDOW` (or `SW_HIDE`) does not.
- Run it asynchronously and show a "starting" state: starting a daemon can take several seconds
  on a slow machine.
- Pass the API range your client was built for, not the daemon's own.
