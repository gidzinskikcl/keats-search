
import logging
from datetime import datetime
import os

from benchmarking.metrics import precision, reciprocal_rank, ndcg
from benchmarking.models import random_search
from benchmarking.models.lucene import bm25, tf_idf, dirichlet, jm, boolean
from benchmarking.utils import loader, saver, wandb_logger
from evaluator import evaluator

BM25_JAR_PATH = "search_engines/lucene-search/target/keats-lucene-search-1.0-SNAPSHOT-jar-with-dependencies.jar"

DOC_PATH = "data/documents/2025-07-01_10-12-35/documents.json"
GROUND_TRUTH = "data/queries/validated/keats-search_queries_24-06-2025.csv"

# Create timestamped directory
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_DIR = os.path.join("data", "evaluation", "pre-annotated", TIMESTAMP)
# OUTPUT_DIR = os.path.join("data", "evaluation", "results", TIMESTAMP)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    # Load data
    logger.info("Loading queries and ground truth...")
    queries = loader.load_valid_queries_from_csv(path=GROUND_TRUTH)
    logger.info("Done loading queries and ground truth.")
    
    # Define models
    models = [
        random_search.RandomSearchEngine(doc_path=DOC_PATH),
        bm25.BM25SearchEngine(jar_path=BM25_JAR_PATH, doc_path=DOC_PATH),
        tf_idf.TFIDFSearchEngine(jar_path=BM25_JAR_PATH, doc_path=DOC_PATH),
        dirichlet.DirichletSearchEngine(jar_path=BM25_JAR_PATH, doc_path=DOC_PATH),
        jm.LMJelinekMercerSearchEngine(jar_path=BM25_JAR_PATH, doc_path=DOC_PATH),
        boolean.BooleanSearchEngine(jar_path=BM25_JAR_PATH, doc_path=DOC_PATH)
    ]
    model_names = [model.__class__.__name__ for model in models]
    logger.info(f"Initialized models: {', '.join(model_names)}")

    # Run evaluation for each model
    print("Evaluation running...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for model in models:
        model_name = model.__class__.__name__
        logger.info(f"Evaluating model: {model_name}")
        print(f"{model_name}")

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



# def main():
#     # Load data
#     logger.info("Loading queries and ground truth...")
#     queries = loader.load_valid_queries_from_csv(path=GROUND_TRUTH)
#     ground_truth = loader.load_ground_truth(path=GROUND_TRUTH)
#     logger.info("Done loading queries and ground truth.")
    
#     # Define models
#     models = [
#         random_search.RandomSearchEngine(doc_path=DOC_PATH),
#         # bm25.BM25SearchEngine(jar_path=BM25_JAR_PATH, doc_path=DOC_PATH),
#         # tf_idf.TFIDFSearchEngine(jar_path=BM25_JAR_PATH, doc_path=DOC_PATH),
#     ]
#     model_names = [model.__class__.__name__ for model in models]
#     logger.info(f"Initialized models: {', '.join(model_names)}")

#     # Define metrics
#     K = 10
#     metrics = [
#         precision.Precision(k=K),
#         reciprocal_rank.ReciprocalRank(k=K),
#         ndcg.NDCG(k=K),
#     ]
#     metric_names = [metric.__class__.__name__ for metric in metrics]
#     logger.info(f"Using metrics: {', '.join(metric_names)} (k={K})")

#     # Initialize evaluator
#     eval = evaluator.Evaluator(metrics)
#     wandb_log = wandb_logger.WandbLogger(project="keats-search", run_name="baseline-eval")

#     # Run evaluation for each model
#     print("Evaluation running...")
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     for model in models:
#         model_name = model.__class__.__name__
#         logger.info(f"Evaluating model: {model_name}")
#         print(f"{model_name}")
#         results = eval.evaluate(model=model, queries=queries, ground_truth=ground_truth)

#         for metric_name, score in results["mean"].items():
#             print(f"  {metric_name}: {score:.4f}")

#         # Log overall metrics
#         wandb_log.log_mean_metrics(model_name, results["mean"])
#         # Log per-query scores as a W&B table and charts
#         wandb_log.log_per_query_metrics(model_name, results["per_query"])

#         saver.save_evaluation_results(
#             model_name=model_name, 
#             mean_metrics=results["mean"], 
#             per_query_metrics=results["per_query"],
#             output_dir=OUTPUT_DIR
#         )


#     logger.info(f"Saved per-query metrics to {OUTPUT_DIR}")
#     logger.info("Evaluation complete.")


if __name__ == "__main__":
    main()
