from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.change_event_data_entity import ChangeEventDataEntity

T = TypeVar("T", bound="ChangeEventData")


@_attrs_define
class ChangeEventData:
    """
    Attributes:
        entity (ChangeEventDataEntity):
        entity_id (str):
        project_id (None | str):
        deleted (bool): Entity disappeared from the observed database snapshot. Soft deletion remains an ordinary
            invalidation.
        git_revision (None | str): Observed Git HEAD for this project; live changes may not yet be committed to Git.
    """

    entity: ChangeEventDataEntity
    entity_id: str
    project_id: None | str
    deleted: bool
    git_revision: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entity = self.entity.value

        entity_id = self.entity_id

        project_id: None | str
        project_id = self.project_id

        deleted = self.deleted

        git_revision: None | str
        git_revision = self.git_revision

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity": entity,
                "entity_id": entity_id,
                "project_id": project_id,
                "deleted": deleted,
                "git_revision": git_revision,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        entity = ChangeEventDataEntity(d.pop("entity"))

        entity_id = d.pop("entity_id")

        def _parse_project_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        project_id = _parse_project_id(d.pop("project_id"))

        deleted = d.pop("deleted")

        def _parse_git_revision(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        git_revision = _parse_git_revision(d.pop("git_revision"))

        change_event_data = cls(
            entity=entity,
            entity_id=entity_id,
            project_id=project_id,
            deleted=deleted,
            git_revision=git_revision,
        )

        change_event_data.additional_properties = d
        return change_event_data

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
