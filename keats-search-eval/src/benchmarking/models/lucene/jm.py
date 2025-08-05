from datetime import timedelta
import subprocess
import json

from schemas import schemas
from benchmarking.models import search_model


class LMJelinekMercerSearchEngine(search_model.SearchModel):
    JAR_PATH = "search_engines/lucene-search/target/jm-search-jar-with-dependencies.jar"

    def __init__(self, doc_path: str, k: int, lambda_: float = 0.7):
        self.doc_path = doc_path
        self.k = k
        self.lambda_ = lambda_

    def _parse_timestamp(self, ts: str | None) -> timedelta | None:
        if ts is None:
            return None
        h, m, s = map(int, ts.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def search(self, query: schemas.Query) -> list[schemas.SearchResult]:
        proc = subprocess.run(
            [
                "java",
                "-jar",
                self.JAR_PATH,
                self.doc_path,
                query.question,
                str(self.k),
                str(self.lambda_),
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

            # Parse start and end timestamps (handle nulls)
            start = self._parse_timestamp(d.get("start"))
            end = self._parse_timestamp(d.get("end"))
            timestamp = schemas.Timestamp(start=start, end=end)

            if d["type"] == "SLIDE":
                doc_type = schemas.MaterialType.SLIDES
            elif d["type"] == "VIDEO_TRANSCRIPT":
                doc_type = schemas.MaterialType.TRANSCRIPT
            else:
                raise ValueError(f"Unknown document type: {d['type']}")

            doc = schemas.DocumentSchema(
                doc_id=d["documentId"],
                content=d["content"],
                course_name=d["courseName"],
                title=d["title"],
                timestamp=timestamp,
                pageNumber=d["slideNumber"],
                keywords=d["keywords"],
                doc_type=doc_type,
                speaker=d["speaker"],
            )
            results.append(schemas.SearchResult(document=doc, score=d.get("score")))
        return results
