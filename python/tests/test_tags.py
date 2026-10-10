"""Tag collections use daemon data and project-scoped mutations."""

import json
from dataclasses import FrozenInstanceError

import httpx
import pytest
from test_library import (
    card_payload,
    failure,
    holder_for,
    mock_cli,
    ok,
    project_payload,
)

from holder import Holder, Tag
from holder.exceptions import (
    APIError,
    AuthenticationError,
    ClosedError,
    ConnectionError,
    NotFoundError,
    ProtocolError,
)
from holder.models.tag import TagCollection


def tagged_card(names):
    return {**card_payload(content=True), "tags": names}


def test_lazy_tag_collections_lookup_cache_and_reverse_cards():
    requests = []

    def respond(request):
        requests.append(request)
        path = request.url.path
        if path == "/projects/p-0/tags":
            return ok(
                [
                    {"tag": "research", "card_count": 2},
                    {"tag": "draft", "card_count": 1},
                ]
            )
        if path == "/projects/p-0/cards":
            assert request.url.params["tag"] == "research"
            assert request.url.params["parent"] == "roots"
            return ok({"items": [card_payload()], "next_cursor": None})
        if path.startswith("/cards/"):
            return ok(tagged_card(["research", "draft"]))
        return ok(project_payload())

    with holder_for(respond) as h:
        project = h.projects.get("p-0")
        card = project.cards.get("c-0000")
        assert isinstance(project.tags, TagCollection)
        assert isinstance(card.tags, TagCollection)
        assert len(requests) == 2
        tags = list(project.tags)
        assert [t.name for t in tags] == ["research", "draft"]
        assert tags[0].card_count == 2
        assert isinstance(tags[0], Tag)
        assert tags[0].project_id == project.id
        with pytest.raises(FrozenInstanceError):
            tags[0].name = "Changed"
        assert project.tags[0] is tags[0]
        assert len(requests) == 3
        assert project.tags.get("research").card_count == 2
        assert tags[0].refresh() is tags[0]
        assert [t.name for t in card.tags] == ["research", "draft"]
        assert card.tags[0].card_count is None
        assert card.tags[0].cards.roots()[0].project_id == project.id
        assert card.tags.get("draft").name == "draft"
        with pytest.raises(NotFoundError):
            project.tags.get("missing")
        with pytest.raises(TypeError):
            project.tags.get(None)
        assert not hasattr(project.tags, "add")
        with pytest.raises(IndexError):
            card.tags[2]
    with pytest.raises(ClosedError):
        list(card.tags)


@pytest.mark.parametrize("method", ["add", "remove"])
def test_tag_mutations_send_scope_and_input_unchanged_and_refresh(method):
    names = ["draft"]
    requests = []
    content = "Old content"

    def respond(request):
        nonlocal content
        requests.append(request)
        if request.url.path.endswith("/tags"):
            assert request.method == ("POST" if method == "add" else "DELETE")
            assert json.loads(request.content) == {
                "project_id": "p-0",
                "tag": "Research",
            }
            names[:] = ["research"]
            content = "Server content\n#research"
            return ok(
                {
                    "card_id": "c-0000",
                    "tag": "research",
                    "outcome": "added" if method == "add" else "removed",
                    "changed": True,
                }
            )
        if request.url.path.startswith("/cards/"):
            return ok(
                {**tagged_card(list(names)), "content": content, "updated_at": 10}
            )
        return ok(project_payload())

    with holder_for(respond) as h:
        card = h.projects.get("p-0").cards.get("c-0000")
        tags = card.tags
        assert [t.name for t in tags] == ["draft"]
        active = iter(tags)
        next(active)
        assert getattr(tags, method)("Research") is tags
        assert card.content == "Server content\n#research"
        assert card.updated_at == 10
        assert [t.name for t in tags] == ["research"]
        with pytest.raises(RuntimeError):
            next(active)
        assert sum(r.method in ("POST", "DELETE") for r in requests) == 1
        with pytest.raises(TypeError):
            getattr(tags, method)(None)
    with pytest.raises(ClosedError):
        getattr(tags, method)("research")


@pytest.mark.parametrize("tags", [None, "research", [1], [""]])
def test_invalid_or_missing_tag_data_is_not_an_empty_collection(tags):
    def respond(request):
        if request.url.path.startswith("/cards/"):
            return ok(tagged_card(tags))
        return ok(project_payload())

    with holder_for(respond) as h, pytest.raises(ProtocolError):
        list(h.projects.get("p-0").cards.get("c-0000").tags)


def test_tag_read_rejects_card_moved_to_another_project():
    calls = 0

    def respond(request):
        nonlocal calls
        if request.url.path.startswith("/cards/"):
            calls += 1
            return ok({**tagged_card([]), "project_id": "p-0" if calls == 1 else "p-1"})
        return ok(project_payload())

    with holder_for(respond) as h:
        card = h.projects.get("p-0").cards.get("c-0000")
        with pytest.raises(NotFoundError):
            list(card.tags)


@pytest.mark.parametrize("method", ["add", "remove"])
@pytest.mark.parametrize(
    "error", ["auth", "transport", "invalid", "scope", "missing", "refresh"]
)
def test_tag_writes_are_not_retried(monkeypatch, method, error):
    cli = mock_cli(monkeypatch)
    writes = []

    def respond(request):
        if request.method in ("POST", "DELETE"):
            writes.append(request)
            if error == "transport":
                raise httpx.ReadError("Interrupted", request=request)
            if error != "refresh":
                return failure(
                    {"auth": 401, "invalid": 400, "scope": 422, "missing": 404}[error]
                )
            return ok(
                {
                    "card_id": "c-0000",
                    "tag": "research",
                    "outcome": "added",
                    "changed": True,
                }
            )
        if request.url.path.startswith("/cards/"):
            return failure(404) if writes else ok(tagged_card(["draft"]))
        return ok(project_payload())

    exception = {
        "auth": AuthenticationError,
        "transport": ConnectionError,
        "invalid": APIError,
        "scope": APIError,
        "missing": NotFoundError,
        "refresh": NotFoundError,
    }[error]
    with Holder(transport=httpx.MockTransport(respond)) as h:
        card = h.projects.get("p-0").cards.get("c-0000")
        assert card.tags[0].name == "draft"
        with pytest.raises(exception):
            getattr(card.tags, method)("research")
        assert len(writes) == 1
        assert cli.call_count == 2
        if error == "refresh":
            with pytest.raises(NotFoundError):
                list(card.tags)


def test_content_update_invalidates_cached_tags():
    names = ["draft"]

    def respond(request):
        if request.method == "PATCH":
            names.clear()
            return ok({"card_id": "c-0000"})
        if request.url.path.startswith("/cards/"):
            return ok(tagged_card(list(names)))
        return ok(project_payload())

    with holder_for(respond) as h:
        card = h.projects.get("p-0").cards.get("c-0000")
        assert card.tags[0].name == "draft"
        card.update(content="No tags")
        assert list(card.tags) == []
