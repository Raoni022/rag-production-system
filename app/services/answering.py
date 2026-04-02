def answer(query, results):
    if not results:
        return "I don't have enough information to answer this reliably."

    context = " ".join([r["content"] for r in results])
    return f"Based on documents: {context}"
