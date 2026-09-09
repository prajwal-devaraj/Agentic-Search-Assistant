from __future__ import annotations

import asyncio
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.config import get_settings
from app.prajna import PrajnaOrchestrator
from app.prajna.providers import build_model_provider, build_search_provider
from app.schemas import SearchRequest, SearchResponse

settings = get_settings()
app = FastAPI(
    title="PRAJNA Agentic Search API",
    version="0.1.0",
    description="Evidence-first universal search powered by the PRAJNA framework.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = PrajnaOrchestrator(
    search=build_search_provider(settings),
    model=build_model_provider(settings),
)


@app.get("/")
async def root() -> dict:
    return {"name": "PRAJNA", "framework": "Plan → Retrieve → Assess → Join → Navigate → Answer"}


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "environment": settings.prajna_env,
        "model_provider": settings.prajna_model_provider,
        "search_provider": settings.prajna_search_provider,
    }


@app.get("/v1/framework")
async def framework() -> dict:
    return {
        "name": "PRAJNA",
        "steps": ["Plan", "Retrieve", "Assess", "Join", "Navigate", "Answer"],
        "principle": "Evidence before eloquence",
    }


@app.post("/v1/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    return await orchestrator.run(request)


@app.post("/v1/search/stream")
async def search_stream(request: SearchRequest) -> StreamingResponse:
    async def events():
        stages = ["Plan", "Retrieve", "Assess", "Join", "Navigate"]
        for index, stage in enumerate(stages, start=1):
            payload = json.dumps({"stage": stage, "progress": index * 14})
            yield f"event: progress\ndata: {payload}\n\n"
            await asyncio.sleep(0.08)
        response = await orchestrator.run(request)
        yield f"event: result\ndata: {response.model_dump_json()}\n\n"
        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")
