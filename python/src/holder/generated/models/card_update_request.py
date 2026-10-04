from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardUpdateRequest")


@_attrs_define
class CardUpdateRequest:
    """
    Attributes:
        updated_at (int):
        content (str | Unset):
        title (None | str | Unset):
        parent_card_id (None | str | Unset):
        sort_key (float | Unset):
    """

    updated_at: int
    content: str | Unset = UNSET
    title: None | str | Unset = UNSET
    parent_card_id: None | str | Unset = UNSET
    sort_key: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_at = self.updated_at

        content = self.content

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        parent_card_id: None | str | Unset
        if isinstance(self.parent_card_id, Unset):
            parent_card_id = UNSET
        else:
            parent_card_id = self.parent_card_id

        sort_key = self.sort_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_at": updated_at,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content
        if title is not UNSET:
            field_dict["title"] = title
        if parent_card_id is not UNSET:
            field_dict["parent_card_id"] = parent_card_id
        if sort_key is not UNSET:
            field_dict["sort_key"] = sort_key

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        updated_at = d.pop("updated_at")

        content = d.pop("content", UNSET)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_parent_card_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_card_id = _parse_parent_card_id(d.pop("parent_card_id", UNSET))

        sort_key = d.pop("sort_key", UNSET)

        card_update_request = cls(
            updated_at=updated_at,
            content=content,
            title=title,
            parent_card_id=parent_card_id,
            sort_key=sort_key,
        )

        card_update_request.additional_properties = d
        return card_update_request

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
