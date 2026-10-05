from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.storage_location_request_provider import StorageLocationRequestProvider
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.storage_location_request_configuration import (
        StorageLocationRequestConfiguration,
    )


T = TypeVar("T", bound="StorageLocationRequest")


@_attrs_define
class StorageLocationRequest:
    """
    Attributes:
        project_id (str):
        name (str):
        provider (StorageLocationRequestProvider):
        location_id (str | Unset):
        configuration (StorageLocationRequestConfiguration | Unset):
    """

    project_id: str
    name: str
    provider: StorageLocationRequestProvider
    location_id: str | Unset = UNSET
    configuration: StorageLocationRequestConfiguration | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        name = self.name

        provider = self.provider.value

        location_id = self.location_id

        configuration: dict[str, Any] | Unset = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = self.configuration.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "name": name,
                "provider": provider,
            }
        )
        if location_id is not UNSET:
            field_dict["location_id"] = location_id
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.storage_location_request_configuration import (
            StorageLocationRequestConfiguration,
        )

        d = dict(src_dict)
        project_id = d.pop("project_id")

        name = d.pop("name")

        provider = StorageLocationRequestProvider(d.pop("provider"))

        location_id = d.pop("location_id", UNSET)

        _configuration = d.pop("configuration", UNSET)
        configuration: StorageLocationRequestConfiguration | Unset
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = StorageLocationRequestConfiguration.from_dict(
                _configuration
            )

        storage_location_request = cls(
            project_id=project_id,
            name=name,
            provider=provider,
            location_id=location_id,
            configuration=configuration,
        )

        storage_location_request.additional_properties = d
        return storage_location_request

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
