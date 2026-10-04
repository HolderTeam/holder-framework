from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AiThread")


@_attrs_define
class AiThread:
    """
    Attributes:
        thread_id (str):
        project_id (str):
        title (str):
        created_at (int):
        updated_at (int):
        card_id (None | str | Unset):
    """

    thread_id: str
    project_id: str
    title: str
    created_at: int
    updated_at: int
    card_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thread_id = self.thread_id

        project_id = self.project_id

        title = self.title

        created_at = self.created_at

        updated_at = self.updated_at

        card_id: None | str | Unset
        if isinstance(self.card_id, Unset):
            card_id = UNSET
        else:
            card_id = self.card_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "thread_id": thread_id,
                "project_id": project_id,
                "title": title,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if card_id is not UNSET:
            field_dict["card_id"] = card_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        thread_id = d.pop("thread_id")

        project_id = d.pop("project_id")

        title = d.pop("title")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_card_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        card_id = _parse_card_id(d.pop("card_id", UNSET))

        ai_thread = cls(
            thread_id=thread_id,
            project_id=project_id,
            title=title,
            created_at=created_at,
            updated_at=updated_at,
            card_id=card_id,
        )

        ai_thread.additional_properties = d
        return ai_thread

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
