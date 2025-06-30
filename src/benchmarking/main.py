
from benchmarking.metrics import precision, reciprocal_rank, ndcg
from benchmarking.models import random_search
from benchmarking.models.lucene import bm25
from benchmarking.utils import loader, wandb_logger
from evaluator import evaluator


BM25_JAR_PATH = "search_engines/lucene-search/target/keats-lucene-search-1.0-SNAPSHOT-jar-with-dependencies.jar"

DOC_PATH = "data/testing/documents/document-test.json"

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    # Load data
    logger.info("Loading queries and ground truth...")
    queries = loader.load_queries(path="data/queries.json")
    ground_truth = loader.load_ground_truth("data/ground_truth.json")
    logger.info("Done loading queries and ground truth.")
    
    # Define models
    models = [
        random_search.RandomSearchEngine(doc_path=DOC_PATH),
        bm25.BM25SearchEngine(jar_path=BM25_JAR_PATH, doc_path=DOC_PATH),
        # TFIDFModel(),
        # EmbeddingModel()
    ]
    model_names = [model.__class__.__name__ for model in models]
    logger.info(f"Initialized models: {', '.join(model_names)}")

    # Define metrics
    K = 5
    metrics = [
        precision.Precision(k=K),
        reciprocal_rank.ReciprocalRank(k=K),
        ndcg.NDCG(k=K),
    ]
    metric_names = [metric.__class__.__name__ for metric in metrics]
    logger.info(f"Using metrics: {', '.join(metric_names)} (k={K})")

    # Initialize evaluator
    eval = evaluator.Evaluator(metrics)
    wandb_log = wandb_logger.WandbLogger(project="keats-search", run_name="baseline-eval")

    # Run evaluation for each model
    print("Evaluation running...")
    for model in models:
        model_name = model.__class__.__name__
        logger.info(f"Evaluating model: {model_name}")
        print(f"{model_name}")
        results = eval.evaluate(model=model, queries=queries, ground_truth=ground_truth)

        for metric_name, score in results["mean"].items():
            print(f"  {metric_name}: {score:.4f}")

        # Log overall metrics
        wandb_log.log_mean_metrics(model_name, results["mean"])
        # Log per-query scores as a W&B table and charts
        wandb_log.log_per_query_metrics(model_name, results["per_query"])

    logger.info("Evaluation complete.")


if __name__ == "__main__":
    main()
