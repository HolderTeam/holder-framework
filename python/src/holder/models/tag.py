"""Project-scoped tags and their synchronous collections."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING, Any, Self

from ..collections import Collection
from ..exceptions import NotFoundError, ProtocolError
from ..generated.api.default import (
    delete_cards_card_id_tags,
    get_cards_card_id,
    get_projects_project_id_tags,
    post_cards_card_id_tags,
)
from ..generated.models import CardTagMutationRequest

if TYPE_CHECKING:
    from .card import Card, CardCollection
    from .project import Project


class TagCollection(Collection["Tag"]):
    """Lazy project tags, ordered by usage count and then name."""

    def __init__(self, project: Project) -> None:
        self._project = project
        super().__init__(project._holder)

    def _clone(self, query: dict[str, Any]) -> Self:
        return type(self)(self._project)

    def _fetch_page(self) -> tuple[list[Tag], None]:
        data = self._holder._call(get_projects_project_id_tags, self._project.id)
        return [Tag(row.tag, self._project, row.card_count) for row in data], None

    def get(self, name: str) -> Tag:
        """Fetch a tag by its normalized name, independently of cached results."""
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        for tag in self.all():
            if tag.name == name:
                return tag
        raise NotFoundError(404, "not_found", "Tag not found in this collection")


class CardTagCollection(TagCollection):
    """Tags attached to one card; mutations use the daemon's editable tag line."""

    def __init__(self, card: Card) -> None:
        self._card = card
        super().__init__(card._project)

    def _clone(self, query: dict[str, Any]) -> Self:
        return type(self)(self._card)

    def _fetch_page(self) -> tuple[list[Tag], None]:
        data = self._holder._call(get_cards_card_id, self._card.id)
        if data.project_id != self._project.id:
            raise NotFoundError(404, "not_found", "Card not found in this project")
        # The generated client retains the daemon's tag array as an additional
        # property because CardData does not yet declare it explicitly.
        names = data.additional_properties.get("tags")
        if not isinstance(names, list) or any(
            not isinstance(name, str) or not name for name in names
        ):
            raise ProtocolError("Card response did not include valid tags")
        return [Tag(name, self._project) for name in names], None

    def add(self, name: str) -> Self:
        """Add a tag and refresh the card. Validation and normalization are server-side."""
        return self._mutate(post_cards_card_id_tags, name)

    def remove(self, name: str) -> Self:
        """Remove a trailing-line tag; body mentions remain until content is edited."""
        return self._mutate(delete_cards_card_id_tags, name)

    def _mutate(self, endpoint: Any, name: str) -> Self:
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self._holder._call(
            endpoint,
            self._card.id,
            body=CardTagMutationRequest(project_id=self._project.id, tag=name),
            write=True,
        )
        # Invalidate even if the following read fails. The write is never retried.
        self.refresh()
        self._card.refresh()
        return self


@dataclass(frozen=True, eq=False)
class Tag:
    """A normalized project tag.

    Project listings supply card_count; tags read from a card omit it until
    refresh() fetches their project-wide count.
    """

    name: str
    _project: Project = field(repr=False, compare=False)
    card_count: int | None = None

    @property
    def project_id(self) -> str:
        return self._project.id

    @cached_property
    def cards(self) -> CardCollection:
        return self._project.cards.filter(tag=self.name)

    def refresh(self) -> Self:
        fresh = self._project.tags.get(self.name)
        object.__setattr__(self, "card_count", fresh.card_count)
        return self
