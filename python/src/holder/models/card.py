"""Cards and their project-scoped synchronous collection queries."""

from __future__ import annotations

import time
from dataclasses import dataclass, field, fields
from functools import cached_property
from typing import TYPE_CHECKING, Any, Self

from ..collections import Collection
from ..exceptions import NotFoundError, ProtocolError
from ..generated.api.default import (
    get_cards_card_id,
    get_projects_project_id_cards,
    patch_cards_card_id,
    post_cards,
    post_cards_card_id_move,
)
from ..generated.models import (
    CardCreateRequest,
    CardMoveIntent,
    CardMoveRequest,
    CardUpdateRequest,
)
from ..generated.models.get_projects_project_id_cards_parent_type_0 import (
    GetProjectsProjectIdCardsParentType0 as CardParent,
)
from ..generated.types import UNSET, Unset
from .search import CardSearchCollection
from .tag import CardTagCollection

if TYPE_CHECKING:
    from .project import Project


class CardCollection(Collection["Card"]):
    def __init__(self, project: Project, query: dict[str, Any] | None = None) -> None:
        self._project = project
        super().__init__(project._holder, query)

    def create(self, *, title: str, content: str = "") -> Card:
        """Create a root card, or a child when called on a children collection.

        Tag filters do not add tags to the content. Cached listings remain
        unchanged until refreshed. The write is never retried; if the subsequent
        fetch fails, the card may already exist.
        """
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        parent = self._query.get("parent", UNSET)
        if parent == CardParent.ROOTS:
            parent = UNSET
        data = self._holder._call(
            post_cards,
            body=CardCreateRequest(
                project_id=self._project.id,
                title=title,
                content=content,
                parent_card_id=parent,
            ),
            write=True,
        )
        return self.get(data.card_id)

    def _clone(self, query: dict[str, Any]) -> Self:
        return type(self)(self._project, query)

    def filter(self, *, tag: str) -> Self:
        if not isinstance(tag, str) or not tag.strip():
            raise ValueError("tag must be a nonempty string")
        return self._clone({**self._query, "tag": tag})

    def roots(self) -> Self:
        return self._clone({**self._query, "parent": CardParent.ROOTS})

    def search(self, query: str) -> CardSearchCollection:
        """Search this project's cards using the daemon's full-text query syntax.

        Tag and hierarchy filters cannot be combined with the search endpoint.
        """
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        if not query.strip():
            raise ValueError("query must be nonempty")
        if self._query:
            raise ValueError("Search does not support tag or hierarchy filters")
        return CardSearchCollection(self._project, query)

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

    @cached_property
    def tags(self) -> CardTagCollection:
        return CardTagCollection(self)

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
        if "tags" in self.__dict__:
            self.tags.refresh()
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

    def move(
        self,
        *,
        parent: Card | Unset = UNSET,
        before: Card | Unset = UNSET,
        after: Card | Unset = UNSET,
    ) -> Self:
        """Move into a parent or immediately before/after a target card.

        Supply exactly one Card. Relative moves adopt the target's parent.
        The daemon enforces project membership and prevents hierarchy cycles.
        The moved card is refreshed; evaluated listings need explicit refresh.
        Writes are never retried, even if the subsequent refresh fails.
        """
        supplied = [
            (intent, target)
            for intent, target in (
                (CardMoveIntent.INTO, parent),
                (CardMoveIntent.BEFORE, before),
                (CardMoveIntent.AFTER, after),
            )
            if not isinstance(target, Unset)
        ]
        if len(supplied) != 1:
            raise TypeError("Supply exactly one of parent, before or after")
        intent, target = supplied[0]
        if not isinstance(target, Card):
            raise TypeError("The move target must be a Card")
        self._project._holder._call(
            post_cards_card_id_move,
            self.id,
            body=CardMoveRequest(
                project_id=self._project.id,
                intent=intent,
                target_card_id=target.id,
            ),
            write=True,
        )
        return self.refresh()
