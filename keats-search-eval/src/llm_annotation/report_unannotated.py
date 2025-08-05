import pandas as pd
import json
import pathlib

# Paths
jsonl_paths = [
    pathlib.Path(
        "keats-search-eval/data/evaluation/llm-annotated/results/run-07-06-2025_12-30-00/annotations_new.jsonl"
    ),
    pathlib.Path(
        "keats-search-eval/data/evaluation/llm-annotated/results/splade/run-07-14-2025_18-20-00/annotations_new.jsonl"
    ),
    pathlib.Path(
        "keats-search-eval/data/evaluation/llm-annotated/results/tfidf/run-07-23-2025_01-00-00/annotations.jsonl"
    ),
    pathlib.Path(
        "keats-search-eval/data/evaluation/llm-annotated/results/colbert/run-07-23-2025_02-17-00/annotations.jsonl"
    ),
    pathlib.Path(
        "keats-search-eval/data/evaluation/llm-annotated/results/bm25_ce/run-07-24-2025_16-10-00/annotations.jsonl"
    ),
    pathlib.Path(
        "keats-search-eval/data/evaluation/llm-annotated/results/dpr/run-07-30-2025_11-15-00/annotations.jsonl"
    ),
]
csv_folder = pathlib.Path(
    "keats-search-eval/data/evaluation/pre-annotated/2025-07-06_12-52-45"
)

# Define models: name -> filename
models = {
    "bm25": "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_13-47-43/bm25searchengine_predictions.csv",
    "splade": "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_18-13-02/spladesearchengine_predictions.csv",
    "tfidf": "keats-search-eval/data/evaluation/pre-annotated/2025-07-22_03-03-14/tfidfsearchengine_predictions.csv",
    "dpr": "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_15-12-39/dprsearchengine_predictions.csv",
    "colbert": "keats-search-eval/data/evaluation/pre-annotated/2025-07-22_11-42-22/colbertsearchengine_predictions.csv",
    "bm25_ce": "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_13-47-43/bm25crossencodersearchengine_predictions.csv",
    "ance": "keats-search-eval/data/evaluation/pre-annotated/2025-08-01_22-33-19/ancesearchengine_predictions.csv",
}


# Load and combine annotated pairs
annotated_pairs = set()
duplicates = set()

for jsonl_path in jsonl_paths:
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            pair = (data["query_id"], data["id"])
            if pair in annotated_pairs:
                duplicates.add(pair)
            annotated_pairs.add(pair)

print(f"✅ Total unique annotated (query_id, doc_id) pairs: {len(annotated_pairs)}")
print(f"⚠️  Duplicate (query_id, doc_id) pairs found across files: {len(duplicates)}\n")

# Load all model pairs
model_pairs = {}
for model_name, csv_path in models.items():
    df = pd.read_csv(pathlib.Path(csv_path))
    pairs = set(zip(df["query_id"], df["id"]))
    model_pairs[model_name] = pairs

# Compare with annotated pairs and BM25
bm25_pairs = model_pairs["bm25"]

for model_name, pairs in model_pairs.items():
    unannotated = pairs - annotated_pairs
    unique_to_model = unannotated - bm25_pairs

    print(f"{model_name.upper()}:")
    print(f"  🔍 Unannotated pairs (not in JSONL): {len(unannotated)}")
    print()
