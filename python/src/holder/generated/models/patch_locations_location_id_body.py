from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patch_locations_location_id_body_configuration import (
        PatchLocationsLocationIdBodyConfiguration,
    )


T = TypeVar("T", bound="PatchLocationsLocationIdBody")


@_attrs_define
class PatchLocationsLocationIdBody:
    """
    Attributes:
        name (str | Unset):
        configuration (PatchLocationsLocationIdBodyConfiguration | Unset):
    """

    name: str | Unset = UNSET
    configuration: PatchLocationsLocationIdBodyConfiguration | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        configuration: dict[str, Any] | Unset = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = self.configuration.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.patch_locations_location_id_body_configuration import (
            PatchLocationsLocationIdBodyConfiguration,
        )

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _configuration = d.pop("configuration", UNSET)
        configuration: PatchLocationsLocationIdBodyConfiguration | Unset
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = PatchLocationsLocationIdBodyConfiguration.from_dict(
                _configuration
            )

        patch_locations_location_id_body = cls(
            name=name,
            configuration=configuration,
        )

        patch_locations_location_id_body.additional_properties = d
        return patch_locations_location_id_body

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
