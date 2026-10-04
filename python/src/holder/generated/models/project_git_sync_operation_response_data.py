from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.project_git_sync_operation_response_data_status import (
    ProjectGitSyncOperationResponseDataStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_git_sync_operation_response_data_pull import (
        ProjectGitSyncOperationResponseDataPull,
    )
    from ..models.project_git_sync_operation_response_data_push import (
        ProjectGitSyncOperationResponseDataPush,
    )


T = TypeVar("T", bound="ProjectGitSyncOperationResponseData")


@_attrs_define
class ProjectGitSyncOperationResponseData:
    """
    Attributes:
        project_id (str):
        branch (str):
        status (ProjectGitSyncOperationResponseDataStatus):
        error_code (None | str): Stable operation failure code. Git failures are returned in a successful HTTP envelope.
        error_message (None | str):
        pull (ProjectGitSyncOperationResponseDataPull):
        push (ProjectGitSyncOperationResponseDataPush):
        remote_url (None | str | Unset):
    """

    project_id: str
    branch: str
    status: ProjectGitSyncOperationResponseDataStatus
    error_code: None | str
    error_message: None | str
    pull: ProjectGitSyncOperationResponseDataPull
    push: ProjectGitSyncOperationResponseDataPush
    remote_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        branch = self.branch

        status = self.status.value

        error_code: None | str
        error_code = self.error_code

        error_message: None | str
        error_message = self.error_message

        pull = self.pull.to_dict()

        push = self.push.to_dict()

        remote_url: None | str | Unset
        if isinstance(self.remote_url, Unset):
            remote_url = UNSET
        else:
            remote_url = self.remote_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "branch": branch,
                "status": status,
                "error_code": error_code,
                "error_message": error_message,
                "pull": pull,
                "push": push,
            }
        )
        if remote_url is not UNSET:
            field_dict["remote_url"] = remote_url

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.project_git_sync_operation_response_data_pull import (
            ProjectGitSyncOperationResponseDataPull,
        )
        from ..models.project_git_sync_operation_response_data_push import (
            ProjectGitSyncOperationResponseDataPush,
        )

        d = dict(src_dict)
        project_id = d.pop("project_id")

        branch = d.pop("branch")

        status = ProjectGitSyncOperationResponseDataStatus(d.pop("status"))

        def _parse_error_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_code = _parse_error_code(d.pop("error_code"))

        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("error_message"))

        pull = ProjectGitSyncOperationResponseDataPull.from_dict(d.pop("pull"))

        push = ProjectGitSyncOperationResponseDataPush.from_dict(d.pop("push"))

        def _parse_remote_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        remote_url = _parse_remote_url(d.pop("remote_url", UNSET))

        project_git_sync_operation_response_data = cls(
            project_id=project_id,
            branch=branch,
            status=status,
            error_code=error_code,
            error_message=error_message,
            pull=pull,
            push=push,
            remote_url=remote_url,
        )

        project_git_sync_operation_response_data.additional_properties = d
        return project_git_sync_operation_response_data

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
