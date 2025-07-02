import pytest
from benchmarking.metrics import ndcg
from benchmarking.schemas import schemas

def gt_entry(relevance: dict[str, schemas.RelevanceScore]) -> schemas.GroundTruthEntry:
    return schemas.GroundTruthEntry(query="test", query_id="test1", relevance_scores=relevance)

@pytest.mark.skip(reason="Not in use")
def test_perfect_ranking():
    metric = ndcg.NDCG(k=3)
    ground_truth = gt_entry({
        "doc1": schemas.RelevanceScore.HIGHLY_RELEVANT,
        "doc2": schemas.RelevanceScore.MODERATELY_RELEVANT,
        "doc3": schemas.RelevanceScore.SLIGHTLY_RELEVANT
    })
    ranked = [
        schemas.Document(doc_id="doc1", content="Heap memory explained", course="Algorithms", lecture="Lecture 1"),
        schemas.Document(doc_id="doc2", content="What is stack memory", course="Algorithms", lecture="Lecture 1"),
        schemas.Document(doc_id="doc3", content="Heap vs stack differences", course="Algorithms", lecture="Lecture 1"),
    ]
    assert metric.evaluate(ground_truth, ranked) == 1.0

@pytest.mark.skip(reason="Not in use")
def test_worst_ranking():
    metric = ndcg.NDCG(k=3)
    ground_truth = gt_entry({
        "doc1": schemas.RelevanceScore.HIGHLY_RELEVANT,
        "doc2": schemas.RelevanceScore.MODERATELY_RELEVANT,
        "doc3": schemas.RelevanceScore.SLIGHTLY_RELEVANT
    })
    ranked = [ # reversed
        schemas.Document(doc_id="doc3", content="Heap vs stack differences", course="Algorithms", lecture="Lecture 1"),
        schemas.Document(doc_id="doc2", content="What is stack memory", course="Algorithms", lecture="Lecture 1"),
        schemas.Document(doc_id="doc1", content="Heap memory explained", course="Algorithms", lecture="Lecture 1"),
    ]
    score = metric.evaluate(ground_truth, ranked)
    assert 0.0 < score < 1.0

@pytest.mark.skip(reason="Not in use")
def test_partial_relevance():
    metric = ndcg.NDCG(k=3)
    ground_truth = gt_entry({
        "doc1": schemas.RelevanceScore.HIGHLY_RELEVANT,
        "doc2": schemas.RelevanceScore.IRRELEVANT,
        "doc3": schemas.RelevanceScore.MODERATELY_RELEVANT
    })
    ranked = [ # doc2 is irrelevant at top
        schemas.Document(doc_id="doc2", content="What is stack memory", course="Algorithms", lecture="Lecture 1"),
        schemas.Document(doc_id="doc3", content="Heap vs stack differences", course="Algorithms", lecture="Lecture 1"),
        schemas.Document(doc_id="doc1", content="Heap memory explained", course="Algorithms", lecture="Lecture 1"),
    ]
    score = metric.evaluate(ground_truth, ranked)
    assert 0.0 < score < 1.0

@pytest.mark.skip(reason="Not in use")
def test_empty_ranking():
    metric = ndcg.NDCG(k=3)
    ground_truth = gt_entry({
        "doc1": schemas.RelevanceScore.HIGHLY_RELEVANT,
        "doc2": schemas.RelevanceScore.MODERATELY_RELEVANT
    })
    ranked = []
    assert metric.evaluate(ground_truth, ranked) == 0.0

@pytest.mark.skip(reason="Not in use")
def test_no_relevant_docs():
    metric = ndcg.NDCG(k=3)
    ground_truth = gt_entry({
        "doc1": schemas.RelevanceScore.IRRELEVANT,
        "doc2": schemas.RelevanceScore.IRRELEVANT
    })
    ranked = [
        schemas.Document(doc_id="doc1", content="Heap memory explained", course="Algorithms", lecture="Lecture 1"),
        schemas.Document(doc_id="doc2", content="What is stack memory", course="Algorithms", lecture="Lecture 1"),
    ]
    assert metric.evaluate(ground_truth, ranked) == 0.0
