"""Opt-in integration against an isolated, disposable holderd process.

Set HOLDER_TEST_DAEMON to a built holderd executable. This never uses the user's
normal daemon, database, or projects.
"""

import json
import os
import subprocess
import time
from pathlib import Path

import httpx
import pytest

from holder import Holder
from holder.exceptions import APIError, NotFoundError

DAEMON = os.environ.get("HOLDER_TEST_DAEMON")
pytestmark = pytest.mark.skipif(
    not DAEMON, reason="Set HOLDER_TEST_DAEMON for live integration"
)


@pytest.fixture
def daemon(tmp_path, monkeypatch):
    binary = Path(DAEMON).resolve()
    for variable, directory in (
        ("XDG_DATA_HOME", "data"),
        ("XDG_CONFIG_HOME", "config"),
        ("XDG_CACHE_HOME", "cache"),
        ("HOLDER_PROJECTS_ROOT", "projects"),
        ("HOLDER_TEST_KEYSTORE_DIR", "keystore"),
    ):
        monkeypatch.setenv(variable, str(tmp_path / directory))
    # An explicit cwd supplies schema/catalog resources in source-development builds.
    cwd = os.environ.get("HOLDER_TEST_DAEMON_CWD", str(binary.parent.parent))
    with (tmp_path / "daemon.log").open("w") as log:
        process = subprocess.Popen(
            [str(binary), "--bind", "127.0.0.1", "--port", "0"],
            cwd=cwd,
            stdout=log,
            stderr=log,
        )
        try:
            info_path = tmp_path / "data/holder/server/holder.json"
            deadline = time.monotonic() + 15
            while True:
                if process.poll() is not None:
                    pytest.fail("Disposable daemon exited during startup")
                try:
                    info = json.loads(info_path.read_text())
                    url = f"http://127.0.0.1:{info['port']}"
                    token = info["auth_token"]
                    with httpx.Client(
                        base_url=url,
                        headers={"Authorization": f"Bearer {token}"},
                        timeout=2,
                    ) as probe:
                        if probe.get("/health").status_code == 200:
                            break
                except (OSError, ValueError, KeyError, httpx.TransportError):
                    pass
                if time.monotonic() >= deadline:
                    pytest.fail("Disposable daemon did not become healthy")
                time.sleep(0.05)
            with httpx.Client(
                base_url=url, headers={"Authorization": f"Bearer {token}"}, timeout=10
            ) as raw:
                yield url, token, raw, binary.parent / "holderctl"
        finally:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def create_project(raw, name):
    response = raw.post("/projects", json={"name": name, "privacy_mode": "plain"})
    assert response.status_code == 201
    return response.json()["data"]["project_id"]


def create_card(raw, project_id, index, parent=None):
    response = raw.post(
        "/cards",
        json={
            "project_id": project_id,
            "title": f"Card {index}",
            "content": f"body {index}\n#research",
            "parent_card_id": parent,
        },
    )
    assert response.status_code == 201
    return response.json()["data"]["card_id"]


def test_create_read_edit_workflow_against_daemon(daemon):
    url, token, _, _ = daemon
    with Holder(url=url, token=token) as h:
        project = h.projects.create(name="Python workflow", privacy_mode="plain")
        assert project.id
        assert project.root_path
        assert project.created_at > 0
        assert h.projects.get(project.id).name == "Python workflow"
        assert list(project.cards) == []
        card = project.cards.create(title="Research", content="Notes\n#research")
        child = card.children.create(title="Follow-up")
        sibling = project.cards.roots().create(title="Another root")
        assert card.parent_card_id is None
        assert child.parent_card_id == card.id
        assert child.content == ""
        assert sibling.sort_key > card.sort_key
        assert list(project.cards) == []
        assert {c.id for c in project.cards.refresh()} == {
            card.id,
            child.id,
            sibling.id,
        }
        assert {c.id for c in project.cards.roots()} == {card.id, sibling.id}
        assert [c.id for c in card.children] == [child.id]
        assert [c.id for c in project.cards.filter(tag="Research")] == [card.id]
        assert child.update(title="Next step", content="More notes") is child
        assert project.cards.get(child.id).content == "More notes"
        assert child.title == "Next step"
        assert project.update(name="Renamed Python workflow") is project
        assert h.projects.get(project.id).name == "Renamed Python workflow"
        project.refresh()
        assert len(list(project.cards.all())) == 3
        assert len(list(project.cards.roots())) == 2


