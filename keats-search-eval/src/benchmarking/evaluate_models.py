
import json
import logging
from datetime import datetime
import os

from benchmarking.metrics import scikit_metrics
from benchmarking.utils import loader, saver, wandb_logger

# Constants
PREDICTION_DIR = "keats-search-eval/data/evaluation/pre-annotated/2025-07-03_15-28-44" # contains all models
GROUND_TRUTH = "keats-search-eval/data/queries/validated/keats-search_queries_24-06-2025.csv"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_DIR = os.path.join("keats-search-eval/data", "evaluation", "gt-annotated", "results", TIMESTAMP)
DOC_PATH = "keats-search-eval/data/documents/2025-07-03_12-22-08/documents.json"
MODELS = [
    "RandomSearchEngine",
    "BM25SearchEngine", 
    "TFIDFSearchEngine", 
    "BooleanSearchEngine",
    "dirichletsearchengine_mu_500",
    "dirichletsearchengine_mu_1000",
    "dirichletsearchengine_mu_1500",
    "dirichletsearchengine_mu_2000",
    "lmjelinekmercersearchengine_lambda_0.1",
    "lmjelinekmercersearchengine_lambda_0.3",
    "lmjelinekmercersearchengine_lambda_0.5",
    "lmjelinekmercersearchengine_lambda_0.7",
    "lmjelinekmercersearchengine_lambda_0.9"
]
K = [1, 5, 10]



logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def main():
    # Load ground truth
    relevant_pairs = loader.load_ground_truth_pairs(csv_path=GROUND_TRUTH)
    logger.info("Loaded ground truth...")

    wandb_log = wandb_logger.WandbLogger(project="keats-search", run_name="baseline-eval")
    results_by_k = {}
    for k in K:
        logger.info(f"Running evaluation with k={k}")
        print(f"\n=== EVALUATION @k={k} ===")
        
        # Initialize metrics
        metrics = [
            scikit_metrics.PrecisionAtK(k=k),
            scikit_metrics.MRRAtK(k=k)
        ]
        print(f"Using metrics: {', '.join(m.name for m in metrics)}")


        # Evaluation
        for model_name in MODELS:
            logger.info(f"Evaluating model: {model_name}")
            print(f"{model_name}")

            model_predictions_path = os.path.join(PREDICTION_DIR, f"{model_name.lower()}_predictions.csv")
            predictions = loader.load_model_predictions(model_predictions_path)

            mean_scores = {metric.name: 0.0 for metric in metrics}
            per_query_metrics = {}

            for query_id, doc_list in predictions.items():
                per_query_scores = {}
                for metric in metrics:
                    score = metric.compute(query_id=query_id, retrieved_docs=doc_list, relevant_pairs=relevant_pairs)
                    per_query_scores[metric.name] = score
                    mean_scores[metric.name] += score
                per_query_metrics[query_id] = per_query_scores


            # Average
            total_queries = len(predictions)
            for name in mean_scores:
                mean_scores[name] /= total_queries

            if k not in results_by_k:
                results_by_k[k] = {}
            results_by_k[k][model_name] = mean_scores

            for name, score in mean_scores.items():
                print(f"  {name}: {score:.4f}")

            wandb_log.log_mean_metrics(f"{model_name}@k={k}", mean_scores)
            wandb_log.log_per_query_metrics(f"{model_name}@k={k}", per_query_metrics)

            model_output_dir = os.path.join(OUTPUT_DIR, f"k={k}")
            os.makedirs(model_output_dir, exist_ok=True)

            saver.save_evaluation_results(
                model_name=model_name, 
                mean_metrics=mean_scores, 
                per_query_metrics=per_query_metrics,
                output_dir=model_output_dir,
                k=k
            )
    combined_json_path = os.path.join(OUTPUT_DIR, f"mean_metrics_all_k.json")
    with open(combined_json_path, "w") as f:
        json.dump(results_by_k, f, indent=4)

    logger.info(f"Saved per-query metrics to {OUTPUT_DIR}")
    logger.info("Evaluation complete.")


if __name__ == "__main__":
    main()
