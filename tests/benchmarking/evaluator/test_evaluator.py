import pytest
from unittest.mock import Mock
from collections import OrderedDict

from benchmarking.metrics import precision, reciprocal_rank
from benchmarking.evaluator import evaluator
from benchmarking.models.search_model import SearchModel
from benchmarking.schemas import schemas


@pytest.fixture
def mocked_search_model():
    mock_model = Mock(spec=SearchModel)
    
    mock_model.search.return_value = [
        schemas.Document(doc_id="doc1", content="Heap memory explained", course="Algorithms", lecture="Lecture 1"),
        schemas.Document(doc_id="doc2", content="What is stack memory", course="Algorithms", lecture="Lecture 1"),
        schemas.Document(doc_id="doc3", content="Heap vs stack differences", course="Algorithms", lecture="Lecture 1"),
    ]
    
    return mock_model


@pytest.fixture
def metric_list():
    return [
        precision.Precision(k=2),
        reciprocal_rank.ReciprocalRank(k=3)
    ]


@pytest.fixture
def sample_queries():
    return [schemas.Query(id="q1", question="heap vs stack")]


@pytest.fixture
def sample_ground_truth():
    gt_entry = schemas.GroundTruthEntry(
        query="heap vs stack",
        query_id="q1",
        relevance_scores=OrderedDict({
            "doc1": schemas.RelevanceScore.HIGHLY_RELEVANT,
            "doc3": schemas.RelevanceScore.MODERATELY_RELEVANT
        })
    )
    return schemas.GroundTruth(entries={"q1": gt_entry})

@pytest.fixture
def expected():
    return {
        "per_query": {
            "q1": {
                "Precision": 0.5,        # top-2: doc1 + doc2 -> only doc1 is relevant
                "ReciprocalRank": 1.0    # doc1 is at rank 1
            }
        },
        "mean": {
            "Precision": 0.5,
            "ReciprocalRank": 1.0
        }
    }

def test_evaluate(mocked_search_model, metric_list, sample_queries, sample_ground_truth, expected):
    ev = evaluator.Evaluator(metrics=metric_list)

    observed = ev.evaluate(
        model=mocked_search_model,
        queries=sample_queries,
        ground_truth=sample_ground_truth
    )
    assert observed == expected
