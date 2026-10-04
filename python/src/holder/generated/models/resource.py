from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.resource_asset import ResourceAsset
    from ..models.resource_metadata import ResourceMetadata


T = TypeVar("T", bound="Resource")


@_attrs_define
class Resource:
    """
    Attributes:
        resource_id (str):
        project_id (str):
        type_ (str): Friendly, extensible type rather than a closed enum.
        label (str):
        metadata (ResourceMetadata): Permissive metadata map. Repeated and custom values are preserved in order.
        assets (list[ResourceAsset]):
        created_at (int):
        updated_at (int):
    """

    resource_id: str
    project_id: str
    type_: str
    label: str
    metadata: ResourceMetadata
    assets: list[ResourceAsset]
    created_at: int
    updated_at: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_id = self.resource_id

        project_id = self.project_id

        type_ = self.type_

        label = self.label

        metadata = self.metadata.to_dict()

        assets = []
        for assets_item_data in self.assets:
            assets_item = assets_item_data.to_dict()
            assets.append(assets_item)

        created_at = self.created_at

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_id": resource_id,
                "project_id": project_id,
                "type": type_,
                "label": label,
                "metadata": metadata,
                "assets": assets,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.resource_asset import ResourceAsset
        from ..models.resource_metadata import ResourceMetadata

        d = dict(src_dict)
        resource_id = d.pop("resource_id")

        project_id = d.pop("project_id")

        type_ = d.pop("type")

        label = d.pop("label")

        metadata = ResourceMetadata.from_dict(d.pop("metadata"))

        assets = []
        _assets = d.pop("assets")
        for assets_item_data in _assets:
            assets_item = ResourceAsset.from_dict(assets_item_data)

            assets.append(assets_item)

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        resource = cls(
            resource_id=resource_id,
            project_id=project_id,
            type_=type_,
            label=label,
            metadata=metadata,
            assets=assets,
            created_at=created_at,
            updated_at=updated_at,
        )

        resource.additional_properties = d
        return resource

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
