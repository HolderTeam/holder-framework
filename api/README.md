# api

The HTTP contract between the Holder daemon and its clients.

- [`openapi.yaml`](openapi.yaml) - the OpenAPI description of every endpoint. It is the canonical
  contract: a change to the daemon's HTTP behaviour changes this file in the same pull request.
  The daemon serves it at `GET /openapi.yaml`, and the Python client in [`python/`](../python/)
  is generated from a tested snapshot of it.
- [`API_VERSION`](API_VERSION) - the compatibility version clients check (`MAJOR.MINOR`). It is
  separate from the release version in the root [`VERSION`](../VERSION). A client states the range
  it supports with `holderctl ensure --api-min` and `--api-max-exclusive`.
- [`docs/CLIENTS.md`](docs/CLIENTS.md) - how a client finds, authenticates to and uses a daemon.
- [`docs/event-streams.md`](docs/event-streams.md) - the server-sent event streams and how to
  stay in sync with them.

How the daemon starts and stops (`holderctl ensure`, the idle exit) is documented with the
daemon, in [`daemon/docs/`](../daemon/docs/).

## Debian source package

A Debian source package is built from `daemon/` alone. Its workflow copies this directory into
`daemon/` first, and the CMake build uses that copy when the directory beside `daemon/` is not
there. The copy is ignored by Git (`daemon/.gitignore`).
