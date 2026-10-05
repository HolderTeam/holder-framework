from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.storage_location_provider import StorageLocationProvider
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.storage_location_configuration import StorageLocationConfiguration


T = TypeVar("T", bound="StorageLocation")


@_attrs_define
class StorageLocation:
    """
    Attributes:
        location_id (str):
        project_id (str):
        name (str):
        provider (StorageLocationProvider):
        configuration (StorageLocationConfiguration): Portable non-secret provider configuration.
        bound (bool):
        created_at (int):
        updated_at (int):
        binding_preview (None | str | Unset): Safe display text; credentials are never returned.
    """

    location_id: str
    project_id: str
    name: str
    provider: StorageLocationProvider
    configuration: StorageLocationConfiguration
    bound: bool
    created_at: int
    updated_at: int
    binding_preview: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        location_id = self.location_id

        project_id = self.project_id

        name = self.name

        provider = self.provider.value

        configuration = self.configuration.to_dict()

        bound = self.bound

        created_at = self.created_at

        updated_at = self.updated_at

        binding_preview: None | str | Unset
        if isinstance(self.binding_preview, Unset):
            binding_preview = UNSET
        else:
            binding_preview = self.binding_preview

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "location_id": location_id,
                "project_id": project_id,
                "name": name,
                "provider": provider,
                "configuration": configuration,
                "bound": bound,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if binding_preview is not UNSET:
            field_dict["binding_preview"] = binding_preview

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.storage_location_configuration import (
            StorageLocationConfiguration,
        )

        d = dict(src_dict)
        location_id = d.pop("location_id")

        project_id = d.pop("project_id")

        name = d.pop("name")

        provider = StorageLocationProvider(d.pop("provider"))

        configuration = StorageLocationConfiguration.from_dict(d.pop("configuration"))

        bound = d.pop("bound")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_binding_preview(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        binding_preview = _parse_binding_preview(d.pop("binding_preview", UNSET))

        storage_location = cls(
            location_id=location_id,
            project_id=project_id,
            name=name,
            provider=provider,
            configuration=configuration,
            bound=bound,
            created_at=created_at,
            updated_at=updated_at,
            binding_preview=binding_preview,
        )

        storage_location.additional_properties = d
        return storage_location

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
