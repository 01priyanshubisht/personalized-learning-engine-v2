from app.retrieval.opensearch_store import OpenSearchStore


store = OpenSearchStore()

store.create_index()

print("Index created.")
print("Documents:", store.count())