from pydantic import BaseModel, Field
from typing import List


class IngestRequest(BaseModel):
    document_id: str
    title: str
    content: str
    chunk_size: int = 300
    chunk_overlap: int = 50


class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


class ChunkResult(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    content: str
    score: int


class AnswerRequest(BaseModel):
    query: str
    top_k: int = 3


class AnswerResponse(BaseModel):
    query: str
    answer: str
    citations: List[ChunkResult]
