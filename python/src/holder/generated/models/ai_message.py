from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AiMessage")


@_attrs_define
class AiMessage:
    """
    Attributes:
        message_id (str):
        thread_id (str):
        role (str):
        source (str):
        content (str):
        created_at (int):
        provider (None | str | Unset):
        model (None | str | Unset):
        deleted_at (int | None | Unset):
        prompt_hash (None | str | Unset):
        meta_json (None | str | Unset):
    """

    message_id: str
    thread_id: str
    role: str
    source: str
    content: str
    created_at: int
    provider: None | str | Unset = UNSET
    model: None | str | Unset = UNSET
    deleted_at: int | None | Unset = UNSET
    prompt_hash: None | str | Unset = UNSET
    meta_json: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message_id = self.message_id

        thread_id = self.thread_id

        role = self.role

        source = self.source

        content = self.content

        created_at = self.created_at

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        model: None | str | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        deleted_at: int | None | Unset
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = self.deleted_at

        prompt_hash: None | str | Unset
        if isinstance(self.prompt_hash, Unset):
            prompt_hash = UNSET
        else:
            prompt_hash = self.prompt_hash

        meta_json: None | str | Unset
        if isinstance(self.meta_json, Unset):
            meta_json = UNSET
        else:
            meta_json = self.meta_json

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message_id": message_id,
                "thread_id": thread_id,
                "role": role,
                "source": source,
                "content": content,
                "created_at": created_at,
            }
        )
        if provider is not UNSET:
            field_dict["provider"] = provider
        if model is not UNSET:
            field_dict["model"] = model
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if prompt_hash is not UNSET:
            field_dict["prompt_hash"] = prompt_hash
        if meta_json is not UNSET:
            field_dict["meta_json"] = meta_json

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        message_id = d.pop("message_id")

        thread_id = d.pop("thread_id")

        role = d.pop("role")

        source = d.pop("source")

        content = d.pop("content")

        created_at = d.pop("created_at")

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_deleted_at(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        def _parse_prompt_hash(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt_hash = _parse_prompt_hash(d.pop("prompt_hash", UNSET))

        def _parse_meta_json(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        meta_json = _parse_meta_json(d.pop("meta_json", UNSET))

        ai_message = cls(
            message_id=message_id,
            thread_id=thread_id,
            role=role,
            source=source,
            content=content,
            created_at=created_at,
            provider=provider,
            model=model,
            deleted_at=deleted_at,
            prompt_hash=prompt_hash,
            meta_json=meta_json,
        )

        ai_message.additional_properties = d
        return ai_message

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
