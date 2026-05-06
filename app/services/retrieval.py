from __future__ import annotations

import math
import re
from collections import Counter
from typing import Dict, Iterable, List

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_\-]+")


def tokenize(text: str) -> List[str]:
    return [token.lower() for token in _TOKEN_RE.findall(text)]


def score(query: str, text: str) -> float:
    """Lightweight lexical score for local, dependency-free retrieval.

    This is deliberately simple and explainable. It is not a replacement for
    embeddings; it creates a working first version that can later be swapped
    for vector search behind the same service boundary.
    """
    query_terms = tokenize(query)
    if not query_terms:
        return 0.0

    text_terms = tokenize(text)
    if not text_terms:
        return 0.0

    query_counts = Counter(query_terms)
    text_counts = Counter(text_terms)
    overlap = sum(min(query_counts[token], text_counts[token]) for token in query_counts)
    coverage = overlap / max(len(query_terms), 1)
    density = overlap / math.sqrt(max(len(text_terms), 1))
    return round(coverage + density, 4)


def search(query: str, chunks: Iterable[Dict[str, str]], top_k: int = 3) -> List[Dict[str, object]]:
    scored: List[Dict[str, object]] = []

    for chunk in chunks:
        chunk_score = score(query, chunk["content"])
        if chunk_score > 0:
            result = dict(chunk)
            result["score"] = chunk_score
            scored.append(result)

    return sorted(scored, key=lambda item: item["score"], reverse=True)[:top_k]
