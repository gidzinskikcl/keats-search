import json
import pandas as pd
import numpy as np

# Paths to the two JSON files
# gt_path = "keats-search-eval/data/evaluation/gt-annotated/results/2025-07-22_14-16-41/mean_metrics_all_k.json"
gt_path = "keats-search-eval/data/evaluation/gt-annotated/results/2025-08-02_14-40-43/mean_metrics_all_k.json"
llm_path = "keats-search-eval/data/evaluation/llm-annotated/results/model_2025-07-23_02-14-00/mean_metrics_all_k.json"

# Models to include (uncomment to include)
name_normalizer = {
    "BM25SearchEngine": "BM25",
    "bm25": "BM25",
    "SpladeSearchEngine": "SPLADE",
    "splade": "SPLADE",
    "ColBERTSearchEngine": "ColBERT",
    "colbert": "ColBERT",
    "DPRSearchEngine": "DPR",
    "dpr": "DPR",
    "TFIDFSearchEngine": "TF-IDF",
    "tfidf": "TF-IDF",
    "BM25CrossEncoderSearchEngine": "BM25+CE",
    "bm25_ce": "BM25+CE",
    "ance": "ANCE",
    "ANCESearchEngine": "ANCE",
    # "BM25_ColbertEngine": "BM25+ColBERT",
    # "SBERTSearchEngine": "SBERT",
    # "GTRSearchEngineST": "GTR",
}

# Load both JSON files
with open(gt_path) as f:
    gt_data = json.load(f)
with open(llm_path) as f:
    llm_data = json.load(f)

model_metrics = {}

# Combine all metrics across k values and sources
for source_data in [gt_data, llm_data]:
    for k, models in source_data.items():
        for model_name, metrics in models.items():
            normalized = name_normalizer.get(model_name)
            if not normalized:
                continue  # skip models not in name_normalizer
            if normalized not in model_metrics:
                model_metrics[normalized] = {}
            model_metrics[normalized].update(metrics)

# Convert to DataFrame
df = pd.DataFrame.from_dict(model_metrics, orient="index")

# Filter + order columns
ordered_columns = [
    "Precision@1",
    # "Precision@5",
    # "Precision@10",
    "NDCG@5",
    "NDCG@10",
    "MRR@5",
    "MRR@10",
]
df = df[[col for col in ordered_columns if col in df.columns]]

# Remove 'Random' row just in case
df = df.drop(index="Random", errors="ignore")


# Desired row/model order
desired_order = ["ColBERT", "SPLADE", "BM25+CE", "BM25", "TF-IDF", "ANCE", "DPR"]
df = df.loc[[model for model in desired_order if model in df.index]]

# Format with LaTeX: bold best, underline second-best
formatted_df = pd.DataFrame(index=df.index, columns=df.columns)

for col in df.columns:
    col_values = df[col]
    # Ignore NaNs
    col_sorted = col_values.dropna().sort_values(ascending=False)
    if len(col_sorted) == 0:
        continue

    best = col_sorted.iloc[0]
    second_best = col_sorted.iloc[1] if len(col_sorted) > 1 else None

    for idx, val in col_values.items():
        if pd.isna(val):
            formatted_df.at[idx, col] = "--"
        elif val == best:
            formatted_df.at[idx, col] = f"\\textbf{{{val:.3f}}}".rstrip("0").rstrip(".")
        elif val == second_best:
            formatted_df.at[idx, col] = f"\\underline{{{val:.3f}}}".rstrip("0").rstrip(
                "."
            )
        else:
            formatted_df.at[idx, col] = f"{val:.3f}".rstrip("0").rstrip(".")


# Round and format
df_clean = formatted_df


# Generate LaTeX tabular
latex_body = df_clean.to_latex(
    index=True,
    header=True,
    column_format="l" + "r" * len(df_clean.columns),
    escape=False,
    na_rep="--",
)

# Strip LaTeX environment
lines = latex_body.strip().splitlines()
tabular_only = "\n".join(
    line
    for line in lines
    if not line.startswith("\\begin") and not line.startswith("\\end")
)

# Save result
# Save result
with open("search_engine_tabular_31-07.tex", "w") as f:
    f.write("\\begin{tabular}{lrrrrrrrr}\n")
    f.write("\\toprule\n")
    f.write(" & " + " & ".join(df_clean.columns) + " \\\\\n")
    f.write("\\midrule\n")
    for idx, row in df_clean.iterrows():
        f.write(idx + " & " + " & ".join(row.values) + " \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")


# Print to confirm
print(df_clean)
