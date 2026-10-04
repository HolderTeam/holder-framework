from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="MilestoneUpdateRequest")


@_attrs_define
class MilestoneUpdateRequest:
    """Partial milestone update. Omitted properties remain unchanged; null clears a nullable property.

    Attributes:
        start_at (int | Unset): Unix epoch seconds. When changing an all-day milestone, encode the local calendar date
            at local midnight.
        end_at (int | None | Unset): Inclusive milestone end, or null to clear it. The resulting end must not precede
            start_at.
        all_day (bool | Unset): Whether start_at and end_at carry local calendar-date semantics rather than timed-
            instant semantics.
        kind (None | str | Unset):
        description (None | str | Unset):
    """

    start_at: int | Unset = UNSET
    end_at: int | None | Unset = UNSET
    all_day: bool | Unset = UNSET
    kind: None | str | Unset = UNSET
    description: None | str | Unset = UNSET

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

        field_dict.update({})
        if start_at is not UNSET:
            field_dict["start_at"] = start_at
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
        start_at = d.pop("start_at", UNSET)

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

        milestone_update_request = cls(
            start_at=start_at,
            end_at=end_at,
            all_day=all_day,
            kind=kind,
            description=description,
        )

        return milestone_update_request
