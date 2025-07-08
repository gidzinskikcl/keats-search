import os
import csv
import json
import random
from datetime import datetime
from collections import defaultdict

# GROUND_TRUTH_PATH = "keats-search-eval/data/queries/validated/keats-search_queries_24-06-2025.csv"
GROUND_TRUTH_PATH = "keats-search-eval/data/queries/validated/keats-search_queries_with_content_24-06-2025.csv"  # updated

# BM25_RESULTS_PATH = "keats-search-eval/data/evaluation/pre-annotated/2025-07-03_15-28-44/bm25searchengine_predictions.csv"
BM25_RESULTS_PATH = "keats-search-eval/data/evaluation/pre-annotated/2025-07-06_12-52-45/bm25searchengine_predictions.csv"

DOCUMENTS_JSON_PATH = "keats-search-eval/data/documents/2025-07-05_16-26-20/documents.json"


OUTPUT_BASE = "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample"
SAMPLE = "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-04_19-29-24/benchmark_samples.json"


def load_ground_truth(path):
    data = []

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["label"] == "valid":
                data.append({
                    "query_id": row["index"],
                    "question": row["question"],
                    "doc_id": row["doc_id"],
                    "answer": row.get("answer"),
                    "course_name": row.get("course_name"),
                    "lecture_title": row.get("lecture_title")
                })

    return data

def load_bm25_top1(path):
    data = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["rank"] == "1":
                data.append({
                    "query_id": row["query_id"],
                    "doc_id": row["doc_id"],
                    "content": row["answer"],
                    "course": row["course"],
                    "lecture": row["lecture"]
                })
    return data

def load_all_documents(path):
    with open(path, encoding="utf-8") as f:
        docs = json.load(f)
    return {doc["documentId"]: doc for doc in docs}


def load_sample_queries_ids(path):
    with open(path, encoding="utf-8") as f:
        samples = json.load(f)
    return [s["query_id"] for s in samples]

def load_sample_queries(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_random_doc_ids(path):
    with open(path, encoding="utf-8") as f:
        samples = json.load(f)
    return {s["query_id"]: s["random_doc"]["doc_id"] for s in samples}

def build_samples(sample_items, gt, bm25_top1, all_docs):
    # Index ground truth and BM25 for fast lookup
    gt_map = {g["query_id"]: g for g in gt}
    bm25_map = {b["query_id"]: b for b in bm25_top1}
    result = []

    for sample in sample_items:
        qid = sample["query_id"]
        if qid not in gt_map or qid not in bm25_map:
            continue  # Skip if either required component is missing

        g = gt_map[qid]
        b = bm25_map[qid]
        gt_doc_id = g["doc_id"]
        bm25_doc_id = b["doc_id"]
        random_doc_id = sample["random_doc"]["doc_id"]


        gt_doc = all_docs.get(gt_doc_id)
        random_doc = all_docs.get(random_doc_id)

        if not gt_doc or not random_doc:
            continue  # Skip if any doc is missing

        result.append({
            "query_id": qid,
            "question": g["question"],
            "ground_truth": {
                "doc_id": gt_doc_id,
                "content": gt_doc["content"],
                "course": gt_doc["courseName"],
                "lecture": gt_doc["title"]
            },
            "top1_bm25": {
                "doc_id": bm25_doc_id,
                "content": b["content"],
                "course": b["course"],
                "lecture": b["lecture"]
            },
            "random_doc": {
                "doc_id": random_doc_id,
                "content": random_doc["content"],
                "course": random_doc["courseName"],
                "lecture": random_doc["title"]
            }
        })

    return result
                
    
def main():
    ground_truth = load_ground_truth(GROUND_TRUTH_PATH)
    bm25_top1 = load_bm25_top1(BM25_RESULTS_PATH)
    all_docs = load_all_documents(DOCUMENTS_JSON_PATH)

    old_samples = load_sample_queries(SAMPLE)

    # Define invalid query_ids
    invalid_query_ids = {"28", "30", "84"}

    # Create lookup maps
    gt_map = {g["query_id"]: g for g in ground_truth}
    bm25_map = {b["query_id"]: b for b in bm25_top1}
    used_query_ids = {s["query_id"] for s in old_samples}

    # Track invalid sample positions and random_doc entries
    replacement_indices = []
    old_random_docs = []

    for idx, sample in enumerate(old_samples):
        if sample["query_id"] in invalid_query_ids:
            replacement_indices.append(idx)
            old_random_docs.append(sample["random_doc"])

    # Select 3 valid, unused new samples
    candidates = [
        g for g in ground_truth
        if g["query_id"] not in used_query_ids
        and g["query_id"] in bm25_map
        and g["doc_id"] in all_docs
        and bm25_map[g["query_id"]]["doc_id"] in all_docs
    ]
    new_gt_samples = random.sample(candidates, 3)

    # Build replacement samples (in same order as invalids)
    replacements = []
    for g, random_doc in zip(new_gt_samples, old_random_docs):
        qid = g["query_id"]
        bm25 = bm25_map[qid]
        gt_doc = all_docs[g["doc_id"]]
        bm25_doc = all_docs[bm25["doc_id"]]

        replacements.append({
            "query_id": qid,
            "question": g["question"],
            "ground_truth": {
                "doc_id": g["doc_id"],
                "content": gt_doc["content"],
                "course": gt_doc["courseName"],
                "lecture": gt_doc["title"]
            },
            "top1_bm25": {
                "doc_id": bm25["doc_id"],
                "content": bm25["content"],
                "course": bm25["course"],
                "lecture": bm25["lecture"]
            },
            "random_doc": random_doc
        })

    built_samples = build_samples(old_samples, ground_truth, bm25_top1, all_docs)
    final_samples = []
    replacement_idx = 0

    for sample in old_samples:
        qid = sample["query_id"]
        if qid in invalid_query_ids:
            # Use next replacement in the correct order
            final_samples.append(replacements[replacement_idx])
            replacement_idx += 1
        else:
            # Use the originally built sample
            built_sample = next(b for b in built_samples if b["query_id"] == qid)
            final_samples.append(built_sample)


    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join(OUTPUT_BASE, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "benchmark_samples.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(final_samples, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(final_samples)} samples to {out_path}")


if __name__ == "__main__":
    main()
