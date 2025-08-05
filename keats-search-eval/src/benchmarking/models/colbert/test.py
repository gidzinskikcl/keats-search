from dataclasses import dataclass

from benchmarking.models.colbert import colbert_engine


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
    def search(self, query: Query) -> list[SearchResult]:
        raise NotImplementedError


# --- Test run ---
if __name__ == "__main__":
    doc_path = "keats-search-eval/data/documents/final/documents.json"
    # doc_path = "keats-search-eval/data/documents/final/sample_doc.json"

    query = Query(query_id="q1", question="Machine Learning")

    colbert = colbert_engine.ColBERTSearchEngine(doc_path=doc_path, k=10)

    results = colbert.search(query)

    print(f"\nQuery: {query.question}")
    print("Top Results:")
    for idx, result in enumerate(results, start=1):
        print(f"{idx}: [{result.score:.4f}] {result.document.id}")
