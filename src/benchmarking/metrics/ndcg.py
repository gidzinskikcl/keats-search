import math

import numpy as np
from sklearn.metrics import ndcg_score, dcg_score

from benchmarking.metrics import metric
from benchmarking.schemas import schemas

class NDCG(metric.Metric):
    def __init__(self, k: int):
        self.k = k

    def evaluate(self, ground_truth_entry: schemas.GroundTruthEntry, ranked_list: list[schemas.Document]) -> float:
        scores = ground_truth_entry.relevance_scores

        # If no documents were ranked, return 0
        if not ranked_list:
            return 0.0

        # Get top-k predictions
        docs = ranked_list[:self.k]

        # Build relevance score vector aligned with prediction order
        predicted_rels = [
            scores.get(doc.doc_id, schemas.RelevanceScore.IRRELEVANT).value
            for doc in docs
        ]

        # Build ideal relevance vector
        ideal_rels = [s.value for s in scores.values()][:self.k]

        # Convert to sklearn-compatible shape: (1, k)
        y_pred = np.asarray([predicted_rels])
        y_true = np.asarray([ideal_rels])

        # If no relevant documents in ground truth, IDCG = 0 -> NDCG = 0
        if sum(ideal_rels) == 0:
            return 0.0

        # Use ndcg_score for final result
        result = ndcg_score(y_true, y_pred, k=self.k)
        return result

    # def evaluate(self, ground_truth_entry: schemas.GroundTruthEntry, ranked_list: list[schemas.Document]) -> float:
    #     scores = ground_truth_entry.relevance_scores

    #     # DCG@k
    #     dcg = 0.0
    #     for i, doc_id in enumerate(ranked_list[:self.k]):
    #         rel = scores.get(doc_id, schemas.RelevanceScore.IRRELEVANT).value
    #         if rel > 0:
    #             dcg += rel / math.log2(i + 2)  # log2(i+2) for 1-based index

    #     # IDCG@k: ideal DCG with top-k highest relevance scores
    #     ideal_rels = sorted(
    #         [score.value for score in scores.values()],
    #         reverse=True
    #     )[:self.k]

    #     idcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(ideal_rels))

    #     return dcg / idcg if idcg > 0 else 0.0
