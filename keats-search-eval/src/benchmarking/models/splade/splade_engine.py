import os
import time
import json
import torch
from tqdm import tqdm
from transformers import AutoTokenizer
from splade.models import transformer_rep

from schemas import schemas
from benchmarking.models import search_model


class SpladeSearchEngine(search_model.SearchModel):

    def __init__(
        self,
        doc_path: str,
        k: int,
        model_name: str = "naver/splade-cocondenser-ensembledistil",
        index_dir: str = "keats-search-eval/src/benchmarking/models/splade/splade_index",
        force_reindex: bool = False,
    ):
        self.doc_path = doc_path
        self.k = k
        self.model_name = model_name
        self.index_dir = index_dir
        self.force_reindex = force_reindex

        print("Loading SPLADE model...")
        start = time.time()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = transformer_rep.Splade(self.model_name, agg="max", fp16=False)
        self.model.eval()
        print(f"Model loaded in {time.time() - start:.2f}s")

        if force_reindex or not self._check_index_exists():
            self._index_documents()
        else:
            self._load_index()

    def _check_index_exists(self):
        return os.path.exists(
            os.path.join(self.index_dir, "doc_vecs.pt")
        ) and os.path.exists(os.path.join(self.index_dir, "documents.json"))

    def _load_documents(self):
        with open(self.doc_path) as f:
            docs_raw = json.load(f)
        return docs_raw

    def _index_documents(self):
        os.makedirs(self.index_dir, exist_ok=True)

        print("Loading and encoding documents...")
        docs_raw = self._load_documents()
        self.documents = docs_raw  # Keep raw for now
        self.ids = [doc["id"] for doc in docs_raw]
        self.doc_texts = [doc["content"] for doc in docs_raw]
        truncated_count = 0

        self.doc_vecs = []
        for text in tqdm(self.doc_texts, desc="Encoding documents"):
            tokens = self.tokenizer(
                text, return_tensors="pt", truncation=True, padding=True
            )
            input_ids = tokens["input_ids"]
            if input_ids.shape[1] == self.tokenizer.model_max_length:
                truncated_count += 1
            with torch.no_grad():
                rep = self.model(d_kwargs=tokens)["d_rep"]
            self.doc_vecs.append(rep.squeeze())

        # Save vectors and docs
        torch.save(self.doc_vecs, os.path.join(self.index_dir, "doc_vecs.pt"))
        with open(os.path.join(self.index_dir, "documents.json"), "w") as f:
            json.dump(docs_raw, f)

    def _load_index(self):
        print("Loading index from disk...")
        self.doc_vecs = torch.load(os.path.join(self.index_dir, "doc_vecs.pt"))
        with open(os.path.join(self.index_dir, "documents.json")) as f:
            docs_raw = json.load(f)
        self.documents = docs_raw  # just keep raw dicts, don't instantiate schemas here
        self.ids = [doc["id"] for doc in self.documents]

    def _encode_query(self, text: str):
        tokens = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        with torch.no_grad():
            rep = self.model(q_kwargs=tokens)["q_rep"]
        return rep.squeeze()

    def _score(self, query_vec, doc_vecs):
        return [
            (id, float((query_vec * vec).sum())) for id, vec in zip(self.ids, doc_vecs)
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
