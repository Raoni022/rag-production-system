class InMemoryStore:
    def __init__(self):
        self.chunks = []

    def add(self, items):
        self.chunks.extend(items)

    def list(self):
        return self.chunks

store = InMemoryStore()
