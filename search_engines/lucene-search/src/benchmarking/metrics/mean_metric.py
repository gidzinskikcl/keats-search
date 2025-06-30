from benchmarking.schemas import schemas
from benchmarking.metrics import metric

class MeanMetric:
    def __init__(self, metric: metric.Metric):
        self.metric = metric

    def evaluate(self, ground_truth: schemas.GroundTruth, predictions: schemas.Predictions) -> float:
        total = 0.0
        count = 0

        for query_id, prediction_entry in predictions.items():
            entry = ground_truth[query_id]
            ranked_list = prediction_entry.ranked_list
            score = self.metric.evaluate(ground_truth_entry=entry, ranked_list=ranked_list)
            total += score
            count += 1

        return total / count if count > 0 else 0.0
