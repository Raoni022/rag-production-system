from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def setup_function():
    client.delete("/documents")


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ingest_document_creates_chunks():
    payload = {
        "document_id": "doc-1",
        "title": "RAG Basics",
        "content": "Retrieval augmented generation improves answer grounding by retrieving relevant context before generation. " * 5,
        "chunk_size": 120,
        "chunk_overlap": 20,
    }

    response = client.post("/documents/ingest", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == "doc-1"
    assert data["chunks_created"] > 1


def test_search_returns_relevant_chunks():
    client.post(
        "/documents/ingest",
        json={
            "document_id": "doc-1",
            "title": "RAG Basics",
            "content": "Grounded answers require retrieval, citations, and fallback behavior when context is weak. " * 4,
        },
    )

    response = client.post("/retrieval/search", json={"query": "retrieval citations", "top_k": 2})

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "retrieval citations"
    assert len(data["results"]) >= 1
    assert data["results"][0]["score"] > 0


def test_answer_generation_returns_citations():
    client.post(
        "/documents/ingest",
        json={
            "document_id": "doc-2",
            "title": "Fallback Behavior",
            "content": "A RAG system should return a fallback when retrieved context is insufficient. Citations help users verify grounded answers. " * 4,
        },
    )

    response = client.post("/answers/generate", json={"query": "fallback citations", "top_k": 3})

    assert response.status_code == 200
    data = response.json()
    assert data["fallback_used"] is False
    assert len(data["citations"]) >= 1
    assert "Based on the retrieved context" in data["answer"]


def test_answer_generation_falls_back_without_context():
    response = client.post("/answers/generate", json={"query": "unknown topic", "top_k": 3})

    assert response.status_code == 200
    data = response.json()
    assert data["fallback_used"] is True
    assert data["citations"] == []
