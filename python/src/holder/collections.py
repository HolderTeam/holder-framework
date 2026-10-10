"""Shared lazy iteration and caching for Holder collections."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar

if TYPE_CHECKING:
    from .client import Holder

T = TypeVar("T")


class Collection(Generic[T]):
    """Lazy query with a progressively populated cache and independent iterators."""

    def __init__(self, holder: Holder, query: dict[str, Any] | None = None) -> None:
        self._holder = holder
        self._query = dict(query or {})
        self._cache: list[T] = []
        self._next: int | str | None = None
        self._done = False
        self._generation = 0

    def __iter__(self) -> Iterator[T]:
        self._holder._active()
        generation = self._generation
        index = 0
        while True:
            self._holder._active()
            if generation != self._generation:
                raise RuntimeError("Collection was refreshed during iteration")
            if index == len(self._cache):
                if self._done:
                    return
                rows, next_cursor = self._fetch_page()
                self._cache.extend(rows)
                self._next = next_cursor
                self._done = next_cursor is None
                if not rows:
                    return
            yield self._cache[index]
            index += 1

    def __getitem__(self, index: int) -> T:
        if not isinstance(index, int):
            raise TypeError("Collection indices must be integers")
        if index < 0:
            raise IndexError("Collection indices must be nonnegative")
        for position, item in enumerate(self):
            if position == index:
                return item
        raise IndexError("Collection index out of range")

    def all(self) -> Self:
        return self._clone(self._query)

    def refresh(self) -> Self:
        self._holder._active()
        self._cache.clear()
        self._next = None
        self._done = False
        self._generation += 1
        return self

    def _clone(self, query: dict[str, Any]) -> Self:
        raise NotImplementedError

    def _fetch_page(self) -> tuple[list[T], int | str | None]:
        raise NotImplementedError
