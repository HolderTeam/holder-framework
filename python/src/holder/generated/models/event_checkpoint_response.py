from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.event_checkpoint import EventCheckpoint


T = TypeVar("T", bound="EventCheckpointResponse")


@_attrs_define
class EventCheckpointResponse:
    """
    Attributes:
        ok (bool):
        data (EventCheckpoint):
    """

    ok: bool
    data: EventCheckpoint
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ok": ok,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.event_checkpoint import EventCheckpoint

        d = dict(src_dict)
        ok = d.pop("ok")

        data = EventCheckpoint.from_dict(d.pop("data"))

        event_checkpoint_response = cls(
            ok=ok,
            data=data,
        )

        event_checkpoint_response.additional_properties = d
        return event_checkpoint_response

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
