from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardData")


@_attrs_define
class CardData:
    """
    Attributes:
        card_id (str):
        project_id (str):
        title (str):
        rel_path (str):
        sort_key (float):
        created_at (int):
        updated_at (int):
        content (str):
        parent_card_id (None | str | Unset):
        deleted_at (int | None | Unset):
    """

    card_id: str
    project_id: str
    title: str
    rel_path: str
    sort_key: float
    created_at: int
    updated_at: int
    content: str
    parent_card_id: None | str | Unset = UNSET
    deleted_at: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        card_id = self.card_id

        project_id = self.project_id

        title = self.title

        rel_path = self.rel_path

        sort_key = self.sort_key

        created_at = self.created_at

        updated_at = self.updated_at

        content = self.content

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
                "content": content,
            }
        )
        if parent_card_id is not UNSET:
            field_dict["parent_card_id"] = parent_card_id
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at

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

        content = d.pop("content")

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

        card_data = cls(
            card_id=card_id,
            project_id=project_id,
            title=title,
            rel_path=rel_path,
            sort_key=sort_key,
            created_at=created_at,
            updated_at=updated_at,
            content=content,
            parent_card_id=parent_card_id,
            deleted_at=deleted_at,
        )

        card_data.additional_properties = d
        return card_data

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
