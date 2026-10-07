from app.retrieval.embedding_service import EmbeddingService
from app.retrieval.opensearch_store import OpenSearchStore


EVAL_DATASET = [
    # 1-10: exact / lexical
    {"query": "What is a stack?", "relevant_chunks": ["test_document_35"]},
    {"query": "What is a queue?", "relevant_chunks": ["test_document_36"]},
    {"query": "What is a deque?", "relevant_chunks": ["test_document_37"]},
    {"query": "How does a monotonic stack work?", "relevant_chunks": ["test_document_38"]},
    {"query": "How are expressions evaluated using stacks?", "relevant_chunks": ["test_document_39"]},
    {"query": "What is a hash table?", "relevant_chunks": ["test_document_41"]},
    {"query": "How are hash collisions handled?", "relevant_chunks": ["test_document_42"]},
    {"query": "What is load factor in hashing?", "relevant_chunks": ["test_document_43"]},
    {"query": "What is frequency counting?", "relevant_chunks": ["test_document_44", "test_document_147"]},
    {"query": "Hash map versus array", "relevant_chunks": ["test_document_45"]},

    # 11-20: semantic / paraphrased
    {"query": "Which data structure follows last-in-first-out order?", "relevant_chunks": ["test_document_35"]},
    {"query": "Which structure processes the oldest inserted element first?", "relevant_chunks": ["test_document_36"]},
    {"query": "Which structure lets you add and remove elements from both ends?", "relevant_chunks": ["test_document_37"]},
    {"query": "How can a data structure efficiently find the next greater element?", "relevant_chunks": ["test_document_38", "test_document_149"]},
    {"query": "Why can hash table lookup be constant time on average?", "relevant_chunks": ["test_document_41"]},
    {"query": "Why do collisions make hash tables slower?", "relevant_chunks": ["test_document_42", "test_document_43"]},
    {"query": "When should a frequency map be used in an algorithm?", "relevant_chunks": ["test_document_44", "test_document_147"]},
    {"query": "How can a recursive algorithm avoid solving the same subproblem repeatedly?", "relevant_chunks": ["test_document_47", "test_document_128"]},
    {"query": "What technique explores choices and then undoes them?", "relevant_chunks": ["test_document_49"]},
    {"query": "How does pruning improve backtracking?", "relevant_chunks": ["test_document_50"]},

    # 21-30: trees / heaps
    {"query": "What traversal visits root before its children?", "relevant_chunks": ["test_document_54"]},
    {"query": "Why does inorder traversal of a BST produce sorted values?", "relevant_chunks": ["test_document_55", "test_document_61"]},
    {"query": "Which traversal processes children before their parent?", "relevant_chunks": ["test_document_56"]},
    {"query": "How does level order traversal process a tree?", "relevant_chunks": ["test_document_57"]},
    {"query": "How is the height of a binary tree calculated?", "relevant_chunks": ["test_document_58"]},
    {"query": "How can the lowest common ancestor be found in a BST?", "relevant_chunks": ["test_document_59"]},
    {"query": "What property makes binary search trees searchable?", "relevant_chunks": ["test_document_61", "test_document_62"]},
    {"query": "What is the complexity of searching a BST?", "relevant_chunks": ["test_document_62", "test_document_65"]},
    {"query": "What happens when a BST becomes skewed?", "relevant_chunks": ["test_document_65"]},
    {"query": "Why are heaps useful for priority queues?", "relevant_chunks": ["test_document_67", "test_document_70", "test_document_145"]},

    # 31-40: graphs
    {"query": "What is the difference between an adjacency list and matrix?", "relevant_chunks": ["test_document_79", "test_document_80"]},
    {"query": "Which graph representation is better for sparse graphs?", "relevant_chunks": ["test_document_80"]},
    {"query": "How does BFS explore a graph?", "relevant_chunks": ["test_document_83"]},
    {"query": "What is the time complexity of BFS?", "relevant_chunks": ["test_document_84"]},
    {"query": "Why does BFS find shortest paths in unweighted graphs?", "relevant_chunks": ["test_document_85", "test_document_102"]},
    {"query": "When would multi-source BFS be useful?", "relevant_chunks": ["test_document_86"]},
    {"query": "How does DFS explore a graph?", "relevant_chunks": ["test_document_88"]},
    {"query": "How can DFS find connected components?", "relevant_chunks": ["test_document_90"]},
    {"query": "How can a cycle be detected in a directed graph?", "relevant_chunks": ["test_document_94"]},
    {"query": "How does Kahn's algorithm perform topological sorting?", "relevant_chunks": ["test_document_96"]},

    # 41-45: shortest paths / MST
    {"query": "When can Dijkstra's algorithm be used?", "relevant_chunks": ["test_document_98"]},
    {"query": "What is the complexity of Dijkstra with a binary heap?", "relevant_chunks": ["test_document_99"]},
    {"query": "Which shortest path algorithm supports negative edge weights?", "relevant_chunks": ["test_document_100"]},
    {"query": "What algorithm computes all-pairs shortest paths with O(V^3) time?", "relevant_chunks": ["test_document_101"]},
    {"query": "How does Kruskal's algorithm build a minimum spanning tree?", "relevant_chunks": ["test_document_104", "test_document_105"]},

    # 46-50: sorting / binary search / DP / advanced structures
    {"query": "What is the average time complexity of quicksort?", "relevant_chunks": ["test_document_113"]},
    {"query": "How does binary search reduce the search space?", "relevant_chunks": ["test_document_116"]},
    {"query": "What does binary search on answer require?", "relevant_chunks": ["test_document_119"]},
    {"query": "How is memoization different from tabulation?", "relevant_chunks": ["test_document_131", "test_document_132"]},
    {"query": "What data structure supports prefix-sum queries and point updates in O(log n)?", "relevant_chunks": ["test_document_142"]},
]


