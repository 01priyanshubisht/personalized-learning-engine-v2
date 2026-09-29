from app.retrieval.embedding_service import EmbeddingService
import numpy as np


embedding_service = EmbeddingService()

texts = [
    "HashMap provides average constant time lookup.",
    "A dictionary can retrieve values in constant time.",
    "The weather is pleasant today.",
]

vectors = embedding_service.embed_texts(texts)

similarity_01 = np.dot(vectors[0], vectors[1])
similarity_02 = np.dot(vectors[0], vectors[2])

print("HashMap vs Dictionary:", similarity_01)
print("HashMap vs Weather:", similarity_02)