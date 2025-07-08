from collections import defaultdict
import json
from pathlib import Path

# Path to the annotated.json file
ANNOTATED_FILE = Path(
    # "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-06_14-54-56/results/2025-07-06_15-30-51/basic-v1/annotated.json"
    # "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-06_14-54-56/results/2025-07-06_15-30-51/minimum-v1/annotated.json"
    # "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-06_14-54-56/results/2025-07-06_15-30-51/F2-v1/annotated.json"
    "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-06_14-54-56/results/2025-07-06_15-30-51/F4-v1/annotated.json"

)

def is_wrong(entry: dict) -> bool:
    doc_type = entry.get("doc_type")
    relevance = entry.get("relevance")
    
    # It's wrong if relevant when it shouldn't be, or not relevant when it should
    if doc_type in ("ground_truth", "top1_bm25") and relevance == "notrelevant":
        return True
    if doc_type == "random_doc" and relevance == "relevant":
        return True
    return False

def main():
    if not ANNOTATED_FILE.exists():
        print(f"File not found: {ANNOTATED_FILE}")
        return

    with open(ANNOTATED_FILE, "r", encoding="utf-8") as f:
        annotations = json.load(f)

    wrong_entries = [entry for entry in annotations if is_wrong(entry)]

    # Count wrong entries by doc_type
    counts = {
        "random_doc": 0,
        "ground_truth": 0,
        "top1_bm25": 0
    }

    for entry in wrong_entries:
        doc_type = entry["doc_type"]
        if doc_type in counts:
            counts[doc_type] += 1

    total_wrong = len(wrong_entries)
    print(f"Total wrong annotations: {total_wrong}\n")
    for dt, count in counts.items():
        print(f"  of which {dt}: {count}")
    print("")
    
    for i, entry in enumerate(wrong_entries, 1):
        print(f"{i}. Query ID: {entry['query_id']}, Doc Type: {entry['doc_type']}, Relevance: {entry['relevance']}")
        print(f"   Question: {entry['question']}")
        print(f"   Answer: {entry['answer'][:200]}...")  # Print first 200 chars
        print("")


        # --- Find ground_truth documents incorrectly marked as not relevant ---
    not_relevant_gt_doc_ids = [
        entry["doc_id"]
        for entry in annotations
        if entry["doc_type"] == "ground_truth" and entry["relevance"] == "notrelevant"
    ]

    if not_relevant_gt_doc_ids:
        print("Ground truth documents marked as NOT relevant:")
        for doc_id in not_relevant_gt_doc_ids:
            print(f"  - {doc_id}")
    else:
        print("✅ All ground truth documents were marked as relevant.")


    # Group by query_id to match GT and BM25 doc_ids
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef
    query_groups = defaultdict(list)
    for entry in annotations:
        query_groups[entry['query_id']].append(entry)

    y_true = []
    y_pred = []

    skipped = 0

    for query_id, entries in query_groups.items():
        gt_entry = next((e for e in entries if e['doc_type'] == 'ground_truth'), None)
        bm25_entry = next((e for e in entries if e['doc_type'] == 'top1_bm25'), None)
        random_entry = next((e for e in entries if e['doc_type'] == 'random_doc'), None)

        # Evaluate GT (assumed relevant)
        if gt_entry:
            y_true.append(1)
            y_pred.append(1 if gt_entry['relevance'] == 'relevant' else 0)

        # Evaluate random doc (assumed NOT relevant)
        if random_entry:
            y_true.append(0)
            y_pred.append(1 if random_entry['relevance'] == 'relevant' else 0)

        # Evaluate BM25 ONLY if same doc_id as GT
        if gt_entry and bm25_entry and gt_entry['doc_id'] == bm25_entry['doc_id']:
            y_true.append(1)  # trusted as same as GT
            y_pred.append(1 if bm25_entry['relevance'] == 'relevant' else 0)
        else:
            skipped += 1

    # Compute metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    mcc = matthews_corrcoef(y_true, y_pred)

    print("\n=== LLM Annotator Evaluation (Trusted Examples Only) ===")
    print(f"Examples used       : {len(y_true)}")
    print(f"Skipped BM25 cases  : {skipped} (no GT or different doc_id)\n")
    print(f"Accuracy            : {accuracy:.3f}")
    print(f"Precision           : {precision:.3f}")
    print(f"Recall              : {recall:.3f}")
    print(f"F1 Score            : {f1:.3f}")
    print(f"Matthews Corr Coef  : {mcc:.3f}\n")


        # === ESTIMATE FINAL ACCURACY ===
    print("\n=== Estimating Annotator Accuracy from All Sources ===")

    # --- 1. Trusted (GT and Random) ---
    trusted_total = 0
    trusted_correct = 0
    for entry in annotations:
        if entry['doc_type'] == 'ground_truth':
            trusted_total += 1
            if entry['relevance'] == 'relevant':
                trusted_correct += 1
        elif entry['doc_type'] == 'random_doc':
            trusted_total += 1
            if entry['relevance'] == 'notrelevant':
                trusted_correct += 1

    # --- 2. BM25 Auto-agreement ---
    bm25_auto_total = 0
    bm25_auto_correct = 0
    query_groups = defaultdict(list)
    for entry in annotations:
        query_groups[entry['query_id']].append(entry)

    for query_id, group in query_groups.items():
        gt = next((e for e in group if e['doc_type'] == 'ground_truth'), None)
        bm25 = next((e for e in group if e['doc_type'] == 'top1_bm25'), None)
        if gt and bm25 and gt['relevance'] == bm25['relevance']:
            bm25_auto_total += 1
            if gt['relevance'] == 'relevant':
                bm25_auto_correct += 1  # only if both said relevant

    # --- 3. BM25 Manual Judgments (your 12 reviewed queries) ---
    # Format: query_id -> correct label for BM25 (0 = not relevant, 1 = relevant)
    bm25_manual_labels = {
        93: 0,
        151: 0,
        16: 0,
        37: 0,
        188: 0,
        146: 0,
        321: 1,
        136: 0,
        244: 1,
        104: 0,
        335: 0,
        210: 0
    }

    bm25_manual_total = len(bm25_manual_labels)
    bm25_manual_correct = 0

    for entry in annotations:
        if entry['doc_type'] != 'top1_bm25':
            continue
        qid = int(entry['query_id'])
        if qid in bm25_manual_labels:
            annotator_label = 1 if entry['relevance'] == 'relevant' else 0
            if annotator_label == bm25_manual_labels[qid]:
                bm25_manual_correct += 1

    # Final totals
    total_correct = trusted_correct + bm25_auto_correct + bm25_manual_correct
    total_total = trusted_total + bm25_auto_total + bm25_manual_total
    final_accuracy = total_correct / total_total

    # --- PRINT RESULTS ---
    print(f"Trusted (GT + Random):      {trusted_correct}/{trusted_total}")
    print(f"BM25 Auto-agreement:        {bm25_auto_correct}/{bm25_auto_total}")
    print(f"BM25 Manual Judged:         {bm25_manual_correct}/{bm25_manual_total}")
    print(f"\n→ Estimated Annotator Accuracy: {final_accuracy:.3f}")

if __name__ == "__main__":
    main()
