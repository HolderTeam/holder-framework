from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrashItem")


@_attrs_define
class TrashItem:
    """
    Attributes:
        type_ (str):
        card_id (None | str | Unset):
        message_id (None | str | Unset):
        thread_id (None | str | Unset):
        project_id (str | Unset):
        title (None | str | Unset):
        role (None | str | Unset):
        deleted_at (int | Unset):
        created_at (int | Unset):
        rel_path (None | str | Unset):
    """

    type_: str
    card_id: None | str | Unset = UNSET
    message_id: None | str | Unset = UNSET
    thread_id: None | str | Unset = UNSET
    project_id: str | Unset = UNSET
    title: None | str | Unset = UNSET
    role: None | str | Unset = UNSET
    deleted_at: int | Unset = UNSET
    created_at: int | Unset = UNSET
    rel_path: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        card_id: None | str | Unset
        if isinstance(self.card_id, Unset):
            card_id = UNSET
        else:
            card_id = self.card_id

        message_id: None | str | Unset
        if isinstance(self.message_id, Unset):
            message_id = UNSET
        else:
            message_id = self.message_id

        thread_id: None | str | Unset
        if isinstance(self.thread_id, Unset):
            thread_id = UNSET
        else:
            thread_id = self.thread_id

        project_id = self.project_id

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        role: None | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        deleted_at = self.deleted_at

        created_at = self.created_at

        rel_path: None | str | Unset
        if isinstance(self.rel_path, Unset):
            rel_path = UNSET
        else:
            rel_path = self.rel_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if card_id is not UNSET:
            field_dict["card_id"] = card_id
        if message_id is not UNSET:
            field_dict["message_id"] = message_id
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if title is not UNSET:
            field_dict["title"] = title
        if role is not UNSET:
            field_dict["role"] = role
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if rel_path is not UNSET:
            field_dict["rel_path"] = rel_path

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = d.pop("type")

        def _parse_card_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        card_id = _parse_card_id(d.pop("card_id", UNSET))

        def _parse_message_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message_id = _parse_message_id(d.pop("message_id", UNSET))

        def _parse_thread_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        thread_id = _parse_thread_id(d.pop("thread_id", UNSET))

        project_id = d.pop("project_id", UNSET)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        role = _parse_role(d.pop("role", UNSET))

        deleted_at = d.pop("deleted_at", UNSET)

        created_at = d.pop("created_at", UNSET)

        def _parse_rel_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rel_path = _parse_rel_path(d.pop("rel_path", UNSET))

        trash_item = cls(
            type_=type_,
            card_id=card_id,
            message_id=message_id,
            thread_id=thread_id,
            project_id=project_id,
            title=title,
            role=role,
            deleted_at=deleted_at,
            created_at=created_at,
            rel_path=rel_path,
        )

        trash_item.additional_properties = d
        return trash_item

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
