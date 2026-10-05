from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.project_git_sync_operation_response_data_push_status import (
    ProjectGitSyncOperationResponseDataPushStatus,
)

T = TypeVar("T", bound="ProjectGitSyncOperationResponseDataPush")


@_attrs_define
class ProjectGitSyncOperationResponseDataPush:
    """
    Attributes:
        attempted (bool):
        status (ProjectGitSyncOperationResponseDataPushStatus):
        ahead_count (int):
        behind_count (int):
        local_head_commit (None | str):
        error_message (None | str):
    """

    attempted: bool
    status: ProjectGitSyncOperationResponseDataPushStatus
    ahead_count: int
    behind_count: int
    local_head_commit: None | str
    error_message: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempted = self.attempted

        status = self.status.value

        ahead_count = self.ahead_count

        behind_count = self.behind_count

        local_head_commit: None | str
        local_head_commit = self.local_head_commit

        error_message: None | str
        error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempted": attempted,
                "status": status,
                "ahead_count": ahead_count,
                "behind_count": behind_count,
                "local_head_commit": local_head_commit,
                "error_message": error_message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        attempted = d.pop("attempted")

        status = ProjectGitSyncOperationResponseDataPushStatus(d.pop("status"))

        ahead_count = d.pop("ahead_count")

        behind_count = d.pop("behind_count")

        def _parse_local_head_commit(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        local_head_commit = _parse_local_head_commit(d.pop("local_head_commit"))

        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("error_message"))

        project_git_sync_operation_response_data_push = cls(
            attempted=attempted,
            status=status,
            ahead_count=ahead_count,
            behind_count=behind_count,
            local_head_commit=local_head_commit,
            error_message=error_message,
        )

        project_git_sync_operation_response_data_push.additional_properties = d
        return project_git_sync_operation_response_data_push

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
