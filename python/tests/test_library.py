"""Public synchronous API behaviour with a simulated daemon contract."""

import json
import subprocess
from dataclasses import FrozenInstanceError
from unittest.mock import Mock

import httpx
import pytest

from holder import Card, Holder, Project
from holder.exceptions import (
    APIError,
    AuthenticationError,
    ClosedError,
    ConnectionError,
    NotFoundError,
    ProtocolError,
)


def project_payload(index=0):
    return {
        "project_id": f"p-{index}",
        "name": f"Project {index}",
        "root_path": f"/p/{index}",
        "privacy_mode": "plain",
        "created_at": 1,
        "updated_at": 2,
        "sync": {
            "last_commit_at": None,
            "last_push_at": None,
            "last_pull_at": None,
            "uncommitted_changes_count": 0,
            "unpushed_commits_count": 0,
            "last_push_status": None,
            "last_pull_status": None,
            "last_sync_error": None,
            "last_sync_error_at": None,
            "retry_count": 0,
            "next_retry_at": None,
            "pull_retry_count": 0,
            "next_pull_retry_at": None,
            "updated_at": None,
        },
    }


def card_payload(index=0, project_id="p-0", content=False):
    result = {
        "card_id": f"c-{index:04}",
        "project_id": project_id,
        "title": f"Card {index}",
        "rel_path": f"c/{index}.md",
        "sort_key": 0,
        "created_at": 1,
        "updated_at": 2,
        "parent_card_id": None,
        "deleted_at": None,
    }
    if content:
        result["content"] = "current body"
    return result


def ok(data):
    return httpx.Response(200, json={"ok": True, "data": data})


def failure(status):
    return httpx.Response(
        status,
        json={"ok": False, "error": {"code": "failure", "message": "Request failed"}},
    )


def holder_for(handler):
    return Holder(
        url="http://holder.test",
        token="secret-token",
        transport=httpx.MockTransport(handler),
    )


def test_lazy_projects_pages_cache_queries_indexing_and_close():
    requests = []

    def respond(request):
        requests.append(request)
        assert request.headers["Authorization"] == "Bearer secret-token"
        if request.url.path.startswith("/projects/"):
            return ok(project_payload(7))
        offset = int(request.url.params["offset"])
        assert request.url.params["limit"] == "100"
        return ok([project_payload(i) for i in range(offset, min(offset + 100, 205))])

    h = holder_for(respond)
    with pytest.raises(ClosedError):
        next(iter(h))
    with h:
        assert requests == []
        filtered = h.projects.filter(name="Thing").filter(updated_after=10)
        assert requests == []
        assert h.projects[0].id == "p-0"
        assert len(requests) == 1
        assert len(list(h)) == 205
        assert len(requests) == 3
        assert len(list(h.projects)) == 205
        assert h.projects[204].id == "p-204"
        assert len(requests) == 3
        assert isinstance(h.projects.get("p-7"), Project)
        assert len(list(filtered)) == 205
        assert requests[-1].url.params["name"] == "Thing"
        assert requests[-1].url.params["updated_after"] == "10"
        assert len(list(filtered.all())) == 205
        h.projects.refresh()
        assert h.projects[0].id == "p-0"
        with pytest.raises(IndexError):
            h.projects[205]
        with pytest.raises(IndexError):
            h.projects[-1]
        with pytest.raises(TypeError):
            h.projects[:2]
        with pytest.raises(TypeError):
            h.projects.filter(unknown=True)
        assert not hasattr(h, "cards")
        client = h._active().get_httpx_client()
    assert client.is_closed
    with pytest.raises(ClosedError):
        h.projects[0]
    with pytest.raises(ClosedError):
        h.__enter__()


def test_cards_paginate_and_metadata_does_not_fetch_content():
    requests = []

    def respond(request):
        requests.append(request)
        if request.url.path.startswith("/projects") and not request.url.path.endswith(
            "/cards"
        ):
            return ok(project_payload())
        if request.url.path.startswith("/cards/"):
            return ok(card_payload(content=True))
        assert request.url.path == "/projects/p-0/cards"
        after = request.url.params.get("cursor")
        start = 0 if after is None else int(after)
        stop = min(start + 200, 401)
        return ok(
            {
                "items": [card_payload(i) for i in range(start, stop)],
                "next_cursor": str(stop) if stop < 401 else None,
            }
        )

    with holder_for(respond) as h:
        project = h.projects.get("p-0")
        cards = list(project.cards)
        assert len(cards) == 401
        assert isinstance(cards[0], Card)
        assert [r.url.params.get("cursor") for r in requests[1:]] == [
            None,
            "200",
            "400",
        ]
        assert len(requests) == 4
        assert cards[0].content == "current body"
        assert cards[0].content == "current body"
        assert len(requests) == 5
        assert cards[0].title == "Card 0"
        with pytest.raises(FrozenInstanceError):
            cards[0].title = "implicit write"
        assert len(list(project.cards)) == 401
        assert len(requests) == 5


