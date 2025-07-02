from sklearn.metrics import precision_score, ndcg_score

class PrecisionAtK:
    def __init__(self, k: int):
        self.k = k
        self.name = f"Precision@{k}"


    def compute(self, query_id: str, retrieved_docs: list, relevant_pairs: set[tuple[str, str]]) -> float:
        """
        Precision@k = (Number of relevant documents in top-k) / k
        y_true - actual relevance of each returned doc
        y_pred - model's predictions
        """
        if self.k == 0:
            return None
        
        top_k_docs = retrieved_docs[:self.k]
        if not top_k_docs:
            return 0.0  # No docs retrieved at all
        
        y_true = [1 if (query_id, doc.doc_id) in relevant_pairs else 0 for doc in top_k_docs]
        y_pred = [1] * len(y_true)  # all retrieved docs are predicted relevant

        if sum(y_true) == 0:
            return 0.0  # No relevant docs found in top-k
        
        return precision_score(y_true, y_pred, zero_division=0)
    

class MRRAtK:
    def __init__(self, k: int):
        self.k = k
        self.name = f"MRR@{k}"

    def compute(self, query_id: str, retrieved_docs: list, relevant_pairs: set[tuple[str, str]]) -> float:
        top_k_docs = retrieved_docs[:self.k]

        for rank, doc in enumerate(top_k_docs, start=1):  # rank starts at 1
            if (query_id, doc.doc_id) in relevant_pairs:
                return 1.0 / rank  # first relevant doc found

        return 0.0  # no relevant doc in top-k
