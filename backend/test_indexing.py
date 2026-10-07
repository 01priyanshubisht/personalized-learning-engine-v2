from pathlib import Path

from app.ingestion.ingestion_service import IngestionService
from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.opensearch_store import OpenSearchStore


ingestion_service = IngestionService()
embedding_service = EmbeddingService()
store = OpenSearchStore()

# Make sure index exists
store.create_index()

# Phase A → chunks
chunks = ingestion_service.ingest(
    file_path=Path("data/documents/test.pdf"),
    document_id="test_document",
)

print("Chunks created:", len(chunks))

# Chunks → embeddings
texts = [chunk.text for chunk in chunks]

vectors = embedding_service.embed_texts(texts)

print("Vectors created:", len(vectors))

# Embeddings + metadata → OpenSearch
for chunk, vector in zip(chunks, vectors):

    store.add_chunk(
        chunk=chunk,
        embedding=vector,
    )

print("Chunks indexed successfully.")
print("OpenSearch document count:", store.count())