from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.card_history_entry_kind import CardHistoryEntryKind

if TYPE_CHECKING:
    from ..models.card_history_author import CardHistoryAuthor
    from ..models.card_history_entry_saves_item import CardHistoryEntrySavesItem


T = TypeVar("T", bound="CardHistoryEntry")


@_attrs_define
class CardHistoryEntry:
    """
    Attributes:
        first_oid (str):
        last_oid (str):
        parent_oids (list[str]):
        visible_parent_oids (list[str]): Direct parent entries visible on this history page; omitted connections must
            not be inferred across filtered commits or page boundaries.
        author (CardHistoryAuthor):
        started_at (int):
        ended_at (int):
        kind (CardHistoryEntryKind):
        summary (str):
        commit_count (int):
        is_merge (bool):
        saves (list[CardHistoryEntrySavesItem]): Exact saved commits in chronological order; one item for an ungrouped
            entry.
    """

    first_oid: str
    last_oid: str
    parent_oids: list[str]
    visible_parent_oids: list[str]
    author: CardHistoryAuthor
    started_at: int
    ended_at: int
    kind: CardHistoryEntryKind
    summary: str
    commit_count: int
    is_merge: bool
    saves: list[CardHistoryEntrySavesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        first_oid = self.first_oid

        last_oid = self.last_oid

        parent_oids = self.parent_oids

        visible_parent_oids = self.visible_parent_oids

        author = self.author.to_dict()

        started_at = self.started_at

        ended_at = self.ended_at

        kind = self.kind.value

        summary = self.summary

        commit_count = self.commit_count

        is_merge = self.is_merge

        saves = []
        for saves_item_data in self.saves:
            saves_item = saves_item_data.to_dict()
            saves.append(saves_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "first_oid": first_oid,
                "last_oid": last_oid,
                "parent_oids": parent_oids,
                "visible_parent_oids": visible_parent_oids,
                "author": author,
                "started_at": started_at,
                "ended_at": ended_at,
                "kind": kind,
                "summary": summary,
                "commit_count": commit_count,
                "is_merge": is_merge,
                "saves": saves,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.card_history_author import CardHistoryAuthor
        from ..models.card_history_entry_saves_item import (
            CardHistoryEntrySavesItem,
        )

        d = dict(src_dict)
        first_oid = d.pop("first_oid")

        last_oid = d.pop("last_oid")

        parent_oids = cast(list[str], d.pop("parent_oids"))

        visible_parent_oids = cast(list[str], d.pop("visible_parent_oids"))

        author = CardHistoryAuthor.from_dict(d.pop("author"))

        started_at = d.pop("started_at")

        ended_at = d.pop("ended_at")

        kind = CardHistoryEntryKind(d.pop("kind"))

        summary = d.pop("summary")

        commit_count = d.pop("commit_count")

        is_merge = d.pop("is_merge")

        saves = []
        _saves = d.pop("saves")
        for saves_item_data in _saves:
            saves_item = CardHistoryEntrySavesItem.from_dict(saves_item_data)

            saves.append(saves_item)

        card_history_entry = cls(
            first_oid=first_oid,
            last_oid=last_oid,
            parent_oids=parent_oids,
            visible_parent_oids=visible_parent_oids,
            author=author,
            started_at=started_at,
            ended_at=ended_at,
            kind=kind,
            summary=summary,
            commit_count=commit_count,
            is_merge=is_merge,
            saves=saves,
        )

        card_history_entry.additional_properties = d
        return card_history_entry

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
