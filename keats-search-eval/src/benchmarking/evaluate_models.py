import json
import csv
from datetime import datetime
import os

from benchmarking.metrics import scikit_metrics
from benchmarking.utils import loader, saver

GROUND_TRUTH = "keats-search-eval/data/queries/validated/keats-search_queries_with_content_21-07-2025.csv"

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_DIR = os.path.join(
    "keats-search-eval/data", "evaluation", "gt-annotated", "results", TIMESTAMP
)
DOC_PATH = "keats-search-eval/data/documents/2025-07-05_16-26-20/documents.json"

MODELS = {
    "RandomSearchEngine": "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_13-47-43/randomsearchengine_predictions.csv",
    "BM25CrossEncoderSearchEngine": "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_13-47-43/bm25crossencodersearchengine_predictions.csv",
    "SpladeSearchEngine": "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_18-13-02/spladesearchengine_predictions.csv",
    "ColBERTSearchEngine": "keats-search-eval/data/evaluation/pre-annotated/2025-07-22_11-42-22/colbertsearchengine_predictions.csv",
    "BM25SearchEngine": "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_13-47-43/bm25searchengine_predictions.csv",
    "TFIDFSearchEngine": "keats-search-eval/data/evaluation/pre-annotated/2025-07-22_03-03-14/tfidfsearchengine_predictions.csv",
    "ANCESearchEngine": "keats-search-eval/data/evaluation/pre-annotated/2025-08-01_22-33-19/ancesearchengine_predictions.csv",
    "DPRSearchEngine": "keats-search-eval/data/evaluation/pre-annotated/2025-08-02_14-38-09/dprsearchengine_predictions.csv",
}


K = [1, 5, 10]


def load_relevance_dict(csv_path: str) -> dict[str, dict[str, int]]:
    relevance_dict = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["label"].strip().lower() == "valid":
                query_id = int(row["index"].strip())
                doc_id = row["doc_id"].strip()
                relevance_dict.setdefault(query_id, {})[doc_id] = 1  # binary relevance

    return relevance_dict


def main():
    # Load ground truth
    relevance_dict = load_relevance_dict(csv_path=GROUND_TRUTH)

    results_by_k = {}
    for k in K:
        print(f"\n=== EVALUATION @k={k} ===")

        # Initialize metrics
        metrics = [scikit_metrics.PrecisionAtK(k=k), scikit_metrics.MRRAtK(k=k)]
        print(f"Using metrics: {', '.join(m.name for m in metrics)}")

        # Evaluation
        for model_name, model_predictions_path in MODELS.items():
            print(f"Evaluating model: {model_name}")
            print(f"{model_name}")
            predictions = loader.load_model_predictions(model_predictions_path)

            mean_scores = {metric.name: 0.0 for metric in metrics}
            per_query_metrics = {}

            for query_id, doc_list in predictions.items():
                per_query_scores = {}
                for metric in metrics:
                    score = metric.compute(
                        query_id=query_id,
                        retrieved_docs=doc_list,
                        relevant=relevance_dict,  # new param name and structure
                    )
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

            model_output_dir = os.path.join(OUTPUT_DIR, f"k={k}")
            os.makedirs(model_output_dir, exist_ok=True)

            saver.save_evaluation_results(
                model_name=model_name,
                mean_metrics=mean_scores,
                per_query_metrics=per_query_metrics,
                output_dir=model_output_dir,
                k=k,
            )
    combined_json_path = os.path.join(OUTPUT_DIR, f"mean_metrics_all_k.json")
    with open(combined_json_path, "w") as f:
        json.dump(results_by_k, f, indent=4)

    print()
    print("Evaluation complete.")


if __name__ == "__main__":
    main()
