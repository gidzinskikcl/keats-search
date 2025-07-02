import csv
import os
import json
import logging
import pandas as pd

from benchmarking.schemas import schemas

def save_evaluation_results(model_name: str, mean_metrics: dict, per_query_metrics, output_dir: str, k: int):
    """
    Saves evaluation results to a JSON file (mean metrics) and a CSV file (per-query metrics).
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save mean metrics to JSON
    json_path = os.path.join(output_dir, f"{model_name}_mean_metrics@k={k}.json")
    with open(json_path, "w") as f:
        json.dump(mean_metrics, f, indent=4)

    # Save per-query metrics to CSV
    csv_path = os.path.join(output_dir, f"{model_name}_per_query_metrics@k={k}.csv")

    if isinstance(per_query_metrics, dict):
        # If it's already metric → query → score
        df = pd.DataFrame.from_dict(per_query_metrics, orient="index")
        df.index.name = "metric"
        df.reset_index(inplace=True)
    else:
        # Assume it's a list of query dicts
        from collections import defaultdict
        metric_rows = defaultdict(dict)
        for query_result in per_query_metrics:
            query_id = query_result.get("query_id")
            for metric, value in query_result.items():
                if metric != "query_id":
                    metric_rows[metric][query_id] = value
        df = pd.DataFrame.from_dict(metric_rows, orient="index")
        df.index.name = "metric"
        df.reset_index(inplace=True)

    df.to_csv(csv_path, index=False)

def _clean(value):
    if isinstance(value, str):
        return value.replace('\x00', '')  # remove null byte if present
    return value

def save_predictions(
    output_path: str,
    model_name: str,
    predictions: dict[str, dict[str, str | list[schemas.Document]]]
):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(
            csvfile,
            quoting=csv.QUOTE_ALL,      # wrap all fields in quotes
            escapechar='\\',            # allow escaping special characters
            quotechar='"'   
        )
        writer.writerow([
            "query_id", 
            "question", 
            "answer",
            "relevance_score", 
            "rank", 
            "model", 
            "doc_id",
            "course",
            "lecture"
        ])

        for qid, p in predictions.items():
            for rank, doc in enumerate(p["results"], start=1):
                try:
                    writer.writerow([
                        _clean(qid),
                        _clean(p["question"]),
                        _clean(doc.content),
                        _clean(doc.score),
                        rank,
                        _clean(model_name),
                        _clean(doc.doc_id),
                        _clean(doc.course),
                        _clean(doc.lecture)
                    ])
                except Exception as e:
                    logging.error(f"Failed to write row for query {qid}, doc: {doc.doc_id}. Error: {e}")
                    raise
