def chunk_text(text, size=300, overlap=50):
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+size]
        chunks.append(chunk)
        i += size - overlap
    return chunks


def build_chunks(doc_id, title, content):
    raw = chunk_text(content)
    return [
        {
            "chunk_id": f"{doc_id}-{i}",
            "document_id": doc_id,
            "title": title,
            "content": c
        }
        for i, c in enumerate(raw)
    ]
