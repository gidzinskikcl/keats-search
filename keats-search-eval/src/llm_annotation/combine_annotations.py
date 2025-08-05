import json
import pathlib

input_files = [
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
    pathlib.Path(
        "keats-search-eval/data/evaluation/llm-annotated/results/ance/run-08-02-2025_14-45-00/annotations.jsonl"
    ),
]

# Output directory and file
output_dir = pathlib.Path(
    "keats-search-eval/data/evaluation/llm-annotated/total_annotations"
)
output_file = output_dir / "combined_annotations.jsonl"

# Make sure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

# Store unique annotations and track duplicates
seen_pairs = set()
combined_data = []
duplicates = []

# Process each file
for file_path in input_files:
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            pair = (entry["query_id"], entry["id"])

            if pair in seen_pairs:
                duplicates.append(pair)
            else:
                seen_pairs.add(pair)
                combined_data.append(entry)

# Save combined annotations to output
with open(output_file, "w", encoding="utf-8") as f_out:
    for item in combined_data:
        f_out.write(json.dumps(item) + "\n")

# Reporting
print(f"✅ Combined annotations saved to: {output_file}")
print(f"📦 Total unique (query_id, doc_id) pairs: {len(combined_data)}")
print(f"⚠️  Duplicate pairs found across files: {len(duplicates)}")
