# import pandas as pd
# import json
# from pathlib import Path

# """
# Collect ALL (query_id, doc_id) pairs per CSV
# (excluding some), and compare them with annotated pairs
# in the JSONL file. Report how many unannotated pairs exist.
# """

# # Paths
# jsonl_path = Path("keats-search-eval/data/evaluation/llm-annotated/results/run-07-06-2025_12-30-00/annotations.jsonl")
# csv_folder = Path("keats-search-eval/data/evaluation/pre-annotated/2025-07-06_12-52-45")

# # Files to exclude
# excluded_files = {
#     "randomsearchengine_predictions.csv",
#     # "booleansearchengine_predictions.csv",
#     "dirichletsearchengine_mu_500_predictions.csv",
#     "dirichletsearchengine_mu_1000_predictions.csv",
#     "dirichletsearchengine_mu_1500_predictions.csv",
#     "lmjelinekmercersearchengine_lambda_0.1.csv",
#     "lmjelinekmercersearchengine_lambda_0.3.csv",
#     "lmjelinekmercersearchengine_lambda_0.5.csv",
#     "lmjelinekmercersearchengine_lambda_0.9.csv",
#     # "dirichletsearchengine_mu_2000_predictions.csv",
# }

# # Load annotated pairs from JSONL
# annotated_pairs = set()
# with open(jsonl_path, "r", encoding="utf-8") as f:
#     for line in f:
#         data = json.loads(line)
#         annotated_pairs.add((data["query_id"], data["doc_id"]))

# print(f"✅ Total annotated (query_id, doc_id) pairs: {len(annotated_pairs)}\n")

# # Collect ALL (query_id, doc_id) pairs from included CSVs
# all_csv_pairs = set()

# for csv_file in csv_folder.glob("*.csv"):
#     if csv_file.name in excluded_files:
#         continue

#     df = pd.read_csv(csv_file)

#     # Collect all query-doc pairs (no top-5 filter)
#     pairs = set(zip(df["query_id"], df["doc_id"]))
#     all_csv_pairs.update(pairs)

#     unannotated = pairs - annotated_pairs
#     print(f"{csv_file.name}: {len(unannotated)} unannotated pairs from all results")

# # Summary
# annotated_pairs_in_csvs = all_csv_pairs & annotated_pairs
# unannotated_pairs_in_csvs = all_csv_pairs - annotated_pairs

# print(f"\n✅ Annotated pairs found in CSVs: {len(annotated_pairs_in_csvs)}")
# print(f"🔍 Unannotated pairs found in CSVs: {len(unannotated_pairs_in_csvs)}")
# print(f"📊 Total distinct (query_id, doc_id) pairs from all CSVs: {len(all_csv_pairs)}")

#######################################################

import pandas as pd
import json
from pathlib import Path

"""
Simulate what happens if all TFIDF (query_id, doc_id) pairs are annotated.
"""

# Paths
jsonl_path = Path(
    "keats-search-eval/data/evaluation/llm-annotated/results/run-07-06-2025_12-30-00/annotations.jsonl"
)
csv_folder = Path("keats-search-eval/data/evaluation/pre-annotated/2025-07-06_12-52-45")
tfidf_file = "tfidfsearchengine_predictions.csv"  # Simulated as annotated

# Files to exclude
excluded_files = {
    "randomsearchengine_predictions.csv",
    # "booleansearchengine_predictions.csv",
    "dirichletsearchengine_mu_500_predictions.csv",
    "dirichletsearchengine_mu_1000_predictions.csv",
    "dirichletsearchengine_mu_1500_predictions.csv",
    "lmjelinekmercersearchengine_lambda_0.1.csv",
    "lmjelinekmercersearchengine_lambda_0.3.csv",
    "lmjelinekmercersearchengine_lambda_0.5.csv",
    "lmjelinekmercersearchengine_lambda_0.9.csv",
    # "dirichletsearchengine_mu_2000_predictions.csv",
}

# Step 1: Load existing annotations
annotated_pairs = set()
with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        annotated_pairs.add((data["query_id"], data["doc_id"]))

# Step 2: Simulate TFIDF annotation
tfidf_path = csv_folder / tfidf_file
df_tfidf = pd.read_csv(tfidf_path)
tfidf_pairs = set(zip(df_tfidf["query_id"], df_tfidf["doc_id"]))
annotated_pairs |= tfidf_pairs  # simulate them as annotated

print(
    f"✅ Total simulated annotated (query_id, doc_id) pairs (including TFIDF): {len(annotated_pairs)}\n"
)

# Step 3: Recalculate stats from all other included CSVs
all_csv_pairs = set()

for csv_file in csv_folder.glob("*.csv"):
    if csv_file.name in excluded_files:
        continue
    df = pd.read_csv(csv_file)
    pairs = set(zip(df["query_id"], df["doc_id"]))
    all_csv_pairs.update(pairs)

    unannotated = pairs - annotated_pairs
    print(f"{csv_file.name}: {len(unannotated)} unannotated pairs from all results")

# Final Summary
annotated_pairs_in_csvs = all_csv_pairs & annotated_pairs
unannotated_pairs_in_csvs = all_csv_pairs - annotated_pairs

print(
    f"\n✅ Annotated pairs found in CSVs (after TFIDF): {len(annotated_pairs_in_csvs)}"
)
print(
    f"🔍 Unannotated pairs found in CSVs (after TFIDF): {len(unannotated_pairs_in_csvs)}"
)
print(f"📊 Total distinct (query_id, doc_id) pairs from all CSVs: {len(all_csv_pairs)}")
