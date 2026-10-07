from app.retrieval.opensearch_store import OpenSearchStore

store = OpenSearchStore()

if store.client.indices.exists(index=store.INDEX_NAME):
    store.client.indices.delete(index=store.INDEX_NAME)
    print("Old index deleted.")

store.create_index()
print("Fresh index created.")