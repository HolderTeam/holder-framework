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
from holder.exceptions import NotFoundError

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


def test_daemon_card_pages(daemon):
    _, _, raw, _ = daemon
    project = create_project(raw, "Pages")
    ids = sorted(create_card(raw, project, i) for i in range(3))
    response = raw.get(
        "/cards", params={"project_id": project, "view": "all", "limit": 2}
    )
    assert response.status_code == 200
    assert [card["card_id"] for card in response.json()["data"]] == ids[:2]
    response = raw.get(
        "/cards",
        params={
            "project_id": project,
            "view": "all",
            "limit": 2,
            "after_card_id": ids[1],
        },
    )
    assert [card["card_id"] for card in response.json()["data"]] == ids[2:]


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
        assert len(list(project.cards.filter(tag="research"))) == 205
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
