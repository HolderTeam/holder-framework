from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="Milestone")


@_attrs_define
class Milestone:
    """
    Attributes:
        milestone_id (UUID): Canonical milestone identifier; this is not a card ID and is never abbreviated.
        card_id (str):
        start_at (int): Unix epoch seconds. For an all-day milestone, this encodes the originating local date at local
            midnight.
        all_day (bool): When true, start_at and end_at carry local calendar-date semantics and clients should render
            dates rather than ordinary timed instants.
        created_at (int):
        updated_at (int):
        end_at (int | None | Unset): Inclusive milestone end in Unix epoch seconds. For an all-day milestone, this
            encodes the inclusive ending local date at local midnight.
        kind (None | str | Unset):
        description (None | str | Unset):
        card_title (str | Unset): Included in project calendar responses.
    """

    milestone_id: UUID
    card_id: str
    start_at: int
    all_day: bool
    created_at: int
    updated_at: int
    end_at: int | None | Unset = UNSET
    kind: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    card_title: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        milestone_id = str(self.milestone_id)

        card_id = self.card_id

        start_at = self.start_at

        all_day = self.all_day

        created_at = self.created_at

        updated_at = self.updated_at

        end_at: int | None | Unset
        if isinstance(self.end_at, Unset):
            end_at = UNSET
        else:
            end_at = self.end_at

        kind: None | str | Unset
        if isinstance(self.kind, Unset):
            kind = UNSET
        else:
            kind = self.kind

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        card_title = self.card_title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "milestone_id": milestone_id,
                "card_id": card_id,
                "start_at": start_at,
                "all_day": all_day,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if end_at is not UNSET:
            field_dict["end_at"] = end_at
        if kind is not UNSET:
            field_dict["kind"] = kind
        if description is not UNSET:
            field_dict["description"] = description
        if card_title is not UNSET:
            field_dict["card_title"] = card_title

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        milestone_id = UUID(d.pop("milestone_id"))

        card_id = d.pop("card_id")

        start_at = d.pop("start_at")

        all_day = d.pop("all_day")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_end_at(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        end_at = _parse_end_at(d.pop("end_at", UNSET))

        def _parse_kind(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        kind = _parse_kind(d.pop("kind", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        card_title = d.pop("card_title", UNSET)

        milestone = cls(
            milestone_id=milestone_id,
            card_id=card_id,
            start_at=start_at,
            all_day=all_day,
            created_at=created_at,
            updated_at=updated_at,
            end_at=end_at,
            kind=kind,
            description=description,
            card_title=card_title,
        )

        milestone.additional_properties = d
        return milestone

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
