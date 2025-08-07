import argparse
import json
import pathlib
import pandas as pd
import time
from datetime import datetime
from typing import Union

from llm_annotation.prompts import templates
from services.llm_based import client as llm_client
from llm_annotation.llm import annotator

# === Mapping from model name to CSV filename ===
MODEL_TO_CSV = {
    "Random": "randomsearchengine_predictions.csv",
    "BM25+CE": "bm25crossencodersearchengine_predictions.csv",
    "SPLADE": "spladesearchengine_predictions.csv",
    "ColBERT": "colbertsearchengine_predictions.csv",
    "BM25": "bm25searchengine_predictions.csv",
    "TFIDF": "tfidfsearchengine_predictions.csv",
    "ANCE": "ancesearchengine_predictions.csv",
    "DPR": "dprsearchengine_predictions.csv",
}

CSV_BASE_DIR = pathlib.Path("fdata/models_predictions")
DEFAULT_ANNOTATED = pathlib.Path("fdata/ground_truth/annotations.jsonl")
DEFAULT_OUTPUT_DIR = pathlib.Path("fdata/workspace/llm_annotation")


def append_jsonl(path: pathlib.Path, entries: Union[dict, list[dict]]):
    if isinstance(entries, dict):
        entries = [entries]
    with open(path, "a", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")


def annotate_entry(entry: dict, client, prompt_module) -> Union[dict, None]:
    try:
        result = annotator.annotate(
            client=client,
            prompt_module=prompt_module,
            course_name=entry["course_id"],
            lecture_name=entry["lecture_id"],
            question=entry["question"],
            answer=entry["answer"],
        )
        if result:
            result["query_id"] = entry["query_id"]
            result["id"] = entry["id"]
            result["rank"] = entry["rank"]
            result["model"] = entry["model"]
            return result
    except Exception as e:
        return {
            "error": str(e),
            "query_id": entry["query_id"],
            "id": entry["id"],
        }


def run_annotation(
    model_name: str, output_root: pathlib.Path, already_annotated_path: pathlib.Path
):
    if model_name not in MODEL_TO_CSV:
        raise ValueError(
            f"Unknown model name: {model_name}. Choose one of: {list(MODEL_TO_CSV.keys())}"
        )

    csv_input = CSV_BASE_DIR / MODEL_TO_CSV[model_name]
    if not csv_input.exists():
        raise FileNotFoundError(
            f"CSV file not found for model {model_name}: {csv_input}"
        )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = output_root / model_name.lower() / f"run-{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_file = output_dir / "completed_batches.json"
    annotations_file = output_dir / "annotations.jsonl"
    failed_file = output_dir / "failed_annotations.jsonl"
    batch_size = 100

    df = pd.read_csv(csv_input)
    records = df.to_dict(orient="records")

    # already_annotated_pairs = set()
    # if already_annotated_path.exists():
    #     with open(already_annotated_path, "r", encoding="utf-8") as f:
    #         for line in f:
    #             pair = json.loads(line)
    #             already_annotated_pairs.add((pair["query_id"], pair["id"]))

    # records = [
    #     r for r in records if (r["query_id"], r["id"]) not in already_annotated_pairs
    # ]
    total = len(records)
    num_batches = (total + batch_size - 1) // batch_size

    if checkpoint_file.exists():
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            completed_batches = set(json.load(f))
    else:
        completed_batches = set()

    client = llm_client.load_openai_client()
    prompt_module = templates.V2

    print(f"\n=== LLM Annotation Run for {model_name} ===")
    print(f"Input file: {csv_input}")
    print(f"Output dir: {output_dir}")
    print(f"Total to annotate: {total} entries\n")

    total_annotated = 0
    overall_start_time = time.time()

    for batch_id in range(num_batches):
        if batch_id in completed_batches:
            continue

        print(f"\n--- Batch {batch_id + 1}/{num_batches} ---")
        batch_start_time = time.time()

        start = batch_id * batch_size
        end = min(start + batch_size, total)
        batch = records[start:end]

        inprogress_file = output_dir / f"inprogress_batch_{batch_id}.jsonl"
        already_ids = set()
        batch_results = []
        batch_failures = []

        if inprogress_file.exists():
            with open(inprogress_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        item = json.loads(line)
                        already_ids.add((item["query_id"], item["id"]))
                        batch_results.append(item)
                    except:
                        continue

        with open(inprogress_file, "a", encoding="utf-8") as progress_f:
            for entry in batch:
                key = (entry["query_id"], entry["id"])
                if key in already_ids:
                    continue

                result = annotate_entry(entry, client, prompt_module)
                if result is None:
                    continue
                elif "error" in result:
                    batch_failures.append(result)
                    append_jsonl(failed_file, result)
                else:
                    batch_results.append(result)
                    total_annotated += 1
                    print(f"  ✓ Annotated {entry['id']}")
                    progress_f.write(json.dumps(result) + "\n")

        append_jsonl(annotations_file, batch_results)
        inprogress_file.unlink(missing_ok=True)

        completed_batches.add(batch_id)
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(sorted(completed_batches), f, indent=2)

        duration = time.time() - batch_start_time
        print(f"✅ Batch {batch_id + 1} done in {duration:.2f}s")

    total_duration = time.time() - overall_start_time
    print(f"\n🎉 Completed {total_annotated} annotations in {total_duration:.2f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run LLM annotation over search engine results."
    )
    parser.add_argument(
        "--model", required=True, help="Model name (e.g., BM25, SPLADE, ColBERT)"
    )
    parser.add_argument(
        "--outdir", default=str(DEFAULT_OUTPUT_DIR), help="Base output directory"
    )
    parser.add_argument(
        "--already",
        default=str(DEFAULT_ANNOTATED),
        help="Path to combined_annotations.jsonl",
    )

    args = parser.parse_args()
    run_annotation(
        model_name=args.model,
        output_root=pathlib.Path(args.outdir),
        already_annotated_path=pathlib.Path(args.already),
    )
