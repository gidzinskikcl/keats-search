import json
import pathlib
import pandas as pd
import time
from datetime import datetime
from typing import Union

from llm_annotation.prompts import templates
from services.llm_based import client as llm_client
from llm_annotation.llm import annotator

# === Configuration ===
CSV_INPUT = pathlib.Path(
    # "keats-search-eval/data/evaluation/pre-annotated/2025-07-06_12-52-45/bm25searchengine_predictions.csv"
    # "keats-search-eval/data/evaluation/pre-annotated/2025-07-10_16-22-38/spladesearchengine_predictions.csv"
    # "keats-search-eval/data/evaluation/pre-annotated/2025-07-22_03-03-14/tfidfsearchengine_predictions.csv"
    # "keats-search-eval/data/evaluation/pre-annotated/2025-07-22_11-42-22/colbertsearchengine_predictions.csv"
    # "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_13-47-43/bm25crossencodersearchengine_predictions.csv"
    # "keats-search-eval/data/evaluation/pre-annotated/2025-07-21_15-12-39/dprsearchengine_predictions.csv"
    "keats-search-eval/data/evaluation/pre-annotated/2025-08-01_22-33-19/ancesearchengine_predictions.csv"
)
# ALREADY_ANNOTATED = "keats-search-eval/data/evaluation/llm-annotated/results/run-07-06-2025_12-30-00/annotations.jsonl"
ALREADY_ANNOTATED = "keats-search-eval/data/evaluation/llm-annotated/total_annotations/combined_annotations.jsonl"
PROMPT = templates.V2
BATCH_SIZE = 100

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_DIR = pathlib.Path(

    f"keats-search-eval/data/evaluation/llm-annotated/results/ance/run-08-02-2025_14-45-00"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHECKPOINT_FILE = OUTPUT_DIR / "completed_batches.json"
ANNOTATIONS_FILE = OUTPUT_DIR / "annotations.jsonl"
FAILED_FILE = OUTPUT_DIR / "failed_annotations.jsonl"

# === Load Data ===
df = pd.read_csv(CSV_INPUT)
records = df.to_dict(orient="records")

# === Skip already annotated ===
already_annotated_pairs = set()
with open(ALREADY_ANNOTATED, "r", encoding="utf-8") as f:
    for line in f:
        pair = json.loads(line)
        already_annotated_pairs.add((pair["query_id"], pair["id"]))

records = [
    r for r in records if (r["query_id"], r["id"]) not in already_annotated_pairs
]
total = len(records)
num_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

# === Load or Initialize Checkpoint ===
if CHECKPOINT_FILE.exists():
    with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
        completed_batches = set(json.load(f))
else:
    completed_batches = set()

# === Initialize Client ===
client = llm_client.load_openai_client()


# === Helpers ===
def append_jsonl(path: pathlib.Path, entries: Union[dict, list[dict]]):
    if isinstance(entries, dict):
        entries = [entries]
    with open(path, "a", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")


def annotate_entry(entry: dict) -> Union[dict, None]:
    try:
        result = annotator.annotate(
            client=client,
            prompt_module=PROMPT,
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
        print()
        return {
            "error": str(e),
            "query_id": entry["query_id"],
            "id": entry["id"],
        }


print(f"=== LLM Annotation Run Started at {TIMESTAMP} ===")
overall_start_time = time.time()
# === Recover total_annotated from previous progress ===
total_annotated = 0

# Count from completed annotations
if ANNOTATIONS_FILE.exists():
    with open(ANNOTATIONS_FILE, "r", encoding="utf-8") as f:
        total_annotated += sum(1 for _ in f)

# Count any in-progress annotations
for path in OUTPUT_DIR.glob("inprogress_batch_*.jsonl"):
    with open(path, "r", encoding="utf-8") as f:
        total_annotated += sum(1 for _ in f)

print(f"▶️ Resuming annotation. {total_annotated} query-doc pairs already annotated.")


for batch_id in range(num_batches):

    if batch_id in completed_batches:
        continue

    print(f"\n--- Batch {batch_id + 1}/{num_batches} ---")
    batch_start_time = time.time()

    start = batch_id * BATCH_SIZE
    end = min(start + BATCH_SIZE, total)
    batch = records[start:end]

    inprogress_file = OUTPUT_DIR / f"inprogress_batch_{batch_id}.jsonl"
    already_annotated_ids = set()
    batch_results = []
    batch_failures = []

    # Load in-progress annotations into batch_results
    if inprogress_file.exists():
        with open(inprogress_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    item = json.loads(line)
                    already_annotated_ids.add((item["query_id"], item["id"]))
                    batch_results.append(item)  # ← this is missing!
                except:
                    continue

    with open(inprogress_file, "a", encoding="utf-8") as progress_f:
        for entry in batch:
            entry_key = (entry["query_id"], entry["id"])

            if entry_key in already_annotated_ids:
                continue

            result = annotate_entry(entry)
            if result is None:
                continue
            elif "error" in result:
                batch_failures.append(result)
                append_jsonl(FAILED_FILE, result)
            else:
                batch_results.append(result)
                total_annotated += 1
                print(
                    f"  ✓ Saved {len(batch_results)} results, {len(batch_failures)} failures."
                )
                progress_f.write(json.dumps(result) + "\n")

    # Once complete, merge in-progress to annotations file
    append_jsonl(ANNOTATIONS_FILE, batch_results)
    inprogress_file.unlink(missing_ok=True)

    completed_batches.add(batch_id)
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(completed_batches), f, indent=2)

    batch_end_time = time.time()
    duration = batch_end_time - batch_start_time
    print(f"Finished batch {batch_id + 1} in {duration:.2f} seconds.")
    print(f"  ✓ Saved {len(batch_results)} results, {len(batch_failures)} failures.")
    print(f"  🔎 Total query-doc pairs annotated so far: {total_annotated}")


overall_end_time = time.time()
total_duration = overall_end_time - overall_start_time
print(
    f"\n=== LLM Annotation Run Completed in {total_duration:.2f} seconds ({total_duration / 60:.2f} minutes) ==="
)
