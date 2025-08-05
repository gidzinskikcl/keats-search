from benchmarking.models import search_model
from schemas import schemas
from datetime import timedelta
from sentence_transformers import CrossEncoder
import subprocess
import json
from transformers import AutoTokenizer


class BM25CrossEncoderSearchEngine(search_model.SearchModel):
    JAR_PATH = "keats-search-api/bin/bm25-search-api-jar-with-dependencies.jar"

    def __init__(
        self,
        k: int,
        rerank_k: int = 100,
        ce_model_name: str = "cross-encoder/ms-marco-MiniLM-L6-v2",
        max_tokens: int = 512,
        stride: int = 50,
    ):
        self.k = k
        self.rerank_k = rerank_k
        self.ce_model = CrossEncoder(ce_model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(ce_model_name)
        self.max_tokens = max_tokens
        self.stride = stride

    def _parse_timestamp(self, ts: str | None) -> timedelta | None:
        if ts is None:
            return None
        h, m, s = map(int, ts.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def _to_doc_schema(self, d: dict) -> schemas.DocumentSchema:

        if d["type"] == "SLIDE":
            doc_type = schemas.MaterialType.SLIDES
        elif d["type"] == "VIDEO_TRANSCRIPT":
            doc_type = schemas.MaterialType.TRANSCRIPT
        else:
            raise ValueError(f"Unknown document type: {d['type']}")

        return schemas.DocumentSchema(
            id=d["iD"],
            doc_id=d["documentId"],
            content=d["content"],
            course_id=d["courseId"],
            lecture_id=d["lectureId"],
            doc_type=doc_type,
        )

    def _chunk_document(self, content: str) -> list[str]:
        tokens = self.tokenizer.tokenize(content)
        chunks = []

        for i in range(0, len(tokens), self.max_tokens - self.stride):
            chunk_tokens = tokens[i : i + self.max_tokens]
            chunk_text = self.tokenizer.convert_tokens_to_string(chunk_tokens)
            chunks.append(chunk_text)
            if i + self.max_tokens >= len(tokens):
                break

        return chunks

    def search(self, query: schemas.Query) -> list[schemas.SearchResult]:
        # If filters are optional, pass empty string as JSON
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
                str(self.rerank_k),
                filters_json,
            ],
            capture_output=True,
            text=True,
        )

        if proc.returncode != 0:
            print("Java STDERR:", proc.stderr)
            raise RuntimeError(f"Lucene search failed: {proc.stderr.strip()}")

        initial_results = json.loads(proc.stdout)

        # Step 2: Prepare query-document pairs for CE
        # pairs = [(query.question, d["content"]) for d in initial_results]
        # Chunk each document and track which doc each chunk came from
        chunk_pairs = []
        chunk_doc_refs = []

        for doc in initial_results:
            chunks = self._chunk_document(doc["content"])
            for chunk in chunks:
                chunk_pairs.append((query.question, chunk))
                chunk_doc_refs.append(doc)

        # Step 3: Get CE scores
        ce_scores = self.ce_model.predict(chunk_pairs, show_progress_bar=True)

        # Step 4: Rerank based on CE scores
        scored = list(zip(initial_results, ce_scores))
        scored.sort(key=lambda x: x[1], reverse=True)  # sort by CE score

        # Step 5: Return top-k
        top_k = scored[: self.k]
        results = []

        for raw_doc, score in top_k:
            doc_schema = self._to_doc_schema(raw_doc)
            results.append(schemas.SearchResult(document=doc_schema, score=score))

        return results
