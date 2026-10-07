from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.opensearch_store import OpenSearchStore


embedding_service = EmbeddingService()
store = OpenSearchStore()

query = "How can I quickly find a value using a dictionary?"

query_vector = embedding_service.embed_text(query)

results = store.vector_search(
    query_vector=query_vector,
    top_k=5,
)

print("\nSearch Results")
print("==============================")

for rank, result in enumerate(results, start=1):

    print(f"\nRank: {rank}")
    print("Score:", result["score"])
    print("Chunk:", result["chunk_id"])
    print("Section:", result["section"])
    print(
        "Pages:",
        result["page_start"],
        "-",
        result["page_end"],
    )
    print("Text:", result["text"][:300])