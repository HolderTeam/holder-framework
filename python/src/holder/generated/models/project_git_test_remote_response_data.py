from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.project_git_test_remote_response_data_status import (
    ProjectGitTestRemoteResponseDataStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectGitTestRemoteResponseData")


@_attrs_define
class ProjectGitTestRemoteResponseData:
    """
    Attributes:
        project_id (str):
        branch (str):
        status (ProjectGitTestRemoteResponseDataStatus):
        remote_has_head (bool):
        remote_url (None | str | Unset):
        error_code (None | str | Unset):
        error_message (None | str | Unset):
    """

    project_id: str
    branch: str
    status: ProjectGitTestRemoteResponseDataStatus
    remote_has_head: bool
    remote_url: None | str | Unset = UNSET
    error_code: None | str | Unset = UNSET
    error_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        branch = self.branch

        status = self.status.value

        remote_has_head = self.remote_has_head

        remote_url: None | str | Unset
        if isinstance(self.remote_url, Unset):
            remote_url = UNSET
        else:
            remote_url = self.remote_url

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "branch": branch,
                "status": status,
                "remote_has_head": remote_has_head,
            }
        )
        if remote_url is not UNSET:
            field_dict["remote_url"] = remote_url
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        branch = d.pop("branch")

        status = ProjectGitTestRemoteResponseDataStatus(d.pop("status"))

        remote_has_head = d.pop("remote_has_head")

        def _parse_remote_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        remote_url = _parse_remote_url(d.pop("remote_url", UNSET))

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

        project_git_test_remote_response_data = cls(
            project_id=project_id,
            branch=branch,
            status=status,
            remote_has_head=remote_has_head,
            remote_url=remote_url,
            error_code=error_code,
            error_message=error_message,
        )

        project_git_test_remote_response_data.additional_properties = d
        return project_git_test_remote_response_data

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
