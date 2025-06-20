import pytest
from benchmarking.metrics import precision
from benchmarking.schemas import schemas


@pytest.fixture
def ranked():
    result = [
        schemas.Document(doc_id="doc1", content="Heap memory explained"),
        schemas.Document(doc_id="doc2", content="What is stack memory"),
        schemas.Document(doc_id="doc3", content="Heap vs stack differences"),
    ]
    return result

def gt_entry(relevance: dict[str, schemas.RelevanceScore]) -> schemas.GroundTruthEntry:
    return schemas.GroundTruthEntry(query="test", query_id="test1", relevance_scores=relevance)


def test_precision_at_k_all_relevant(ranked):
    metric = precision.Precision(k=3)
    gt = gt_entry({
        "doc1": schemas.RelevanceScore.HIGHLY_RELEVANT,
        "doc2": schemas.RelevanceScore.MODERATELY_RELEVANT,
        "doc3": schemas.RelevanceScore.MODERATELY_RELEVANT,
    })
    assert metric.evaluate(gt, ranked) == 1.0

def test_precision_at_k_partial(ranked):
    metric = precision.Precision(k=3)
    gt = gt_entry({
        "doc1": schemas.RelevanceScore.IRRELEVANT,
        "doc2": schemas.RelevanceScore.HIGHLY_RELEVANT,
        "doc3": schemas.RelevanceScore.SLIGHTLY_RELEVANT,
    })
    assert metric.evaluate(gt, ranked) == 1 / 3

def test_precision_at_k_none1(ranked):
    metric = precision.Precision(k=3)
    gt = gt_entry({
        "doc1": schemas.RelevanceScore.IRRELEVANT,
        "doc2": schemas.RelevanceScore.SLIGHTLY_RELEVANT,
        "doc3": schemas.RelevanceScore.IRRELEVANT,
    })
    assert metric.evaluate(gt, ranked) == 0.0

def test_precision_at_k_none2(ranked):
    metric = precision.Precision(k=3)
    gt = gt_entry({
        "doc1": schemas.RelevanceScore.IRRELEVANT,
        "doc2": schemas.RelevanceScore.IRRELEVANT,
        "doc3": schemas.RelevanceScore.IRRELEVANT,
    })
    assert metric.evaluate(gt, ranked) == 0.0
