from benchmarking.models.splade import splade_engine


def main():
    print("🔧 SPLADE Indexer starting...")

    doc_path = "fdata/ground_truth/documents.json"
    index_dir = "keats-search-eval/src/benchmarking/models/splade/index_test"

    print(f"Document path: {doc_path}")
    print(f"Index will be saved to: {index_dir}")

    # Instantiate the SPLADE engine and trigger indexing
    engine = splade_engine.SpladeSearchEngine(
        doc_path=doc_path,
        k=10,
        index_dir=index_dir,
        force_reindex=True,
    )

    print("✅ SPLADE Indexing complete.")


if __name__ == "__main__":
    main()
