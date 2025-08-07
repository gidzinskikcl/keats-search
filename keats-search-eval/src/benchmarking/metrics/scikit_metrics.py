from sklearn.metrics import precision_score, ndcg_score


class PrecisionAtK:
    def __init__(self, k: int):
        self.k = k
        self.name = f"Precision@{k}"

    def compute(
        self,
        query_id: str,
        retrieved_docs: list,
        relevant: dict[str, dict[str, int]],
    ) -> float:
        if self.k == 0:
            return None

        top_k_docs = retrieved_docs[: self.k]
        if not top_k_docs:
            return 0.0

        query_relevance = relevant[query_id]

        y_true = [
            1 if query_relevance.get(doc.doc_id, 0) > 0 else 0 for doc in top_k_docs
        ]
        y_pred = [1] * len(y_true)

        if sum(y_true) == 0:
            return 0.0

        return precision_score(y_true, y_pred, zero_division=0)


class MRRAtK:
    def __init__(self, k: int):
        self.k = k
        self.name = f"MRR@{k}"

    def compute(
        self,
        query_id: str,
        retrieved_docs: list,
        relevant: dict[str, dict[str, int]],
    ) -> float:
        top_k_docs = retrieved_docs[: self.k]

        query_relevance = relevant[query_id]

        for rank, doc in enumerate(top_k_docs, start=1):
            if query_relevance.get(doc.doc_id, 0) > 0:
                return 1.0 / rank

        return 0.0


class NDCGAtK:
    def __init__(self, k: int):
        self.k = k
        self.name = f"NDCG@{k}"

    def compute(
        self,
        query_id: str,
        retrieved_docs: list,
        relevant: dict[str, dict[str, int]],
    ) -> float:
        top_k_docs = retrieved_docs[: self.k]

        if not top_k_docs:
            return 0.0

        query_relevance = relevant[query_id]

        y_true = [query_relevance.get(doc.doc_id, 0) for doc in top_k_docs]
        y_score = [1.0] * len(y_true)

        return ndcg_score([y_true], [y_score], k=self.k)
