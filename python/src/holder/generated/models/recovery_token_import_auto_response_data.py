from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.recovery_token_import_auto_response_data_pull_status import (
    RecoveryTokenImportAutoResponseDataPullStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="RecoveryTokenImportAutoResponseData")


@_attrs_define
class RecoveryTokenImportAutoResponseData:
    """
    Attributes:
        project_id (str):
        project_created (bool):
        remote_hint_present (bool):
        remote_configured (bool):
        pull_status (RecoveryTokenImportAutoResponseDataPullStatus):
        remote_error (None | str | Unset):
        pull_error (None | str | Unset):
    """

    project_id: str
    project_created: bool
    remote_hint_present: bool
    remote_configured: bool
    pull_status: RecoveryTokenImportAutoResponseDataPullStatus
    remote_error: None | str | Unset = UNSET
    pull_error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        project_created = self.project_created

        remote_hint_present = self.remote_hint_present

        remote_configured = self.remote_configured

        pull_status = self.pull_status.value

        remote_error: None | str | Unset
        if isinstance(self.remote_error, Unset):
            remote_error = UNSET
        else:
            remote_error = self.remote_error

        pull_error: None | str | Unset
        if isinstance(self.pull_error, Unset):
            pull_error = UNSET
        else:
            pull_error = self.pull_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "project_created": project_created,
                "remote_hint_present": remote_hint_present,
                "remote_configured": remote_configured,
                "pull_status": pull_status,
            }
        )
        if remote_error is not UNSET:
            field_dict["remote_error"] = remote_error
        if pull_error is not UNSET:
            field_dict["pull_error"] = pull_error

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        project_created = d.pop("project_created")

        remote_hint_present = d.pop("remote_hint_present")

        remote_configured = d.pop("remote_configured")

        pull_status = RecoveryTokenImportAutoResponseDataPullStatus(
            d.pop("pull_status")
        )

        def _parse_remote_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        remote_error = _parse_remote_error(d.pop("remote_error", UNSET))

        def _parse_pull_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pull_error = _parse_pull_error(d.pop("pull_error", UNSET))

        recovery_token_import_auto_response_data = cls(
            project_id=project_id,
            project_created=project_created,
            remote_hint_present=remote_hint_present,
            remote_configured=remote_configured,
            pull_status=pull_status,
            remote_error=remote_error,
            pull_error=pull_error,
        )

        recovery_token_import_auto_response_data.additional_properties = d
        return recovery_token_import_auto_response_data

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
