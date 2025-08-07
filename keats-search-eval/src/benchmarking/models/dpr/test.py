import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from benchmarking.models.dpr import dpr_search_engine
from schemas import schemas


def test_engine():
    doc_path = "keats-search-eval/data/documents/final/documents.json"

    # For the first time (builds and saves index)
    # searcher = dpr_search_engine.DPRSearchEngine(
    #     doc_path=doc_path, k=10, force_reindex=True
    # )

    # Later (loads from disk)
    searcher = dpr_search_engine.DPRSearchEngine(doc_path=doc_path, k=10)

    question = "Machine Learning"
    query = schemas.Query(id=1, question=question)
    results = searcher.search(query=query)
    for idx, r in enumerate(results, start=1):
        print(f"{idx}: {r.document.doc_id} | {r.score}")


if __name__ == "__main__":
    test_engine()
