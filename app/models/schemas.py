from typing import List

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    document_id: str = Field(..., min_length=1, examples=["doc-001"])
    title: str = Field(..., min_length=1, examples=["RAG System Design Notes"])
    content: str = Field(
        ...,
        min_length=20,
        examples=[
            "Retrieval-augmented generation improves answer grounding by retrieving relevant context before generation."
        ],
    )
    chunk_size: int = Field(default=300, ge=80, le=2000)
    chunk_overlap: int = Field(default=50, ge=0, le=500)


class IngestResponse(BaseModel):
    document_id: str
    title: str
    chunks_created: int


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=3, ge=1, le=10)


class ChunkResult(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    content: str
    score: float


class SearchResponse(BaseModel):
    query: str
    top_k: int
    results: List[ChunkResult]


class AnswerRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=3, ge=1, le=10)


class AnswerResponse(BaseModel):
    query: str
    answer: str
    citations: List[ChunkResult]
    fallback_used: bool


class HealthResponse(BaseModel):
    status: str
    service: str
