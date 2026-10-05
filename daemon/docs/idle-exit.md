# Idle exit: a daemon that stops when nothing needs it

`holderd --idle-exit SECONDS` makes the daemon stop itself once it has been unused for that
long. It is meant for a daemon that exists only to serve one client application (a desktop
window, a script) so that closing the application leaves nothing running. It is off by
default, and a daemon started without it never stops by itself. The systemd user service
does not use it.

```sh
holderd --idle-exit 30
holderctl ensure --idle-exit 30      # start (or reuse) a daemon on behalf of a client
```

`SECONDS` is a whole number from 1 to 86400.

## What keeps the daemon running

The daemon is idle, and stops, only when **all** of these hold:

1. No request is being executed or having its response written. A streaming AI run executes
   inside its request, so it counts.
2. No event stream is open: the change feed (`GET /events`) and the AI run and runner event
   streams. A client that stays subscribed is present for as long as it is subscribed.
3. No background work is running: a sync pass (the pull when the daemon starts, or a push or
   pull cycle), a local model download, or a resource import.
4. Nothing has happened for `SECONDS`: no connection arrived, no request started or finished,
   no stream closed, no background work started or finished.

The fourth condition is a quiet period. It restarts every time something happens, which is
why a client that drops its event stream (a network blip, a restart of its view) and
reconnects within `SECONDS` still finds the daemon. The clock also starts when the daemon
finishes starting, so the process that started it has `SECONDS` to connect.

## What does not keep it running

- **Scheduled sync that is not running.** The sync worker pushes only every 20 minutes and
  pulls every 5, so a short-lived daemon may never reach its next scheduled push. That is
  covered by the final push below, rather than by keeping the daemon alive. A sync that is
  running when the quiet period would end finishes first.
- **The local model runner's status probe**, which only polls.
- **A connection that was accepted but has sent no request.**

## Saying goodbye

A client that is closing can tell the daemon with `POST /bye` (authenticated, no body, returns
`{"ok":true}`). It is a hint, not a command. The daemon still waits for `SECONDS` of quiet in
general, but once a client has said goodbye it waits only 3 seconds, and only while nothing else
happens:

- Running work and open event streams still keep it up, so a second client that stays
  subscribed is never cut off by the first one leaving.
- A new connection, or any request other than `/bye`, cancels the goodbye and the full period
  applies again.
- The goodbye request itself, and the stream closing right after it, count as the last activity,
  so the 3 seconds start from the moment the client has gone.
- A daemon started without `--idle-exit`, such as the systemd service, acknowledges it and
  ignores it.

Calling it is best effort. A client that crashes or loses the connection never says goodbye, and
the daemon falls back to its idle period, so nothing depends on it being sent. A client that
needs the daemon to keep running should hold an event stream open, which is what presence means;
a script that only makes occasional requests can lose its daemon 3 seconds after another
client's goodbye if it was not using it at the time.

The log says `a client said goodbye and nothing has happened since; exiting…` in this case,
instead of `idle for N seconds…`.

## The final push

When the daemon finds itself idle, and before it stops, it pushes every project that has
commits not yet pushed to its remote. This ignores the usual 20-minute push interval, since
there will be no later chance. It does not pull.

- A project is skipped if it has no remote, or if its count of unpushed commits is known and
  zero. When the count is not known (the repository has no remote-tracking branch yet) the
  push is attempted, and the remote answers.
- It respects the back-off after a failed push, so a machine that is offline is not held up
  retrying. If a push fails the commits stay local, a warning is logged, and the next run
  pushes them.
- The push does not count as activity. If nothing used the daemon in the meantime it stops
  straight after; if a request arrived while it was pushing, it carries on running.

## How it stops

It takes the same graceful path as `SIGTERM`, after the final push: it stops accepting
connections, background workers finish what they are doing, and it exits with status 0. The log says
`idle for N seconds with no requests, event streams or background work; exiting.`

The info file (`holder.json`) is left behind, as it is after any exit. Clients detect that
the daemon has gone from its dead process and failed health check, and `holderctl ensure`
starts a fresh one.

## For client applications

- Start the daemon through `holderctl ensure --idle-exit SECONDS` (see [ensure.md](ensure.md)).
  It applies only to a daemon that `ensure` starts itself; an already running daemon and the
  systemd service are left as they are.
- Keep an event stream open while the application is open. That is the presence signal, and
  an application that already subscribes to `/events` needs no extra code. A client with no
  stream relies on its requests: any request within `SECONDS` keeps the daemon alive.
- Choose `SECONDS` long enough to cover a reconnect, and short enough that closing the
  application feels like it takes the daemon away. Tens of seconds is typical.
