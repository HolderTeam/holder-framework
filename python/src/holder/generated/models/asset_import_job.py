from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.asset_import_job_status import AssetImportJobStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssetImportJob")


@_attrs_define
class AssetImportJob:
    """
    Attributes:
        job_id (str):
        status (AssetImportJobStatus):
        duplicate_reused (bool):
        resource_id (None | str | Unset):
        asset_id (None | str | Unset):
        error (None | str | Unset):
    """

    job_id: str
    status: AssetImportJobStatus
    duplicate_reused: bool
    resource_id: None | str | Unset = UNSET
    asset_id: None | str | Unset = UNSET
    error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        status = self.status.value

        duplicate_reused = self.duplicate_reused

        resource_id: None | str | Unset
        if isinstance(self.resource_id, Unset):
            resource_id = UNSET
        else:
            resource_id = self.resource_id

        asset_id: None | str | Unset
        if isinstance(self.asset_id, Unset):
            asset_id = UNSET
        else:
            asset_id = self.asset_id

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "status": status,
                "duplicate_reused": duplicate_reused,
            }
        )
        if resource_id is not UNSET:
            field_dict["resource_id"] = resource_id
        if asset_id is not UNSET:
            field_dict["asset_id"] = asset_id
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        job_id = d.pop("job_id")

        status = AssetImportJobStatus(d.pop("status"))

        duplicate_reused = d.pop("duplicate_reused")

        def _parse_resource_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        resource_id = _parse_resource_id(d.pop("resource_id", UNSET))

        def _parse_asset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        asset_id = _parse_asset_id(d.pop("asset_id", UNSET))

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        asset_import_job = cls(
            job_id=job_id,
            status=status,
            duplicate_reused=duplicate_reused,
            resource_id=resource_id,
            asset_id=asset_id,
            error=error,
        )

        asset_import_job.additional_properties = d
        return asset_import_job

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
