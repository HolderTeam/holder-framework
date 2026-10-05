from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.project_update_request_privacy_mode import ProjectUpdateRequestPrivacyMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectUpdateRequest")


@_attrs_define
class ProjectUpdateRequest:
    """
    Attributes:
        updated_at (int):
        name (None | str | Unset):
        root_path (None | str | Unset):
        git_remote_url (None | str | Unset):
        git_provider (None | str | Unset):
        privacy_mode (ProjectUpdateRequestPrivacyMode | Unset):
        project_key_id (None | str | Unset):
    """

    updated_at: int
    name: None | str | Unset = UNSET
    root_path: None | str | Unset = UNSET
    git_remote_url: None | str | Unset = UNSET
    git_provider: None | str | Unset = UNSET
    privacy_mode: ProjectUpdateRequestPrivacyMode | Unset = UNSET
    project_key_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_at = self.updated_at

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        root_path: None | str | Unset
        if isinstance(self.root_path, Unset):
            root_path = UNSET
        else:
            root_path = self.root_path

        git_remote_url: None | str | Unset
        if isinstance(self.git_remote_url, Unset):
            git_remote_url = UNSET
        else:
            git_remote_url = self.git_remote_url

        git_provider: None | str | Unset
        if isinstance(self.git_provider, Unset):
            git_provider = UNSET
        else:
            git_provider = self.git_provider

        privacy_mode: str | Unset = UNSET
        if not isinstance(self.privacy_mode, Unset):
            privacy_mode = self.privacy_mode.value

        project_key_id: None | str | Unset
        if isinstance(self.project_key_id, Unset):
            project_key_id = UNSET
        else:
            project_key_id = self.project_key_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_at": updated_at,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if root_path is not UNSET:
            field_dict["root_path"] = root_path
        if git_remote_url is not UNSET:
            field_dict["git_remote_url"] = git_remote_url
        if git_provider is not UNSET:
            field_dict["git_provider"] = git_provider
        if privacy_mode is not UNSET:
            field_dict["privacy_mode"] = privacy_mode
        if project_key_id is not UNSET:
            field_dict["project_key_id"] = project_key_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        updated_at = d.pop("updated_at")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_root_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        root_path = _parse_root_path(d.pop("root_path", UNSET))

        def _parse_git_remote_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        git_remote_url = _parse_git_remote_url(d.pop("git_remote_url", UNSET))

        def _parse_git_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        git_provider = _parse_git_provider(d.pop("git_provider", UNSET))

        _privacy_mode = d.pop("privacy_mode", UNSET)
        privacy_mode: ProjectUpdateRequestPrivacyMode | Unset
        if isinstance(_privacy_mode, Unset):
            privacy_mode = UNSET
        else:
            privacy_mode = ProjectUpdateRequestPrivacyMode(_privacy_mode)

        def _parse_project_key_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_key_id = _parse_project_key_id(d.pop("project_key_id", UNSET))

        project_update_request = cls(
            updated_at=updated_at,
            name=name,
            root_path=root_path,
            git_remote_url=git_remote_url,
            git_provider=git_provider,
            privacy_mode=privacy_mode,
            project_key_id=project_key_id,
        )

        project_update_request.additional_properties = d
        return project_update_request

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
