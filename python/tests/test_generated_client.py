"""Exercise generated transport and serialization without a live daemon."""

import ast
import asyncio
import hashlib
import importlib
import json
import pkgutil
import re
from pathlib import Path

import httpx
import pytest
from ruamel.yaml import YAML

from holder import generated
from holder.generated import AuthenticatedClient, Client
from holder.generated.api.default import (
    get_ai_runs_run_id_events,
    get_cards,
    get_health,
    get_openapi_yaml,
    get_ping,
    get_resources_resource_id_assets_asset_id_content,
    patch_cards_card_id,
)
from holder.generated.errors import UnexpectedStatus
from holder.generated.models import CardUpdateRequest, ErrorResponse, HealthResponse

ROOT = Path(__file__).resolve().parents[1]


def test_every_contract_operation_is_generated():
    schema = YAML(typ="safe").load((ROOT / "openapi/openapi.yaml").read_text())
    expected = {
        (method, re.sub(r"\{[^}]+\}", "{}", path))
        for path, operations in schema["paths"].items()
        for method in operations
        if method
        in {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
    }
    actual = set()
    for file in (ROOT / "src/holder/generated/api").rglob("*.py"):
        tree = ast.parse(file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                values = {
                    key.value: value
                    for key, value in zip(node.keys, node.values)
                    if isinstance(key, ast.Constant)
                }
                if "method" not in values or "url" not in values:
                    continue
                url = values["url"]
                if isinstance(url, ast.Call):
                    url = url.func.value
                # Python keywords may acquire a suffix (e.g. type -> type_).
                actual.add(
                    (values["method"].value, re.sub(r"\{[^}]+\}", "{}", url.value))
                )
    assert actual == expected


def test_snapshot_matches_provenance():
    provenance = json.loads((ROOT / "openapi/provenance.json").read_text())
    assert (
        hashlib.sha256((ROOT / "openapi/openapi.yaml").read_bytes()).hexdigest()
        == provenance["sha256"]
    )


def test_all_generated_modules_import():
    for module in pkgutil.walk_packages(generated.__path__, generated.__name__ + "."):
        importlib.import_module(module.name)


def test_authenticated_health_response():
    def respond(request):
        assert request.headers["Authorization"] == "Bearer test-token"
        assert request.url.path == "/health"
        return httpx.Response(
            200,
            json={
                "ok": True,
                "data": {
                    "db_ok": True,
                    "uptime_ms": 123,
                    "api_version": "0.1.0",
                    "server_version": "test",
                    "pid": 42,
                    "crypt_filter": {
                        "path": "/example/filter",
                        "exists": True,
                        "executable": True,
                    },
                },
            },
        )

    with AuthenticatedClient(
        base_url="http://127.0.0.1:11499",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(respond)},
    ) as client:
        response = get_health.sync_detailed(client=client)
    assert response.status_code == 200
    assert isinstance(response.parsed, HealthResponse)
    assert response.parsed.data.pid == 42


def test_card_query_and_error_envelope():
    def respond(request):
        assert request.url.params["project_id"] == "project & one"
        assert request.url.params["tag"] == "hello world"
        assert "parent_card_id" not in request.url.params
        return httpx.Response(
            401,
            json={
                "ok": False,
                "error": {
                    "code": "unauthorized",
                    "message": "Token required",
                },
            },
        )

    with Client(
        base_url="http://holder.test",
        httpx_args={
            "transport": httpx.MockTransport(respond),
        },
    ) as client:
        result = get_cards.sync(
            client=client, project_id="project & one", tag="hello world"
        )
    assert isinstance(result, ErrorResponse)
    assert result.error.code == "unauthorized"


def test_patch_preserves_omitted_and_explicit_null_fields():
    def respond(request):
        assert request.method == "PATCH"
        assert request.url.raw_path == b"/cards/card%2Fone"
        assert json.loads(request.content) == {"updated_at": 123, "title": None}
        return httpx.Response(
            401, json={"ok": False, "error": {"code": "auth", "message": "auth"}}
        )

    body = CardUpdateRequest(updated_at=123, title=None)
    assert CardUpdateRequest.from_dict(body.to_dict()).to_dict() == body.to_dict()
    with Client(
        base_url="http://holder.test",
        httpx_args={
            "transport": httpx.MockTransport(respond),
        },
    ) as client:
        patch_cards_card_id.sync("card/one", client=client, body=body)


@pytest.mark.parametrize(
    "endpoint,args,content_type,payload",
    [
        (get_openapi_yaml, (), "application/yaml", b"openapi: 3.0.3\n"),
        (
            get_ai_runs_run_id_events,
            ("run-1",),
            "text/event-stream",
            b"data: hello\n\ndata: done\n\n",
        ),
    ],
)
def test_text_responses_are_buffered(endpoint, args, content_type, payload):
    with Client(
        base_url="http://holder.test",
        httpx_args={
            "transport": httpx.MockTransport(
                lambda request: httpx.Response(
                    200,
                    content=payload,
                    headers={"Content-Type": content_type},
                )
            ),
        },
    ) as client:
        result = endpoint.sync_detailed(*args, client=client)
    assert result.content == payload
    assert result.parsed == payload.decode()


def test_binary_asset_preserves_bytes_and_headers():
    payload = b"\x00\xff\x80asset"
    with Client(
        base_url="http://holder.test",
        httpx_args={
            "transport": httpx.MockTransport(
                lambda request: httpx.Response(
                    200,
                    content=payload,
                    headers={"Content-Disposition": 'attachment; filename="asset.bin"'},
                )
            ),
        },
    ) as client:
        result = get_resources_resource_id_assets_asset_id_content.sync_detailed(
            "resource",
            "asset",
            client=client,
        )
    assert result.content == payload
    assert result.parsed.payload.read() == payload
    assert result.headers["Content-Disposition"] == 'attachment; filename="asset.bin"'


def test_unexpected_status_can_raise():
    with (
        Client(
            base_url="http://holder.test",
            raise_on_unexpected_status=True,
            httpx_args={
                "transport": httpx.MockTransport(
                    lambda request: httpx.Response(418, content=b"unexpected")
                ),
            },
        ) as client,
        pytest.raises(UnexpectedStatus),
    ):
        get_ping.sync(client=client)


def test_async_public_ping():
    async def run():
        def respond(request):
            assert "Authorization" not in request.headers
            return httpx.Response(200, text="pong")

        async with Client(
            base_url="http://holder.test",
            httpx_args={
                "transport": httpx.MockTransport(respond),
            },
        ) as client:
            result = await get_ping.asyncio(client=client)
            assert result.value == "pong"

    asyncio.run(run())
