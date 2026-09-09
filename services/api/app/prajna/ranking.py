from __future__ import annotations

import hashlib
from urllib.parse import urlparse

from app.schemas import Source
from .contracts import RawSearchResult


def _tokens(text: str) -> set[str]:
    punctuation = ".,:;!?()[]{}\"'"
    return {t.lower().strip(punctuation) for t in text.split() if len(t) > 2}


def score_results(query: str, raw: list[RawSearchResult], limit: int) -> list[Source]:
    query_tokens = _tokens(query)
    seen_urls: set[str] = set()
    scored: list[Source] = []

    for item in raw:
        if not item.url or item.url in seen_urls:
            continue
        seen_urls.add(item.url)
        content_tokens = _tokens(item.title + " " + item.snippet)
        overlap = len(query_tokens & content_tokens) / max(1, len(query_tokens))
        score = min(0.99, 0.48 + overlap * 0.45)
        domain = urlparse(item.url).netloc.removeprefix("www.") or "unknown"
        sid = "S" + hashlib.sha1(item.url.encode()).hexdigest()[:7]
        scored.append(
            Source(
                id=sid,
                title=item.title,
                url=item.url,
                snippet=item.snippet,
                domain=domain,
                score=round(score, 3),
                published_at=item.published_at,
            )
        )

    scored.sort(key=lambda x: x.score, reverse=True)
    return scored[:limit]
