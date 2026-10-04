from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="AiLocalModelConfigData")


@_attrs_define
class AiLocalModelConfigData:
    """
    Attributes:
        fast_model (None | str):
        strong_model (None | str):
        deep_model (None | str):
        updated_at (int | None):
    """

    fast_model: None | str
    strong_model: None | str
    deep_model: None | str
    updated_at: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fast_model: None | str
        fast_model = self.fast_model

        strong_model: None | str
        strong_model = self.strong_model

        deep_model: None | str
        deep_model = self.deep_model

        updated_at: int | None
        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fast_model": fast_model,
                "strong_model": strong_model,
                "deep_model": deep_model,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_fast_model(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        fast_model = _parse_fast_model(d.pop("fast_model"))

        def _parse_strong_model(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        strong_model = _parse_strong_model(d.pop("strong_model"))

        def _parse_deep_model(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        deep_model = _parse_deep_model(d.pop("deep_model"))

        def _parse_updated_at(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        updated_at = _parse_updated_at(d.pop("updated_at"))

        ai_local_model_config_data = cls(
            fast_model=fast_model,
            strong_model=strong_model,
            deep_model=deep_model,
            updated_at=updated_at,
        )

        ai_local_model_config_data.additional_properties = d
        return ai_local_model_config_data

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
