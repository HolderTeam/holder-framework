from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.card_history_version import CardHistoryVersion


T = TypeVar("T", bound="CardHistorySnapshotResponseData")


@_attrs_define
class CardHistorySnapshotResponseData:
    """
    Attributes:
        card_id (str):
        snapshot (CardHistoryVersion):
    """

    card_id: str
    snapshot: CardHistoryVersion
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        card_id = self.card_id

        snapshot = self.snapshot.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "card_id": card_id,
                "snapshot": snapshot,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.card_history_version import CardHistoryVersion

        d = dict(src_dict)
        card_id = d.pop("card_id")

        snapshot = CardHistoryVersion.from_dict(d.pop("snapshot"))

        card_history_snapshot_response_data = cls(
            card_id=card_id,
            snapshot=snapshot,
        )

        card_history_snapshot_response_data.additional_properties = d
        return card_history_snapshot_response_data

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
