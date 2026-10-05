from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.asset_placement import AssetPlacement


T = TypeVar("T", bound="ResourceAsset")


@_attrs_define
class ResourceAsset:
    """
    Attributes:
        asset_id (str):
        resource_id (str):
        original_filename (str):
        media_type (str):
        byte_size (int):
        plaintext_sha256 (str):
        placements (list[AssetPlacement]):
        created_at (int):
        updated_at (int):
    """

    asset_id: str
    resource_id: str
    original_filename: str
    media_type: str
    byte_size: int
    plaintext_sha256: str
    placements: list[AssetPlacement]
    created_at: int
    updated_at: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_id = self.asset_id

        resource_id = self.resource_id

        original_filename = self.original_filename

        media_type = self.media_type

        byte_size = self.byte_size

        plaintext_sha256 = self.plaintext_sha256

        placements = []
        for placements_item_data in self.placements:
            placements_item = placements_item_data.to_dict()
            placements.append(placements_item)

        created_at = self.created_at

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asset_id": asset_id,
                "resource_id": resource_id,
                "original_filename": original_filename,
                "media_type": media_type,
                "byte_size": byte_size,
                "plaintext_sha256": plaintext_sha256,
                "placements": placements,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.asset_placement import AssetPlacement

        d = dict(src_dict)
        asset_id = d.pop("asset_id")

        resource_id = d.pop("resource_id")

        original_filename = d.pop("original_filename")

        media_type = d.pop("media_type")

        byte_size = d.pop("byte_size")

        plaintext_sha256 = d.pop("plaintext_sha256")

        placements = []
        _placements = d.pop("placements")
        for placements_item_data in _placements:
            placements_item = AssetPlacement.from_dict(placements_item_data)

            placements.append(placements_item)

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        resource_asset = cls(
            asset_id=asset_id,
            resource_id=resource_id,
            original_filename=original_filename,
            media_type=media_type,
            byte_size=byte_size,
            plaintext_sha256=plaintext_sha256,
            placements=placements,
            created_at=created_at,
            updated_at=updated_at,
        )

        resource_asset.additional_properties = d
        return resource_asset

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