def test_scoped_navigation_queries_membership_and_refresh():
    requests = []

    def respond(request):
        requests.append(request)
        if request.url.path.startswith("/projects") and not request.url.path.endswith(
            "/cards"
        ):
            return ok(project_payload())
        if request.url.path.startswith("/cards/"):
            return ok(
                card_payload(
                    project_id="p-other"
                    if request.url.path.endswith("foreign")
                    else "p-0",
                    content=True,
                )
            )
        return ok({"items": [card_payload()], "next_cursor": None})

    with holder_for(respond) as h:
        project = h.projects.get("p-0")
        tagged = project.cards.filter(tag="research").filter(tag="other")
        assert tagged[0].id == "c-0000"
        assert requests[-1].url.params["tag"] == "other"
        assert "cursor" not in requests[-1].url.params
        card = project.cards.roots()[0]
        assert requests[-1].url.params["parent"] == "roots"
        assert card.children[0].id == "c-0000"
        assert requests[-1].url.params["parent"] == card.id
        with pytest.raises(NotFoundError):
            project.cards.get("foreign")
        assert tagged.roots()[0].id == card.id
        assert requests[-1].url.params["tag"] == "other"
        assert requests[-1].url.params["parent"] == "roots"
        assert project.cards.roots().filter(tag="research")[0].id == card.id
        assert requests[-1].url.params["tag"] == "research"
        assert requests[-1].url.params["parent"] == "roots"
        project.refresh()
        card.refresh()
        assert card.content == "current body"


def test_update_fetches_fresh_body_and_refreshes_after_write():
    requests = []
    title = "Original"

    def respond(request):
        nonlocal title
        requests.append(request)
        if request.url.path.startswith("/projects") and not request.url.path.endswith(
            "/cards"
        ):
            return ok(project_payload())
        if request.method == "PATCH":
            body = json.loads(request.content)
            assert body["content"] == "current body"
            assert isinstance(body["updated_at"], int) and body["updated_at"] > 2
            title = body["title"]
            return ok({"card_id": "c-0000"})
        return ok({**card_payload(content=True), "title": title})

    with holder_for(respond) as h:
        card = h.projects.get("p-0").cards.get("c-0000")
        requests.clear()
        assert card.update(title="Better") is card
        assert [r.method for r in requests] == ["GET", "PATCH", "GET"]
        assert card.title == "Better"
        with pytest.raises(TypeError):
            card.update()
        with pytest.raises(TypeError):
            card.update(content=None)


def test_content_only_update_preserves_omitted_title():
    def respond(request):
        if request.url.path.startswith("/projects") and not request.url.path.endswith(
            "/cards"
        ):
            return ok(project_payload())
        if request.method == "PATCH":
            assert json.loads(request.content)["content"] == "replacement"
            assert "title" not in json.loads(request.content)
            return ok({"card_id": "c-0000"})
        return ok(card_payload(content=True))

    with holder_for(respond) as h:
        h.projects.get("p-0").cards.get("c-0000").update(content="replacement")


@pytest.mark.parametrize(
    "status,error",
    [
        (401, AuthenticationError),
        (404, NotFoundError),
        (400, APIError),
        (503, APIError),
    ],
)
def test_api_errors(status, error):
    with holder_for(lambda request: failure(status)) as h:
        with pytest.raises(error) as caught:
            h.projects.get("missing")
        assert caught.value.status == status
        assert caught.value.code == "failure"
        assert caught.value.message == "Request failed"


