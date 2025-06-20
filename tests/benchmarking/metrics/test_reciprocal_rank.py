import pytest

from benchmarking.metrics import reciprocal_rank
from benchmarking.schemas import schemas 




def gt_entry(relevance: dict[str, schemas.RelevanceScore]) -> schemas.GroundTruthEntry:
    return schemas.GroundTruthEntry(query="test", query_id="test1", relevance_scores=relevance)


def test_rr_at_k_hit_first():
    rr = reciprocal_rank.ReciprocalRank(k=5)
    gt = gt_entry({
        "doc1": schemas.RelevanceScore.HIGHLY_RELEVANT,
        "doc2": schemas.RelevanceScore.MODERATELY_RELEVANT,
    })
    ranked = [
        schemas.Document(doc_id="doc1", content="Heap memory explained"),
        schemas.Document(doc_id="doc2", content="What is stack memory"),
        schemas.Document(doc_id="doc3", content="Heap vs stack differences"),
    ]
    assert rr.evaluate(gt, ranked) == pytest.approx(1.0)

def test_rr_at_k_hit_third():
    rr = reciprocal_rank.ReciprocalRank(k=5)
    gt = gt_entry({
        "doc3": schemas.RelevanceScore.MODERATELY_RELEVANT
    })
    ranked = [
        schemas.Document(doc_id="doc1", content="Heap memory explained"),
        schemas.Document(doc_id="doc2", content="What is stack memory"),
        schemas.Document(doc_id="doc3", content="Heap vs stack differences"),
        schemas.Document(doc_id="doc4", content="What is a parser combinator"),
        schemas.Document(doc_id="doc5", content="Examples of DSML"),
    ]
    assert rr.evaluate(gt, ranked) == pytest.approx(1.0 / 3)

def test_rr_at_k_no_hit():
    rr = reciprocal_rank.ReciprocalRank(k=5)
    gt = gt_entry({
        "doc1": schemas.RelevanceScore.IRRELEVANT,
        "doc2": schemas.RelevanceScore.SLIGHTLY_RELEVANT,
    })
    ranked = [
        schemas.Document(doc_id="doc3", content="Heap vs stack differences"),
        schemas.Document(doc_id="doc4", content="What is a parser combinator"),
        schemas.Document(doc_id="doc5", content="Examples of DSML"),
    ]
    assert rr.evaluate(gt, ranked) == 0.0
