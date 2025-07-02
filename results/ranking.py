import json

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def get_score(data, k, model, metric):
    return data.get(k, {}).get(model, {}).get(metric, None)

def generate_markdown_table(data, k_metrics):
    all_models = set()
    for k, _ in k_metrics:
        all_models.update(data.get(k, {}).keys())
    all_models = sorted(all_models)

    # Header
    header = ["| Rank | Model Name |"] + [f" {metric} |" for _, metric in k_metrics]
    separator = ["|------|-------------|"] + ["----------|" for _ in k_metrics]

    # Rows
    rows = []
    for model in all_models:
        row = [f"`{model}`"]
        for k, metric in k_metrics:
            score = get_score(data, k, model, metric)
            row.append(f"{score:.4f}" if score is not None else "-")
        rows.append((model, row))

    # Sort rows by first metric
    rows.sort(key=lambda x: float(x[1][1]) if x[1][1] != "-" else -1, reverse=True)

    # Final formatted rows
    markdown_rows = [f"| {i+1} | {' | '.join(row)} |" for i, (_, row) in enumerate(rows)]

    return "\n".join([
        "### Model Rankings",
        "",
        "".join(header),
        "".join(separator),
        "\n".join(markdown_rows),
        ""
    ])

def main():
    path = "results/mean_metrics_results.json"
    data = load_json(path)

    k_metrics = [("1", "Precision@1"), ("5", "MRR@5"), ("10", "MRR@10")]

    markdown = generate_markdown_table(data, k_metrics)
    print(markdown)

if __name__ == "__main__":
    main()
