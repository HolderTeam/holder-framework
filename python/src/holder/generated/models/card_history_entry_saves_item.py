from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="CardHistoryEntrySavesItem")


@_attrs_define
class CardHistoryEntrySavesItem:
    """
    Attributes:
        oid (str):
        parent_oids (list[str]):
        authored_at (int):
        committed_at (int):
        message (str):
    """

    oid: str
    parent_oids: list[str]
    authored_at: int
    committed_at: int
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        oid = self.oid

        parent_oids = self.parent_oids

        authored_at = self.authored_at

        committed_at = self.committed_at

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "oid": oid,
                "parent_oids": parent_oids,
                "authored_at": authored_at,
                "committed_at": committed_at,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        oid = d.pop("oid")

        parent_oids = cast(list[str], d.pop("parent_oids"))

        authored_at = d.pop("authored_at")

        committed_at = d.pop("committed_at")

        message = d.pop("message")

        card_history_entry_saves_item = cls(
            oid=oid,
            parent_oids=parent_oids,
            authored_at=authored_at,
            committed_at=committed_at,
            message=message,
        )

        card_history_entry_saves_item.additional_properties = d
        return card_history_entry_saves_item

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