def recall_at_k(results, relevant_chunks, k):
    retrieved = {result["chunk_id"] for result in results[:k]}
    return int(bool(retrieved.intersection(relevant_chunks)))


def reciprocal_rank(results, relevant_chunks):
    for rank, result in enumerate(results, start=1):
        if result["chunk_id"] in relevant_chunks:
            return 1.0 / rank
    return 0.0


def evaluate_method(store, embedder, method_name, k_values=(5, 10)):
    recall_scores = {k: [] for k in k_values}
    reciprocal_ranks = []

    print("\n" + "=" * 70)
    print(method_name)
    print("=" * 70)

    for number, item in enumerate(EVAL_DATASET, start=1):
        query = item["query"]
        relevant = set(item["relevant_chunks"])
        query_vector = embedder.embed_text(query)

        if method_name == "BM25":
            results = store.keyword_search(query=query, top_k=10)
        elif method_name == "Vector":
            results = store.vector_search(query_vector=query_vector, top_k=10)
        elif method_name == "Hybrid":
            results = store.hybrid_search(
                query=query,
                query_vector=query_vector,
                top_k=10,
            )
        else:
            raise ValueError(f"Unknown method: {method_name}")

        for k in k_values:
            recall_scores[k].append(
                recall_at_k(results, relevant, k)
            )

        rr = reciprocal_rank(results, relevant)
        reciprocal_ranks.append(rr)

        print(
            f"{number:02d}. {query}\n"
            f"    Relevant: {sorted(relevant)}\n"
            f"    Top 5: {[r['chunk_id'] for r in results[:5]]}\n"
            f"    Recall@5: {recall_scores[5][-1]} | "
            f"RR: {rr:.3f}"
        )

    print("\nSummary")
    print("-" * 30)

    for k in k_values:
        mean_recall = sum(recall_scores[k]) / len(recall_scores[k])
        print(f"Recall@{k}: {mean_recall:.4f}")

    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    print(f"MRR:       {mrr:.4f}")

    return {
        f"Recall@{k}": sum(recall_scores[k]) / len(recall_scores[k])
        for k in k_values
    } | {"MRR": mrr}


def main():
    store = OpenSearchStore()
    embedder = EmbeddingService()

    print(f"Evaluation queries: {len(EVAL_DATASET)}")
    print(f"Indexed chunks: {store.count()}")

    results = {}

    for method in ("BM25", "Vector", "Hybrid"):
        results[method] = evaluate_method(
            store,
            embedder,
            method,
        )

    print("\n" + "=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print(
        f"{'Method':<12}"
        f"{'Recall@5':<12}"
        f"{'Recall@10':<12}"
        f"{'MRR':<12}"
    )

    for method, metrics in results.items():
        print(
            f"{method:<12}"
            f"{metrics['Recall@5']:<12.4f}"
            f"{metrics['Recall@10']:<12.4f}"
            f"{metrics['MRR']:<12.4f}"
        )


if __name__ == "__main__":
    main()
