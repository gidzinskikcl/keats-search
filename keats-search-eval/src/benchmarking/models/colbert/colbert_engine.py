import json
from datetime import timedelta
from colbert import Searcher, Indexer
from colbert.data import Collection
from colbert.infra import Run, RunConfig, ColBERTConfig

from schemas import schemas
from benchmarking.models import search_model

from typing import Optional


class ColBERTSearchEngine(search_model.SearchModel):

    def __init__(self, doc_path: str, k: int):
        self.k = k

        self.searcher = Searcher(
            index="/Users/piotrgidzinski/KeatsSearch_workspace/keats-search/keats-search-eval/src/benchmarking/models/colbert/experiments_maxlen512/maxlen512/keats_indexes/maxlen512",
            checkpoint="/Users/piotrgidzinski/KeatsSearch_workspace/keats-search/keats-search-eval/src/benchmarking/models/colbert/colbertv2.0",
        )
        self.searcher.collection = Collection(
            "keats-search-eval/src/benchmarking/models/colbert/collection.tsv"
        )

        # Load documents.json into a list
        with open(doc_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        with open(
            "keats-search-eval/src/benchmarking/models/colbert/pid2docid.json",
            "r",
            encoding="utf-8",
        ) as f:
            self.pid2docid = {int(k): v for k, v in json.load(f).items()}

    def _parse_timestamp(self, ts: str | None) -> timedelta | None:
        if ts is None:
            return None
        h, m, s = map(int, ts.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def search(
        self, query: schemas.Query, candidate_doc_ids: Optional[list[str]] = None
    ) -> list[schemas.SearchResult]:
        ranked = self.searcher.search(
            query.question, k=10 * self.k
        )  # Retrieve more chunks to ensure coverage
        docid_to_best_result = {}

        candidate_set = set(candidate_doc_ids) if candidate_doc_ids else None

        for passage_id, rank, score in zip(*ranked):
            doc_index = self.pid2docid.get(passage_id)
            if doc_index is None or doc_index >= len(self.documents):
                print(
                    f"[Warning] Invalid passage_id={passage_id} maps to unknown doc_index={doc_index}"
                )
                continue

            doc_json = self.documents[doc_index]
            doc_id = doc_json["doc_id"]

            # Skip documents not in candidate set (if provided)
            if candidate_set and doc_id not in candidate_set:
                continue

            # Keep only the best-scoring passage per document
            if (
                doc_id not in docid_to_best_result
                or docid_to_best_result[doc_id].score < score
            ):
                doc_type_str = doc_json["doc_type"]
                if doc_type_str == "pdf":
                    doc_type = schemas.MaterialType.SLIDES
                elif doc_type_str == "mp4":
                    doc_type = schemas.MaterialType.TRANSCRIPT
                else:
                    raise ValueError(f"Unknown document type: {doc_type_str}")

                doc = schemas.DocumentSchema(
                    id=doc_json["id"],
                    doc_id=doc_json["doc_id"],
                    content=doc_json["content"],
                    course_id=doc_json["course_id"],
                    lecture_id=doc_json["lecture_id"],
                    doc_type=doc_type,
                )
                docid_to_best_result[doc_id] = schemas.SearchResult(
                    document=doc, score=score
                )

        top_results = sorted(
            docid_to_best_result.values(), key=lambda r: r.score, reverse=True
        )
        return top_results[: self.k]
