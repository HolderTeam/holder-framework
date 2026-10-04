from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_run_item_policy_trace_type_0 import AiRunItemPolicyTraceType0


T = TypeVar("T", bound="AiRunItem")


@_attrs_define
class AiRunItem:
    """
    Attributes:
        run_id (str):
        mode (str):
        prompt (str):
        status (str):
        created_at (int):
        updated_at (int):
        project_id (None | str | Unset):
        thread_id (None | str | Unset):
        message_id (None | str | Unset):
        context_json (None | str | Unset):
        router_model (None | str | Unset):
        ranked_json (None | str | Unset):
        policy_trace_json (None | str | Unset):
        policy_trace (AiRunItemPolicyTraceType0 | None | Unset):
        chosen_model (None | str | Unset):
        error (None | str | Unset):
    """

    run_id: str
    mode: str
    prompt: str
    status: str
    created_at: int
    updated_at: int
    project_id: None | str | Unset = UNSET
    thread_id: None | str | Unset = UNSET
    message_id: None | str | Unset = UNSET
    context_json: None | str | Unset = UNSET
    router_model: None | str | Unset = UNSET
    ranked_json: None | str | Unset = UNSET
    policy_trace_json: None | str | Unset = UNSET
    policy_trace: AiRunItemPolicyTraceType0 | None | Unset = UNSET
    chosen_model: None | str | Unset = UNSET
    error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ai_run_item_policy_trace_type_0 import (
            AiRunItemPolicyTraceType0,
        )

        run_id = self.run_id

        mode = self.mode

        prompt = self.prompt

        status = self.status

        created_at = self.created_at

        updated_at = self.updated_at

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        thread_id: None | str | Unset
        if isinstance(self.thread_id, Unset):
            thread_id = UNSET
        else:
            thread_id = self.thread_id

        message_id: None | str | Unset
        if isinstance(self.message_id, Unset):
            message_id = UNSET
        else:
            message_id = self.message_id

        context_json: None | str | Unset
        if isinstance(self.context_json, Unset):
            context_json = UNSET
        else:
            context_json = self.context_json

        router_model: None | str | Unset
        if isinstance(self.router_model, Unset):
            router_model = UNSET
        else:
            router_model = self.router_model

        ranked_json: None | str | Unset
        if isinstance(self.ranked_json, Unset):
            ranked_json = UNSET
        else:
            ranked_json = self.ranked_json

        policy_trace_json: None | str | Unset
        if isinstance(self.policy_trace_json, Unset):
            policy_trace_json = UNSET
        else:
            policy_trace_json = self.policy_trace_json

        policy_trace: dict[str, Any] | None | Unset
        if isinstance(self.policy_trace, Unset):
            policy_trace = UNSET
        elif isinstance(self.policy_trace, AiRunItemPolicyTraceType0):
            policy_trace = self.policy_trace.to_dict()
        else:
            policy_trace = self.policy_trace

        chosen_model: None | str | Unset
        if isinstance(self.chosen_model, Unset):
            chosen_model = UNSET
        else:
            chosen_model = self.chosen_model

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "run_id": run_id,
                "mode": mode,
                "prompt": prompt,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id
        if message_id is not UNSET:
            field_dict["message_id"] = message_id
        if context_json is not UNSET:
            field_dict["context_json"] = context_json
        if router_model is not UNSET:
            field_dict["router_model"] = router_model
        if ranked_json is not UNSET:
            field_dict["ranked_json"] = ranked_json
        if policy_trace_json is not UNSET:
            field_dict["policy_trace_json"] = policy_trace_json
        if policy_trace is not UNSET:
            field_dict["policy_trace"] = policy_trace
        if chosen_model is not UNSET:
            field_dict["chosen_model"] = chosen_model
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ai_run_item_policy_trace_type_0 import (
            AiRunItemPolicyTraceType0,
        )

        d = dict(src_dict)
        run_id = d.pop("run_id")

        mode = d.pop("mode")

        prompt = d.pop("prompt")

        status = d.pop("status")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_thread_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        thread_id = _parse_thread_id(d.pop("thread_id", UNSET))

        def _parse_message_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message_id = _parse_message_id(d.pop("message_id", UNSET))

        def _parse_context_json(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        context_json = _parse_context_json(d.pop("context_json", UNSET))

        def _parse_router_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        router_model = _parse_router_model(d.pop("router_model", UNSET))

        def _parse_ranked_json(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ranked_json = _parse_ranked_json(d.pop("ranked_json", UNSET))

        def _parse_policy_trace_json(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        policy_trace_json = _parse_policy_trace_json(d.pop("policy_trace_json", UNSET))

        def _parse_policy_trace(
            data: object,
        ) -> AiRunItemPolicyTraceType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                policy_trace_type_0 = AiRunItemPolicyTraceType0.from_dict(data)

                return policy_trace_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AiRunItemPolicyTraceType0 | None | Unset, data)

        policy_trace = _parse_policy_trace(d.pop("policy_trace", UNSET))

        def _parse_chosen_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        chosen_model = _parse_chosen_model(d.pop("chosen_model", UNSET))

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        ai_run_item = cls(
            run_id=run_id,
            mode=mode,
            prompt=prompt,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            project_id=project_id,
            thread_id=thread_id,
            message_id=message_id,
            context_json=context_json,
            router_model=router_model,
            ranked_json=ranked_json,
            policy_trace_json=policy_trace_json,
            policy_trace=policy_trace,
            chosen_model=chosen_model,
            error=error,
        )

        ai_run_item.additional_properties = d
        return ai_run_item

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
