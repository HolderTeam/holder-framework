from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.project_sync import ProjectSync


T = TypeVar("T", bound="ProjectGitSyncStatusResponseData")


@_attrs_define
class ProjectGitSyncStatusResponseData:
    """
    Attributes:
        project_id (str):
        sync (ProjectSync):
    """

    project_id: str
    sync: ProjectSync
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        sync = self.sync.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "sync": sync,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.project_sync import ProjectSync

        d = dict(src_dict)
        project_id = d.pop("project_id")

        sync = ProjectSync.from_dict(d.pop("sync"))

        project_git_sync_status_response_data = cls(
            project_id=project_id,
            sync=sync,
        )

        project_git_sync_status_response_data.additional_properties = d
        return project_git_sync_status_response_data

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
