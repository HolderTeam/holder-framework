"""Projects and their synchronous collection queries."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from functools import cached_property
from typing import TYPE_CHECKING, Any, Self, cast

from ..collections import Collection
from ..generated.api.default import get_projects, get_projects_project_id
from ..generated.models import ProjectPrivacyMode, ProjectSync
from ..generated.types import UNSET, Unset
from .card import CardCollection

if TYPE_CHECKING:
    from ..client import Holder


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
