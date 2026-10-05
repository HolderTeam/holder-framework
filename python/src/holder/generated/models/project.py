from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.project_privacy_mode import ProjectPrivacyMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_sync import ProjectSync


T = TypeVar("T", bound="Project")


@_attrs_define
class Project:
    """
    Attributes:
        project_id (str):
        name (str):
        root_path (str):
        privacy_mode (ProjectPrivacyMode):
        created_at (int):
        updated_at (int):
        sync (ProjectSync):
        git_remote_url (None | str | Unset):
        git_provider (None | str | Unset):
        project_key_id (None | str | Unset):
        card_count (int | Unset): Present when count=true.
        root_card_count (int | Unset): Present when count=true.
    """

    project_id: str
    name: str
    root_path: str
    privacy_mode: ProjectPrivacyMode
    created_at: int
    updated_at: int
    sync: ProjectSync
    git_remote_url: None | str | Unset = UNSET
    git_provider: None | str | Unset = UNSET
    project_key_id: None | str | Unset = UNSET
    card_count: int | Unset = UNSET
    root_card_count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        name = self.name

        root_path = self.root_path

        privacy_mode = self.privacy_mode.value

        created_at = self.created_at

        updated_at = self.updated_at

        sync = self.sync.to_dict()

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

        project_key_id: None | str | Unset
        if isinstance(self.project_key_id, Unset):
            project_key_id = UNSET
        else:
            project_key_id = self.project_key_id

        card_count = self.card_count

        root_card_count = self.root_card_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "name": name,
                "root_path": root_path,
                "privacy_mode": privacy_mode,
                "created_at": created_at,
                "updated_at": updated_at,
                "sync": sync,
            }
        )
        if git_remote_url is not UNSET:
            field_dict["git_remote_url"] = git_remote_url
        if git_provider is not UNSET:
            field_dict["git_provider"] = git_provider
        if project_key_id is not UNSET:
            field_dict["project_key_id"] = project_key_id
        if card_count is not UNSET:
            field_dict["card_count"] = card_count
        if root_card_count is not UNSET:
            field_dict["root_card_count"] = root_card_count

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.project_sync import ProjectSync

        d = dict(src_dict)
        project_id = d.pop("project_id")

        name = d.pop("name")

        root_path = d.pop("root_path")

        privacy_mode = ProjectPrivacyMode(d.pop("privacy_mode"))

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        sync = ProjectSync.from_dict(d.pop("sync"))

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

        def _parse_project_key_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_key_id = _parse_project_key_id(d.pop("project_key_id", UNSET))

        card_count = d.pop("card_count", UNSET)

        root_card_count = d.pop("root_card_count", UNSET)

        project = cls(
            project_id=project_id,
            name=name,
            root_path=root_path,
            privacy_mode=privacy_mode,
            created_at=created_at,
            updated_at=updated_at,
            sync=sync,
            git_remote_url=git_remote_url,
            git_provider=git_provider,
            project_key_id=project_key_id,
            card_count=card_count,
            root_card_count=root_card_count,
        )

        project.additional_properties = d
        return project

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
