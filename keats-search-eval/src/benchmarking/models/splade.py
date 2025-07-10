import torch
from transformers import AutoTokenizer
from splade.models import transformer_rep
from schemas import schemas
from benchmarking.models import search_model
from tqdm import tqdm
import time


class SpladeSearchEngine(search_model.SearchModel):
    def __init__(
        self,
        documents: list[schemas.DocumentSchema],
        k: int,
        model_name: str = "naver/splade-cocondenser-ensembledistil",
    ):
        self.documents = documents
        self.k = k
        self.model_name = model_name

        print("Loading SPLADE model...")
        start = time.time()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = transformer_rep.Splade(self.model_name, agg="max", fp16=False)
        self.model.eval()
        print(f"Model loaded in {time.time() - start:.2f}s")

        self.doc_ids = [doc.doc_id for doc in self.documents]
        self.doc_texts = [doc.content for doc in self.documents]
        self.doc_vecs = self._encode_documents()

    def _encode_documents(self):
        encoded = []
        for text in tqdm(self.doc_texts, desc="Encoding documents"):
            tokens = self.tokenizer(
                text, return_tensors="pt", truncation=True, padding=True
            )
            with torch.no_grad():
                rep = self.model(d_kwargs=tokens)["d_rep"]
            encoded.append(rep.squeeze())
        return encoded

    def _encode_query(self, text: str):
        tokens = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        with torch.no_grad():
            rep = self.model(q_kwargs=tokens)["q_rep"]
        return rep.squeeze()

    def _score(self, query_vec, doc_vecs):
        return [
            (doc_id, float((query_vec * vec).sum()))
            for doc_id, vec in zip(self.doc_ids, doc_vecs)
        ]

    def search(self, query: schemas.Query) -> list[schemas.SearchResult]:
        query_vec = self._encode_query(query.question)
        scored = self._score(query_vec, self.doc_vecs)
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in ranked[:self.k]:
            doc = next(d for d in self.documents if d.doc_id == doc_id)
            results.append(schemas.SearchResult(document=doc, score=score))
        return results
