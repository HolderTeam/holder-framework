from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AiLocalModelConfigUpdateRequest")


@_attrs_define
class AiLocalModelConfigUpdateRequest:
    """
    Attributes:
        fast_model (None | str | Unset):
        strong_model (None | str | Unset):
        deep_model (None | str | Unset):
        updated_at (int | None | Unset):
    """

    fast_model: None | str | Unset = UNSET
    strong_model: None | str | Unset = UNSET
    deep_model: None | str | Unset = UNSET
    updated_at: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fast_model: None | str | Unset
        if isinstance(self.fast_model, Unset):
            fast_model = UNSET
        else:
            fast_model = self.fast_model

        strong_model: None | str | Unset
        if isinstance(self.strong_model, Unset):
            strong_model = UNSET
        else:
            strong_model = self.strong_model

        deep_model: None | str | Unset
        if isinstance(self.deep_model, Unset):
            deep_model = UNSET
        else:
            deep_model = self.deep_model

        updated_at: int | None | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fast_model is not UNSET:
            field_dict["fast_model"] = fast_model
        if strong_model is not UNSET:
            field_dict["strong_model"] = strong_model
        if deep_model is not UNSET:
            field_dict["deep_model"] = deep_model
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_fast_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fast_model = _parse_fast_model(d.pop("fast_model", UNSET))

        def _parse_strong_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        strong_model = _parse_strong_model(d.pop("strong_model", UNSET))

        def _parse_deep_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        deep_model = _parse_deep_model(d.pop("deep_model", UNSET))

        def _parse_updated_at(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        ai_local_model_config_update_request = cls(
            fast_model=fast_model,
            strong_model=strong_model,
            deep_model=deep_model,
            updated_at=updated_at,
        )

        ai_local_model_config_update_request.additional_properties = d
        return ai_local_model_config_update_request

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
