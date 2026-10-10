"""Synchronous, project-scoped collections for a running Holder daemon."""

from __future__ import annotations

import json
import subprocess
import time
from collections.abc import Iterator
from dataclasses import dataclass, field, fields
from functools import cached_property
from typing import Any, Generic, Self, TypeVar, cast

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    ClosedError,
    ConnectionError,
    NotFoundError,
    ProtocolError,
)
from .generated import AuthenticatedClient
from .generated.api.default import (
    get_cards_card_id,
    get_projects,
    get_projects_project_id,
    get_projects_project_id_cards,
    patch_cards_card_id,
)
from .generated.models import (
    CardUpdateRequest,
    ErrorResponse,
    ProjectPrivacyMode,
    ProjectSync,
)
from .generated.models.get_projects_project_id_cards_parent_type_0 import (
    GetProjectsProjectIdCardsParentType0 as CardParent,
)
from .generated.types import UNSET, Unset

T = TypeVar("T")


class Holder:
    """Control your local knowledge, or connect with an explicit URL/token pair.

    Use as a context manager. Collection queries run only when consumed.
    Local discovery requires holderctl on PATH (or the holderctl argument).
    """

    def __init__(
        self,
        *,
        url: str | None = None,
        token: str | None = None,
        holderctl: str = "holderctl",
        timeout: float | httpx.Timeout = 10.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if (url is None) != (token is None):
            raise ValueError("Supply url and token together, or omit both")
        self._url = url
        self._token = token
        self._local = url is None
        self._holderctl = holderctl
        self._timeout = timeout
        self._transport = transport
        self._client: AuthenticatedClient | None = None
        self._closed = False
        self.projects = ProjectCollection(self)

    def _command(self, *args: str) -> str:
        try:
            result = subprocess.run(
                [self._holderctl, *args],
                capture_output=True,
                text=True,
                timeout=65,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise ConnectionError(
                "Could not run holderctl; install Holder or supply url and token"
            ) from None
        if result.returncode:
            # CLI output and stderr may contain local credentials; never echo them.
            raise ConnectionError(
                f"holderctl {args[0]} failed (exit {result.returncode})"
            )
        return result.stdout

    def _discover(self) -> None:
        try:
            result = json.loads(
                self._command(
                    "ensure",
                    "--json",
                    "--api-min",
                    "0.1",
                    "--api-max-exclusive",
                    "1.0",
                )
            )
            url = result["daemon"]["url"]
            if result.get("ok") is not True or not isinstance(url, str) or not url:
                raise ValueError
            token = self._command("token").strip()
            if not token:
                raise ValueError
        except (ValueError, KeyError, TypeError):
            raise ConnectionError(
                "holderctl did not return valid daemon connection details"
            ) from None
        self._url, self._token = url, token

    def _connect(self) -> None:
        if self._local:
            self._discover()
        self._client = AuthenticatedClient(
            base_url=self._url,
            token=self._token,
            timeout=httpx.Timeout(self._timeout),
            httpx_args={"transport": self._transport} if self._transport else {},
        )
        self._client.__enter__()

    def __enter__(self) -> Self:
        if self._closed or self._client is not None:
            raise ClosedError("Holder contexts cannot be reused")
        self._connect()
        return self

    def __exit__(self, *args: object) -> None:
        self._closed = True
        if self._client is not None:
            self._client.__exit__(*args)

    def _active(self) -> AuthenticatedClient:
        if self._closed or self._client is None:
            raise ClosedError("Use Holder inside with Holder(...) as h")
        return self._client

    def __iter__(self) -> Iterator[Project]:
        return iter(self.projects)

    def _call(
        self, endpoint: Any, *args: Any, write: bool = False, **kwargs: Any
    ) -> Any:
        client = self._active()
        for attempt in range(2):
            try:
                response = endpoint.sync_detailed(*args, client=client, **kwargs)
            except httpx.TransportError:
                raise ConnectionError(
                    "Could not communicate with the Holder daemon"
                ) from None
            except (ValueError, KeyError, TypeError):
                raise ProtocolError("Invalid daemon response") from None
            if (
                response.status_code == 401
                and self._local
                and not write
                and attempt == 0
            ):
                self._discover()
                # Preserve the pool and custom transport while updating a restarted daemon.
                http_client = client.get_httpx_client()
                http_client.base_url = self._url
                http_client.headers["Authorization"] = f"Bearer {self._token}"
                continue
            if isinstance(response.parsed, ErrorResponse):
                error = response.parsed.error
                error_type = {401: AuthenticationError, 404: NotFoundError}.get(
                    response.status_code, APIError
                )
                raise error_type(int(response.status_code), error.code, error.message)
            if response.status_code >= 400:
                error_type = {401: AuthenticationError, 404: NotFoundError}.get(
                    response.status_code, APIError
                )
                # Undocumented statuses are not parsed by generated endpoints.
                try:
                    error = ErrorResponse.from_dict(json.loads(response.content)).error
                except (ValueError, KeyError, TypeError, AttributeError):
                    error = None
                if error is not None:
                    raise error_type(
                        int(response.status_code), error.code, error.message
                    )
                raise error_type(
                    int(response.status_code), "http_error", "Daemon request failed"
                )
            if (
                response.parsed is None
                or getattr(response.parsed, "ok", None) is not True
            ):
                raise ProtocolError("Invalid daemon success envelope")
            return response.parsed.data
        raise AuthenticationError(
            401, "unauthorized", "Daemon rejected refreshed credentials"
        )


class Collection(Generic[T]):
    """Lazy query with a progressively populated cache and independent iterators."""

    def __init__(self, holder: Holder, query: dict[str, Any] | None = None) -> None:
        self._holder = holder
        self._query = dict(query or {})
        self._cache: list[T] = []
        self._next: int | str | None = None
        self._done = False
        self._generation = 0

    def __iter__(self) -> Iterator[T]:
        self._holder._active()
        generation = self._generation
        index = 0
        while True:
            self._holder._active()
            if generation != self._generation:
                raise RuntimeError("Collection was refreshed during iteration")
            if index == len(self._cache):
                if self._done:
                    return
                rows, next_cursor = self._fetch_page()
                self._cache.extend(rows)
                self._next = next_cursor
                self._done = next_cursor is None
                if not rows:
                    return
            yield self._cache[index]
            index += 1

    def __getitem__(self, index: int) -> T:
        if not isinstance(index, int):
            raise TypeError("Collection indices must be integers")
        if index < 0:
            raise IndexError("Collection indices must be nonnegative")
        for position, item in enumerate(self):
            if position == index:
                return item
        raise IndexError("Collection index out of range")

    def all(self) -> Self:
        return self._clone(self._query)

    def refresh(self) -> Self:
        self._holder._active()
        self._cache.clear()
        self._next = None
        self._done = False
        self._generation += 1
        return self

    def _clone(self, query: dict[str, Any]) -> Self:
        raise NotImplementedError

    def _fetch_page(self) -> tuple[list[T], int | str | None]:
        raise NotImplementedError


class ProjectCollection(Collection["Project"]):
    def _clone(self, query: dict[str, Any]) -> Self:
        return type(self)(self._holder, query)

    def filter(
        self,
        *,
        name: str | Unset = UNSET,
        updated_after: int | Unset = UNSET,
        updated_before: int | Unset = UNSET,
    ) -> Self:
        values = {
            key: value
            for key, value in {
                "name": name,
                "updated_after": updated_after,
                "updated_before": updated_before,
            }.items()
            if not isinstance(value, Unset)
        }
        if "name" in values and not isinstance(name, str):
            raise TypeError("name must be a string")
        for key in ("updated_after", "updated_before"):
            if key in values and (
                not isinstance(values[key], int) or isinstance(values[key], bool)
            ):
                raise TypeError(f"{key} must be an integer")
        return self._clone({**self._query, **values})

    def _fetch_page(self) -> tuple[list[Project], int | None]:
        offset = cast(int, self._next or 0)
        data = self._holder._call(get_projects, limit=100, offset=offset, **self._query)
        rows = [Project._from(self._holder, item) for item in data]
        next_offset = offset + len(data) if len(data) == 100 else None
        return rows, next_offset

    def get(self, project_id: str) -> Project:
        project = Project._from(
            self._holder, self._holder._call(get_projects_project_id, project_id)
        )
        # get(id) is a direct scoped lookup, not evaluation of a filtered listing.
        return project


class CardCollection(Collection["Card"]):
    def __init__(self, project: Project, query: dict[str, Any] | None = None) -> None:
        self._project = project
        super().__init__(project._holder, query)

    def _clone(self, query: dict[str, Any]) -> Self:
        return type(self)(self._project, query)

    def filter(self, *, tag: str) -> Self:
        if not isinstance(tag, str) or not tag.strip():
            raise ValueError("tag must be a nonempty string")
        return self._clone({**self._query, "tag": tag})

    def roots(self) -> Self:
        return self._clone({**self._query, "parent": CardParent.ROOTS})

    def _fetch_page(self) -> tuple[list[Card], str | None]:
        data = self._holder._call(
            get_projects_project_id_cards,
            self._project.id,
            limit=200,
            cursor=self._next or UNSET,
            **self._query,
        )
        rows = [Card._from(self._project, item) for item in data.items]
        if any(card.project_id != self._project.id for card in rows):
            raise ProtocolError("Card listing returned an object from another project")
        cursor = data.next_cursor
        if cursor is not None and (
            not isinstance(cursor, str)
            or not cursor
            or not rows
            or cursor == self._next
        ):
            raise ProtocolError("Card pagination did not advance")
        return rows, cursor

    def get(self, card_id: str) -> Card:
        data = self._holder._call(get_cards_card_id, card_id)
        if data.project_id != self._project.id:
            raise NotFoundError(404, "not_found", "Card not found in this project")
        return Card._from(self._project, data)


@dataclass(frozen=True, eq=False)
class Project:
    project_id: str
    name: str
    root_path: str
    privacy_mode: ProjectPrivacyMode
    created_at: int
    updated_at: int
    sync: ProjectSync
    git_remote_url: str | None
    git_provider: str | None
    project_key_id: str | None
    card_count: int | None
    root_card_count: int | None
    _holder: Holder = field(repr=False, compare=False)

    @property
    def id(self) -> str:
        return self.project_id

    @cached_property
    def cards(self) -> CardCollection:
        return CardCollection(self)

    @classmethod
    def _from(cls, holder: Holder, data: Any) -> Self:
        values: dict[str, Any] = {}
        for f in fields(cls):
            if f.name != "_holder":
                value = getattr(data, f.name, None)
                values[f.name] = None if isinstance(value, Unset) else value
        return cls(**values, _holder=holder)

    def refresh(self) -> Self:
        fresh = self._holder.projects.get(self.id)
        for f in fields(self):
            if f.name != "_holder":
                object.__setattr__(self, f.name, getattr(fresh, f.name))
        return self


@dataclass(frozen=True, eq=False)
class Card:
    card_id: str
    project_id: str
    title: str
    rel_path: str
    sort_key: float
    created_at: int
    updated_at: int
    parent_card_id: str | None
    deleted_at: int | None
    child_count: int | None
    _project: Project = field(repr=False, compare=False)
    _content: str | None = field(default=None, repr=False, compare=False)

    @property
    def id(self) -> str:
        return self.card_id

    @property
    def content(self) -> str:
        self._project._holder._active()
        if self._content is None:
            self.refresh()
        if self._content is None:
            raise ProtocolError("Card response did not include content")
        return self._content

    @cached_property
    def children(self) -> CardCollection:
        return CardCollection(self._project, {"parent": self.id})

    @classmethod
    def _from(cls, project: Project, data: Any) -> Self:
        values: dict[str, Any] = {
            f.name: getattr(data, f.name, None)
            for f in fields(cls)
            if not f.name.startswith("_")
        }
        values = {k: None if isinstance(v, Unset) else v for k, v in values.items()}
        return cls(**values, _project=project, _content=getattr(data, "content", None))

    def refresh(self) -> Self:
        fresh = self._project.cards.get(self.id)
        for f in fields(self):
            if f.name != "_project":
                object.__setattr__(self, f.name, getattr(fresh, f.name))
        return self

    def update(
        self, *, title: str | None | Unset = UNSET, content: str | Unset = UNSET
    ) -> Self:
        if isinstance(title, Unset) and isinstance(content, Unset):
            raise TypeError("Supply title or content")
        if not isinstance(title, (str, Unset)) and title is not None:
            raise TypeError("title must be a string or None")
        if not isinstance(content, (str, Unset)):
            raise TypeError("content must be a string")
        # Verify membership and obtain fresh content before any write.
        current = self._project.cards.get(self.id)
        if isinstance(content, Unset):
            content = current.content
        body = CardUpdateRequest(
            updated_at=int(time.time()), title=title, content=content
        )
        self._project._holder._call(patch_cards_card_id, self.id, body=body, write=True)
        return self.refresh()
