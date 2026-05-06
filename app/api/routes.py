from __future__ import annotations

from typing import Dict, List

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    AnswerRequest,
    AnswerResponse,
    ChunkResult,
    HealthResponse,
    IngestRequest,
    IngestResponse,
    SearchRequest,
    SearchResponse,
)
from app.services.answering import answer
from app.services.ingestion import build_chunks
from app.services.retrieval import search

router = APIRouter()

# In-memory store for local demo/evaluator review.
# Production upgrade path: replace with pgvector/FAISS/Chroma behind this boundary.
_CHUNKS: List[Dict[str, str]] = []
_DOCUMENT_IDS: set[str] = set()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="rag-production-system")


@router.post("/documents/ingest", response_model=IngestResponse)
def ingest_document(payload: IngestRequest) -> IngestResponse:
    if payload.chunk_overlap >= payload.chunk_size:
        raise HTTPException(status_code=422, detail="chunk_overlap must be smaller than chunk_size")

    global _CHUNKS
    new_chunks = build_chunks(
        doc_id=payload.document_id,
        title=payload.title,
        content=payload.content,
        chunk_size=payload.chunk_size,
        chunk_overlap=payload.chunk_overlap,
    )

    # Idempotent re-ingestion for demo usage: replace chunks for the same document_id.
    _CHUNKS = [chunk for chunk in _CHUNKS if chunk["document_id"] != payload.document_id]
    _CHUNKS.extend(new_chunks)
    _DOCUMENT_IDS.add(payload.document_id)

    return IngestResponse(
        document_id=payload.document_id,
        title=payload.title,
        chunks_created=len(new_chunks),
    )


@router.post("/retrieval/search", response_model=SearchResponse)
def retrieve(payload: SearchRequest) -> SearchResponse:
    results = search(payload.query, _CHUNKS, top_k=payload.top_k)
    return SearchResponse(
        query=payload.query,
        top_k=payload.top_k,
        results=[ChunkResult(**result) for result in results],
    )


@router.post("/answers/generate", response_model=AnswerResponse)
def generate_answer(payload: AnswerRequest) -> AnswerResponse:
    results = search(payload.query, _CHUNKS, top_k=payload.top_k)
    generated_answer, fallback_used = answer(payload.query, results)
    return AnswerResponse(
        query=payload.query,
        answer=generated_answer,
        citations=[ChunkResult(**result) for result in results],
        fallback_used=fallback_used,
    )


@router.delete("/documents")
def clear_store() -> dict:
    """Clear the local in-memory store.

    This is useful for tests and evaluator demos. A production version would
    require authentication and scoped collection deletion.
    """
    _CHUNKS.clear()
    _DOCUMENT_IDS.clear()
    return {"status": "cleared"}
