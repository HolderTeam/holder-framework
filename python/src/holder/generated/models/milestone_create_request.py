from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="MilestoneCreateRequest")


@_attrs_define
class MilestoneCreateRequest:
    """
    Attributes:
        start_at (int): Unix epoch seconds. For all_day=true, encode the local calendar date at local midnight.
        end_at (int | None | Unset): Inclusive milestone end. For all_day=true, encode the inclusive ending local date
            at local midnight.
        all_day (bool | Unset): Marks start_at and end_at as local calendar dates rather than timed instants. Default:
            False.
        kind (None | str | Unset):
        description (None | str | Unset):
    """

    start_at: int
    end_at: int | None | Unset = UNSET
    all_day: bool | Unset = False
    kind: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_at = self.start_at

        end_at: int | None | Unset
        if isinstance(self.end_at, Unset):
            end_at = UNSET
        else:
            end_at = self.end_at

        all_day = self.all_day

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_at": start_at,
            }
        )
        if end_at is not UNSET:
            field_dict["end_at"] = end_at
        if all_day is not UNSET:
            field_dict["all_day"] = all_day
        if kind is not UNSET:
            field_dict["kind"] = kind
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        start_at = d.pop("start_at")

        def _parse_end_at(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        end_at = _parse_end_at(d.pop("end_at", UNSET))

        all_day = d.pop("all_day", UNSET)

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

        milestone_create_request = cls(
            start_at=start_at,
            end_at=end_at,
            all_day=all_day,
            kind=kind,
            description=description,
        )

        milestone_create_request.additional_properties = d
        return milestone_create_request

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