def test_tag_collections_and_body_mentions_against_daemon(daemon):
    url, token, _, _ = daemon
    with Holder(url=url, token=token) as h:
        project = h.projects.create(name="Python tags", privacy_mode="plain")
        other = h.projects.create(name="Other tags", privacy_mode="plain")
        card = project.cards.create(
            title="Tagged card", content="An inline #body mention.\n\n#draft"
        )
        sibling = project.cards.create(title="Related", content="Related notes")
        foreign = other.cards.create(title="Foreign", content="Foreign notes")
        assert {t.name for t in card.tags} == {"body", "draft"}
        assert {t.name for t in project.tags} == {"body", "draft"}
        cached_project_tags = project.tags
        card.tags.add("Research")
        sibling.tags.add("RESEARCH")
        foreign.tags.add("research")
        assert {t.name for t in card.tags} == {"body", "draft", "research"}
        assert "#research" in card.content
        assert {t.name for t in cached_project_tags} == {"body", "draft"}
        tag = project.tags.get("research")
        assert tag.card_count == 2
        assert tag.project_id == project.id
        assert {c.id for c in tag.cards} == {card.id, sibling.id}
        assert project.tags.refresh()[0].name == "research"
        assert {c.id for c in card.tags.get("research").cards} == {card.id, sibling.id}
        before = card.content
        card.tags.add("research")
        assert card.content == before
        card.tags.remove("DRAFT")
        assert {t.name for t in card.tags} == {"body", "research"}
        card.tags.remove("missing")
        before = card.content
        card.tags.remove("body")
        assert card.content == before
        assert {t.name for t in card.tags} == {"body", "research"}
        card.tags.remove("research")
        assert [t.name for t in card.tags] == ["body"]
        assert tag.refresh().card_count == 1
        assert {c.id for c in tag.cards.refresh()} == {sibling.id}
        card.update(content="The user removed the inline mention.")
        assert list(card.tags) == []


def test_card_moves_against_daemon(daemon):
    url, token, raw, _ = daemon
    with Holder(url=url, token=token) as h:
        project = h.projects.create(name="Python moves", privacy_mode="plain")
        other = h.projects.create(name="Other moves", privacy_mode="plain")
        parent = project.cards.create(title="Parent")
        target = parent.children.create(title="Target")
        root = project.cards.create(title="Root")
        card = project.cards.create(title="Moving", content="Keep this body\n#research")
        child = card.children.create(title="Child")
        foreign = other.cards.create(title="Foreign")
        assert [c.id for c in parent.children] == [target.id]
        assert card.move(parent=parent) is card
        assert card.parent_card_id == parent.id
        assert card.sort_key > target.sort_key
        assert card.content == "Keep this body\n#research"
        assert child.refresh().parent_card_id == card.id
        # Evaluated listings retain their cache until explicitly refreshed.
        assert [c.id for c in parent.children] == [target.id]
        assert {c.id for c in parent.children.refresh()} == {target.id, card.id}
        card.move(before=target)
        assert card.parent_card_id == parent.id
        assert card.sort_key < target.sort_key
        card.move(after=target)
        assert card.sort_key > target.sort_key
        # Relative moves can change hierarchy, including to an existing root's level.
        card.move(before=root)
        assert card.parent_card_id is None
        assert card.sort_key < root.sort_key
        assert child.refresh().parent_card_id == card.id
        assert [c.id for c in parent.children.refresh()] == [target.id]
        with pytest.raises(APIError) as cycle:
            card.move(parent=child)
        assert cycle.value.status == 422
        for kwargs in ({"parent": foreign}, {"before": foreign}, {"after": foreign}):
            with pytest.raises(NotFoundError):
                card.move(**kwargs)
        assert card.refresh().parent_card_id is None
        assert raw.delete(f"/cards/{target.id}").status_code == 200
        with pytest.raises(NotFoundError):
            card.move(after=target)
        assert raw.delete(f"/cards/{card.id}").status_code == 200
        with pytest.raises(NotFoundError):
            card.move(parent=parent)


