import pandas as pd

import json
import csv
import os

from benchmarking.metrics import scikit_metrics
from benchmarking.utils import loader, saver

# === CONFIGURATION ===
K = [1, 5, 10]

GROUND_TRUTH_PATH = "fdata/ground_truth/queries.csv"
ANNOTATIONS = "fdata/ground_truth/annotations.jsonl"

OUTPUT_DIR = "fdata/workspace/results"


PREDICTIONS_DIR = os.getenv("PREDICTIONS_DIR", "fdata/models_predictions")
MODELS_TO_EVAL = os.getenv("EVAL_MODELS", "").split(",")

all_predictions = {
    "Random": f"{PREDICTIONS_DIR}/randomsearchengine_predictions.csv",
    "BM25+CE": f"{PREDICTIONS_DIR}/bm25crossencodersearchengine_predictions.csv",
    "SPLADE": f"{PREDICTIONS_DIR}/spladesearchengine_predictions.csv",
    "ColBERT": f"{PREDICTIONS_DIR}/colbertsearchengine_predictions.csv",
    "BM25": f"{PREDICTIONS_DIR}/bm25searchengine_predictions.csv",
    "TFIDF": f"{PREDICTIONS_DIR}/tfidfsearchengine_predictions.csv",
    "ANCE": f"{PREDICTIONS_DIR}/ancesearchengine_predictions.csv",
    "DPR": f"{PREDICTIONS_DIR}/dprsearchengine_predictions.csv",
}

if MODELS_TO_EVAL and MODELS_TO_EVAL != [""]:
    PREDICTIONS = {
        name: path for name, path in all_predictions.items() if name in MODELS_TO_EVAL
    }
else:
    PREDICTIONS = all_predictions


# === HELPERS ===
def load_csv_relevance_dict(csv_path: str) -> dict[str, dict[str, int]]:
    relevance_dict = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["label"].strip().lower() == "valid":
                query_id = str(int(row["index"].strip()))
                doc_id = row["doc_id"].strip()
                relevance_dict.setdefault(query_id, {})[doc_id] = 1
    return relevance_dict


def load_jsonl_relevance_dict(jsonl_path: str) -> dict[str, dict[str, int]]:
    relevance_dict = {}
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            query_id = str(entry["query_id"])
            doc_id = entry["id"]
            rel = 1 if entry["relevance"].lower() == "relevant" else 0
            relevance_dict.setdefault(query_id, {})[doc_id] = rel
    return relevance_dict


def merge_relevance_dicts(
    dict1: dict[str, dict[str, int]], dict2: dict[str, dict[str, int]]
) -> dict[str, dict[str, int]]:
    merged = {}

    all_queries = set(dict1) | set(dict2)
    for qid in all_queries:
        merged[qid] = {}
        docs1 = dict1.get(qid, {})
        docs2 = dict2.get(qid, {})
        all_docs = set(docs1) | set(docs2)

        for doc_id in all_docs:
            rel1 = docs1.get(doc_id)
            rel2 = docs2.get(doc_id)
            # Prefer LLM if both are present
            if rel2 is not None:
                merged[qid][doc_id] = rel2
            elif rel1 is not None:
                merged[qid][doc_id] = rel1
    return merged


def evaluate(predictions, relevance_dict, results_by_k: dict):
    for k in K:
        print(f"\n=== Evaluation @k={k} ===")
        metrics = [
            scikit_metrics.PrecisionAtK(k=k),
            scikit_metrics.MRRAtK(k=k),
        ]
        if k > 1:
            metrics.append(scikit_metrics.NDCGAtK(k=k))

        print(f"Using metrics: {', '.join(m.name for m in metrics)}")

        for model_name, pred_path in predictions.items():
            retrieved = loader.load_model_predictions(pred_path)

            mean_scores = {m.name: 0.0 for m in metrics}
            per_query_metrics = {}

            for query_id, doc_list in retrieved.items():
                per_query_scores = {}
                for m in metrics:
                    score = m.compute(
                        query_id=str(query_id),
                        retrieved_docs=doc_list,
                        relevant=relevance_dict,
                    )
                    per_query_scores[m.name] = score
                    mean_scores[m.name] += score
                per_query_metrics[query_id] = per_query_scores

            total = len(retrieved)
            for name in mean_scores:
                mean_scores[name] /= total

            out_dir = os.path.join(OUTPUT_DIR, f"k={k}")
            os.makedirs(out_dir, exist_ok=True)
            saver.save_evaluation_results(
                model_name=model_name,
                mean_metrics=mean_scores,
                per_query_metrics=per_query_metrics,
                output_dir=out_dir,
                k=k,
            )

            if str(k) not in results_by_k:
                results_by_k[str(k)] = {}
            results_by_k[str(k)][model_name] = mean_scores

            # Print just the final results per model
            print(f"{model_name}")
            for name, score in mean_scores.items():
                print(f"  {name}: {score:.4f}")


