from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class RawSearchResult:
    title: str
    url: str
    snippet: str
    published_at: str | None = None


class SearchProvider(Protocol):
    async def search(self, query: str, limit: int) -> list[RawSearchResult]: ...


class ModelProvider(Protocol):
    async def plan(self, query: str, mode: str) -> list[str]: ...
    async def answer(self, query: str, mode: str, evidence_text: str) -> str: ...
