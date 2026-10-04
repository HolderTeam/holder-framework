from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="AiMessageCaptureResponseData")


@_attrs_define
class AiMessageCaptureResponseData:
    """
    Attributes:
        thread_id (str):
        user_message_id (str):
        assistant_message_id (str):
    """

    thread_id: str
    user_message_id: str
    assistant_message_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thread_id = self.thread_id

        user_message_id = self.user_message_id

        assistant_message_id = self.assistant_message_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "thread_id": thread_id,
                "user_message_id": user_message_id,
                "assistant_message_id": assistant_message_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        thread_id = d.pop("thread_id")

        user_message_id = d.pop("user_message_id")

        assistant_message_id = d.pop("assistant_message_id")

        ai_message_capture_response_data = cls(
            thread_id=thread_id,
            user_message_id=user_message_id,
            assistant_message_id=assistant_message_id,
        )

        ai_message_capture_response_data.additional_properties = d
        return ai_message_capture_response_data

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
