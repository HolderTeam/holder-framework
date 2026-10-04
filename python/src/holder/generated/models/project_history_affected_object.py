from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.project_history_affected_object_kind import (
    ProjectHistoryAffectedObjectKind,
)

T = TypeVar("T", bound="ProjectHistoryAffectedObject")


@_attrs_define
class ProjectHistoryAffectedObject:
    """
    Attributes:
        kind (ProjectHistoryAffectedObjectKind):
        paths (list[str]):
    """

    kind: ProjectHistoryAffectedObjectKind
    paths: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        paths = self.paths

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "paths": paths,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        kind = ProjectHistoryAffectedObjectKind(d.pop("kind"))

        paths = cast(list[str], d.pop("paths"))

        project_history_affected_object = cls(
            kind=kind,
            paths=paths,
        )

        project_history_affected_object.additional_properties = d
        return project_history_affected_object

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
