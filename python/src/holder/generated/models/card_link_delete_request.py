from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardLinkDeleteRequest")


@_attrs_define
class CardLinkDeleteRequest:
    """
    Attributes:
        to_card_id (str | Unset):
        to_type (str | Unset):
        kind (str | Unset):
    """

    to_card_id: str | Unset = UNSET
    to_type: str | Unset = UNSET
    kind: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        to_card_id = self.to_card_id

        to_type = self.to_type

        kind = self.kind

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if to_card_id is not UNSET:
            field_dict["to_card_id"] = to_card_id
        if to_type is not UNSET:
            field_dict["to_type"] = to_type
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        to_card_id = d.pop("to_card_id", UNSET)

        to_type = d.pop("to_type", UNSET)

        kind = d.pop("kind", UNSET)

        card_link_delete_request = cls(
            to_card_id=to_card_id,
            to_type=to_type,
            kind=kind,
        )

        card_link_delete_request.additional_properties = d
        return card_link_delete_request

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
