import json
import os
from benchmarking.metrics import scikit_metrics
from benchmarking.utils import loader, saver

PREDICTION_DIR = "keats-search-eval/data/evaluation/pre-annotated/2025-07-06_12-52-45/bm25searchengine_predictions.csv"
GROUND_TRUTH_PATH = "keats-search-eval/data/evaluation/llm-annotated/results/run-07-06-2025_12-30-00/annotations.jsonl"
OUTPUT_DIR = "keats-search-eval/data/evaluation/llm-annotated/results/model_bm25_2025-07-06_12-52-45"

PREDICTIONS = {"bm25": PREDICTION_DIR}
K = [5, 10]


def load_relevance_dict(path: str) -> dict[str, dict[str, int]]:
    relevance_dict = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            query_id = entry["query_id"]
            doc_id = entry["doc_id"]
            relevance = 1 if entry["relevance"].lower() == "relevant" else 0
            relevance_dict.setdefault(query_id, {})[doc_id] = relevance
    return relevance_dict


def main():
    relevance_dict = load_relevance_dict(GROUND_TRUTH_PATH)
    results_by_k = {}
    for k in K:
        print(f"\n=== EVALUATION @k={k} ===")

        # Initialize metrics
        metrics = [
            scikit_metrics.PrecisionAtK(k=k),
            scikit_metrics.MRRAtK(k=k),
            scikit_metrics.NDCGAtK(k=k),
        ]
        print(f"Using metrics: {', '.join(m.name for m in metrics)}")

        # Evaluation
        for model, path in PREDICTIONS.items():
            print(f"Evaluating model: {model}")

            predictions = loader.load_model_predictions(csv_path=path)

            mean_scores = {metric.name: 0.0 for metric in metrics}
            per_query_metrics = {}

            for query_id, doc_list in predictions.items():
                per_query_scores = {}
                for metric in metrics:
                    score = metric.compute(
                        query_id=query_id,
                        retrieved_docs=doc_list,
                        relevant=relevance_dict,
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
            results_by_k[k][model] = mean_scores

            for name, score in mean_scores.items():
                print(f"  {name}: {score:.4f}")

            model_output_dir = os.path.join(OUTPUT_DIR, f"k={k}")
            os.makedirs(model_output_dir, exist_ok=True)

            saver.save_evaluation_results(
                model_name=model,
                mean_metrics=mean_scores,
                per_query_metrics=per_query_metrics,
                output_dir=model_output_dir,
                k=k,
            )

    combined_json_path = os.path.join(OUTPUT_DIR, f"mean_metrics_all_k.json")
    with open(combined_json_path, "w") as f:
        json.dump(results_by_k, f, indent=4)
    print()
    print("Evaluation Complete")


if __name__ == "__main__":
    main()