def test_protocol_empty_and_transport_errors():
    with holder_for(lambda request: ok([])) as h:
        assert list(h.projects) == []
        with pytest.raises(IndexError):
            h.projects[0]
    with (
        holder_for(lambda request: httpx.Response(200, text="not JSON")) as h,
        pytest.raises(ProtocolError),
    ):
        h.projects.get("p")

    def offline(request):
        raise httpx.ConnectError("token=secret-token", request=request)

    with holder_for(offline) as h:
        with pytest.raises(ConnectionError) as caught:
            h.projects.get("p")
        assert "secret-token" not in str(caught.value)


def mock_cli(monkeypatch, result=None):
    runner = Mock(
        side_effect=lambda command, **kwargs: subprocess.CompletedProcess(
            command,
            0,
            "credential\n"
            if command[1] == "token"
            else json.dumps(
                result or {"ok": True, "daemon": {"url": "http://holder.test"}}
            ),
        )
    )
    monkeypatch.setattr("holder.library.subprocess.run", runner)
    return runner


def test_local_discovery_and_read_credential_refresh(monkeypatch):
    cli = mock_cli(monkeypatch)
    requests = []

    def respond(request):
        requests.append(request)
        return failure(401) if len(requests) == 1 else ok(project_payload())

    with Holder(
        transport=httpx.MockTransport(respond), holderctl="/test/holderctl"
    ) as h:
        assert "credential" not in repr(h)
        assert h.projects.get("p-0").name == "Project 0"
        assert len(requests) == 2
        assert cli.call_count == 4
        assert cli.call_args_list[0].args[0] == [
            "/test/holderctl",
            "ensure",
            "--json",
            "--api-min",
            "0.1",
            "--api-max-exclusive",
            "1.0",
        ]


def test_no_retry_of_write_or_explicit_credentials(monkeypatch):
    cli = mock_cli(monkeypatch)
    writes = []

    def respond(request):
        if request.url.path.startswith("/projects") and not request.url.path.endswith(
            "/cards"
        ):
            return ok(project_payload())
        if request.method == "PATCH":
            writes.append(request)
            return failure(401)
        return ok(card_payload(content=True))

    with Holder(transport=httpx.MockTransport(respond)) as h:
        with pytest.raises(AuthenticationError):
            h.projects.get("p-0").cards.get("c-0000").update(title="Better")
        assert len(writes) == 1
        assert cli.call_count == 2
    cli.reset_mock()
    with holder_for(lambda request: failure(401)) as h:
        with pytest.raises(AuthenticationError):
            h.projects.get("p")
        cli.assert_not_called()


@pytest.mark.parametrize(
    "failure_mode", ["missing", "timeout", "exit", "json", "details", "empty_token"]
)
def test_discovery_errors_do_not_expose_credentials(monkeypatch, failure_mode):
    def run(command, **kwargs):
        if failure_mode == "missing":
            raise FileNotFoundError("secret-token")
        if failure_mode == "timeout":
            raise subprocess.TimeoutExpired(command, 65, output="secret-token")
        result = {"ok": True, "daemon": {"url": "http://holder.test"}}
        text = (
            "secret-token"
            if failure_mode == "json"
            else json.dumps({} if failure_mode == "details" else result)
        )
        return subprocess.CompletedProcess(
            command,
            1 if failure_mode == "exit" else 0,
            "" if command[1] == "token" else text,
            "secret-token",
        )

    monkeypatch.setattr("holder.library.subprocess.run", run)
    with pytest.raises(ConnectionError) as caught, Holder():
        pass
    assert "secret-token" not in str(caught.value)


def test_url_and_token_are_a_pair():
    with pytest.raises(ValueError):
        Holder(url="http://remote")
    with pytest.raises(ValueError):
        Holder(token="secret-token")


def test_independent_iterators_and_refresh_invalidates_active_iteration():
    requests = []

    def respond(request):
        requests.append(request)
        return ok([project_payload(0), project_payload(1)])

    with holder_for(respond) as h:
        first, second = iter(h), iter(h)
        assert next(first).id == "p-0"
        assert next(second).id == "p-0"
        assert next(first).id == "p-1"
        assert next(second).id == "p-1"
        assert len(requests) == 1
        h.projects.refresh()
        with pytest.raises(RuntimeError, match="refreshed"):
            next(first)
        assert h.projects[0].id == "p-0"
        assert len(requests) == 2


def test_foreign_card_listing_is_rejected_before_caching():
    def respond(request):
        return (
            ok(project_payload())
            if request.url.path.startswith("/projects")
            and not request.url.path.endswith("/cards")
            else ok(
                {"items": [card_payload(project_id="foreign")], "next_cursor": None}
            )
        )

    with (
        holder_for(respond) as h,
        pytest.raises(ProtocolError, match="another project"),
    ):
        h.projects.get("p-0").cards[0]


