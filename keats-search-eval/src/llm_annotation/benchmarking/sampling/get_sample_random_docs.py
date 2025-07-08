import os
import json

# INPUT_DIR = "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-03_22-22-52"
# INPUT_DIR = "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-04_19-29-24"
INPUT_DIR = "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-05_17-28-37"


OUTPUT_FILENAME = "random_doc_relevance.json"

def process_samples(input_dir, output_filename):
    # Find the latest timestamped directory

    input_path = os.path.join(input_dir, "benchmark_samples.json")

    # Load the original samples
    with open(input_path, encoding="utf-8") as f:
        samples = json.load(f)

    # Create simplified data
    simplified = []
    for sample in samples:
        simplified.append({
            "query_id": sample["query_id"],
            "question": sample["question"],
            "random_doc": {
                "doc_id": sample["random_doc"]["doc_id"],
                "content": sample["random_doc"]["content"],
                "course": sample["random_doc"]["course"],
                "lecture": sample["random_doc"]["lecture"]
            },
            "relevance": ""  # Placeholder
        })

    # Save output
    output_path = os.path.join(input_dir, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(simplified, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(simplified)} entries to {output_path}")

if __name__ == "__main__":
    process_samples(INPUT_DIR, OUTPUT_FILENAME)
