# holder-python

Control your knowledge using Python. This is separate
from `holder-kit`, which provides native bindings for offline analysis.

This first iteration evaluates
[openapi-python-client](https://github.com/openapi-generators/openapi-python-client).
The generator is a development dependency;
installed clients only need HTTPX, attrs and typing-extensions.

## Setup

Requires Python 3.11 or newer. Run these commands from the `python/` directory of the
holder-framework repository.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest
python scripts/generate.py --check
python -m build
```

## Use Holder

`Holder()` discovers or starts your local daemon using `holderctl` on PATH.
Supply `url` and `token` together to connect explicitly instead.

```python
from holder import Holder

with Holder() as h:
    for project in h:  # also h.projects
        print(project.name)
        for card in project.cards:
            print(card.title)

    project = h.projects.filter(name="Research")[0]
    card = project.cards.get(card_id)
    card.update(title="A better title")
```

Collections fetch lazily and cache results as you iterate. Use `.all()` for an
independent query and `.refresh()` to discard cached results. Project filters are
`name` (substring), `updated_after`, and `updated_before`; card queries support
`.filter(tag="research")`, `.roots()`, and `card.children`. Tag filters combine
with hierarchy queries. Cards are always scoped to a project.
`get(id)` fetches directly; indexing accepts nonnegative integers.

Card bodies load when you read `card.content`. Explicit `.update(title=...,
content=...)` writes; attribute assignment does not. Both objects support
`.refresh()`. Iteration observes live data rather than a frozen snapshot, and its
cache grows with visited results. Context exit closes the client without stopping
the daemon. Failures raise exceptions from `holder.exceptions`.

## Use the low-level client

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
src/holder/events.py     Handwritten incremental asyncio change-feed transport
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

# Also verify the snapshot against the owning contract (used by CI).
python scripts/generate.py --check --source ../api/openapi.yaml

# Refresh after changes have been tested in the contract's owning repository.
python scripts/generate.py --source ../api/openapi.yaml
```

The generator and Ruff versions are pinned in `pyproject.toml`. Generation runs
in a temporary directory and fails on warnings before replacing the package.
The provenance file records the Framework Git revision, whether the source schema
had uncommitted changes, its SHA-256 and tool versions. No schema transformations
or custom templates are used. The config treats YAML download responses as
plain text so their bodies are retained. CI checks snapshot freshness against
`api/openapi.yaml`, generation, tests and builds
on Python 3.11 and 3.14.
