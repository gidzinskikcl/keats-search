import os
import json
import numpy as np
import torch
import faiss
from datetime import timedelta
from tqdm import tqdm
from transformers import (
    DPRQuestionEncoder,
    DPRContextEncoder,
    DPRQuestionEncoderTokenizer,
    DPRContextEncoderTokenizer,
    AutoTokenizer,
)

from benchmarking.models import search_model
from schemas import schemas


class DPRSearchEngine(search_model.SearchModel):

    def __init__(
        self,
        doc_path: str,
        k: int,
        index_dir: str = "/app/keats-search-eval/src/benchmarking/models/dpr/dpr_index",
        force_reindex: bool = False,
    ):
        self.doc_path = doc_path
        self.k = k
        self.index_dir = index_dir
        self.force_reindex = force_reindex

        self._load_models()

        if force_reindex or not self._check_index_exists():
            print("DPR: Index does not exist or force reindexing is enabled.")
            self._index_documents()
        else:
            print("DPR: Index exists, loading...")
            self._load_documents_and_index()

    def _check_index_exists(self):
        return all(
            os.path.exists(os.path.join(self.index_dir, fname))
            for fname in [
                "faiss.index",
                "doc_map.json",
            ]
        )

    def _parse_timestamp(self, ts: str | None) -> timedelta | None:
        if ts is None:
            return None
        h, m, s = map(int, ts.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def _load_models(self):
        self.q_encoder = DPRQuestionEncoder.from_pretrained(
            "facebook/dpr-question_encoder-multiset-base"
        )
        self.c_encoder = DPRContextEncoder.from_pretrained(
            "facebook/dpr-ctx_encoder-multiset-base"
        )
        self.q_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(
            "facebook/dpr-question_encoder-multiset-base"
        )
        self.c_tokenizer = DPRContextEncoderTokenizer.from_pretrained(
            "facebook/dpr-ctx_encoder-multiset-base"
        )
        self.chunk_tokenizer = AutoTokenizer.from_pretrained(
            "facebook/dpr-ctx_encoder-multiset-base"
        )

    def _index_documents(self):
        os.makedirs(self.index_dir, exist_ok=True)

        with open(self.doc_path) as f:
            documents = json.load(f)

        self.doc_map = {doc["id"]: doc for doc in documents}
        texts = [doc["content"] for doc in documents]
        doc_ids = [doc["id"] for doc in documents]

        print("Encoding full documents (truncating to 512 tokens)...")
        embeddings = []
        batch_size = 16

        for i in tqdm(range(0, len(texts), batch_size)):
            batch_texts = texts[i : i + batch_size]
            inputs = self.c_tokenizer(
                batch_texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            )
            with torch.no_grad():
                embs = self.c_encoder(**inputs).pooler_output.detach().numpy()

            embeddings.extend(embs)

        embeddings = np.array(embeddings)
        self.passage_embeddings = embeddings

        print("Building FAISS index...")
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(self.passage_embeddings)

        print("Saving index and metadata...")
        faiss.write_index(self.index, os.path.join(self.index_dir, "faiss.index"))
        with open(os.path.join(self.index_dir, "doc_map.json"), "w") as f:
            json.dump(self.doc_map, f)

    def _load_documents_and_index(self):
        print("Loading saved index and metadata...")
        self.index = faiss.read_index(os.path.join(self.index_dir, "faiss.index"))
        with open(os.path.join(self.index_dir, "doc_map.json")) as f:
            self.doc_map = json.load(f)

    def search(self, query: schemas.Query) -> list[schemas.SearchResult]:
        inputs = self.q_tokenizer(
            query.question, return_tensors="pt", truncation=True, max_length=512
        )
        with torch.no_grad():
            q_emb = self.q_encoder(**inputs).pooler_output.detach().numpy()

        D, I = self.index.search(q_emb, self.k)

        results = []
        doc_ids = list(self.doc_map.keys())

        for score, idx in zip(D[0], I[0]):
            doc_id = doc_ids[idx]
            doc_meta = self.doc_map[doc_id]

            if doc_meta["doc_type"] == "pdf":
                doc_type = schemas.MaterialType.SLIDES
            elif doc_meta["doc_type"] == "mp4":
                doc_type = schemas.MaterialType.TRANSCRIPT
            else:
                raise ValueError(f"Unknown document type: {doc_meta['doc_type']}")

            doc = schemas.DocumentSchema(
                id=doc_meta["id"],
                doc_id=doc_meta["doc_id"],
                content=doc_meta["content"],
                course_id=doc_meta["course_id"],
                lecture_id=doc_meta["lecture_id"],
                doc_type=doc_type,
            )
            results.append(schemas.SearchResult(document=doc, score=float(score)))

        return results
