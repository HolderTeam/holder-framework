from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.card_reference_resolve_request_scope import (
    CardReferenceResolveRequestScope,
)

T = TypeVar("T", bound="CardReferenceResolveRequest")


@_attrs_define
class CardReferenceResolveRequest:
    """
    Attributes:
        project_id (str):
        reference (str): Full canonical UUID, eligible UUID prefix, or exact card title.
        scope (CardReferenceResolveRequestScope):
    """

    project_id: str
    reference: str
    scope: CardReferenceResolveRequestScope
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        reference = self.reference

        scope = self.scope.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "reference": reference,
                "scope": scope,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        reference = d.pop("reference")

        scope = CardReferenceResolveRequestScope(d.pop("scope"))

        card_reference_resolve_request = cls(
            project_id=project_id,
            reference=reference,
            scope=scope,
        )

        card_reference_resolve_request.additional_properties = d
        return card_reference_resolve_request

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
