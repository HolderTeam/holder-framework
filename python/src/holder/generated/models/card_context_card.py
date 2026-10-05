from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardContextCard")


@_attrs_define
class CardContextCard:
    """
    Attributes:
        card_id (str):
        project_id (str):
        title (str):
        rel_path (str):
        sort_key (float):
        created_at (int):
        updated_at (int):
        parent_card_id (None | str | Unset):
        deleted_at (int | None | Unset):
        child_count (int | Unset): Present when count=true.
    """

    card_id: str
    project_id: str
    title: str
    rel_path: str
    sort_key: float
    created_at: int
    updated_at: int
    parent_card_id: None | str | Unset = UNSET
    deleted_at: int | None | Unset = UNSET
    child_count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        card_id = self.card_id

        project_id = self.project_id

        title = self.title

        rel_path = self.rel_path

        sort_key = self.sort_key

        created_at = self.created_at

        updated_at = self.updated_at

        parent_card_id: None | str | Unset
        if isinstance(self.parent_card_id, Unset):
            parent_card_id = UNSET
        else:
            parent_card_id = self.parent_card_id

        deleted_at: int | None | Unset
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = self.deleted_at

        child_count = self.child_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "card_id": card_id,
                "project_id": project_id,
                "title": title,
                "rel_path": rel_path,
                "sort_key": sort_key,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if parent_card_id is not UNSET:
            field_dict["parent_card_id"] = parent_card_id
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if child_count is not UNSET:
            field_dict["child_count"] = child_count

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        card_id = d.pop("card_id")

        project_id = d.pop("project_id")

        title = d.pop("title")

        rel_path = d.pop("rel_path")

        sort_key = d.pop("sort_key")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_parent_card_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_card_id = _parse_parent_card_id(d.pop("parent_card_id", UNSET))

        def _parse_deleted_at(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        child_count = d.pop("child_count", UNSET)

        card_context_card = cls(
            card_id=card_id,
            project_id=project_id,
            title=title,
            rel_path=rel_path,
            sort_key=sort_key,
            created_at=created_at,
            updated_at=updated_at,
            parent_card_id=parent_card_id,
            deleted_at=deleted_at,
            child_count=child_count,
        )

        card_context_card.additional_properties = d
        return card_context_card

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
