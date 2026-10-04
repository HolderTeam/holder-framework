from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="RebuildData")


@_attrs_define
class RebuildData:
    """
    Attributes:
        project_id (str):
        cards (int):
        ai_messages (int):
        ai_threads (int):
        links (int):
    """

    project_id: str
    cards: int
    ai_messages: int
    ai_threads: int
    links: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        cards = self.cards

        ai_messages = self.ai_messages

        ai_threads = self.ai_threads

        links = self.links

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "cards": cards,
                "ai_messages": ai_messages,
                "ai_threads": ai_threads,
                "links": links,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        cards = d.pop("cards")

        ai_messages = d.pop("ai_messages")

        ai_threads = d.pop("ai_threads")

        links = d.pop("links")

        rebuild_data = cls(
            project_id=project_id,
            cards=cards,
            ai_messages=ai_messages,
            ai_threads=ai_threads,
            links=links,
        )

        rebuild_data.additional_properties = d
        return rebuild_data

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
