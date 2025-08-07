from collections import defaultdict
import json
import pathlib
from csv import DictWriter
import pandas as pd
from statistics import mean
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    matthews_corrcoef,
)

# === Paths ===
BASE_DIR = pathlib.Path(
    "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-06_14-54-56"
)

ANNOTATED_FILE = {
    "Minimum": BASE_DIR / "results/2025-07-06_15-30-51/minimum-v1/annotated.json",
    "Basic": BASE_DIR / "results/2025-07-06_15-30-51/basic-v1/annotated.json",
    "F2": BASE_DIR / "results/2025-07-06_15-30-51/F2-v1/annotated.json",
    "F4": BASE_DIR / "results/2025-07-06_15-30-51/F4-v1/annotated.json",
}

TOKEN_USAGE_JSON = {
    "Minimum": BASE_DIR / "results/2025-07-06_15-30-51/minimum-v1/token_usage.json",
    "Basic": BASE_DIR / "results/2025-07-06_15-30-51/basic-v1/token_usage.json",
    "F2": BASE_DIR / "results/2025-07-06_15-30-51/F2-v1/token_usage.json",
    "F4": BASE_DIR / "results/2025-07-06_15-30-51/F4-v1/token_usage.json",
}

TOKEN_USAGE_SUMMARY_PATH = (
    BASE_DIR / "results/2025-07-06_15-30-51/token_usage_summary.csv"
)
BENCHMARK_FILE = BASE_DIR / "benchmark_samples.json"


# === Utility Functions ===


def is_wrong(entry: dict) -> bool:
    doc_type = entry.get("doc_type")
    relevance = entry.get("relevance")
    return (doc_type == "ground_truth" and relevance == "notrelevant") or (
        doc_type == "random_doc" and relevance == "relevant"
    )


def load_token_usage_summary(path: pathlib.Path) -> dict[str, float]:
    df = pd.read_csv(path)
    usage_map = {}
    for _, row in df.iterrows():
        variant = row["variant"].lower()
        if variant.endswith("-v1"):
            usage_map[variant] = row["average_prompt_tokens"]
    return usage_map


