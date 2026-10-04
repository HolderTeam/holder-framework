from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.caste_recommended_model_required_caste import (
    CasteRecommendedModelRequiredCaste,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CasteRecommendedModel")


@_attrs_define
class CasteRecommendedModel:
    """
    Attributes:
        tag (str):
        required_caste (CasteRecommendedModelRequiredCaste):
        installed (bool):
        provider (None | str | Unset):
        engine (None | str | Unset):
        category (None | str | Unset):
    """

    tag: str
    required_caste: CasteRecommendedModelRequiredCaste
    installed: bool
    provider: None | str | Unset = UNSET
    engine: None | str | Unset = UNSET
    category: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tag = self.tag

        required_caste = self.required_caste.value

        installed = self.installed

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        engine: None | str | Unset
        if isinstance(self.engine, Unset):
            engine = UNSET
        else:
            engine = self.engine

        category: None | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tag": tag,
                "required_caste": required_caste,
                "installed": installed,
            }
        )
        if provider is not UNSET:
            field_dict["provider"] = provider
        if engine is not UNSET:
            field_dict["engine"] = engine
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        tag = d.pop("tag")

        required_caste = CasteRecommendedModelRequiredCaste(d.pop("required_caste"))

        installed = d.pop("installed")

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        def _parse_engine(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        engine = _parse_engine(d.pop("engine", UNSET))

        def _parse_category(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        caste_recommended_model = cls(
            tag=tag,
            required_caste=required_caste,
            installed=installed,
            provider=provider,
            engine=engine,
            category=category,
        )

        caste_recommended_model.additional_properties = d
        return caste_recommended_model

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
