import json
import random
from datetime import timedelta
from schemas import schemas
from benchmarking.models import search_model


class RandomSearchEngine(search_model.SearchModel):
    def __init__(self, doc_path: str):
        self.doc_path = doc_path
        self.documents = self._load_documents()

    def _load_documents(self) -> list[schemas.DocumentSchema]:
        with open(self.doc_path) as f:
            raw_docs = json.load(f)

        return [
            schemas.DocumentSchema(
                id=doc["id"],
                doc_id=doc["doc_id"],
                content=doc["content"],
                course_id=doc["course_id"],
                lecture_id=doc["lecture_id"],
                doc_type=self._get_type(doc["doc_type"]),
            )
            for doc in raw_docs
        ]

    def search(self, query: schemas.Query) -> list[schemas.SearchResult]:
        sampled_docs = random.sample(self.documents, k=min(10, len(self.documents)))

        return [
            schemas.SearchResult(
                document=doc,
                score=random.uniform(0.0, 1.0),  # Random score between 0.0 and 1.0
            )
            for doc in sampled_docs
        ]

    def _get_type(self, value: str) -> str:
        if value == "pdf":
            return schemas.MaterialType.SLIDES
        elif value == "mp4":
            return schemas.MaterialType.TRANSCRIPT
        else:
            raise ValueError(f"Unknown document type: {value}")


def _parse_time(hhmmss: str) -> timedelta:
    try:
        h, m, s = map(int, hhmmss.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)
    except Exception:
        return timedelta()  # fallback to 0
