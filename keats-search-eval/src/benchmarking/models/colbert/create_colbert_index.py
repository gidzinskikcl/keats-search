from colbert import Indexer
from colbert.infra import Run, RunConfig, ColBERTConfig


def main():
    collection_path = "keats-search-eval/src/benchmarking/models/colbert/collection.tsv"
    index_name = "maxlen512"
    checkpoint_path = "keats-search-eval/src/benchmarking/models/colbert/colbertv2.0"
    experiment_root = (
        "/Users/piotrgidzinski/KeatsSearch_workspace/keats-search/experiments_maxlen512"
    )
    nbits = 2

    with Run().context(RunConfig(nranks=1, experiment=index_name)):
        config = ColBERTConfig(
            doc_maxlen=512,
            nbits=nbits,
            root=experiment_root,
            overwrite="force_silent_overwrite",
        )
        indexer = Indexer(checkpoint=checkpoint_path, config=config)
        indexer.index(name=index_name, collection=collection_path)

    print("ColBERT index creation complete.")


if __name__ == "__main__":
    main()
