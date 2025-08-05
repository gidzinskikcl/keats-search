from datetime import timedelta
import subprocess
import json

from schemas import schemas
from benchmarking.models import search_model


class BM25SearchEngine(search_model.SearchModel):
    JAR_PATH = "keats-search-api/bin/bm25-search-api-jar-with-dependencies.jar"

    def __init__(self, doc_path: str, k: int):
        self.doc_path = doc_path
        self.k = k

    def _parse_timestamp(self, ts: str | None) -> timedelta | None:
        if ts is None:
            return None
        h, m, s = map(int, ts.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def search(self, query: schemas.Query) -> list[schemas.SearchResult]:
        filters_json = "{}"
        proc = subprocess.run(
            [
                "java",
                "-jar",
                self.JAR_PATH,
                "--mode",
                "search",
                "keats-search-api/data/index",
                query.question,
                str(self.k),
                filters_json,
            ],
            capture_output=True,
            text=True,
        )

        if proc.returncode != 0:
            print("Java STDERR:", proc.stderr)
            raise RuntimeError(f"Lucene search failed: {proc.stderr.strip()}")

        ranked = json.loads(proc.stdout)
        results = []

        for d in ranked:

            if d["type"] == "SLIDE":
                doc_type = schemas.MaterialType.SLIDES
            elif d["type"] == "VIDEO_TRANSCRIPT":
                doc_type = schemas.MaterialType.TRANSCRIPT
            else:
                raise ValueError(f"Unknown document type: {d['type']}")

            doc = schemas.DocumentSchema(
                id=d["iD"],
                doc_id=d["documentId"],
                content=d["content"],
                course_id=d["courseId"],
                lecture_id=d["lectureId"],
                doc_type=doc_type,
            )
            results.append(schemas.SearchResult(document=doc, score=d.get("score")))
        return results
