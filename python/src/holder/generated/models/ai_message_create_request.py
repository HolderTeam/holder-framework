from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AiMessageCreateRequest")


@_attrs_define
class AiMessageCreateRequest:
    """
    Attributes:
        thread_id (str):
        role (str):
        source (str):
        content (str):
        message_id (str | Unset): Optional; server generates if omitted.
        provider (None | str | Unset):
        model (None | str | Unset):
        created_at (int | Unset): Optional; server uses current time if omitted or 0.
        prompt_hash (None | str | Unset):
        meta_json (None | str | Unset):
    """

    thread_id: str
    role: str
    source: str
    content: str
    message_id: str | Unset = UNSET
    provider: None | str | Unset = UNSET
    model: None | str | Unset = UNSET
    created_at: int | Unset = UNSET
    prompt_hash: None | str | Unset = UNSET
    meta_json: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thread_id = self.thread_id

        role = self.role

        source = self.source

        content = self.content

        message_id = self.message_id

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

        created_at = self.created_at

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
                "thread_id": thread_id,
                "role": role,
                "source": source,
                "content": content,
            }
        )
        if message_id is not UNSET:
            field_dict["message_id"] = message_id
        if provider is not UNSET:
            field_dict["provider"] = provider
        if model is not UNSET:
            field_dict["model"] = model
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if prompt_hash is not UNSET:
            field_dict["prompt_hash"] = prompt_hash
        if meta_json is not UNSET:
            field_dict["meta_json"] = meta_json

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        thread_id = d.pop("thread_id")

        role = d.pop("role")

        source = d.pop("source")

        content = d.pop("content")

        message_id = d.pop("message_id", UNSET)

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

        created_at = d.pop("created_at", UNSET)

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

        ai_message_create_request = cls(
            thread_id=thread_id,
            role=role,
            source=source,
            content=content,
            message_id=message_id,
            provider=provider,
            model=model,
            created_at=created_at,
            prompt_hash=prompt_hash,
            meta_json=meta_json,
        )

        ai_message_create_request.additional_properties = d
        return ai_message_create_request

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
