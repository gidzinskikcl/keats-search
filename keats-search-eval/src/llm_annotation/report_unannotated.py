import pandas as pd
import json
from pathlib import Path

# Paths
jsonl_path = Path(
    "keats-search-eval/data/evaluation/llm-annotated/results/run-07-06-2025_12-30-00/annotations.jsonl"
)
csv_folder = Path("keats-search-eval/data/evaluation/pre-annotated/2025-07-06_12-52-45")

# Define models: name -> filename
models = {
    "bm25": csv_folder / "bm25searchengine_predictions.csv",
    "splade": Path(
        "keats-search-eval/data/evaluation/pre-annotated/2025-07-10_16-22-38/spladesearchengine_predictions.csv"
    ),
    "boolean": csv_folder / "booleansearchengine_predictions.csv",
    "tfidf": csv_folder / "tfidfsearchengine_predictions.csv",
}


# Load annotated pairs
annotated_pairs = set()
with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        annotated_pairs.add((data["query_id"], data["doc_id"]))

print(f"✅ Total annotated (query_id, doc_id) pairs: {len(annotated_pairs)}\n")

# Load all model pairs
model_pairs = {}
for model_name, csv_path in models.items():
    df = pd.read_csv(csv_path)
    pairs = set(zip(df["query_id"], df["doc_id"]))
    model_pairs[model_name] = pairs

# Compare with annotated pairs and BM25
bm25_pairs = model_pairs["bm25"]

for model_name, pairs in model_pairs.items():
    unannotated = pairs - annotated_pairs
    unique_to_model = unannotated - bm25_pairs

    print(f"{model_name.upper()}:")
    print(f"  🔍 Unannotated pairs (not in JSONL): {len(unannotated)}")
    print()
