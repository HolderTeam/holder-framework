from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="SearchMessageItem")


@_attrs_define
class SearchMessageItem:
    """
    Attributes:
        message_id (str):
        created_at (int):
        snippet (str):
        rank (float):
    """

    message_id: str
    created_at: int
    snippet: str
    rank: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message_id = self.message_id

        created_at = self.created_at

        snippet = self.snippet

        rank = self.rank

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message_id": message_id,
                "created_at": created_at,
                "snippet": snippet,
                "rank": rank,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        message_id = d.pop("message_id")

        created_at = d.pop("created_at")

        snippet = d.pop("snippet")

        rank = d.pop("rank")

        search_message_item = cls(
            message_id=message_id,
            created_at=created_at,
            snippet=snippet,
            rank=rank,
        )

        search_message_item.additional_properties = d
        return search_message_item

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
