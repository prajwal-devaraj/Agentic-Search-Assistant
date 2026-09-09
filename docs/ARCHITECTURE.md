# Architecture

## System view

```text
 Web (Next.js) ─┐
 Mobile (Expo) ─┼──> FastAPI Gateway ──> PRAJNA Orchestrator
 Desktop(Tauri) ┘                         │
                                         ├── Plan
                                         ├── Retrieve ──> Search adapters
                                         ├── Assess
                                         ├── Join ──────> Evidence graph
                                         ├── Navigate
                                         └── Answer ────> Model adapters
                                               │
                                      Postgres / Redis
```

## PRAJNA orchestration contract

The orchestrator consumes a `SearchRequest` and returns a `SearchResponse` with:

- a session id
- generated answer
- source cards
- evidence graph
- trust summary
- machine-readable framework trace (step names + status, never private model chain-of-thought)

The trace is intentionally operational rather than hidden reasoning. It lets developers debug latency, provider failures, evidence counts, and fallback behavior without exposing private model deliberation.

## Reliability

Each provider is behind an interface. Search failure falls back to deterministic demo evidence in development; model failure falls back to extractive synthesis. Production deployments should disable demo fallback for high-stakes use cases and surface provider errors explicitly.

## Scale path

1. API stateless horizontal scaling.
2. Redis for result caching, rate limits, ephemeral progress.
3. PostgreSQL for accounts, sessions, feedback, long-lived metadata.
4. pgvector for user-authorized semantic memory and team knowledge.
5. Async worker/queue for scheduled or multi-minute research missions.
6. Object storage for uploaded files and generated research artifacts.
