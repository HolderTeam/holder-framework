from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_metadata import ResourceMetadata


T = TypeVar("T", bound="ResourceCreateRequest")


@_attrs_define
class ResourceCreateRequest:
    """
    Attributes:
        project_id (str):
        type_ (str):
        label (str):
        resource_id (str | Unset): Optional; server generates if omitted.
        metadata (ResourceMetadata | Unset): Permissive metadata map. Repeated and custom values are preserved in order.
        created_at (int | Unset):
        updated_at (int | Unset):
    """

    project_id: str
    type_: str
    label: str
    resource_id: str | Unset = UNSET
    metadata: ResourceMetadata | Unset = UNSET
    created_at: int | Unset = UNSET
    updated_at: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        type_ = self.type_

        label = self.label

        resource_id = self.resource_id

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        created_at = self.created_at

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "type": type_,
                "label": label,
            }
        )
        if resource_id is not UNSET:
            field_dict["resource_id"] = resource_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.resource_metadata import ResourceMetadata

        d = dict(src_dict)
        project_id = d.pop("project_id")

        type_ = d.pop("type")

        label = d.pop("label")

        resource_id = d.pop("resource_id", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ResourceMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ResourceMetadata.from_dict(_metadata)

        created_at = d.pop("created_at", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        resource_create_request = cls(
            project_id=project_id,
            type_=type_,
            label=label,
            resource_id=resource_id,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
        )

        resource_create_request.additional_properties = d
        return resource_create_request

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
