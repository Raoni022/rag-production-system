# RAG Production System

A production-oriented Retrieval-Augmented Generation (RAG) API built with FastAPI.

This repository is designed to demonstrate practical AI engineering skills that companies actually look for:
- document ingestion
- chunking and retrieval
- grounded answers with citations
- configurable top-k retrieval
- fallback behavior when the knowledge base is insufficient
- simple evaluation-ready architecture

## Why this project exists

Most RAG demos are toy chatbots. This project is intentionally structured like a backend service that can evolve into a production system.

The goal is to demonstrate proficiency in:
- Python backend engineering
- FastAPI design
- document processing
- retrieval architecture
- vector search concepts
- LLM application design
- observability-minded structure

## Current version

This initial version includes:
- FastAPI app with modular structure
- health endpoint
- document ingestion endpoint
- in-memory chunk store for local development
- simple retrieval endpoint
- answer generation endpoint with citations
- configurable `top_k`
- deterministic fallback when context is weak

## Planned upgrades

- persistent vector database (FAISS / Chroma / Supabase pgvector)
- embeddings-based semantic retrieval
- PDF and DOCX parsing
- evaluation suite for groundedness and relevance
- latency and retrieval logging
- multi-collection support
- Docker-based local environment

## Architecture

```text
client
  -> FastAPI API
      -> ingestion service
      -> retrieval service
      -> answering service
      -> in-memory store (v1)
```

Future production shape:

```text
client
  -> FastAPI API
      -> ingestion pipeline
      -> embedding provider
      -> vector database
      -> retrieval + ranking
      -> answer generation
      -> observability / metrics
```

## Endpoints

### `GET /health`
Returns service status.

### `POST /documents/ingest`
Accepts raw text content, splits it into chunks, and stores it for retrieval.

### `POST /retrieval/search`
Returns the most relevant chunks for a query using a lightweight lexical scoring strategy.

### `POST /answers/generate`
Builds a grounded answer using retrieved chunks and returns citations.

## Quick start

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

### 4. Open the docs

```text
http://127.0.0.1:8000/docs
```

## Example requests

### Ingest a document

```bash
curl -X POST http://127.0.0.1:8000/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc-1",
    "title": "RAG Basics",
    "content": "Retrieval-augmented generation improves answer grounding by using external documents.",
    "chunk_size": 220,
    "chunk_overlap": 40
  }'
```

### Search retrieval

```bash
curl -X POST http://127.0.0.1:8000/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What improves grounding?",
    "top_k": 3
  }'
```

### Generate an answer

```bash
curl -X POST http://127.0.0.1:8000/answers/generate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does RAG reduce hallucinations?",
    "top_k": 3
  }'
```

## Project structure

```text
app/
  api/
    routes.py
  core/
    config.py
  models/
    schemas.py
  services/
    answering.py
    ingestion.py
    retrieval.py
    store.py
  main.py
tests/
Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

## What this project demonstrates to recruiters

- clear backend structure instead of notebook-only work
- separation of concerns
- practical RAG fundamentals
- room for evaluation and production upgrades
- engineering decisions that can be discussed in interviews

## Suggested interview talking points

- why the first version uses a lightweight retrieval strategy
- how to migrate from lexical scoring to embeddings
- trade-offs between speed, complexity, and quality
- how to measure groundedness and retrieval quality
- when to return “I don’t know” instead of fabricating an answer

## License

MIT
