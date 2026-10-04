from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.card_tag_mutation_result_outcome import CardTagMutationResultOutcome

T = TypeVar("T", bound="CardTagMutationResult")


@_attrs_define
class CardTagMutationResult:
    """
    Attributes:
        card_id (str):
        tag (str): Normalized tag without the leading
        outcome (CardTagMutationResultOutcome):
        changed (bool): True only when card content was changed.
    """

    card_id: str
    tag: str
    outcome: CardTagMutationResultOutcome
    changed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        card_id = self.card_id

        tag = self.tag

        outcome = self.outcome.value

        changed = self.changed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "card_id": card_id,
                "tag": tag,
                "outcome": outcome,
                "changed": changed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        card_id = d.pop("card_id")

        tag = d.pop("tag")

        outcome = CardTagMutationResultOutcome(d.pop("outcome"))

        changed = d.pop("changed")

        card_tag_mutation_result = cls(
            card_id=card_id,
            tag=tag,
            outcome=outcome,
            changed=changed,
        )

        card_tag_mutation_result.additional_properties = d
        return card_tag_mutation_result

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
