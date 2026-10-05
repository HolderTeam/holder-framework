from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_provider_credential import AiProviderCredential
    from ..models.ai_status_pull_job import AiStatusPullJob


T = TypeVar("T", bound="AiStatusData")


@_attrs_define
class AiStatusData:
    """
    Attributes:
        checked_at (int):
        runner_available (bool):
        runner_last_checked (int):
        active_runs (int):
        active_pull_jobs (int):
        pulls (list[AiStatusPullJob]):
        cloud (list[AiProviderCredential]):
        cloud_configured_providers (int):
        runner_version (None | str | Unset):
        runner_error (None | str | Unset):
    """

    checked_at: int
    runner_available: bool
    runner_last_checked: int
    active_runs: int
    active_pull_jobs: int
    pulls: list[AiStatusPullJob]
    cloud: list[AiProviderCredential]
    cloud_configured_providers: int
    runner_version: None | str | Unset = UNSET
    runner_error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checked_at = self.checked_at

        runner_available = self.runner_available

        runner_last_checked = self.runner_last_checked

        active_runs = self.active_runs

        active_pull_jobs = self.active_pull_jobs

        pulls = []
        for pulls_item_data in self.pulls:
            pulls_item = pulls_item_data.to_dict()
            pulls.append(pulls_item)

        cloud = []
        for cloud_item_data in self.cloud:
            cloud_item = cloud_item_data.to_dict()
            cloud.append(cloud_item)

        cloud_configured_providers = self.cloud_configured_providers

        runner_version: None | str | Unset
        if isinstance(self.runner_version, Unset):
            runner_version = UNSET
        else:
            runner_version = self.runner_version

        runner_error: None | str | Unset
        if isinstance(self.runner_error, Unset):
            runner_error = UNSET
        else:
            runner_error = self.runner_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checked_at": checked_at,
                "runner_available": runner_available,
                "runner_last_checked": runner_last_checked,
                "active_runs": active_runs,
                "active_pull_jobs": active_pull_jobs,
                "pulls": pulls,
                "cloud": cloud,
                "cloud_configured_providers": cloud_configured_providers,
            }
        )
        if runner_version is not UNSET:
            field_dict["runner_version"] = runner_version
        if runner_error is not UNSET:
            field_dict["runner_error"] = runner_error

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ai_provider_credential import (
            AiProviderCredential,
        )
        from ..models.ai_status_pull_job import AiStatusPullJob

        d = dict(src_dict)
        checked_at = d.pop("checked_at")

        runner_available = d.pop("runner_available")

        runner_last_checked = d.pop("runner_last_checked")

        active_runs = d.pop("active_runs")

        active_pull_jobs = d.pop("active_pull_jobs")

        pulls = []
        _pulls = d.pop("pulls")
        for pulls_item_data in _pulls:
            pulls_item = AiStatusPullJob.from_dict(pulls_item_data)

            pulls.append(pulls_item)

        cloud = []
        _cloud = d.pop("cloud")
        for cloud_item_data in _cloud:
            cloud_item = AiProviderCredential.from_dict(cloud_item_data)

            cloud.append(cloud_item)

        cloud_configured_providers = d.pop("cloud_configured_providers")

        def _parse_runner_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        runner_version = _parse_runner_version(d.pop("runner_version", UNSET))

        def _parse_runner_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        runner_error = _parse_runner_error(d.pop("runner_error", UNSET))

        ai_status_data = cls(
            checked_at=checked_at,
            runner_available=runner_available,
            runner_last_checked=runner_last_checked,
            active_runs=active_runs,
            active_pull_jobs=active_pull_jobs,
            pulls=pulls,
            cloud=cloud,
            cloud_configured_providers=cloud_configured_providers,
            runner_version=runner_version,
            runner_error=runner_error,
        )

        ai_status_data.additional_properties = d
        return ai_status_data

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
