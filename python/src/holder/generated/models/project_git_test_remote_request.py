from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectGitTestRemoteRequest")


@_attrs_define
class ProjectGitTestRemoteRequest:
    """
    Attributes:
        remote_url (None | str | Unset): Optional remote URL override for this read-only probe. Stored project
            configuration and Git configuration are unchanged. If omitted, uses the configured URL; null probes no remote.
        branch (None | str | Unset): Optional branch hint, echoed in the result. If omitted, reports local_default. The
            probe lists remote refs without resolving or fetching a branch.
    """

    remote_url: None | str | Unset = UNSET
    branch: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        remote_url: None | str | Unset
        if isinstance(self.remote_url, Unset):
            remote_url = UNSET
        else:
            remote_url = self.remote_url

        branch: None | str | Unset
        if isinstance(self.branch, Unset):
            branch = UNSET
        else:
            branch = self.branch

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if remote_url is not UNSET:
            field_dict["remote_url"] = remote_url
        if branch is not UNSET:
            field_dict["branch"] = branch

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_remote_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        remote_url = _parse_remote_url(d.pop("remote_url", UNSET))

        def _parse_branch(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        branch = _parse_branch(d.pop("branch", UNSET))

        project_git_test_remote_request = cls(
            remote_url=remote_url,
            branch=branch,
        )

        project_git_test_remote_request.additional_properties = d
        return project_git_test_remote_request

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
