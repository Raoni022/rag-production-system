from __future__ import annotations

from typing import Dict, List


def chunk_text(text: str, size: int = 300, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks for simple retrieval.

    This intentionally uses character-based chunking for a lightweight local demo.
    The API keeps chunking isolated so it can later be replaced with token-aware
    chunking without changing the route layer.
    """
    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    if overlap >= size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: List[str] = []
    cursor = 0
    step = size - overlap

    while cursor < len(cleaned):
        chunk = cleaned[cursor : cursor + size].strip()
        if chunk:
            chunks.append(chunk)
        cursor += step

    return chunks


def build_chunks(
    doc_id: str,
    title: str,
    content: str,
    chunk_size: int = 300,
    chunk_overlap: int = 50,
) -> List[Dict[str, str]]:
    raw_chunks = chunk_text(content, size=chunk_size, overlap=chunk_overlap)
    return [
        {
            "chunk_id": f"{doc_id}-{index}",
            "document_id": doc_id,
            "title": title,
            "content": chunk,
        }
        for index, chunk in enumerate(raw_chunks)
    ]
