from benchmarking.models import search_model
from benchmarking.schemas import schemas
from benchmarking.metrics import metric

class Evaluator:
    def __init__(self, metrics: list[metric.Metric]):
        self.metrics = metrics

    def evaluate(
        self,
        model: search_model.SearchModel,
        queries: list[schemas.Query],
        ground_truth: schemas.GroundTruth
    ) -> dict[str, dict[str, dict[str, float]]]:
        per_query_scores = {}
        aggregated_scores = {m.__class__.__name__: 0.0 for m in self.metrics}
        counts = {m.__class__.__name__: 0 for m in self.metrics}

        for query in queries:
            query_id = query.id
            predictions = model.search(query=query)
            gt_entry = ground_truth[query_id]

            query_scores = {}
            for m in self.metrics:
                metric_name = m.__class__.__name__
                score = m.evaluate(gt_entry, predictions)
                query_scores[metric_name] = score

                aggregated_scores[metric_name] += score
                counts[metric_name] += 1

            per_query_scores[query_id] = query_scores

        mean_scores = {
            name: aggregated_scores[name] / counts[name] if counts[name] > 0 else 0.0
            for name in aggregated_scores
        }

        return {
            "per_query": per_query_scores,
            "mean": mean_scores
        }
