from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.vector_store import VectorStore


embedding_service = EmbeddingService()
vector_store = VectorStore()


documents = [
    {
        "chunk_id": "1",
        "text": "HashMap provides average constant time lookup.",
    },
    {
        "chunk_id": "2",
        "text": "A linked list stores elements using connected nodes.",
    },
    {
        "chunk_id": "3",
        "text": "Photosynthesis converts light energy into chemical energy.",
    },
]


# Index documents
for document in documents:

    vector = embedding_service.embed_text(
        document["text"]
    )

    vector_store.add(
        document=document,
        vector=vector,
    )


# Search
query = "How can I quickly find a value in a dictionary?"

query_vector = embedding_service.embed_text(query)

results = vector_store.search(
    query_vector=query_vector,
    top_k=3,
)


for result in results:

    print(
        result["score"],
        "->",
        result["text"]
    )