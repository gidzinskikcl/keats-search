from colbert import Indexer
from colbert.infra import Run, RunConfig, ColBERTConfig


def main():
    collection_path = "keats-search-eval/src/benchmarking/models/colbert/collection.tsv"
    # collection_path = "keats-search-eval/src/benchmarking/models/colbert/collection2.tsv"

    index_name = "keats_indexes"
    checkpoint_path = "colbert-ir/colbertv2.0"
    experiment_root = "keats-search-eval/src/benchmarking/models/colbert"

    print("Starting ColBERT indexing...")

    with Run().context(RunConfig(nranks=1, experiment="default", root=experiment_root)):
        config = ColBERTConfig(
            doc_maxlen=512,
            nbits=2,
            root=experiment_root,
            experiment="default",
            overwrite="force_silent_overwrite",
        )
        indexer = Indexer(checkpoint=checkpoint_path, config=config)
        indexer.index(name=index_name, collection=collection_path)

    print("✅ ColBERT indexing complete.")


if __name__ == "__main__":
    main()
