import json

from benchmarking.utils import loader
from benchmarking.schemas import schemas

from collections import OrderedDict

def test_load_queries(tmp_path):
    data = [
        {"id": "q1", "question": "heap vs stack"},
        {"id": "q2", "question": "process vs thread"}
    ]
    file_path = tmp_path / "queries.json"
    with open(file_path, "w") as f:
        json.dump(data, f)

    observed = loader.load_queries(str(file_path))
    expected = [
        schemas.Query(id="q1", question="heap vs stack"),
        schemas.Query(id="q2", question="process vs thread"),
    ]

    assert observed == expected


def test_load_ground_truth(tmp_path):
    data = {
        "q1": {
            "query": "heap vs stack",
            "query_id": "q1",
            "relevance_scores": {
                "doc1": "HIGHLY_RELEVANT",
                "doc3": "MODERATELY_RELEVANT"
            }
        },
        "q2": {
            "query": "process vs thread",
            "query_id": "q2",
            "relevance_scores": {
                "doc2": "SLIGHTLY_RELEVANT",
                "doc4": "IRRELEVANT"
            }
        }
    }

    file_path = tmp_path / "ground_truth.json"
    with open(file_path, "w") as f:
        json.dump(data, f)

    observed = loader.load_ground_truth(str(file_path))

    expected = schemas.GroundTruth(entries={
        "q1": schemas.GroundTruthEntry(
            query="heap vs stack",
            query_id="q1",
            relevance_scores=OrderedDict({
                "doc1": schemas.RelevanceScore.HIGHLY_RELEVANT,
                "doc3": schemas.RelevanceScore.MODERATELY_RELEVANT
            })
        ),
        "q2": schemas.GroundTruthEntry(
            query="process vs thread",
            query_id="q2",
            relevance_scores=OrderedDict({
                "doc2": schemas.RelevanceScore.SLIGHTLY_RELEVANT,
                "doc4": schemas.RelevanceScore.IRRELEVANT
            })
        )
    })

    assert observed == expected
