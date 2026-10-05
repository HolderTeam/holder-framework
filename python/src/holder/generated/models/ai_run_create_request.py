from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_run_create_request_context import AiRunCreateRequestContext


T = TypeVar("T", bound="AiRunCreateRequest")


@_attrs_define
class AiRunCreateRequest:
    """
    Attributes:
        prompt (str):
        mode (str | Unset): auto or model
        model (str | Unset): Optional explicit model id; interpreted for local or cloud selected provider.
        provider (str | Unset): Optional cloud provider id when local runner is unavailable.
        project_id (str | Unset):
        thread_id (str | Unset):
        context (AiRunCreateRequestContext | Unset):
    """

    prompt: str
    mode: str | Unset = UNSET
    model: str | Unset = UNSET
    provider: str | Unset = UNSET
    project_id: str | Unset = UNSET
    thread_id: str | Unset = UNSET
    context: AiRunCreateRequestContext | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        mode = self.mode

        model = self.model

        provider = self.provider

        project_id = self.project_id

        thread_id = self.thread_id

        context: dict[str, Any] | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode
        if model is not UNSET:
            field_dict["model"] = model
        if provider is not UNSET:
            field_dict["provider"] = provider
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ai_run_create_request_context import (
            AiRunCreateRequestContext,
        )

        d = dict(src_dict)
        prompt = d.pop("prompt")

        mode = d.pop("mode", UNSET)

        model = d.pop("model", UNSET)

        provider = d.pop("provider", UNSET)

        project_id = d.pop("project_id", UNSET)

        thread_id = d.pop("thread_id", UNSET)

        _context = d.pop("context", UNSET)
        context: AiRunCreateRequestContext | Unset
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = AiRunCreateRequestContext.from_dict(_context)

        ai_run_create_request = cls(
            prompt=prompt,
            mode=mode,
            model=model,
            provider=provider,
            project_id=project_id,
            thread_id=thread_id,
            context=context,
        )

        ai_run_create_request.additional_properties = d
        return ai_run_create_request

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
