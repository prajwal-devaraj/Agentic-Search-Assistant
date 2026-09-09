from __future__ import annotations

from enum import StrEnum
from pydantic import BaseModel, Field, HttpUrl


class SearchMode(StrEnum):
    QUICK = "quick"
    DEEP = "deep"
    COMPARE = "compare"
    CODE = "code"
    NEWS = "news"


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=4000)
    mode: SearchMode = SearchMode.QUICK
    max_sources: int = Field(default=6, ge=2, le=20)
    session_id: str | None = None


class Source(BaseModel):
    id: str
    title: str
    url: str
    snippet: str
    domain: str
    score: float = Field(ge=0, le=1)
    published_at: str | None = None


class EvidenceEdge(BaseModel):
    claim: str
    source_ids: list[str]
    stance: str = "supports"


class TrustSummary(BaseModel):
    band: str
    score: int = Field(ge=0, le=100)
    source_count: int
    domain_diversity: int
    agreement_ratio: float
    notes: list[str]


class FrameworkStep(BaseModel):
    name: str
    status: str
    detail: str


class SearchResponse(BaseModel):
    session_id: str
    query: str
    mode: SearchMode
    answer: str
    sources: list[Source]
    evidence: list[EvidenceEdge]
    trust: TrustSummary
    trace: list[FrameworkStep]
