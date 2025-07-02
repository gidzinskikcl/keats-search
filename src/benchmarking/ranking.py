import json

def load_json(path): # No test
    with open(path, 'r') as f:
        return json.load(f)

def rank_models(data, k: str, metric_key: str): # No test
    print(f"\n=== Ranking for k={k} using {metric_key} ===")
    models_scores = []
    for model_name, metrics in data.get(k, {}).items():
        score = metrics.get(metric_key)
        if score is not None:
            models_scores.append((model_name, score))

    # Sort descending
    models_scores.sort(key=lambda x: x[1], reverse=True)

    for rank, (model, score) in enumerate(models_scores, start=1):
        print(f"{rank:>2}. {model:<40} {score:.4f}")

def merge_results(data1, data2): # No test
    merged = {}

    all_ks = set(data1.keys()) | set(data2.keys())

    for k in all_ks:
        merged[k] = {}
        models_1 = data1.get(k, {})
        models_2 = data2.get(k, {})

        # Combine model entries under this k
        merged[k].update(models_1)
        merged[k].update(models_2)

    return merged


def main():
    path1 = "data/evaluation/gt-annotated/results/2025-07-02_17-16-24/mean_metrics_all_k.json"
    path2 = "data/evaluation/gt-annotated/results/2025-07-02_17-21-18/mean_metrics_all_k.json"

    data1 = load_json(path1)
    data2 = load_json(path2)

    merged = merge_results(data1, data2)


    rank_models(merged, k="1", metric_key="Precision@1")
    rank_models(merged, k="5", metric_key="MRR@5")
    rank_models(merged, k="10", metric_key="MRR@10")

if __name__ == "__main__":
    main()
