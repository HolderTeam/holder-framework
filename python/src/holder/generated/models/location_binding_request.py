from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location_binding_request_values import LocationBindingRequestValues


T = TypeVar("T", bound="LocationBindingRequest")


@_attrs_define
class LocationBindingRequest:
    """
    Attributes:
        values (LocationBindingRequestValues):
        preview (str | Unset):
    """

    values: LocationBindingRequestValues
    preview: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        values = self.values.to_dict()

        preview = self.preview

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "values": values,
            }
        )
        if preview is not UNSET:
            field_dict["preview"] = preview

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.location_binding_request_values import (
            LocationBindingRequestValues,
        )

        d = dict(src_dict)
        values = LocationBindingRequestValues.from_dict(d.pop("values"))

        preview = d.pop("preview", UNSET)

        location_binding_request = cls(
            values=values,
            preview=preview,
        )

        location_binding_request.additional_properties = d
        return location_binding_request

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