def test_card_search_against_daemon(daemon):
    url, token, raw, _ = daemon
    with Holder(url=url, token=token) as h:
        project = h.projects.create(name="Python search", privacy_mode="plain")
        other = h.projects.create(name="Other search", privacy_mode="plain")
        cards = [
            project.cards.create(
                title=f"Search card {i}",
                content=f"research notes number {i}" + (" café" if i == 0 else ""),
            )
            for i in range(101)
        ]
        child = cards[0].children.create(
            title="Child", content="research notes for a child"
        )
        other.cards.create(
            title="Foreign", content="research notes from another project"
        )
        project.cards.create(title="Unrelated", content="Nothing matching here")
        assert raw.delete(f"/cards/{cards[1].id}").status_code == 200
        results = project.cards.search('"research notes"')
        rows = list(results)
        expected = {c.id for c in cards} - {cards[1].id}
        expected.add(child.id)
        assert len(rows) == 101
        assert {r.card_id for r in rows} == expected
        assert project.cards.search("café")[0].card_id == cards[0].id
        assert [r.rank for r in rows] == sorted(r.rank for r in rows)
        assert all("research" in r.snippet for r in rows)
        first = rows[0]
        assert first.card.project_id == project.id
        assert "research notes" in first.card.content
        assert list(project.cards.search("quartzunfindable")) == []
        with pytest.raises(APIError) as malformed:
            list(project.cards.search('"'))
        assert malformed.value.status == 400
        first.card.update(content="Changed to unrelated content")
        assert raw.delete(f"/cards/{rows[1].card_id}").status_code == 200
        with pytest.raises(NotFoundError):
            _ = rows[1].card
        assert len(list(results)) == 101  # Already evaluated search stays cached.
        assert {r.card_id for r in results.refresh()} == expected - {
            first.card_id,
            rows[1].card_id,
        }


def test_daemon_card_pages(daemon):
    _, _, raw, _ = daemon
    project = create_project(raw, "Pages")
    ids = sorted(create_card(raw, project, i) for i in range(3))
    response = raw.get(f"/projects/{project}/cards", params={"limit": 2})
    assert response.status_code == 200
    page = response.json()["data"]
    assert [card["card_id"] for card in page["items"]] == ids[:2]
    response = raw.get(
        f"/projects/{project}/cards", params={"limit": 2, "cursor": page["next_cursor"]}
    )
    assert [card["card_id"] for card in response.json()["data"]["items"]] == ids[2:]
    assert response.json()["data"]["next_cursor"] is None


def test_project_scoped_collections_against_daemon(daemon):
    url, token, raw, cli = daemon
    project_id = create_project(raw, "Collection integration")
    other_project = create_project(raw, "Other")
    ids = [create_card(raw, project_id, i) for i in range(205)]
    child = create_card(raw, project_id, 205, ids[0])
    foreign = create_card(raw, other_project, 1)
    assert raw.delete(f"/cards/{ids[1]}").status_code == 200
    with Holder(url=url, token=token) as h:
        project = h.projects.filter(name="Collection integration")[0]
        assert project.id == project_id
        cards = list(project.cards)
        assert len(cards) == 205
        assert {card.id for card in cards} == (set(ids) - {ids[1]}) | {child}
        assert len(list(project.cards.roots())) == 204
        assert project.cards.get(ids[0]).children[0].id == child
        assert len(list(project.cards.filter(tag="Research"))) == 205
        assert len(list(project.cards.roots().filter(tag="RESEARCH"))) == 204
        assert project.cards.get(ids[0]).children.filter(tag="ReSeArCh")[0].id == child
        with pytest.raises(NotFoundError):
            project.cards.get(foreign)
        card = project.cards.get(ids[0])
        assert card.content == "body 0\n#research"
        card.update(title="Updated through Python")
        assert card.title == "Updated through Python"
        assert card.content == "body 0\n#research"
    # Exercise the zero-argument discovery path against the same isolated env.
    with Holder(holderctl=str(cli)) as h:
        assert h.projects.get(project_id).name == "Collection integration"
