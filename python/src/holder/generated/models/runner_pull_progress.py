from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="RunnerPullProgress")


@_attrs_define
class RunnerPullProgress:
    """
    Attributes:
        completed (int):
        total (int):
        percent (float):
        stage (str):
    """

    completed: int
    total: int
    percent: float
    stage: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        completed = self.completed

        total = self.total

        percent = self.percent

        stage = self.stage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completed": completed,
                "total": total,
                "percent": percent,
                "stage": stage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        completed = d.pop("completed")

        total = d.pop("total")

        percent = d.pop("percent")

        stage = d.pop("stage")

        runner_pull_progress = cls(
            completed=completed,
            total=total,
            percent=percent,
            stage=stage,
        )

        runner_pull_progress.additional_properties = d
        return runner_pull_progress

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
