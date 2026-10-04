from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectUpdateResponseData")


@_attrs_define
class ProjectUpdateResponseData:
    """
    Attributes:
        project_id (str):
        git_remote_changed (bool | Unset): Present when git_remote_url is supplied. Reports whether the stored remote
            URL changed, including disconnecting it. Reapplying the same value returns false. The URL is persisted only
            after Git accepts the remote operation.
    """

    project_id: str
    git_remote_changed: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        git_remote_changed = self.git_remote_changed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
            }
        )
        if git_remote_changed is not UNSET:
            field_dict["git_remote_changed"] = git_remote_changed

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        git_remote_changed = d.pop("git_remote_changed", UNSET)

        project_update_response_data = cls(
            project_id=project_id,
            git_remote_changed=git_remote_changed,
        )

        project_update_response_data.additional_properties = d
        return project_update_response_data

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
