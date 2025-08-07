import os
from benchmarking.models.dpr import dpr_search_engine


def main():
    print("DPR Indexer starting...")

    doc_path = "fdata/ground_truth/documents.json"
    index_dir = "keats-search-eval/src/benchmarking/models/dpr/index_test"

    print(f"Document path: {doc_path}")
    print(f"Index will be saved to: {index_dir}")

    # Instantiate engine with force_reindex=True
    engine = dpr_search_engine.DPRSearchEngine(
        doc_path=doc_path,
        k=10,
        index_dir=index_dir,
        force_reindex=True,
    )

    print("✅ DPR Indexing complete.")


if __name__ == "__main__":
    main()
