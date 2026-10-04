from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_metadata import ResourceMetadata


T = TypeVar("T", bound="ResourceUpdateRequest")


@_attrs_define
class ResourceUpdateRequest:
    """
    Attributes:
        type_ (str | Unset):
        label (str | Unset):
        metadata (ResourceMetadata | Unset): Permissive metadata map. Repeated and custom values are preserved in order.
        updated_at (int | Unset):
    """

    type_: str | Unset = UNSET
    label: str | Unset = UNSET
    metadata: ResourceMetadata | Unset = UNSET
    updated_at: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        label = self.label

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if label is not UNSET:
            field_dict["label"] = label
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.resource_metadata import ResourceMetadata

        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        label = d.pop("label", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ResourceMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ResourceMetadata.from_dict(_metadata)

        updated_at = d.pop("updated_at", UNSET)

        resource_update_request = cls(
            type_=type_,
            label=label,
            metadata=metadata,
            updated_at=updated_at,
        )

        resource_update_request.additional_properties = d
        return resource_update_request

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
