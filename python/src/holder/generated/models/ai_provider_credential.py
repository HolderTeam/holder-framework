from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="AiProviderCredential")


@_attrs_define
class AiProviderCredential:
    """
    Attributes:
        provider (str):
        configured (bool):
        api_key_preview (str):
        created_at (int):
        updated_at (int):
    """

    provider: str
    configured: bool
    api_key_preview: str
    created_at: int
    updated_at: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        configured = self.configured

        api_key_preview = self.api_key_preview

        created_at = self.created_at

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "configured": configured,
                "api_key_preview": api_key_preview,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        provider = d.pop("provider")

        configured = d.pop("configured")

        api_key_preview = d.pop("api_key_preview")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        ai_provider_credential = cls(
            provider=provider,
            configured=configured,
            api_key_preview=api_key_preview,
            created_at=created_at,
            updated_at=updated_at,
        )

        ai_provider_credential.additional_properties = d
        return ai_provider_credential

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
