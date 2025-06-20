import json
from benchmarking.schemas import schemas
from collections import OrderedDict

def load_queries(path: str) -> list[schemas.Query]:
    with open(path, "r") as f:
        data = json.load(f)
    return [schemas.Query(id=entry["id"], question=entry["question"]) for entry in data]

def load_ground_truth(path: str) -> schemas.GroundTruth:
    with open(path, "r") as f:
        raw = json.load(f)

    entries = {}
    for qid, entry in raw.items():
        scores = OrderedDict({
            doc_id: schemas.RelevanceScore[score_str]
            for doc_id, score_str in entry["relevance_scores"].items()
        })
        entries[qid] = schemas.GroundTruthEntry(
            query=entry["query"],
            query_id=entry["query_id"],
            relevance_scores=scores
        )

    return schemas.GroundTruth(entries=entries)
