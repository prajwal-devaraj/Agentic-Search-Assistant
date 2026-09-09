from __future__ import annotations

import re
from urllib.parse import quote_plus

import httpx

from app.config import Settings
from .contracts import ModelProvider, RawSearchResult, SearchProvider


class DemoSearchProvider(SearchProvider):
    async def search(self, query: str, limit: int) -> list[RawSearchResult]:
        topics = [
            ("Primary overview", "https://example.com/overview"),
            ("Technical reference", "https://example.org/reference"),
            ("Independent analysis", "https://example.net/analysis"),
            ("Implementation notes", "https://docs.example.com/implementation"),
            ("Recent discussion", "https://news.example.com/update"),
            ("Evaluation guide", "https://research.example.org/evaluation"),
        ]
        words = " ".join(query.strip().split())
        return [
            RawSearchResult(
                title=f"{title}: {words[:64]}",
                url=url + "?q=" + quote_plus(words),
                snippet=(
                    f"Demonstration evidence for '{words}'. Configure Brave Search for live retrieval. "
                    "This record exists so the full PRAJNA pipeline works without paid credentials."
                ),
            )
            for title, url in topics[:limit]
        ]


class BraveSearchProvider(SearchProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search(self, query: str, limit: int) -> list[RawSearchResult]:
        headers = {"Accept": "application/json", "X-Subscription-Token": self.api_key}
        params = {"q": query, "count": min(limit, 20), "text_decorations": False}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                "https://api.search.brave.com/res/v1/web/search", headers=headers, params=params
            )
            response.raise_for_status()
            payload = response.json()
        results = []
        for item in payload.get("web", {}).get("results", []):
            results.append(
                RawSearchResult(
                    title=item.get("title", "Untitled"),
                    url=item.get("url", ""),
                    snippet=re.sub(r"<[^>]+>", "", item.get("description", "")),
                    published_at=item.get("age"),
                )
            )
        return results


class DemoModelProvider(ModelProvider):
    async def plan(self, query: str, mode: str) -> list[str]:
        base = [query]
        if mode in {"deep", "compare", "news"}:
            base.append(f"{query} evidence analysis")
        if mode == "code":
            base.append(f"{query} official documentation implementation")
        return base[:3]

    async def answer(self, query: str, mode: str, evidence_text: str) -> str:
        lines = [line.strip() for line in evidence_text.splitlines() if line.strip()]
        source_lines = [line for line in lines if line.startswith("[")]
        count = len(source_lines)
        return (
            f"PRAJNA demo mode processed **{query}** using the **{mode}** lens and assembled "
            f"{count} evidence items. The pipeline is working end-to-end. Configure a live search "
            "provider and model provider to replace this deterministic synthesis with current, cited "
            "research. The sources below remain inspectable so the answer is never detached from its evidence."
        )


class OpenAIModelProvider(ModelProvider):
    def __init__(self, api_key: str, model: str):
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def plan(self, query: str, mode: str) -> list[str]:
        response = await self.client.responses.create(
            model=self.model,
            input=(
                "Generate up to 3 concise web-search queries for the user request. "
                "Return one query per line, no bullets.\n"
                f"Mode: {mode}\nRequest: {query}"
            ),
        )
        text = response.output_text.strip()
        queries = [q.strip(" -0123456789.\t") for q in text.splitlines() if q.strip()]
        return queries[:3] or [query]

    async def answer(self, query: str, mode: str, evidence_text: str) -> str:
        response = await self.client.responses.create(
            model=self.model,
            input=(
                "You are the synthesis layer of PRAJNA, an evidence-first search assistant. "
                "Answer only from the provided evidence. Cite sources inline using [S1], [S2], etc. "
                "If evidence is weak or conflicting, say so clearly. Do not invent URLs.\n\n"
                f"Mode: {mode}\nQuestion: {query}\n\nEvidence:\n{evidence_text}"
            ),
        )
        return response.output_text.strip()


def build_search_provider(settings: Settings) -> SearchProvider:
    if settings.prajna_search_provider == "brave" and settings.brave_search_api_key:
        return BraveSearchProvider(settings.brave_search_api_key)
    return DemoSearchProvider()


def build_model_provider(settings: Settings) -> ModelProvider:
    if settings.prajna_model_provider == "openai" and settings.openai_api_key:
        return OpenAIModelProvider(settings.openai_api_key, settings.openai_model)
    return DemoModelProvider()
