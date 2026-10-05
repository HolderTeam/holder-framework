from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.calendar_card_activity import CalendarCardActivity
    from ..models.milestone import Milestone


T = TypeVar("T", bound="ProjectCalendarResponseData")


@_attrs_define
class ProjectCalendarResponseData:
    """
    Attributes:
        project_id (str):
        from_ (int): Inclusive lower bound in Unix epoch seconds.
        to (int): Inclusive upper bound in Unix epoch seconds.
        milestones (list[Milestone]):
        created_cards (list[CalendarCardActivity]):
        updated_cards (list[CalendarCardActivity]):
    """

    project_id: str
    from_: int
    to: int
    milestones: list[Milestone]
    created_cards: list[CalendarCardActivity]
    updated_cards: list[CalendarCardActivity]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        from_ = self.from_

        to = self.to

        milestones = []
        for milestones_item_data in self.milestones:
            milestones_item = milestones_item_data.to_dict()
            milestones.append(milestones_item)

        created_cards = []
        for created_cards_item_data in self.created_cards:
            created_cards_item = created_cards_item_data.to_dict()
            created_cards.append(created_cards_item)

        updated_cards = []
        for updated_cards_item_data in self.updated_cards:
            updated_cards_item = updated_cards_item_data.to_dict()
            updated_cards.append(updated_cards_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "from": from_,
                "to": to,
                "milestones": milestones,
                "created_cards": created_cards,
                "updated_cards": updated_cards,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.calendar_card_activity import (
            CalendarCardActivity,
        )
        from ..models.milestone import Milestone

        d = dict(src_dict)
        project_id = d.pop("project_id")

        from_ = d.pop("from")

        to = d.pop("to")

        milestones = []
        _milestones = d.pop("milestones")
        for milestones_item_data in _milestones:
            milestones_item = Milestone.from_dict(milestones_item_data)

            milestones.append(milestones_item)

        created_cards = []
        _created_cards = d.pop("created_cards")
        for created_cards_item_data in _created_cards:
            created_cards_item = CalendarCardActivity.from_dict(created_cards_item_data)

            created_cards.append(created_cards_item)

        updated_cards = []
        _updated_cards = d.pop("updated_cards")
        for updated_cards_item_data in _updated_cards:
            updated_cards_item = CalendarCardActivity.from_dict(updated_cards_item_data)

            updated_cards.append(updated_cards_item)

        project_calendar_response_data = cls(
            project_id=project_id,
            from_=from_,
            to=to,
            milestones=milestones,
            created_cards=created_cards,
            updated_cards=updated_cards,
        )

        project_calendar_response_data.additional_properties = d
        return project_calendar_response_data

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
