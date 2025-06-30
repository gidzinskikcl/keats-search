import math

from benchmarking.metrics import metric
from benchmarking.schemas import schemas

class NDCG(metric.Metric):
    def __init__(self, k: int):
        self.k = k

    def evaluate(self, ground_truth_entry: schemas.GroundTruthEntry, ranked_list: list[schemas.Document]) -> float:
        scores = ground_truth_entry.relevance_scores

        if not ranked_list:
            return 0.0

        # Top-k predictions
        docs = ranked_list[:self.k]

        # Relevance of predicted docs
        predicted_rels = [
            scores.get(doc.doc_id, schemas.RelevanceScore.IRRELEVANT).value
            for doc in docs
        ]

        # Ideal sorted relevance values
        ideal_rels = sorted(
            [score.value for score in scores.values()],
            reverse=True
        )[:self.k]

        # Compute DCG
        dcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(predicted_rels))

        # Compute IDCG
        idcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(ideal_rels))

        return dcg / idcg if idcg > 0 else 0.0
