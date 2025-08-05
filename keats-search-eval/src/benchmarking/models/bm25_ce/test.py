import torch
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
from typing import List

from benchmarking.models.bm25_ce import bm25_ce_engine


# --- Mock schemas (normally you'd import these) ---
@dataclass
class DocumentSchema:
    doc_id: str
    content: str


@dataclass
class Query:
    query_id: str
    question: str


@dataclass
class SearchResult:
    document: DocumentSchema
    score: float


# --- Dummy SearchModel interface ---
class SearchModel:
    def search(self, query: Query) -> List[SearchResult]:
        raise NotImplementedError


# --- Test run ---
if __name__ == "__main__":
    doc_path = "keats-search-eval/data/documents/2025-07-05_16-26-20/documents.json"

    query = Query(query_id="q1", question="Machine Learning")

    search_engine = bm25_ce_engine.BM25CrossEncoderSearchEngine(k=10)

    results = search_engine.search(query)

    print(f"\nQuery: {query.question}")
    print("Top Results:")
    for idx, result in enumerate(results, start=1):
        print(f"{idx}: [{result.score:.4f}] {result.document.id}")
