import json


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def get_score(data, k, model, metric):
    return data.get(k, {}).get(model, {}).get(metric, None)


def generate_markdown_tables(data, k_metrics):
    all_models = set()
    for k, _ in k_metrics:
        all_models.update(data.get(k, {}).keys())
    all_models = sorted(all_models)

    tables = []

    for k, metric in k_metrics:
        header = "| Rank | Model Name | Score |\n"
        separator = "|------|-------------|--------|\n"

        rows = []
        for model in all_models:
            score = get_score(data, k, model, metric)
            score_str = f"{score:.4f}" if score is not None else "-"
            rows.append((model, score if score is not None else -1, score_str))

        # Sort rows descending by score
        rows.sort(key=lambda x: x[1], reverse=True)

        markdown_rows = [
            f"| {i+1} | `{model}` | {score_str} |"
            for i, (model, _, score_str) in enumerate(rows)
        ]

        table = (
            f"### Rankings for {metric} (k={k})\n\n{header}{separator}"
            + "\n".join(markdown_rows)
            + "\n"
        )
        tables.append(table)

    return "\n".join(tables)


def main():
    # path = "keats-search-eval/data/evaluation/gt-annotated/results/2025-07-05_19-16-50/mean_metrics_all_k.json"
    path_gt = "keats-search-eval/data/evaluation/gt-annotated/results/2025-07-06_13-51-09/mean_metrics_all_k.json"
    path_llm = "keats-search-eval/data/evaluation/llm-annotated/results/model_bm25_2025-07-06_12-52-45/mean_metrics_all_k.json"

    readme_path = "keats-search-eval/README.md"

    data_gt = load_json(path_gt)
    data_llm = load_json(path_llm)

    # Metrics to report
    k_metrics_gt = [("1", "Precision@1"), ("5", "MRR@5"), ("10", "MRR@10")]
    k_metrics_llm = [
        ("5", "Precision@5"),
        ("5", "MRR@5"),
        ("5", "NDCG@5"),
        ("10", "Precision@10"),
        ("10", "MRR@10"),
        ("10", "NDCG@10"),
    ]

    # Generate markdown for both
    markdown_gt = "## Ground Truth Annotated Evaluation\n\n"
    markdown_gt += generate_markdown_tables(data_gt, k_metrics_gt)

    markdown_llm = "## LLM-Annotated Evaluation\n\n"
    markdown_llm += generate_markdown_tables(data_llm, k_metrics_llm)

    # Combine and save
    markdown = "# Evaluation Summary\n\n" + markdown_gt + "\n---\n" + markdown_llm

    print(markdown)

    with open(readme_path, "w") as f:
        f.write(markdown)


if __name__ == "__main__":
    main()
