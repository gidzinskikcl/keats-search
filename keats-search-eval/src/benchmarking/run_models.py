import logging
from datetime import datetime
import os

from benchmarking.models import random_search
from benchmarking.models.ance import ance_engine
from benchmarking.models.splade import splade_engine
from benchmarking.models.bm25_ce import bm25_ce_engine
from benchmarking.models.dpr import dpr_search_engine
from benchmarking.models.colbert import colbert_engine
from benchmarking.models.lucene import bm25, tf_idf
from benchmarking.utils import loader, saver

import sys
import os
import contextlib


@contextlib.contextmanager
def suppress_output():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


DOC_PATH = "keats-search-eval/data/documents/final/documents.json"
GROUND_TRUTH = "keats-search-eval/data/queries/validated/keats-search_queries_with_content_24-06-2025.csv"
K = 10

# Create timestamped directory
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """
    This main is for running models and saving predictions only
    """
    OUTPUT_DIR = os.path.join(
        "keats-search-eval/data", "evaluation", "pre-annotated", TIMESTAMP
    )
    # Load data
    print("Loading queries and ground truth...")
    queries = loader.load_valid_queries_from_csv(path=GROUND_TRUTH)
    print("Done loading queries and ground truth.")

    print("\nInitializing models...\nNOTE: log messages may be printed by the models during initialization.")
    print("======================================================")
    print("======================================================")
    print("\n\n")

    # Define models
    models = [
        random_search.RandomSearchEngine(doc_path=DOC_PATH),
        tf_idf.TFIDFSearchEngine(doc_path=DOC_PATH, k=K),
        bm25.BM25SearchEngine(doc_path=DOC_PATH, k=K),
        splade_engine.SpladeSearchEngine(doc_path=DOC_PATH, k=K),
        dpr_search_engine.DPRSearchEngine(doc_path=DOC_PATH, k=K),
        ance_engine.AnceSearchEngine(doc_path=DOC_PATH, k=K),
        colbert_engine.ColBERTSearchEngine(doc_path=DOC_PATH, k=K),
        bm25_ce_engine.BM25CrossEncoderSearchEngine(k=K),
    ]
    print("\n\n")
    print("======================================================")
    print("======================================================")
    print("Models initialized")
    model_names = [model.__class__.__name__ for model in models]
    print(f"Initialized models: {', '.join(model_names)}")

    # Run evaluation for each model
    print(
        "Evaluation running...\nNOTE: log messages may be printed by the models during initialization."
    )
    print("\n\n")
    print("======================================================")
    print("======================================================")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for model in models:
        model_name = model.__class__.__name__
        print("Running model:")
        logger.info(f"{model_name}: ...")

        predictions = {}
        for query in queries:
            top_results = model.search(query=query)
            query_result = {"question": query.question, "results": top_results}
            predictions[query.id] = query_result

        output_path = os.path.join(OUTPUT_DIR, f"{model_name.lower()}_predictions.csv")
        saver.save_predictions(
            output_path=output_path, model_name=model_name, predictions=predictions
        )
        logger.info(f"{model_name}: DONE")
    print("======================================================")
    print("======================================================")
    print("\n\n")
    print("Evaluation completed. Predictions saved.")
    logger.info(f"Saved predictions in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
