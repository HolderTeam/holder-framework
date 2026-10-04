from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="MilestoneRemoveResult")


@_attrs_define
class MilestoneRemoveResult:
    """
    Attributes:
        card_id (str):
        milestone_id (UUID): Canonical milestone identifier supplied in the request.
        removed (bool): True when the milestone existed and was removed; false when it was already absent.
    """

    card_id: str
    milestone_id: UUID
    removed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        card_id = self.card_id

        milestone_id = str(self.milestone_id)

        removed = self.removed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "card_id": card_id,
                "milestone_id": milestone_id,
                "removed": removed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        card_id = d.pop("card_id")

        milestone_id = UUID(d.pop("milestone_id"))

        removed = d.pop("removed")

        milestone_remove_result = cls(
            card_id=card_id,
            milestone_id=milestone_id,
            removed=removed,
        )

        milestone_remove_result.additional_properties = d
        return milestone_remove_result

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