def generate_latex_table(json_path, output_tex_path):
    name_normalizer = {
        "BM25": "BM25",
        "SPLADE": "SPLADE",
        "ColBERT": "ColBERT",
        "DPR": "DPR",
        "TFIDF": "TF-IDF",
        "BM25+CE": "BM25+CE",
        "ANCE": "ANCE",
    }

    with open(json_path) as f:
        all_data = json.load(f)

    model_metrics = {}
    for k, models in all_data.items():
        for model_name, metrics in models.items():
            normalized = name_normalizer.get(model_name)
            if not normalized:
                continue
            if normalized not in model_metrics:
                model_metrics[normalized] = {}
            model_metrics[normalized].update(metrics)

    df = pd.DataFrame.from_dict(model_metrics, orient="index")

    ordered_columns = [
        "Precision@1",
        "NDCG@5",
        "NDCG@10",
        "MRR@5",
        "MRR@10",
    ]
    df = df[[col for col in ordered_columns if col in df.columns]]
    df = df.drop(index="Random", errors="ignore")

    desired_order = [
        "ColBERT",
        "SPLADE",
        "BM25+CE",
        "BM25",
        "TF-IDF",
        "ANCE",
        "DPR",
    ]
    df = df.loc[[model for model in desired_order if model in df.index]]

    formatted_df = pd.DataFrame(index=df.index, columns=df.columns)

    for col in df.columns:
        col_values = df[col]
        col_sorted = col_values.dropna().sort_values(ascending=False)
        if len(col_sorted) == 0:
            continue

        best = col_sorted.iloc[0]
        second_best = col_sorted.iloc[1] if len(col_sorted) > 1 else None

        for idx, val in col_values.items():
            if pd.isna(val):
                formatted_df.at[idx, col] = "--"
            elif val == best:
                formatted_df.at[idx, col] = f"\\textbf{{{val:.3f}}}".rstrip("0").rstrip(
                    "."
                )
            elif val == second_best:
                formatted_df.at[idx, col] = f"\\underline{{{val:.3f}}}".rstrip(
                    "0"
                ).rstrip(".")
            else:
                formatted_df.at[idx, col] = f"{val:.3f}".rstrip("0").rstrip(".")

    df_clean = formatted_df

    with open(output_tex_path, "w") as f:
        f.write("\\begin{tabular}{l" + "r" * len(df_clean.columns) + "}\n")
        f.write("\\toprule\n")
        f.write(" & " + " & ".join(df_clean.columns) + " \\\\\n")
        f.write("\\midrule\n")
        for idx, row in df_clean.iterrows():
            f.write(idx + " & " + " & ".join(row.values) + " \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}\n")

    print("\nGenerated LaTeX table:")
    print(df_clean)


def main():
    print("Loading CSV-based GT relevance...")
    gt_relevance = load_csv_relevance_dict(GROUND_TRUTH_PATH)

    print("Loading JSONL-based LLM relevance...")
    llm_relevance = load_jsonl_relevance_dict(ANNOTATIONS)

    print("Merging GT and LLM relevance...")
    merged_relevance = merge_relevance_dicts(gt_relevance, llm_relevance)

    results_by_k = {}
    evaluate(PREDICTIONS, merged_relevance, results_by_k)

    out_path = os.path.join(OUTPUT_DIR, "mean_metrics_all_k.json")
    with open(out_path, "w") as f:
        json.dump(results_by_k, f, indent=4)

    ############################LATEX############################
    print("\nGenerating LaTeX table...")
    generate_latex_table(
        out_path, os.path.join(OUTPUT_DIR, "search_engine_tabular.tex")
    )
    ############################LATEX############################

    print("\nEvaluation complete.")


if __name__ == "__main__":
    main()
