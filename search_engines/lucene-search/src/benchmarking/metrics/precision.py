from benchmarking.metrics import metric
from benchmarking.schemas import schemas


class Precision(metric.Metric):
    def __init__(self, k: int):
        self.k = k

    def evaluate(self, ground_truth_entry: schemas.GroundTruthEntry, ranked_list: list[schemas.Document]) -> float:
        scores = ground_truth_entry.relevance_scores
        top_k = ranked_list[:self.k]

        num_relevant = 0
        for doc in top_k:
            doc_id = doc.doc_id
            rel = scores.get(doc_id, schemas.RelevanceScore.IRRELEVANT).value
            if rel >= schemas.RelevanceScore.MODERATELY_RELEVANT.value:
                num_relevant += 1

        return num_relevant / len(top_k) if top_k else 0.0
