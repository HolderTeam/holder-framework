from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.health_data_crypt_filter import HealthDataCryptFilter


T = TypeVar("T", bound="HealthData")


@_attrs_define
class HealthData:
    """
    Attributes:
        db_ok (bool):
        uptime_ms (int):
        api_version (str):
        server_version (str):
        pid (int):
        crypt_filter (HealthDataCryptFilter):
    """

    db_ok: bool
    uptime_ms: int
    api_version: str
    server_version: str
    pid: int
    crypt_filter: HealthDataCryptFilter
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        db_ok = self.db_ok

        uptime_ms = self.uptime_ms

        api_version = self.api_version

        server_version = self.server_version

        pid = self.pid

        crypt_filter = self.crypt_filter.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "db_ok": db_ok,
                "uptime_ms": uptime_ms,
                "api_version": api_version,
                "server_version": server_version,
                "pid": pid,
                "crypt_filter": crypt_filter,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.health_data_crypt_filter import (
            HealthDataCryptFilter,
        )

        d = dict(src_dict)
        db_ok = d.pop("db_ok")

        uptime_ms = d.pop("uptime_ms")

        api_version = d.pop("api_version")

        server_version = d.pop("server_version")

        pid = d.pop("pid")

        crypt_filter = HealthDataCryptFilter.from_dict(d.pop("crypt_filter"))

        health_data = cls(
            db_ok=db_ok,
            uptime_ms=uptime_ms,
            api_version=api_version,
            server_version=server_version,
            pid=pid,
            crypt_filter=crypt_filter,
        )

        health_data.additional_properties = d
        return health_data

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
