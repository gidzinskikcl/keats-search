import subprocess
import json
from datetime import timedelta
from typing import List

import config
import logger as api_logger
from core import schemas, engine


class BM25SearchEngine(engine.SearchEngine):
    """
    A search engine wrapper that delegates Lucene-based searching via subprocess.
    Assumes the index has already been created separately.
    """

    def __init__(self, index_dir: str = config.settings.INDEX_DIR):
        self.index_dir = index_dir
        self.logger = api_logger.get_logger(self.__class__.__name__)
        self.JAR_PATH = config.settings.LUCENE_JAR_PATH

    def _parse_timestamp(self, ts: str | None) -> timedelta | None:
        if ts is None:
            return None
        h, m, s = map(int, ts.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def _serialize_filters(self, filters: schemas.Filter) -> str:
        payload = {}

        print(filters)

        if filters.courses_ids:
            payload["courseId"] = filters.courses_ids
        if filters.lectures_ids:
            payload["lectureId"] = filters.lectures_ids
        if filters.doc_ids:
            payload["documentId"] = filters.doc_ids

        return json.dumps(payload)

    def search(
        self,
        query: schemas.Query,
        top_k: int = config.settings.TOP_K,
        filters: schemas.Filter = None,
    ) -> List[schemas.SearchResult]:
        serialized_filters = self._serialize_filters(filters)

        self.logger.info(
            f"Running search: '{query.question}' with filters: {serialized_filters}"
        )

        proc = subprocess.run(
            [
                "java",
                "-jar",
                self.JAR_PATH,
                "--mode",
                "search",
                self.index_dir,
                query.question,
                str(top_k),
                serialized_filters,
            ],
            capture_output=True,
            text=True,
        )

        if proc.returncode != 0:
            self.logger.error(f"Lucene search failed: {proc.stderr.strip()}")
            raise RuntimeError(f"Lucene search failed: {proc.stderr.strip()}")

        ranked = json.loads(proc.stdout)
        results = []

        for d in ranked:
            start = self._parse_timestamp(d.get("start"))
            end = self._parse_timestamp(d.get("end"))
            timestamp = schemas.Timestamp(start=start, end=end)

            doc_type = self._get_doc_type(d["type"])

            doc = schemas.DocumentSchema(
                id=d["iD"],
                doc_id=d["documentId"],
                content=d["content"],
                course_name=d["courseName"],
                lecture_title=d["lectureTitle"],
                lecture_id=d["lectureId"],
                course_id=d["courseId"],
                timestamp=timestamp,
                page_number=d["pageNumber"],
                doc_type=doc_type,
            )
            results.append(schemas.SearchResult(document=doc, score=d.get("score")))

        self.logger.info(f"Search returned {len(results)} results")
        return results

    def _get_doc_type(self, t: str) -> schemas.MaterialType:
        match t:
            case "SLIDE":
                return schemas.MaterialType.SLIDES
            case "VIDEO_TRANSCRIPT":
                return schemas.MaterialType.TRANSCRIPT
            case _:
                raise ValueError(f"Unknown document type: {t}")
