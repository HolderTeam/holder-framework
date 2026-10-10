"""High-level card moves preserve the daemon's placement rules."""

import json

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

from holder import Holder
from holder.exceptions import (
    APIError,
    AuthenticationError,
    ClosedError,
    ConnectionError,
    NotFoundError,
)


def moved():
    return ok(
        {
            "card_id": "c-0000",
            "parent_card_id": "c-0001",
            "sort_key": 42,
            "revision": 10,
        }
    )


@pytest.mark.parametrize(
    "argument,intent", [("parent", "into"), ("before", "before"), ("after", "after")]
)
def test_move_maps_intent_and_refreshes_card(argument, intent):
    requests = []
    changed = False

    def respond(request):
        nonlocal changed
        requests.append(request)
        if request.method == "POST":
            assert request.url.path == "/cards/c-0000/move"
            assert json.loads(request.content) == {
                "project_id": "p-0",
                "intent": intent,
                "target_card_id": "c-0001",
            }
            changed = True
            return moved()
        if request.url.path == "/projects/p-0":
            return ok(project_payload())
        if request.url.path == "/cards/c-0001":
            return ok(card_payload(1, content=True))
        data = card_payload(content=True)
        if changed:
            data.update(
                parent_card_id="c-0001",
                sort_key=42,
                updated_at=10,
                content="Fresh server content",
            )
        return ok(data)

    with holder_for(respond) as h:
        project = h.projects.get("p-0")
        card = project.cards.get("c-0000")
        target = project.cards.get("c-0001")
        assert card.move(**{argument: target}) is card
        assert card.parent_card_id == "c-0001"
        assert card.sort_key == 42
        assert card.updated_at == 10
        assert card.content == "Fresh server content"
        assert [r.method for r in requests[-2:]] == ["POST", "GET"]
    with pytest.raises(ClosedError):
        card.move(parent=target)


def test_move_argument_validation_does_not_write():
    def respond(request):
        assert request.method == "GET"
        if request.url.path.startswith("/projects/"):
            return ok(project_payload())
        return ok(card_payload(content=True))

    with holder_for(respond) as h:
        card = h.projects.get("p-0").cards.get("c-0000")
        for kwargs in (
            {},
            {"parent": card, "before": card},
            {"before": card, "after": card},
            {"parent": None},
            {"before": "c-0000"},
            {"after": 1},
        ):
            with pytest.raises(TypeError):
                card.move(**kwargs)


@pytest.mark.parametrize(
    "error", ["auth", "transport", "invalid", "scope", "missing", "conflict", "refresh"]
)
def test_move_write_failures_are_not_retried(monkeypatch, error):
    cli = mock_cli(monkeypatch)
    writes = []

    def respond(request):
        if request.method == "POST":
            writes.append(request)
            if error == "transport":
                raise httpx.ReadError("Interrupted", request=request)
            if error == "refresh":
                return moved()
            return failure(
                {
                    "auth": 401,
                    "invalid": 400,
                    "scope": 422,
                    "missing": 404,
                    "conflict": 409,
                }[error]
            )
        if request.url.path.startswith("/cards/"):
            return failure(404) if writes else ok(card_payload(content=True))
        return ok(project_payload())

    exception = {
        "auth": AuthenticationError,
        "transport": ConnectionError,
        "invalid": APIError,
        "scope": APIError,
        "missing": NotFoundError,
        "conflict": APIError,
        "refresh": NotFoundError,
    }[error]
    with Holder(transport=httpx.MockTransport(respond)) as h:
        card = h.projects.get("p-0").cards.get("c-0000")
        with pytest.raises(exception):
            card.move(parent=card)
        assert len(writes) == 1
        assert cli.call_count == 2
        assert card.parent_card_id is None
