from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.asset_placement_encoding import AssetPlacementEncoding

T = TypeVar("T", bound="AssetPlacement")


@_attrs_define
class AssetPlacement:
    """
    Attributes:
        placement_id (str):
        location_id (str):
        encoding (AssetPlacementEncoding):
        stored_byte_size (int):
        created_at (int):
    """

    placement_id: str
    location_id: str
    encoding: AssetPlacementEncoding
    stored_byte_size: int
    created_at: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        placement_id = self.placement_id

        location_id = self.location_id

        encoding = self.encoding.value

        stored_byte_size = self.stored_byte_size

        created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "placement_id": placement_id,
                "location_id": location_id,
                "encoding": encoding,
                "stored_byte_size": stored_byte_size,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        placement_id = d.pop("placement_id")

        location_id = d.pop("location_id")

        encoding = AssetPlacementEncoding(d.pop("encoding"))

        stored_byte_size = d.pop("stored_byte_size")

        created_at = d.pop("created_at")

        asset_placement = cls(
            placement_id=placement_id,
            location_id=location_id,
            encoding=encoding,
            stored_byte_size=stored_byte_size,
            created_at=created_at,
        )

        asset_placement.additional_properties = d
        return asset_placement

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
