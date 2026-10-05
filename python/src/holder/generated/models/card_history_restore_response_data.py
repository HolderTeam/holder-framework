from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="CardHistoryRestoreResponseData")


@_attrs_define
class CardHistoryRestoreResponseData:
    """
    Attributes:
        card_id (str):
        restored_from_oid (str): Canonical full commit object ID of the selected historical snapshot.
        result_oid (str): Canonical full commit object ID created by the restoration.
        title (str):
        updated_at (int):
        deleted_at (int | None):
    """

    card_id: str
    restored_from_oid: str
    result_oid: str
    title: str
    updated_at: int
    deleted_at: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        card_id = self.card_id

        restored_from_oid = self.restored_from_oid

        result_oid = self.result_oid

        title = self.title

        updated_at = self.updated_at

        deleted_at: int | None
        deleted_at = self.deleted_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "card_id": card_id,
                "restored_from_oid": restored_from_oid,
                "result_oid": result_oid,
                "title": title,
                "updated_at": updated_at,
                "deleted_at": deleted_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        card_id = d.pop("card_id")

        restored_from_oid = d.pop("restored_from_oid")

        result_oid = d.pop("result_oid")

        title = d.pop("title")

        updated_at = d.pop("updated_at")

        def _parse_deleted_at(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at"))

        card_history_restore_response_data = cls(
            card_id=card_id,
            restored_from_oid=restored_from_oid,
            result_oid=result_oid,
            title=title,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )

        card_history_restore_response_data.additional_properties = d
        return card_history_restore_response_data

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
