from typing import Any

from opensearchpy import OpenSearch


class OpenSearchStore:
    INDEX_NAME = "learning_chunks"

    def __init__(self, host: str = "localhost", port: int = 9200):
        self.client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            use_ssl=False,
            verify_certs=False,
            ssl_show_warn=False,
        )

    def keyword_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        body = {
            "size": top_k,
            "query": {
                "match": {
                    "text": query,
                }
            },
        }

        response = self.client.search(
            index=self.INDEX_NAME,
            body=body,
        )

        results = []

        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            results.append(
                {
                    "chunk_id": source["chunk_id"],
                    "document_id": source["document_id"],
                    "page_start": source["page_start"],
                    "page_end": source["page_end"],
                    "section": source["section"],
                    "text": source["text"],
                    "score": hit["_score"],
                }
            )

        return results

    def hybrid_search(
        self,
        query: str,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        keyword_results = self.keyword_search(
            query=query,
            top_k=top_k,
        )

        vector_results = self.vector_search(
            query_vector=query_vector,
            top_k=top_k,
        )

        fused = {}

        def add_results(results):
            for rank, result in enumerate(results, start=1):
                chunk_id = result["chunk_id"]

                if chunk_id not in fused:
                    fused[chunk_id] = {
                        **result,
                        "score": 0.0,
                    }

                fused[chunk_id]["score"] += 1.0 / (60 + rank)

        add_results(keyword_results)
        add_results(vector_results)

        return sorted(
            fused.values(),
            key=lambda item: item["score"],
            reverse=True,
        )[:top_k]

    def create_index(self) -> None:
        if self.client.indices.exists(index=self.INDEX_NAME):
            return

        mapping = {
            "settings": {
                "index": {
                    "knn": True,
                }
            },
            "mappings": {
                "properties": {
                    "chunk_id": {"type": "keyword"},
                    "document_id": {"type": "keyword"},
                    "page_start": {"type": "integer"},
                    "page_end": {"type": "integer"},
                    "section": {"type": "keyword"},
                    "text": {"type": "text"},
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": 384,
                        "space_type": "cosinesimil",
                    },
                }
            },
        }

        self.client.indices.create(
            index=self.INDEX_NAME,
            body=mapping,
        )

    def vector_search(self, query_vector: list[float], top_k: int = 5) -> list[dict]:
        body = {
            "size": top_k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_vector,
                        "k": top_k,
                    }
                }
            },
        }

        response = self.client.search(
            index=self.INDEX_NAME,
            body=body,
        )

        results = []

        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            results.append(
                {
                    "chunk_id": source["chunk_id"],
                    "document_id": source["document_id"],
                    "page_start": source["page_start"],
                    "page_end": source["page_end"],
                    "section": source["section"],
                    "text": source["text"],
                    "score": hit["_score"],
                }
            )

        return results

    def add_chunk(self, chunk, embedding: list[float]) -> None:
        document = {
            "chunk_id": chunk.chunk_id,
            "document_id": chunk.document_id,
            "page_start": chunk.page_start,
            "page_end": chunk.page_end,
            "section": chunk.section,
            "text": chunk.text,
            "embedding": embedding,
        }

        self.client.index(
            index=self.INDEX_NAME,
            id=chunk.chunk_id,
            body=document,
        )

    def add_document(self, document: dict[str, Any]) -> None:
        self.client.index(
            index=self.INDEX_NAME,
            id=document["chunk_id"],
            body=document,
        )

    def count(self) -> int:
        response = self.client.count(index=self.INDEX_NAME)
        return response["count"]