import os
import csv
import json
import random
from datetime import datetime
from collections import defaultdict

GROUND_TRUTH_PATH = "keats-search-eval/data/queries/validated/keats-search_queries_24-06-2025.csv"
BM25_RESULTS_PATH = "keats-search-eval/data/evaluation/pre-annotated/2025-07-02_15-44-29/bm25searchengine_predictions.csv"
DOCUMENTS_JSON_PATH = "keats-search-eval/data/documents/2025-07-03_12-22-08/documents.json"

OUTPUT_BASE = "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample"

def load_ground_truth(path):
    relevant = defaultdict(set)
    queries = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row["index"]
            did = row["doc_id"]
            if row.get("valid", "true").lower() != "false":
                relevant[qid].add(did)
                queries[qid] = row["question"]
    return queries, relevant

def load_bm25_top1(path):
    top1 = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["rank"] == "1":
                top1[row["query_id"]] = {
                    "doc_id": row["doc_id"],
                    "content": row["answer"],
                    "course": row["course"],
                    "lecture": row["lecture"]
                }
    return top1

def load_all_documents(path):
    with open(path, encoding="utf-8") as f:
        docs = json.load(f)
    return {doc["documentId"]: doc for doc in docs}

def build_samples(queries, relevant, bm25_top1, all_docs, n=30):
    # Build valid (query_id, ground_truth_doc_id) pairs where BM25 top1 exists
    valid_pairs = [
        (qid, did)
        for qid, doc_ids in relevant.items()
        if qid in bm25_top1
        for did in doc_ids
        if did in all_docs
    ]

    # Sample n pairs
    sampled_pairs = random.sample(valid_pairs, k=min(n, len(valid_pairs)))
    samples = []

    for qid, gt_doc_id in sampled_pairs:
        top1_doc = bm25_top1[qid]

        distractors = list(set(all_docs.keys()) - {gt_doc_id, top1_doc["doc_id"]})
        if not distractors:
            continue

        random_doc_id = random.choice(distractors)
        random_doc = all_docs[random_doc_id]
        gt_doc = all_docs[gt_doc_id]

        samples.append({
            "query_id": qid,
            "question": queries[qid],
            "ground_truth": {
                "doc_id": gt_doc_id,
                "content": gt_doc["content"],
                "course": gt_doc["courseName"],
                "lecture": gt_doc["title"]
            },
            "top1_bm25": top1_doc,
            "random_doc": {
                "doc_id": random_doc_id,
                "content": random_doc["content"],
                "course": random_doc["courseName"],
                "lecture": random_doc["title"]
            }
        })

    return samples


def save_samples(samples, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "benchmark_samples.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(samples)} samples to {out_path}")

def main():
    queries, relevant = load_ground_truth(GROUND_TRUTH_PATH)
    bm25_top1 = load_bm25_top1(BM25_RESULTS_PATH)
    all_docs = load_all_documents(DOCUMENTS_JSON_PATH)

    samples = build_samples(queries, relevant, bm25_top1, all_docs, n=30)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join(OUTPUT_BASE, timestamp)
    save_samples(samples, output_dir)

if __name__ == "__main__":
    main()
