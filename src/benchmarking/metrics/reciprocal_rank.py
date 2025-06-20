from benchmarking.metrics import metric
from benchmarking.schemas import schemas

class ReciprocalRank(metric.Metric):
    def __init__(self, k: int):
        self.k = k

    def evaluate(self, ground_truth_entry: schemas.GroundTruthEntry, ranked_list: list[schemas.Document]) -> float:
        scores = ground_truth_entry.relevance_scores

        for i, doc in enumerate(ranked_list[:self.k]):
            doc_id = doc.doc_id
            rel = scores.get(doc_id, schemas.RelevanceScore.IRRELEVANT).value
            if rel >= schemas.RelevanceScore.MODERATELY_RELEVANT.value:
                return 1.0 / (i + 1)

        return 0.0  # no relevant document found
