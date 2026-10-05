from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.resource_attachment_response_data_outcome import (
    ResourceAttachmentResponseDataOutcome,
)

T = TypeVar("T", bound="ResourceAttachmentResponseData")


@_attrs_define
class ResourceAttachmentResponseData:
    """
    Attributes:
        card_id (str):
        resource_id (str):
        changed (bool):
        outcome (ResourceAttachmentResponseDataOutcome):
    """

    card_id: str
    resource_id: str
    changed: bool
    outcome: ResourceAttachmentResponseDataOutcome
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        card_id = self.card_id

        resource_id = self.resource_id

        changed = self.changed

        outcome = self.outcome.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "card_id": card_id,
                "resource_id": resource_id,
                "changed": changed,
                "outcome": outcome,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        card_id = d.pop("card_id")

        resource_id = d.pop("resource_id")

        changed = d.pop("changed")

        outcome = ResourceAttachmentResponseDataOutcome(d.pop("outcome"))

        resource_attachment_response_data = cls(
            card_id=card_id,
            resource_id=resource_id,
            changed=changed,
            outcome=outcome,
        )

        resource_attachment_response_data.additional_properties = d
        return resource_attachment_response_data

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
