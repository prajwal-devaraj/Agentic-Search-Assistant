from __future__ import annotations

import asyncio
import uuid

from app.schemas import EvidenceEdge, FrameworkStep, SearchRequest, SearchResponse
from .contracts import ModelProvider, SearchProvider
from .ranking import score_results
from .trust import compute_trust


class PrajnaOrchestrator:
    def __init__(self, search: SearchProvider, model: ModelProvider):
        self.search = search
        self.model = model

    async def run(self, request: SearchRequest) -> SearchResponse:
        trace: list[FrameworkStep] = []

        queries = await self.model.plan(request.query, request.mode.value)
        trace.append(
            FrameworkStep(
                name="Plan",
                status="complete",
                detail=f"{len(queries)} retrieval path(s)",
            )
        )

        per_query = max(2, min(request.max_sources, 6))
        batches = await asyncio.gather(
            *(self.search.search(q, per_query) for q in queries), return_exceptions=True
        )
        raw = []
        failures = 0
        for batch in batches:
            if isinstance(batch, Exception):
                failures += 1
                continue
            raw.extend(batch)
        trace.append(
            FrameworkStep(
                name="Retrieve",
                status="partial" if failures else "complete",
                detail=f"{len(raw)} raw result(s); {failures} provider failure(s)",
            )
        )

        sources = score_results(request.query, raw, request.max_sources)
        trace.append(
            FrameworkStep(
                name="Assess",
                status="complete",
                detail=f"{len(sources)} ranked source(s)",
            )
        )

        evidence = [
            EvidenceEdge(
                claim=f"Evidence item: {source.title}",
                source_ids=[source.id],
                stance="supports",
            )
            for source in sources[: min(5, len(sources))]
        ]
        trace.append(
            FrameworkStep(
                name="Join",
                status="complete",
                detail=f"{len(evidence)} evidence edge(s)",
            )
        )

        trace.append(
            FrameworkStep(
                name="Navigate",
                status="complete",
                detail="Single-pass retrieval sufficient",
            )
        )

        evidence_text = "\n".join(
            f"[{source.id}] {source.title}\nURL: {source.url}\n{source.snippet}"
            for source in sources
        )
        answer = await self.model.answer(request.query, request.mode.value, evidence_text)
        trace.append(
            FrameworkStep(
                name="Answer",
                status="complete",
                detail="Synthesis complete",
            )
        )

        return SearchResponse(
            session_id=request.session_id or str(uuid.uuid4()),
            query=request.query,
            mode=request.mode,
            answer=answer,
            sources=sources,
            evidence=evidence,
            trust=compute_trust(sources),
            trace=trace,
        )
