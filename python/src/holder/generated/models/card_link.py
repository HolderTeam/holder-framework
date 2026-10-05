from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardLink")


@_attrs_define
class CardLink:
    """
    Attributes:
        from_card_id (str):
        to_card_id (str):
        to_type (str): Target type (card, ai_message, ai_thread, resource).
        kind (str):
        created_at (int):
        label (None | str | Unset):
    """

    from_card_id: str
    to_card_id: str
    to_type: str
    kind: str
    created_at: int
    label: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_card_id = self.from_card_id

        to_card_id = self.to_card_id

        to_type = self.to_type

        kind = self.kind

        created_at = self.created_at

        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from_card_id": from_card_id,
                "to_card_id": to_card_id,
                "to_type": to_type,
                "kind": kind,
                "created_at": created_at,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        from_card_id = d.pop("from_card_id")

        to_card_id = d.pop("to_card_id")

        to_type = d.pop("to_type")

        kind = d.pop("kind")

        created_at = d.pop("created_at")

        def _parse_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        card_link = cls(
            from_card_id=from_card_id,
            to_card_id=to_card_id,
            to_type=to_type,
            kind=kind,
            created_at=created_at,
            label=label,
        )

        card_link.additional_properties = d
        return card_link

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
