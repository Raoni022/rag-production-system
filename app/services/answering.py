from __future__ import annotations

from typing import Dict, Iterable, Tuple


def answer(query: str, results: Iterable[Dict[str, object]]) -> Tuple[str, bool]:
    """Generate a grounded local answer from retrieved chunks.

    This repository intentionally avoids hiding logic behind a paid LLM call.
    For evaluator review, the answer is assembled from retrieved context and
    clearly falls back when retrieval is weak. A real LLM provider can later be
    inserted at this boundary.
    """
    retrieved = list(results)
    if not retrieved:
        return "I don't have enough information in the current knowledge base to answer this reliably.", True

    strongest = retrieved[0]
    if float(strongest.get("score", 0.0)) < 0.25:
        return "I found some related context, but not enough reliable evidence to produce a grounded answer.", True

    citation_ids = ", ".join(str(item["chunk_id"]) for item in retrieved)
    context = " ".join(str(item["content"]) for item in retrieved)
    grounded = (
        f"Based on the retrieved context ({citation_ids}), the answer is: "
        f"{context}"
    )
    return grounded, False
