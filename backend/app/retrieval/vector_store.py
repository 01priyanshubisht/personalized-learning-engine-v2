import numpy as np


class VectorStore:

    def __init__(self):
        self.documents = []
        self.vectors = []

    def add(
        self,
        document: dict,
        vector: list[float],
    ) -> None:

        self.documents.append(document)
        self.vectors.append(vector)

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[dict]:

        if not self.vectors:
            return []

        query = np.array(query_vector)

        scores = []

        for index, vector in enumerate(self.vectors):

            stored_vector = np.array(vector)

            similarity = np.dot(
                query,
                stored_vector
            )

            scores.append(
                (index, float(similarity))
            )

        scores.sort(
            key=lambda item: item[1],
            reverse=True
        )

        results = []

        for index, score in scores[:top_k]:

            result = self.documents[index].copy()

            result["score"] = score

            results.append(result)

        return results