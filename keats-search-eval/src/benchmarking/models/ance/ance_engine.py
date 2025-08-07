import os
import time
import json
import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from schemas import schemas
from benchmarking.models import search_model


class AnceSearchEngine(search_model.SearchModel):

    def __init__(
        self,
        doc_path: str,
        k: int,
        model_name: str = "sentence-transformers/msmarco-roberta-base-ance-firstp",
        index_dir: str = "/app/keats-search-eval/src/benchmarking/models/ance/ance_index",
        force_reindex: bool = False,
    ):
        self.doc_path = doc_path
        self.k = k
        self.model_name = model_name
        self.index_dir = index_dir
        self.force_reindex = force_reindex

        print("Loading ANCE model...")
        start = time.time()
        self.model = SentenceTransformer(self.model_name)
        print(f"Model loaded in {time.time() - start:.2f}s")

        if force_reindex or not self._check_index_exists():
            print("ANCE: Index does not exist or force reindexing is enabled.")
            self._index_documents()
        else:
            print("ANCE: index exists...")
            self._load_index()

    def _check_index_exists(self):
        return os.path.exists(
            os.path.join(self.index_dir, "doc_vecs.pt")
        ) and os.path.exists(os.path.join(self.index_dir, "documents.json"))

    def _load_documents(self):
        with open(self.doc_path) as f:
            return json.load(f)

    def _index_documents(self):
        os.makedirs(self.index_dir, exist_ok=True)
        print("Loading and encoding documents...")
        docs_raw = self._load_documents()
        self.documents = docs_raw
        self.ids = [doc["id"] for doc in docs_raw]
        self.doc_texts = [doc["content"] for doc in docs_raw]

        # Use SentenceTransformer's efficient batching
        self.doc_vecs = self.model.encode(
            self.doc_texts, convert_to_tensor=True, show_progress_bar=True
        )
        torch.save(self.doc_vecs, os.path.join(self.index_dir, "doc_vecs.pt"))
        with open(os.path.join(self.index_dir, "documents.json"), "w") as f:
            json.dump(docs_raw, f)

    def _load_index(self):
        print("Loading index from disk...")
        self.doc_vecs = torch.load(
            os.path.join(self.index_dir, "doc_vecs.pt"),
            map_location=torch.device("cpu"),
        )
        with open(os.path.join(self.index_dir, "documents.json")) as f:
            self.documents = json.load(f)
        self.ids = [doc["id"] for doc in self.documents]

    def _encode_query(self, text: str):
        return self.model.encode(text, convert_to_tensor=True)

    def _score(self, query_vec, doc_vecs):
        return [
            (id, float(torch.dot(query_vec, vec)))
            for id, vec in zip(self.ids, doc_vecs)
        ]

    def search(self, query: schemas.Query) -> list[schemas.SearchResult]:
        query_vec = self._encode_query(query.question)
        scored = self._score(query_vec, self.doc_vecs)
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)

        results = []
        doc_map = {doc["id"]: doc for doc in self.documents}
        for id, score in ranked[: self.k]:
            doc = doc_map[id]
            doc_type_map = {
                "pdf": schemas.MaterialType.SLIDES,
                "mp4": schemas.MaterialType.TRANSCRIPT,
            }

            doc_schema = schemas.DocumentSchema(
                id=doc["id"],
                doc_id=doc["doc_id"],
                content=doc["content"],
                course_id=doc["course_id"],
                lecture_id=doc["lecture_id"],
                doc_type=doc_type_map[doc["doc_type"]],
            )
            results.append(schemas.SearchResult(document=doc_schema, score=score))
        return results
