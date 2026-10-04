from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.project_encryption_check_response_data_privacy_mode import (
    ProjectEncryptionCheckResponseDataPrivacyMode,
)

if TYPE_CHECKING:
    from ..models.project_encryption_check import ProjectEncryptionCheck


T = TypeVar("T", bound="ProjectEncryptionCheckResponseData")


@_attrs_define
class ProjectEncryptionCheckResponseData:
    """
    Attributes:
        project_id (str):
        privacy_mode (ProjectEncryptionCheckResponseDataPrivacyMode):
        check (ProjectEncryptionCheck):
    """

    project_id: str
    privacy_mode: ProjectEncryptionCheckResponseDataPrivacyMode
    check: ProjectEncryptionCheck
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        privacy_mode = self.privacy_mode.value

        check = self.check.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "privacy_mode": privacy_mode,
                "check": check,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.project_encryption_check import (
            ProjectEncryptionCheck,
        )

        d = dict(src_dict)
        project_id = d.pop("project_id")

        privacy_mode = ProjectEncryptionCheckResponseDataPrivacyMode(
            d.pop("privacy_mode")
        )

        check = ProjectEncryptionCheck.from_dict(d.pop("check"))

        project_encryption_check_response_data = cls(
            project_id=project_id,
            privacy_mode=privacy_mode,
            check=check,
        )

        project_encryption_check_response_data.additional_properties = d
        return project_encryption_check_response_data

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
