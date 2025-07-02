import pytest
from benchmarking.metrics import mean_metric, precision
from benchmarking.schemas import schemas

def docs(*ids):
    return [schemas.Document(doc_id=doc_id, content="", course="", lecture="") for doc_id in ids]

@pytest.mark.skip(reason="Not in use")
def test_mean_metric_precision():
    metric = precision.Precision(k=2)
    aggregator = mean_metric.MeanMetric(metric)

    gt = schemas.GroundTruth(entries={
        "q1": schemas.GroundTruthEntry(
            query="q1",
            query_id="q1_1",
            relevance_scores={
                "doc1": schemas.RelevanceScore.MODERATELY_RELEVANT,
                "doc2": schemas.RelevanceScore.IRRELEVANT
            }
        ),
        "q2": schemas.GroundTruthEntry(
            query="q2",
            query_id="q2_1",
            relevance_scores={
                "doc3": schemas.RelevanceScore.HIGHLY_RELEVANT,
                "doc4": schemas.RelevanceScore.IRRELEVANT
            }
        )
    })

    preds = schemas.Predictions(entries={
        "q1": schemas.PredictionsEntry(
            query="q1",
            query_id="q1_1",
            ranked_list=docs("doc1", "doc2")
        ),
        "q2": schemas.PredictionsEntry(
            query="q2",
            query_id="q2_1",
            ranked_list=docs("doc4", "doc3")
        )
    })
    assert aggregator.evaluate(ground_truth=gt, predictions=preds) == 0.5
