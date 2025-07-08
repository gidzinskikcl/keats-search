
import logging
from datetime import datetime
import os

from benchmarking.models import random_search
from benchmarking.models.lucene import bm25, tf_idf, dirichlet, jm, boolean
from benchmarking.utils import loader, saver

# DOC_PATH = "keats-search-eval/data/documents/2025-07-03_12-22-08/documents.json" # with UA subtitles
DOC_PATH = "keats-search-eval/data/documents/2025-07-05_16-26-20/documents.json" # without UA subtitles

# GROUND_TRUTH = "keats-search-eval/data/queries/validated/keats-search_queries_24-06-2025.csv" # not updated
GROUND_TRUTH = "keats-search-eval/data/queries/validated/keats-search_queries_with_content_24-06-2025.csv"  # updated
K=10

# Create timestamped directory
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    """
    This main is for running models and saving predictions only
    """
    OUTPUT_DIR = os.path.join("keats-search-eval/data", "evaluation", "pre-annotated", TIMESTAMP)
    # Load data
    print("Loading queries and ground truth...")
    queries = loader.load_valid_queries_from_csv(path=GROUND_TRUTH)
    print("Done loading queries and ground truth.")
    
    # Define models
    models = [
        random_search.RandomSearchEngine(doc_path=DOC_PATH),
        bm25.BM25SearchEngine(doc_path=DOC_PATH, k=K),
        tf_idf.TFIDFSearchEngine(doc_path=DOC_PATH, k=K),
        boolean.BooleanSearchEngine(doc_path=DOC_PATH, k=K),
        dirichlet.DirichletSearchEngine(doc_path=DOC_PATH, k=K, mu_=500),
        dirichlet.DirichletSearchEngine(doc_path=DOC_PATH, k=K, mu_=1000),
        dirichlet.DirichletSearchEngine(doc_path=DOC_PATH, k=K, mu_=1500),
        dirichlet.DirichletSearchEngine(doc_path=DOC_PATH, k=K, mu_=2000),
        jm.LMJelinekMercerSearchEngine(doc_path=DOC_PATH, k=K, lambda_=0.1),
        jm.LMJelinekMercerSearchEngine(doc_path=DOC_PATH, k=K, lambda_=0.3),
        jm.LMJelinekMercerSearchEngine(doc_path=DOC_PATH, k=K, lambda_=0.5),
        jm.LMJelinekMercerSearchEngine(doc_path=DOC_PATH, k=K, lambda_=0.7),
        jm.LMJelinekMercerSearchEngine(doc_path=DOC_PATH, k=K, lambda_=0.9),
    ]
    model_names = [model.__class__.__name__ for model in models]
    print(f"Initialized models: {', '.join(model_names)}")

    # Run evaluation for each model
    print("Evaluation running...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for model in models:
        if isinstance(model, dirichlet.DirichletSearchEngine):
            model_name = f"DirichletSearchEngine_mu_{model.mu_}"
        elif isinstance(model, jm.LMJelinekMercerSearchEngine):
            model_name = f"LMJelinekMercerSearchEngine_lambda_{model.lambda_}"
        else:
            model_name = model.__class__.__name__
        print("Evaluating model:")
        logger.info(f"{model_name}: ...")

        predictions = {}
        for query in queries:
            top_results = model.search(query=query)
            query_result = {
                "question": query.question,
                "results": top_results
            }
            predictions[query.id] = query_result

        output_path = os.path.join(OUTPUT_DIR, f"{model_name.lower()}_predictions.csv")
        saver.save_predictions(output_path=output_path, model_name=model_name, predictions=predictions)
        logger.info(f"{model_name}: DONE")
    logger.info(f"Saved predictions in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
