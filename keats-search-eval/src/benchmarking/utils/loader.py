import csv
import json
from schemas import schemas

from datetime import timedelta


def load_queries(path: str) -> list[schemas.Query]:
    with open(path, "r") as f:
        data = json.load(f)
    return [schemas.Query(id=entry["id"], question=entry["question"]) for entry in data]


def load_valid_queries_from_csv(path: str) -> list[schemas.Query]:
    queries = []
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["label"].strip().lower() == "valid":
                query_id = row["index"].strip()
                question = row["question"].strip()
                queries.append(schemas.Query(id=query_id, question=question))
    return queries


def load_ground_truth_pairs(csv_path: str) -> set[tuple[str, str]]:  # No test
    relevant_pairs = set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["label"].strip().lower() == "valid":
                qid = row["index"].strip()
                doc_id = row["doc_id"].strip()
                relevant_pairs.add((qid, doc_id))
    return relevant_pairs


class PredictedDocument:
    def __init__(self, doc_id):
        self.doc_id = doc_id


def load_model_predictions(
    csv_path: str,
) -> dict[str, list[PredictedDocument]]:  # No test
    predictions = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query_id = row["query_id"].strip()

            doc_id = row["id"].strip()
            doc = PredictedDocument(doc_id)

            if query_id not in predictions:
                predictions[query_id] = []
            predictions[query_id].append(doc)
    return predictions


def parse_timestamp(ts: str | None) -> timedelta | None:
    if ts is None:
        return None
    h, m, s = map(int, ts.split(":"))
    return timedelta(hours=h, minutes=m, seconds=s)


def load_documents_from_json(path: str) -> list[schemas.DocumentSchema]:
    with open(path, "r", encoding="utf-8") as f:
        raw_docs = json.load(f)

    documents = []
    for d in raw_docs:
        start = parse_timestamp(d.get("start"))
        end = parse_timestamp(d.get("end"))
        timestamp = schemas.Timestamp(start=start, end=end)

        doc_type_str = d.get("type", "").lower()
        if doc_type_str == "slide":
            doc_type = schemas.MaterialType.SLIDES
        elif doc_type_str == "video_transcript":
            doc_type = schemas.MaterialType.TRANSCRIPT
        else:
            raise ValueError(f"Unknown material type: {doc_type_str}")

        doc = schemas.DocumentSchema(
            doc_id=d["documentId"],
            content=d["content"],
            title=d["title"],
            timestamp=timestamp,
            pageNumber=d.get("slideNumber", -1),
            keywords=d.get("keywords", []),
            doc_type=doc_type,
            speaker=d.get("speaker", ""),
            course_name=d["courseName"],
        )
        documents.append(doc)

    return documents
