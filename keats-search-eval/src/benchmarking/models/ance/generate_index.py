from benchmarking.models.ance import ance_engine


def main():
    print("ANCE Indexer starting...")

    doc_path = "fdata/ground_truth/documents.json"
    index_dir = "keats-search-eval/src/benchmarking/models/ance/index_test"

    print(f"Document path: {doc_path}")
    print(f"Index will be saved to: {index_dir}")

    # Instantiates the ANCE engine and builds index
    engine = ance_engine.AnceSearchEngine(
        doc_path=doc_path,
        k=10,
        index_dir=index_dir,
        force_reindex=True,
    )

    print("✅ ANCE Indexing complete.")


if __name__ == "__main__":
    main()
