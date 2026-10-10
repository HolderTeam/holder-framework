"""Project-scoped card search results and lazy pagination."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING, Any, Self, cast

from ..collections import Collection
from ..generated.api.default import get_search_cards

if TYPE_CHECKING:
    from .card import Card
    from .project import Project


class CardSearchCollection(Collection["CardSearchResult"]):
    """Lazy relevance-ordered results, with the usual all/refresh/index behavior."""

    def __init__(self, project: Project, query: str) -> None:
        self._project = project
        super().__init__(project._holder, {"q": query})

    def _clone(self, query: dict[str, Any]) -> Self:
        return type(self)(self._project, query["q"])

    def _fetch_page(self) -> tuple[list[CardSearchResult], int | None]:
        offset = cast(int, self._next or 0)
        data = self._holder._call(
            get_search_cards,
            project_id=self._project.id,
            q=self._query["q"],
            limit=100,
            offset=offset,
        )
        rows = [CardSearchResult._from(self._project, item) for item in data]
        return rows, offset + len(rows) if len(rows) == 100 else None


@dataclass(frozen=True, eq=False)
class CardSearchResult:
    """Search metadata from one query, with lazy access to the current card."""

    card_id: str
    title: str
    created_at: int
    updated_at: int
    snippet: str
    rank: float
    _project: Project = field(repr=False, compare=False)

    @cached_property
    def card(self) -> Card:
        return self._project.cards.get(self.card_id)

    @classmethod
    def _from(cls, project: Project, data: Any) -> Self:
        return cls(
            card_id=data.card_id,
            title=data.title,
            created_at=data.created_at,
            updated_at=data.updated_at,
            snippet=data.snippet,
            rank=data.rank,
            _project=project,
        )
