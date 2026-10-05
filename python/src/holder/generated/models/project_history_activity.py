from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.card_history_author import CardHistoryAuthor
    from ..models.project_history_affected_object import ProjectHistoryAffectedObject


T = TypeVar("T", bound="ProjectHistoryActivity")


@_attrs_define
class ProjectHistoryActivity:
    """
    Attributes:
        oid (str):
        parent_oids (list[str]):
        author (CardHistoryAuthor):
        authored_at (int):
        committed_at (int):
        message (str):
        affected_objects (list[ProjectHistoryAffectedObject]):
        is_merge (bool):
    """

    oid: str
    parent_oids: list[str]
    author: CardHistoryAuthor
    authored_at: int
    committed_at: int
    message: str
    affected_objects: list[ProjectHistoryAffectedObject]
    is_merge: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        oid = self.oid

        parent_oids = self.parent_oids

        author = self.author.to_dict()

        authored_at = self.authored_at

        committed_at = self.committed_at

        message = self.message

        affected_objects = []
        for affected_objects_item_data in self.affected_objects:
            affected_objects_item = affected_objects_item_data.to_dict()
            affected_objects.append(affected_objects_item)

        is_merge = self.is_merge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "oid": oid,
                "parent_oids": parent_oids,
                "author": author,
                "authored_at": authored_at,
                "committed_at": committed_at,
                "message": message,
                "affected_objects": affected_objects,
                "is_merge": is_merge,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.card_history_author import CardHistoryAuthor
        from ..models.project_history_affected_object import (
            ProjectHistoryAffectedObject,
        )

        d = dict(src_dict)
        oid = d.pop("oid")

        parent_oids = cast(list[str], d.pop("parent_oids"))

        author = CardHistoryAuthor.from_dict(d.pop("author"))

        authored_at = d.pop("authored_at")

        committed_at = d.pop("committed_at")

        message = d.pop("message")

        affected_objects = []
        _affected_objects = d.pop("affected_objects")
        for affected_objects_item_data in _affected_objects:
            affected_objects_item = ProjectHistoryAffectedObject.from_dict(
                affected_objects_item_data
            )

            affected_objects.append(affected_objects_item)

        is_merge = d.pop("is_merge")

        project_history_activity = cls(
            oid=oid,
            parent_oids=parent_oids,
            author=author,
            authored_at=authored_at,
            committed_at=committed_at,
            message=message,
            affected_objects=affected_objects,
            is_merge=is_merge,
        )

        project_history_activity.additional_properties = d
        return project_history_activity

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
