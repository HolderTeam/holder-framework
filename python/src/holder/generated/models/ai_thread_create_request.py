from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AiThreadCreateRequest")


@_attrs_define
class AiThreadCreateRequest:
    """
    Attributes:
        project_id (str):
        title (str):
        thread_id (str | Unset): Optional; server generates if omitted.
        card_id (None | str | Unset):
        created_at (int | Unset): Optional; server uses current time if omitted or 0.
        updated_at (int | Unset): Optional; server uses created_at if omitted or 0.
    """

    project_id: str
    title: str
    thread_id: str | Unset = UNSET
    card_id: None | str | Unset = UNSET
    created_at: int | Unset = UNSET
    updated_at: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        title = self.title

        thread_id = self.thread_id

        card_id: None | str | Unset
        if isinstance(self.card_id, Unset):
            card_id = UNSET
        else:
            card_id = self.card_id

        created_at = self.created_at

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "title": title,
            }
        )
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id
        if card_id is not UNSET:
            field_dict["card_id"] = card_id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        title = d.pop("title")

        thread_id = d.pop("thread_id", UNSET)

        def _parse_card_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        card_id = _parse_card_id(d.pop("card_id", UNSET))

        created_at = d.pop("created_at", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        ai_thread_create_request = cls(
            project_id=project_id,
            title=title,
            thread_id=thread_id,
            card_id=card_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        ai_thread_create_request.additional_properties = d
        return ai_thread_create_request

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