def load_bm25_pairs(path: pathlib.Path) -> set[tuple[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {(entry["query_id"], entry["top1_bm25"]["doc_id"]) for entry in data}


def compute_token_stats_ordered(usage_path: pathlib.Path) -> tuple[int, float, int]:
    with open(usage_path, "r", encoding="utf-8") as f:
        usage_entries = json.load(f)

    if len(usage_entries) % 3 != 0:
        raise ValueError(
            "Expected number of entries to be divisible by 3 (GT, BM25, random per query)"
        )

    filtered = []
    for i in range(0, len(usage_entries), 3):
        group = usage_entries[i : i + 3]
        if len(group) != 3:
            continue  # skip incomplete group
        gt, _, random = group  # skip the BM25 entry (middle one)
        filtered.extend([gt, random])

    total_tokens_list = [e["total_tokens"] for e in filtered]
    total = sum(total_tokens_list)
    avg = mean(total_tokens_list)
    return total, avg, len(filtered)


# === Main Evaluation ===


def main():
    print("\n========== Combined Evaluation ==========\n")

    token_usage_summary = load_token_usage_summary(TOKEN_USAGE_SUMMARY_PATH)
    bm25_pairs = load_bm25_pairs(BENCHMARK_FILE)
    results = []
    for prompt_name, annotated_path in ANNOTATED_FILE.items():
        variant_key = prompt_name.lower() + "-v1"
        prompt_token_length = token_usage_summary[variant_key]
        token_path = TOKEN_USAGE_JSON[prompt_name]

        if not annotated_path.exists():
            print(f"❌ File not found: {annotated_path}")
            continue

        with open(annotated_path, "r", encoding="utf-8") as f:
            entrs = json.load(f)

        annttns = [a for a in entrs if a["doc_type"] in ["ground_truth", "random_doc"]]

        query_groups = defaultdict(list)
        for entry in annttns:
            query_groups[entry["query_id"]].append(entry)

        y_true, y_pred = [], []
        for entries in query_groups.values():
            gt = next((e for e in entries if e["doc_type"] == "ground_truth"), None)
            rnd = next((e for e in entries if e["doc_type"] == "random_doc"), None)
            if gt:
                y_true.append(1)
                y_pred.append(1 if gt["relevance"] == "relevant" else 0)
            if rnd:
                y_true.append(0)
                y_pred.append(1 if rnd["relevance"] == "relevant" else 0)

        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        mcc = matthews_corrcoef(y_true, y_pred)

        wrong_entries = [entry for entry in annttns if is_wrong(entry)]
        counts = {"random_doc": 0, "ground_truth": 0}
        for entry in wrong_entries:
            if entry["doc_type"] in counts:
                counts[entry["doc_type"]] += 1

        total_tokens, avg_tokens, count = compute_token_stats_ordered(token_path)

        # === Output ===
        print(f"Variant: {prompt_name}")
        print(f"Prompt Length       : {prompt_token_length}")
        print(f"Total Token Usage   : {total_tokens}")
        print(f"Avg Token Usage     : {avg_tokens:.1f}\n")

        print(f"Accuracy              : {accuracy:.3f}")
        print(f"Precision             : {precision:.3f}")
        print(f"Recall                : {recall:.3f}")
        print(f"F1 Score              : {f1:.3f}")
        print(f"Matthews Corr Coef    : {mcc:.3f}")

        print(f"Total wrong annotations: {len(wrong_entries)}")
        for dt, count in counts.items():
            print(f"  - {dt}: {count}")

        not_relevant_gt_doc_ids = [
            entry["doc_id"]
            for entry in annttns
            if entry["doc_type"] == "ground_truth"
            and entry["relevance"] == "notrelevant"
        ]
        if not not_relevant_gt_doc_ids:
            print("✅ All ground truth documents were marked as relevant.")
        else:
            print("Ground truth documents marked as NOT relevant:")
            for doc_id in not_relevant_gt_doc_ids:
                print(f"  - {doc_id}")
        print()

        results.append(
            {
                "Prompt": prompt_name,
                "Accuracy": round(accuracy, 3),
                "F1 Score": round(f1, 3),
                "Average Tokens Used": round(avg_tokens, 1),
            }
        )
        print("======================================================")

    # output_csv = "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-06_14-54-56/results/llm_annotation_eval_summary.csv"
    # with open(output_csv, "w", newline="") as f:
    #     writer = DictWriter(
    #         f, fieldnames=["Prompt", "Accuracy", "F1 Score", "Average Tokens Used"]
    #     )
    #     writer.writeheader()
    #     writer.writerows(results)

    df = pd.DataFrame(results)

    # Get max for Accuracy and F1 Score, min for Average Tokens Used
    max_accuracy = df["Accuracy"].max()
    max_f1 = df["F1 Score"].max()
    min_tokens = df["Average Tokens Used"].min()

    # Apply formatting
    df["Accuracy"] = df["Accuracy"].apply(
        lambda x: f"\\textbf{{{x:.3f}}}" if x == max_accuracy else f"{x:.3f}"
    )
    df["F1 Score"] = df["F1 Score"].apply(
        lambda x: f"\\textbf{{{x:.3f}}}" if x == max_f1 else f"{x:.3f}"
    )
    df["Average Tokens Used"] = df["Average Tokens Used"].apply(
        lambda x: f"\\textbf{{{x:.1f}}}" if x == min_tokens else f"{x:.1f}"
    )

    # Export LaTeX
    latex_table = df.to_latex(index=False, escape=False)
    output_tex = "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-06_14-54-56/results/llm_annotation_eval_summary.tex"
    with open(output_tex, "w") as f:
        f.write(latex_table)

    print(f"\n✅ Saved summary to {output_tex}")


if __name__ == "__main__":
    main()
