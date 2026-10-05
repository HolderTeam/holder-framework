from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_message_capture_request_context_type_0 import (
        AiMessageCaptureRequestContextType0,
    )


T = TypeVar("T", bound="AiMessageCaptureRequest")


@_attrs_define
class AiMessageCaptureRequest:
    """
    Attributes:
        project_id (str):
        prompt (str):
        response (str):
        thread_id (None | str | Unset):
        source (None | str | Unset):
        provider (None | str | Unset):
        model (None | str | Unset):
        url (None | str | Unset):
        context (AiMessageCaptureRequestContextType0 | None | Unset):
        created_at (int | None | Unset):
    """

    project_id: str
    prompt: str
    response: str
    thread_id: None | str | Unset = UNSET
    source: None | str | Unset = UNSET
    provider: None | str | Unset = UNSET
    model: None | str | Unset = UNSET
    url: None | str | Unset = UNSET
    context: AiMessageCaptureRequestContextType0 | None | Unset = UNSET
    created_at: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ai_message_capture_request_context_type_0 import (
            AiMessageCaptureRequestContextType0,
        )

        project_id = self.project_id

        prompt = self.prompt

        response = self.response

        thread_id: None | str | Unset
        if isinstance(self.thread_id, Unset):
            thread_id = UNSET
        else:
            thread_id = self.thread_id

        source: None | str | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

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

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        context: dict[str, Any] | None | Unset
        if isinstance(self.context, Unset):
            context = UNSET
        elif isinstance(self.context, AiMessageCaptureRequestContextType0):
            context = self.context.to_dict()
        else:
            context = self.context

        created_at: int | None | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "prompt": prompt,
                "response": response,
            }
        )
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id
        if source is not UNSET:
            field_dict["source"] = source
        if provider is not UNSET:
            field_dict["provider"] = provider
        if model is not UNSET:
            field_dict["model"] = model
        if url is not UNSET:
            field_dict["url"] = url
        if context is not UNSET:
            field_dict["context"] = context
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ai_message_capture_request_context_type_0 import (
            AiMessageCaptureRequestContextType0,
        )

        d = dict(src_dict)
        project_id = d.pop("project_id")

        prompt = d.pop("prompt")

        response = d.pop("response")

        def _parse_thread_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        thread_id = _parse_thread_id(d.pop("thread_id", UNSET))

        def _parse_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

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

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_context(
            data: object,
        ) -> AiMessageCaptureRequestContextType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                context_type_0 = AiMessageCaptureRequestContextType0.from_dict(data)

                return context_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AiMessageCaptureRequestContextType0 | None | Unset, data)

        context = _parse_context(d.pop("context", UNSET))

        def _parse_created_at(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        ai_message_capture_request = cls(
            project_id=project_id,
            prompt=prompt,
            response=response,
            thread_id=thread_id,
            source=source,
            provider=provider,
            model=model,
            url=url,
            context=context,
            created_at=created_at,
        )

        ai_message_capture_request.additional_properties = d
        return ai_message_capture_request

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
