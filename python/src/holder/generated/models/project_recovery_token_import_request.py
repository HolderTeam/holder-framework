from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="ProjectRecoveryTokenImportRequest")


@_attrs_define
class ProjectRecoveryTokenImportRequest:
    """
    Attributes:
        pin (str):
        recovery_token (str): Serialized `.hrk` recovery token JSON payload.
    """

    pin: str
    recovery_token: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pin = self.pin

        recovery_token = self.recovery_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pin": pin,
                "recovery_token": recovery_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        pin = d.pop("pin")

        recovery_token = d.pop("recovery_token")

        project_recovery_token_import_request = cls(
            pin=pin,
            recovery_token=recovery_token,
        )

        project_recovery_token_import_request.additional_properties = d
        return project_recovery_token_import_request

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
