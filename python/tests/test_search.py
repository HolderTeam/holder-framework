"""Lazy card search and access to full project-scoped cards."""

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

from holder import CardSearchResult, Holder
from holder.exceptions import (
    APIError,
    ClosedError,
    ConnectionError,
    NotFoundError,
    ProtocolError,
)


def search_payload(index=0):
    return {
        "card_id": f"c-{index:04}",
        "title": f"Search title {index}",
        "created_at": 1,
        "updated_at": 2,
        "snippet": "Some [research] notes",
        "rank": -1.0 / (index + 1),
    }


def test_lazy_search_pages_cache_clone_and_full_card_access():
    requests = []
    query = '  "research notes" OR café  '

    def respond(request):
        requests.append(request)
        if request.url.path == "/projects/p-0":
            return ok(project_payload())
        if request.url.path.startswith("/cards/"):
            assert request.url.path == "/cards/c-0000"
            return ok(card_payload(content=True))
        assert request.url.path == "/search/cards"
        assert request.url.params["project_id"] == "p-0"
        assert request.url.params["q"] == query
        assert request.url.params["limit"] == "100"
        offset = int(request.url.params["offset"])
        return ok([search_payload(i) for i in range(offset, min(offset + 100, 205))])

    with holder_for(respond) as h:
        results = h.projects.get("p-0").cards.search(query)
        assert len(requests) == 1
        first = results[0]
        assert isinstance(first, CardSearchResult)
        assert first.title == "Search title 0"
        assert first.snippet == "Some [research] notes"
        assert first.rank == -1
        assert first.created_at == 1
        assert first.updated_at == 2
        with pytest.raises(FrozenInstanceError):
            first.snippet = "Changed"
        assert len(requests) == 2
        rows = list(results)
        assert len(rows) == 205
        assert [r.card_id for r in rows] == [f"c-{i:04}" for i in range(205)]
        assert next(iter(results)) is first
        assert [r.url.params["offset"] for r in requests[1:]] == ["0", "100", "200"]
        assert first.card.id == first.card_id
        assert first.card.content == "current body"
        assert (
            first.card.title == "Card 0"
        )  # A live card can differ from search metadata.
        assert first.card is first.card
        assert len(requests) == 5
        clone = results.all()
        assert clone[0] is not first
        assert results[0] is first
        assert results.refresh()[0] is not first
    with pytest.raises(ClosedError):
        list(results)
    with pytest.raises(ClosedError):
        _ = rows[1].card


@pytest.mark.parametrize("count", [0, 100])
def test_empty_and_exact_page_search_termination(count):
    offsets = []

    def respond(request):
        if request.url.path == "/projects/p-0":
            return ok(project_payload())
        offset = int(request.url.params["offset"])
        offsets.append(offset)
        return ok([search_payload(i) for i in range(offset, count)])

    with holder_for(respond) as h:
        results = h.projects.get("p-0").cards.search("research")
        assert len(list(results)) == count
        assert offsets == ([0] if count == 0 else [0, 100])
        with pytest.raises(IndexError):
            results[count]


def test_search_validation_rejects_unsupported_filters_without_requests():
    def respond(request):
        assert request.url.path == "/projects/p-0"
        return ok(project_payload())

    with holder_for(respond) as h:
        cards = h.projects.get("p-0").cards
        with pytest.raises(TypeError):
            cards.search(None)
        for query in ("", " \n\t"):
            with pytest.raises(ValueError):
                cards.search(query)
        for filtered in (cards.filter(tag="research"), cards.roots()):
            with pytest.raises(ValueError, match="filters"):
                filtered.search("research")
        assert cards.all().search("research") is not None


@pytest.mark.parametrize("error", ["invalid", "unavailable", "transport", "malformed"])
def test_search_errors_are_reported_on_iteration(error):
    def respond(request):
        if request.url.path == "/projects/p-0":
            return ok(project_payload())
        if error == "transport":
            raise httpx.ReadError("Interrupted", request=request)
        if error == "malformed":
            return ok([{"card_id": "c-0000"}])
        return failure(400 if error == "invalid" else 501)

    exception = {
        "invalid": APIError,
        "unavailable": APIError,
        "transport": ConnectionError,
        "malformed": ProtocolError,
    }[error]
    with holder_for(respond) as h:
        results = h.projects.get("p-0").cards.search("research")
        with pytest.raises(exception):
            next(iter(results))


@pytest.mark.parametrize("foreign", [False, True])
def test_result_card_access_checks_live_membership_and_deletion(foreign):
    def respond(request):
        if request.url.path == "/projects/p-0":
            return ok(project_payload())
        if request.url.path == "/search/cards":
            return ok([search_payload()])
        return (
            ok(card_payload(project_id="p-1", content=True))
            if foreign
            else failure(404)
        )

    with holder_for(respond) as h:
        result = h.projects.get("p-0").cards.search("research")[0]
        with pytest.raises(NotFoundError):
            _ = result.card


def test_search_refreshes_local_credentials_without_losing_query(monkeypatch):
    cli = mock_cli(monkeypatch)
    attempts = 0

    def respond(request):
        nonlocal attempts
        if request.url.path == "/projects/p-0":
            return ok(project_payload())
        assert dict(request.url.params) == {
            "project_id": "p-0",
            "q": "research",
            "limit": "100",
            "offset": "0",
        }
        attempts += 1
        return failure(401) if attempts == 1 else ok([search_payload()])

    with Holder(transport=httpx.MockTransport(respond)) as h:
        assert h.projects.get("p-0").cards.search("research")[0].card_id == "c-0000"
        assert attempts == 2
        assert cli.call_count == 4
