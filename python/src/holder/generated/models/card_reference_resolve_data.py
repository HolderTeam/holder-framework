from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.card_reference_resolve_data_match_kind import (
    CardReferenceResolveDataMatchKind,
)
from ..models.card_reference_resolve_data_status import CardReferenceResolveDataStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_reference_candidate import CardReferenceCandidate


T = TypeVar("T", bound="CardReferenceResolveData")


@_attrs_define
class CardReferenceResolveData:
    """
    Attributes:
        status (CardReferenceResolveDataStatus):
        match_kind (CardReferenceResolveDataMatchKind | Unset): Present for resolved and ambiguous results.
        card (CardReferenceCandidate | Unset):
        candidates (list[CardReferenceCandidate] | Unset): Present for an ambiguous result and contains two candidates.
    """

    status: CardReferenceResolveDataStatus
    match_kind: CardReferenceResolveDataMatchKind | Unset = UNSET
    card: CardReferenceCandidate | Unset = UNSET
    candidates: list[CardReferenceCandidate] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        match_kind: str | Unset = UNSET
        if not isinstance(self.match_kind, Unset):
            match_kind = self.match_kind.value

        card: dict[str, Any] | Unset = UNSET
        if not isinstance(self.card, Unset):
            card = self.card.to_dict()

        candidates: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.candidates, Unset):
            candidates = []
            for candidates_item_data in self.candidates:
                candidates_item = candidates_item_data.to_dict()
                candidates.append(candidates_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if match_kind is not UNSET:
            field_dict["match_kind"] = match_kind
        if card is not UNSET:
            field_dict["card"] = card
        if candidates is not UNSET:
            field_dict["candidates"] = candidates

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.card_reference_candidate import (
            CardReferenceCandidate,
        )

        d = dict(src_dict)
        status = CardReferenceResolveDataStatus(d.pop("status"))

        _match_kind = d.pop("match_kind", UNSET)
        match_kind: CardReferenceResolveDataMatchKind | Unset
        if isinstance(_match_kind, Unset):
            match_kind = UNSET
        else:
            match_kind = CardReferenceResolveDataMatchKind(_match_kind)

        _card = d.pop("card", UNSET)
        card: CardReferenceCandidate | Unset
        if isinstance(_card, Unset):
            card = UNSET
        else:
            card = CardReferenceCandidate.from_dict(_card)

        _candidates = d.pop("candidates", UNSET)
        candidates: list[CardReferenceCandidate] | Unset = UNSET
        if _candidates is not UNSET:
            candidates = []
            for candidates_item_data in _candidates:
                candidates_item = CardReferenceCandidate.from_dict(candidates_item_data)

                candidates.append(candidates_item)

        card_reference_resolve_data = cls(
            status=status,
            match_kind=match_kind,
            card=card,
            candidates=candidates,
        )

        card_reference_resolve_data.additional_properties = d
        return card_reference_resolve_data

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
