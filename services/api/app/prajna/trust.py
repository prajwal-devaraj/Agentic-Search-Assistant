from __future__ import annotations

from app.schemas import Source, TrustSummary


def compute_trust(sources: list[Source]) -> TrustSummary:
    count = len(sources)
    diversity = len({s.domain for s in sources})
    avg_score = sum(s.score for s in sources) / max(1, count)
    agreement = min(1.0, 0.55 + 0.05 * max(0, count - 1)) if count else 0.0

    score = int(min(95, round(avg_score * 55 + min(diversity, 6) * 6 + min(count, 8) * 1.5)))
    band = "high" if score >= 80 else "medium" if score >= 60 else "low"
    notes = [
        f"{count} source(s) survived ranking and de-duplication.",
        f"Evidence spans {diversity} distinct domain(s).",
        "Trust is a heuristic quality signal, not a factual guarantee.",
    ]
    return TrustSummary(
        band=band,
        score=score,
        source_count=count,
        domain_diversity=diversity,
        agreement_ratio=round(agreement, 2),
        notes=notes,
    )