def test_update_never_writes_a_card_that_changed_project():
    gets = []
    writes = []

    def respond(request):
        if request.url.path.startswith("/projects") and not request.url.path.endswith(
            "/cards"
        ):
            return ok(project_payload())
        if request.method == "PATCH":
            writes.append(request)
        gets.append(request)
        return ok(
            card_payload(
                project_id="p-0" if len(gets) == 1 else "foreign", content=True
            )
        )

    with holder_for(respond) as h:
        card = h.projects.get("p-0").cards.get("c-0000")
        with pytest.raises(NotFoundError):
            card.update(title="Wrong project")
        assert writes == []


def test_title_update_preserves_body_changed_since_card_was_loaded():
    current_body = "old body"

    def respond(request):
        nonlocal current_body
        if request.url.path.startswith("/projects") and not request.url.path.endswith(
            "/cards"
        ):
            return ok(project_payload())
        if request.method == "PATCH":
            assert json.loads(request.content)["content"] == "new body"
            return ok({"card_id": "c-0000"})
        return ok({**card_payload(content=True), "content": current_body})

    with holder_for(respond) as h:
        card = h.projects.get("p-0").cards.get("c-0000")
        assert card.content == "old body"
        current_body = "new body"
        card.update(title="Better")
        assert card.content == "new body"


def test_local_restart_updates_origin_and_credentials_without_reopening_transport(
    monkeypatch,
):
    results = iter(
        [
            {"ok": True, "daemon": {"url": "http://old.test"}},
            "old-token",
            {"ok": True, "daemon": {"url": "http://new.test"}},
            "new-token",
        ]
    )

    def run(command, **kwargs):
        value = next(results)
        return subprocess.CompletedProcess(
            command, 0, value if isinstance(value, str) else json.dumps(value)
        )

    monkeypatch.setattr("holder.library.subprocess.run", run)

    class Transport(httpx.MockTransport):
        closed = False

        def close(self):
            self.closed = True

    def respond(request):
        assert not transport.closed
        if request.url.host == "old.test":
            assert request.headers["Authorization"] == "Bearer old-token"
            return failure(401)
        assert request.url.host == "new.test"
        assert request.headers["Authorization"] == "Bearer new-token"
        return ok(project_payload())

    transport = Transport(respond)
    with Holder(transport=transport) as h:
        assert h.projects.get("p-0").id == "p-0"
    assert transport.closed


@pytest.mark.parametrize("query_kind", ["tag", "roots", "children"])
def test_filtered_card_collections_follow_continuation(query_kind):
    requests = []

    def respond(request):
        if request.url.path == "/projects/p-0":
            return ok(project_payload())
        if request.url.path == "/cards/c-0000":
            return ok(card_payload(content=True))
        assert request.url.path == "/projects/p-0/cards"
        requests.append(request)
        assert request.url.params["tag"] == "research"
        if query_kind == "roots":
            assert request.url.params["parent"] == "roots"
        elif query_kind == "children":
            assert request.url.params["parent"] == "c-0000"
        cursor = request.url.params.get("cursor")
        return ok(
            {
                "items": [card_payload(0 if cursor is None else 1)],
                "next_cursor": "continuation" if cursor is None else None,
            }
        )

    with holder_for(respond) as h:
        project = h.projects.get("p-0")
        query = project.cards
        if query_kind == "roots":
            query = query.roots()
        elif query_kind == "children":
            query = query.get("c-0000").children
        assert [card.id for card in query.filter(tag="research")] == [
            "c-0000",
            "c-0001",
        ]
        assert len(requests) == 2
        assert requests[1].url.params["cursor"] == "continuation"


@pytest.mark.parametrize(
    "items,cursor", [([], "more"), ([card_payload()], ""), ([card_payload()], "same")]
)
def test_invalid_card_continuation_is_rejected(items, cursor):
    def respond(request):
        if request.url.path == "/projects/p-0":
            return ok(project_payload())
        return ok({"items": items, "next_cursor": cursor})

    with holder_for(respond) as h:
        collection = h.projects.get("p-0").cards
        if cursor == "same":
            collection._next = "same"
        with pytest.raises(ProtocolError, match="did not advance"):
            list(collection)
