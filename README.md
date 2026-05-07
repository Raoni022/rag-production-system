# RAG Production System

A production-oriented Retrieval-Augmented Generation (RAG) backend blueprint built with FastAPI.

This repository is intentionally small, runnable, and evaluator-friendly. It demonstrates the core backend boundaries of a RAG system without hiding the architecture behind a paid LLM call or a notebook-only demo.

## Evaluator Quick Scan

| Area | Current implementation |
|---|---|
| API | FastAPI REST API |
| Ingestion | Raw text ingestion with configurable chunking |
| Retrieval | Lightweight lexical retrieval for local reproducibility |
| Answering | Grounded answer assembly from retrieved chunks |
| Citations | Returned as structured chunk references |
| Fallback | Explicit fallback when context is missing or weak |
| Tests | API tests for health, ingestion, retrieval, answer generation, and fallback |
| Runtime | Local Python or Docker |
| Upgrade path | Embeddings, pgvector/FAISS/Chroma, PDF/DOCX parsing, evaluation suite |

## Why this project exists

Most RAG demos are toy chatbots. This project is structured as a backend service that can evolve into a production system.

The goal is to demonstrate practical AI engineering skills that companies actually look for:

- document ingestion
- chunking and retrieval
- grounded answers with citations
- configurable top-k retrieval
- fallback behavior when the knowledge base is insufficient
- modular backend boundaries
- testable API behavior
- clear upgrade path toward vector search and evaluation

## Current version

This version includes:

- `GET /health`
- `POST /documents/ingest`
- `POST /retrieval/search`
- `POST /answers/generate`
- `DELETE /documents` for local demo/test reset
- in-memory chunk store for local development
- lightweight lexical retrieval
- citation-aware answer response
- deterministic fallback behavior
- API tests with `pytest`
- Dockerfile for local containerized review

## What is implemented vs. intentionally simplified

Implemented:

- FastAPI route layer
- Pydantic request/response schemas
- configurable chunking
- in-memory document/chunk store
- lexical retrieval service
- grounded answer assembly
- fallback behavior
- tests for core behavior

Intentionally simplified for this portfolio version:

- no paid LLM provider call
- no persistent vector database
- no PDF/DOCX parser yet
- no auth/rate limiting yet
- no production observability stack yet

This is best read as a production-oriented RAG backend blueprint, not a fully deployed enterprise RAG platform.

## Architecture

```text
Client
  -> FastAPI API
      -> Ingestion Service
          -> Chunking
          -> In-memory Chunk Store
      -> Retrieval Service
          -> Lightweight Scoring
          -> top_k Results
      -> Answering Service
          -> Grounded Answer
          -> Citations
          -> Fallback When Context Is Weak
```

Future production shape:

```text
Client
  -> FastAPI API
      -> Document Parser
      -> Token-aware Chunking
      -> Embedding Provider
      -> Vector Database / pgvector
      -> Retrieval + Reranking
      -> LLM Answer Generation
      -> Evaluation + Observability
```

## Endpoints

### `GET /health`

Returns service status.

### `POST /documents/ingest`

Accepts raw text content, splits it into chunks, and stores it for retrieval.

### `POST /retrieval/search`

Returns the most relevant chunks for a query using lightweight lexical scoring.

### `POST /answers/generate`

Builds a grounded answer using retrieved chunks and returns citations.

### `DELETE /documents`

Clears the local in-memory store. Intended for tests and local demos only.

## Quick start

### Local Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### Docker

```bash
docker build -t rag-production-system .
docker run --rm -p 8000:8000 rag-production-system
```

## Example requests

### Ingest a document

```bash
curl -X POST http://127.0.0.1:8000/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc-1",
    "title": "RAG Basics",
    "content": "Retrieval-augmented generation improves answer grounding by using external documents. Citations help users verify where an answer came from. Fallback behavior matters when the knowledge base is insufficient.",
    "chunk_size": 220,
    "chunk_overlap": 40
  }'
```

### Search retrieval

```bash
curl -X POST http://127.0.0.1:8000/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "citations grounding fallback",
    "top_k": 3
  }'
```

### Generate an answer

```bash
curl -X POST http://127.0.0.1:8000/answers/generate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Why do citations matter in RAG?",
    "top_k": 3
  }'
```

Expected response shape:

```json
{
  "query": "Why do citations matter in RAG?",
  "answer": "Based on the retrieved context (...), the answer is: ...",
  "citations": [
    {
      "chunk_id": "doc-1-0",
      "document_id": "doc-1",
      "title": "RAG Basics",
      "content": "...",
      "score": 1.23
    }
  ],
  "fallback_used": false
}
```

### Run tests

```bash
pytest -q
```

## Project structure

```text
app/
  api/
    routes.py
  models/
    schemas.py
  services/
    answering.py
    ingestion.py
    retrieval.py
  main.py
tests/
  test_rag_api.py
Dockerfile
requirements.txt
README.md
```

## What this project demonstrates to recruiters and technical evaluators

- backend-first AI engineering instead of notebook-only work
- separation between API, ingestion, retrieval, and answering logic
- practical RAG fundamentals
- honest fallback behavior instead of hallucinated answers
- citation-aware response design
- clear boundaries for replacing lexical retrieval with embeddings/vector search
- testable API behavior

## Suggested interview talking points

- why the first version uses lightweight lexical retrieval
- how to migrate retrieval to embeddings + pgvector
- how to add PDF/DOCX parsing
- how to evaluate groundedness, answer relevance, and retrieval quality
- when to return a fallback instead of fabricating an answer
- how to add observability, latency logging, and per-query evaluation traces

## Roadmap

- persistent vector database using Supabase pgvector or PostgreSQL + pgvector
- embeddings-based semantic retrieval
- PDF and DOCX parsing
- evaluation suite for groundedness and relevance
- retrieval latency and quality logging
- multi-collection support
- authentication and rate limiting
- Docker Compose with persistent services

## License

MIT
