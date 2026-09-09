# PRAJNA — Universal Agentic Search Assistant

> **Search less. Understand more. Act with evidence.**

PRAJNA is a cross-platform agentic search system designed by **Prajwal Devaraj**. It combines live retrieval, evidence ranking, transparent citations, answer synthesis, session memory, search modes, and a provider-neutral agent runtime in one codebase.

The project is intentionally structured as a product, not a single chatbot demo: the same core API powers web, iOS/Android, and macOS/Windows/Linux clients.

## Original framework: PRAJNA

**P**lan → **R**etrieve → **A**ssess → **J**oin → **N**avigate → **A**nswer

1. **Plan** — classify intent, choose a mode, and generate focused retrieval queries.
2. **Retrieve** — fan out across configured search providers.
3. **Assess** — normalize, de-duplicate, score, and filter evidence.
4. **Join** — connect evidence to claims and create an evidence graph.
5. **Navigate** — decide whether another retrieval pass is needed.
6. **Answer** — synthesize a concise cited answer and compute a trust summary.

The framework is implemented in `services/api/app/prajna/` and does not depend on a single model vendor.

## Product surfaces

- **Web/PWA** — Next.js 16, React, TypeScript, responsive UI with installable app shell and offline shell caching.
- **Mobile** — Expo SDK 57 / React Native for iOS and Android.
- **Desktop** — Tauri 2 shell for macOS, Windows, and Linux.
- **API** — FastAPI with streaming search events, provider adapters, health checks, and OpenAPI docs.
- **Data** — PostgreSQL + pgvector-ready schema, Redis-ready cache layer.
- **Ops** — Docker Compose, GitHub Actions, linting, tests, environment templates.

## Standout ideas

### Evidence Graph
Every result can expose a lightweight graph of answer claims and supporting sources instead of hiding retrieval behind a black box.

### Trust Panel
PRAJNA returns source count, domain diversity, freshness hints, agreement ratio, and an explainable confidence band. It is a heuristic quality signal—not a guarantee of truth.

### Search Lenses
`quick`, `deep`, `compare`, `code`, and `news` change retrieval depth and synthesis style without forcing users to learn prompt engineering.

### Provider-neutral intelligence
Run with the built-in demo model, OpenAI, or extend the adapters for Gemini, Anthropic, local models, enterprise search, internal docs, or domain tools.

### No-key demo mode
The platform boots without paid APIs. It returns deterministic demonstration evidence so the entire interface, streaming pipeline, tests, and architecture can be evaluated immediately.

## Repository layout

```text
apps/
  web/                 Next.js universal web experience
  mobile/              Expo iOS/Android client
  desktop/             Tauri desktop shell
services/
  api/                  FastAPI + PRAJNA framework
packages/
  protocol/             shared TypeScript contracts
infra/
  postgres/             database bootstrap
  nginx/                reverse-proxy example
docs/
  ARCHITECTURE.md
  PRODUCT.md
  SECURITY.md
  ROADMAP.md
.github/workflows/      CI
```

## Quick start

### 1. Backend

```bash
cd services/api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -e '.[dev]'
cp ../../.env.example ../../.env
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000/docs`.

### 2. Web

```bash
corepack enable
pnpm install
pnpm --filter @prajna/web dev
```

Open `http://localhost:3000`.

### 3. Mobile

```bash
pnpm --filter @prajna/mobile start
```

Use Expo development tooling to run on iOS or Android.

### 4. Full local stack

```bash
docker compose up --build
```

## Real search + model configuration

Copy `.env.example` to `.env`. The zero-config default is `demo`.

```env
PRAJNA_MODEL_PROVIDER=demo
PRAJNA_SEARCH_PROVIDER=demo
```

For OpenAI synthesis:

```env
PRAJNA_MODEL_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.6
```

For Brave Search:

```env
PRAJNA_SEARCH_PROVIDER=brave
BRAVE_SEARCH_API_KEY=...
```

Adapters are intentionally small so other providers can be added without changing the orchestrator.

## API example

```bash
curl -X POST http://localhost:8000/v1/search \
  -H 'content-type: application/json' \
  -d '{"query":"How does vector search improve RAG?","mode":"deep"}'
```

## Engineering principles

- evidence before eloquence
- graceful degradation when providers fail
- typed contracts at every boundary
- provider independence
- secure-by-default secrets handling
- transparent quality signals
- responsive UX before feature count
- observable, testable agent steps

## What is implemented vs. extensible

Implemented in this package: working API, PRAJNA pipeline, demo provider, OpenAI adapter, Brave Search adapter, evidence scoring, trust summary, SSE streaming, responsive web client, Expo mobile client, Tauri shell, tests, Docker, and CI.

Designed extension points: authenticated user accounts, cloud sync, browser extension, speech-to-speech, camera search, enterprise connectors, scheduled research, collaborative spaces, on-device embeddings, and production vector-memory policies.

## License

MIT © 2026 Prajwal Devaraj
