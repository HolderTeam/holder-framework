from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.project_create_request_privacy_mode import ProjectCreateRequestPrivacyMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectCreateRequest")


@_attrs_define
class ProjectCreateRequest:
    """
    Attributes:
        name (str):
        project_id (str | Unset): Optional; server generates if omitted.
        root_path (str | Unset): Optional; server chooses a default if omitted.
        git_remote_url (None | str | Unset):
        git_provider (None | str | Unset):
        privacy_mode (ProjectCreateRequestPrivacyMode | Unset): Optional; defaults to encrypted_git.
        project_key_id (None | str | Unset): Optional keyring identifier (metadata only).
        created_at (int | Unset): Optional; server uses current time if omitted or 0.
        updated_at (int | Unset): Optional; server uses created_at if omitted or 0.
    """

    name: str
    project_id: str | Unset = UNSET
    root_path: str | Unset = UNSET
    git_remote_url: None | str | Unset = UNSET
    git_provider: None | str | Unset = UNSET
    privacy_mode: ProjectCreateRequestPrivacyMode | Unset = UNSET
    project_key_id: None | str | Unset = UNSET
    created_at: int | Unset = UNSET
    updated_at: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        project_id = self.project_id

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

        created_at = self.created_at

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
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
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        project_id = d.pop("project_id", UNSET)

        root_path = d.pop("root_path", UNSET)

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
        privacy_mode: ProjectCreateRequestPrivacyMode | Unset
        if isinstance(_privacy_mode, Unset):
            privacy_mode = UNSET
        else:
            privacy_mode = ProjectCreateRequestPrivacyMode(_privacy_mode)

        def _parse_project_key_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_key_id = _parse_project_key_id(d.pop("project_key_id", UNSET))

        created_at = d.pop("created_at", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        project_create_request = cls(
            name=name,
            project_id=project_id,
            root_path=root_path,
            git_remote_url=git_remote_url,
            git_provider=git_provider,
            privacy_mode=privacy_mode,
            project_key_id=project_key_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        project_create_request.additional_properties = d
        return project_create_request

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
