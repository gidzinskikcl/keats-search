import logging
import os

from benchmarking.models import random_search
from benchmarking.models.ance import ance_engine
from benchmarking.models.splade import splade_engine
from benchmarking.models.bm25_ce import bm25_ce_engine
from benchmarking.models.dpr import dpr_search_engine
from benchmarking.models.colbert import colbert_engine
from benchmarking.models.lucene import bm25, tf_idf
from benchmarking.utils import loader, saver

# === CONFIGURATION ===
DOC_PATH = "fdata/ground_truth/documents.json"
GROUND_TRUTH = "fdata/ground_truth/queries.csv"
OUTPUT_DIR = "fdata/workspace/models_predictions"
K = 10

# === LOGGING SETUP ===
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

USE_TEST_INDEX = True  # or from env/CLI

BASE_DIR = "/app/keats-search-eval/src/benchmarking/models"


def index_path(model: str, name: str):
    subdir = "index_test" if USE_TEST_INDEX else name
    return f"{BASE_DIR}/{model}/{subdir}"


def main():
    print("WELCOME TO KEATS SEARCH BENCHMARKING")
    print("\nLoading queries...")
    queries = loader.load_valid_queries_from_csv(path=GROUND_TRUTH)
    print(f"Loaded {len(queries)} queries.\n")

    print("Initializing models...\n")
    models = [
        random_search.RandomSearchEngine(doc_path=DOC_PATH),
        tf_idf.TFIDFSearchEngine(
            doc_path=DOC_PATH, k=K, index_dir=index_path("lucene", "index")
        ),
        bm25.BM25SearchEngine(
            doc_path=DOC_PATH, k=K, index_dir=index_path("lucene", "index")
        ),
        splade_engine.SpladeSearchEngine(
            doc_path=DOC_PATH, k=K, index_dir=index_path("splade", "splade_index")
        ),
        dpr_search_engine.DPRSearchEngine(
            doc_path=DOC_PATH, k=K, index_dir=index_path("dpr", "dpr_index")
        ),
        ance_engine.AnceSearchEngine(
            doc_path=DOC_PATH, k=K, index_dir=index_path("ance", "ance_index")
        ),
        colbert_engine.ColBERTSearchEngine(doc_path=DOC_PATH, k=K),  # unchanged
        bm25_ce_engine.BM25CrossEncoderSearchEngine(
            k=K, index_dir=index_path("lucene", "index")
        ),
    ]

    print("Models initialized:", [model.__class__.__name__ for model in models])

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\nRunning predictions for all models...\n")
    for model in models:
        model_name = model.__class__.__name__
        logger.info(f"{model_name}: running search...")

        predictions = {}
        for query in queries:
            top_results = model.search(query=query)
            predictions[query.id] = {
                "question": query.question,
                "results": top_results,
            }

        output_path = os.path.join(OUTPUT_DIR, f"{model_name.lower()}_predictions.csv")
        saver.save_predictions(
            output_path=output_path, model_name=model_name, predictions=predictions
        )
        logger.info(f"{model_name}: saved to {output_path}")

    print("\n✅ Benchmarking complete. Results saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
