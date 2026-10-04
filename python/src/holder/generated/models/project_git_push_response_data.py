from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.project_git_push_response_data_status import (
    ProjectGitPushResponseDataStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectGitPushResponseData")


@_attrs_define
class ProjectGitPushResponseData:
    """
    Attributes:
        project_id (str):
        branch (str):
        status (ProjectGitPushResponseDataStatus):
        ahead_count (int):
        behind_count (int):
        remote_url (None | str | Unset):
        local_head_commit (None | str | Unset):
        error_code (None | str | Unset):
        error_message (None | str | Unset):
        next_action (None | str | Unset):
    """

    project_id: str
    branch: str
    status: ProjectGitPushResponseDataStatus
    ahead_count: int
    behind_count: int
    remote_url: None | str | Unset = UNSET
    local_head_commit: None | str | Unset = UNSET
    error_code: None | str | Unset = UNSET
    error_message: None | str | Unset = UNSET
    next_action: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        branch = self.branch

        status = self.status.value

        ahead_count = self.ahead_count

        behind_count = self.behind_count

        remote_url: None | str | Unset
        if isinstance(self.remote_url, Unset):
            remote_url = UNSET
        else:
            remote_url = self.remote_url

        local_head_commit: None | str | Unset
        if isinstance(self.local_head_commit, Unset):
            local_head_commit = UNSET
        else:
            local_head_commit = self.local_head_commit

        error_code: None | str | Unset
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        next_action: None | str | Unset
        if isinstance(self.next_action, Unset):
            next_action = UNSET
        else:
            next_action = self.next_action

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "branch": branch,
                "status": status,
                "ahead_count": ahead_count,
                "behind_count": behind_count,
            }
        )
        if remote_url is not UNSET:
            field_dict["remote_url"] = remote_url
        if local_head_commit is not UNSET:
            field_dict["local_head_commit"] = local_head_commit
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if next_action is not UNSET:
            field_dict["next_action"] = next_action

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        branch = d.pop("branch")

        status = ProjectGitPushResponseDataStatus(d.pop("status"))

        ahead_count = d.pop("ahead_count")

        behind_count = d.pop("behind_count")

        def _parse_remote_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        remote_url = _parse_remote_url(d.pop("remote_url", UNSET))

        def _parse_local_head_commit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        local_head_commit = _parse_local_head_commit(d.pop("local_head_commit", UNSET))

        def _parse_error_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_code = _parse_error_code(d.pop("error_code", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_next_action(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_action = _parse_next_action(d.pop("next_action", UNSET))

        project_git_push_response_data = cls(
            project_id=project_id,
            branch=branch,
            status=status,
            ahead_count=ahead_count,
            behind_count=behind_count,
            remote_url=remote_url,
            local_head_commit=local_head_commit,
            error_code=error_code,
            error_message=error_message,
            next_action=next_action,
        )

        project_git_push_response_data.additional_properties = d
        return project_git_push_response_data

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
