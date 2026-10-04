# holder-python

Experimental Python HTTP client for a running `holder-daemon`. This is separate
from `holder-kit`, which provides native bindings for offline analysis.

This first iteration evaluates
[openapi-python-client](https://github.com/openapi-generators/openapi-python-client).
There is no high-level API yet. The generator is a development dependency;
installed clients only need HTTPX, attrs and typing-extensions.

## Setup

Requires Python 3.11 or newer.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest
python scripts/generate.py --check
python -m build
```

## Try the low-level client

Supply the daemon URL and bearer token explicitly. This experiment does not
discover daemon connection details or read credentials from the machine.

```python
import os

from holder.generated import AuthenticatedClient
from holder.generated.api.default import get_health
from holder.generated.models import HealthResponse

with AuthenticatedClient(
    base_url="http://127.0.0.1:11499",
    token=os.environ["HOLDER_TOKEN"],
    raise_on_unexpected_status=True,
) as client:
    response = get_health.sync_detailed(client=client)
    if isinstance(response.parsed, HealthResponse):
        print(response.parsed.data.server_version)
    else:
        print(response.status_code, response.parsed)
```

`Client` supports public endpoints such as `get_ping`. Endpoint modules expose
`sync`, `sync_detailed`, `asyncio` and `asyncio_detailed`; use `async with` for
asynchronous clients. Detailed responses retain status, headers, raw bytes and
the parsed response. Documented HTTP errors return an `ErrorResponse` when the
contract specifies one; `raise_on_unexpected_status` applies to undocumented
statuses. Transport errors propagate from HTTPX.

## Layout and regeneration

```text
openapi/                 Verbatim contract snapshot, provenance and generator config
src/holder/generated/    Generated transport, endpoint modules and models
scripts/generate.py      Regeneration and comparison against checked-in code
tests/                   Mock HTTP transport and contract coverage checks
```

Do not hand-edit `src/holder/generated`. It is isolated so we can replace it
with a handwritten implementation if this experiment is unsuitable.

```sh
# Regenerate using the checked-in snapshot; no sibling checkout needed.
python scripts/generate.py

# Compare generated output without changing files.
python scripts/generate.py --check

# Refresh after changes have been tested in the contract's owning repository.
python scripts/generate.py --source ../holder-daemon/openapi.yaml
```

The generator and Ruff versions are pinned in `pyproject.toml`. Generation runs
in a temporary directory and fails on warnings before replacing the package.
The provenance file records the daemon Git revision, whether the source schema
had uncommitted changes, its SHA-256 and tool versions. No schema transformations
or custom templates are used. The config treats YAML download responses as
plain text so their bodies are retained. CI checks generation, tests and builds
on Python 3.11 and 3.14.

## Initial findings

The current snapshot generates 105 endpoint modules and 239 model modules,
roughly 40,000 lines of Python. All operations are in `api.default` because the
contract supplies neither tags nor operation IDs; endpoint names follow HTTP
methods and paths. Models are attrs classes with `to_dict` / `from_dict`, enums,
and `UNSET` to distinguish omitted fields from explicit `None`. They are typed
containers, not comprehensive runtime validators.

The first generation exposed misplaced card PATCH and DELETE definitions in
the daemon's OpenAPI contract. Those definitions were moved from the AI-message
backlinks path to `/cards/{card_id}` in holder-daemon, with a regression test.
The checked-in snapshot includes that correction from the daemon's separate
`fix/openapi-card-mutation-paths` branch; provenance records its commit.

**Real-time streaming is the main gap.** The three event-stream operations
generate ordinary HTTP requests which buffer the entire body and return a
string. They do not yield individual events, reconnect or handle cancellation;
long-lived streams may hit the HTTPX timeout. Binary asset downloads are also
buffered in memory, although the bytes and headers are preserved. Streaming
would need a separately designed transport or handwritten implementation.

Local tests cover every contract operation's generated method/path, module
imports, bearer auth, query encoding, PATCH null/omission behavior, error
envelopes, YAML, buffered events, binary downloads and an async public request.
They use HTTPX's mock transport; live-daemon integration has not been tested.
