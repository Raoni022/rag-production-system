def score(query, text):
    return sum(1 for word in query.lower().split() if word in text.lower())


def search(query, chunks, top_k=3):
    scored = []
    for c in chunks:
        s = score(query, c["content"])
        if s > 0:
            c["score"] = s
            scored.append(c)
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]
