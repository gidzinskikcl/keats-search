import json
import pathlib
import statistics
from typing import Union
import pandas as pd

from datetime import datetime

from llm_annotation.prompts import templates
from services.llm_based import client as llm_client
from llm_annotation.llm import annotator

from sklearn.metrics import cohen_kappa_score, mean_absolute_error

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# OUTPUT_REPO = pathlib.Path(f"keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-03_22-22-52/results/{TIMESTAMP}")
# OUTPUT_REPO = pathlib.Path(f"keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-04_19-29-24/results/{TIMESTAMP}")
OUTPUT_REPO = pathlib.Path(
    f"keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-06_14-54-56/results/{TIMESTAMP}"
)


# SAMPLE_DIR = pathlib.Path("keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-03_22-22-52")
# SAMPLE_DIR = pathlib.Path("keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-04_19-29-24")
SAMPLE_DIR = pathlib.Path(
    "keats-search-eval/data/evaluation/llm-annotated/benchmarking/sample/2025-07-06_14-54-56"
)


SAMPLE_FILE = SAMPLE_DIR / "benchmark_samples.json"
PROMPT_VARIANTS = [
    templates.V1,
    templates.V2,
    templates.V3,
    templates.V4,
    # templates.V5,
    # templates.V6,
    # templates.V7,
    # templates.V8
]


def record_token_usage(
    token_usage: list[dict[str, Union[str, int]]], output_repo: pathlib.Path
) -> None:
    prompt_tokens = []
    completion_tokens = []
    total_tokens = []
    costs = []
    for tu in token_usage:
        prompt_tokens.append(tu["prompt_tokens"])
        completion_tokens.append(tu["completion_tokens"])
        total_tokens.append(tu["total_tokens"])
        cost = round(
            (tu["prompt_tokens"] / 1000) * 0.005
            + (tu["completion_tokens"] / 1000) * 0.02,
            6,
        )  # GPT-4o
        costs.append(cost)

    # Compute sums, averages, medians
    summary = {
        "total_prompt_tokens": sum(prompt_tokens),
        "total_completion_tokens": sum(completion_tokens),
        "total_tokens": sum(total_tokens),
        "total_cost_usd": round(sum(costs), 6),
        "average_prompt_tokens": round(statistics.mean(prompt_tokens), 2),
        "average_completion_tokens": round(statistics.mean(completion_tokens), 2),
        "average_total_tokens": round(statistics.mean(total_tokens), 2),
        "average_cost_usd": round(statistics.mean(costs), 6),
        "median_prompt_tokens": round(statistics.median(prompt_tokens), 2),
        "median_completion_tokens": round(statistics.median(completion_tokens), 2),
        "median_total_tokens": round(statistics.median(total_tokens), 2),
        "median_cost_usd": round(statistics.median(costs), 6),
    }

    # Save to JSON
    token_usage_file = pathlib.Path(output_repo) / f"token_usage.json"
    with open(token_usage_file, "w", encoding="utf-8") as f:
        json.dump(token_usage, f, indent=2)

    summary_file = pathlib.Path(output_repo) / f"token_usage_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSaved token usage to {token_usage_file}")
    print(f"\nSaved token usage summary to {summary_file}")


def _save_annotations(annotated: list[dict], output_repo: pathlib.Path) -> None:
    output_repo.mkdir(parents=True, exist_ok=True)
    output_file = output_repo / f"annotated.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(annotated, f, indent=2)
    print(f"Saved structured results to {output_file}")


def annotate_for_variant(prompt_variant: templates.PromptTemplate) -> None:
    prompt_name = prompt_variant.VARIANT
    output_repo = OUTPUT_REPO / f"{prompt_name}"

    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        sample = json.load(f)

    client = llm_client.load_openai_client()
    annotated = []
    token_usage = []

    for idx, s in enumerate(sample, 1):
        query_id = s["query_id"]
        question = s["question"]
        print(
            f"[{idx}/{len(sample)}] Annotating for query ID: {query_id} using prompt variant: {prompt_name}"
        )

        for doc_type in ["ground_truth", "top1_bm25", "random_doc"]:
            doc = s[doc_type]
            try:
                result = annotator.annotate(
                    client=client,
                    prompt_module=prompt_variant,
                    course_name=doc["course"],
                    lecture_name=doc["lecture"],
                    question=question,
                    answer=doc["content"],
                )

                if result:
                    result["query_id"] = query_id
                    result["doc_id"] = doc["doc_id"]
                    result["doc_type"] = doc_type
                    annotated.append(result)

                    token_usage_per_prompt = {
                        "query_id": query_id,
                        "doc_id": doc["doc_id"],
                        "prompt_tokens": result["tokens"]["prompt_tokens"],
                        "completion_tokens": result["tokens"]["completion_tokens"],
                        "total_tokens": result["tokens"]["total_tokens"],
                    }
                    token_usage.append(token_usage_per_prompt)

            except Exception as e:
                print(f"Failed annotation for query {query_id} - {doc_type}: {e}")

    # Save results
    _save_annotations(annotated=annotated, output_repo=output_repo)
    record_token_usage(token_usage=token_usage, output_repo=output_repo)


def evaluate_annotations(
    output_repo: pathlib.Path, prompt_variant: templates.PromptTemplate
) -> None:
    prompt_name = prompt_variant.VARIANT
    result_file = output_repo / prompt_name / "annotated.json"

    with open(result_file, "r", encoding="utf-8") as f:
        annotations = json.load(f)

    rand_rel_path = SAMPLE_DIR / "random_doc_relevance.json"
    with open(rand_rel_path, "r", encoding="utf-8") as f:
        random_doc_relevance = json.load(f)

    relevance_map = {
        f"{entry['query_id']}": entry["relevance"] for entry in random_doc_relevance
    }

    correct = 0
    total = 0
    gold_labels = []
    predicted_labels = []

    for entry in annotations:
        doc_type = entry["doc_type"]
        predicted = 1 if entry["relevance"] == "relevant" else 0
        query_id = entry["query_id"]

        if doc_type in ("ground_truth", "top1_bm25"):
            expected = 1
        elif doc_type == "random_doc":
            key = f"{query_id}"
            rel_value = relevance_map[key]
            if rel_value is None:
                print(
                    f"Missing relevance label for random_doc {key} — assuming not relevant"
                )
                expected = 0
            elif rel_value == "relevant":
                expected = 1
            elif rel_value == "notrelevant":
                expected = 0
            else:
                raise ValueError(
                    f"Unexpected relevance value: {rel_value} for key {key}"
                )
        else:
            raise ValueError(f"Unknown doc_type: {doc_type}")

        gold_labels.append(expected)
        predicted_labels.append(predicted)
        if predicted == expected:
            correct += 1
        total += 1

    accuracy = correct / total if total > 0 else 0.0
    percentage = round(accuracy * 100, 2)

    # Cohen’s Kappa
    kappa = cohen_kappa_score(gold_labels, predicted_labels)

    # MAE
    mae = mean_absolute_error(gold_labels, predicted_labels)

    print(f"\nEvaluation for prompt variant '{prompt_name}':")
    print(f"Total annotations: {total}")
    print(f"Correct annotations: {correct}")
    print(f"Accuracy: {accuracy:.4f} ({percentage}%)")
    print(f"Cohen's Kappa: {kappa:.4f}")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")

    # Save to JSON
    eval_result = {
        "total": total,
        "correct": correct,
        "accuracy": round(accuracy, 4),
        "cohen_kappa": round(kappa, 4),
        "mae": round(mae, 4),
    }
    with open(
        output_repo / prompt_name / "evaluation.json", "w", encoding="utf-8"
    ) as f:
        json.dump(eval_result, f, indent=2)


def summarize_all_results(output_repo: pathlib.Path) -> pd.DataFrame:
    rows = []

    for variant in PROMPT_VARIANTS:
        prompt_name = variant.VARIANT
        eval_file = output_repo / prompt_name / "evaluation.json"

        if eval_file.exists():
            with open(eval_file, "r", encoding="utf-8") as f:
                result = json.load(f)
            result["variant"] = prompt_name
            rows.append(result)

    df = pd.DataFrame(rows)
    df = df[["variant", "accuracy", "cohen_kappa", "mae"]]
    return df


def write_readme_with_rankings(df: pd.DataFrame, output_repo: pathlib.Path):
    df_sorted_acc = df.sort_values(by="accuracy", ascending=False)
    df_sorted_kappa = df.sort_values(by="cohen_kappa", ascending=False)
    df_sorted_mae = df.sort_values(by="mae", ascending=True)

    readme_path = output_repo / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Evaluation Summary\n\n")

        # Full table
        f.write("## Evaluation Table\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n")

        # Rankings
        f.write("## Rankings\n\n")

        f.write("### Accuracy Ranking\n")
        f.write(
            "\n".join(
                f"{i+1}. {row['variant']} ({row['accuracy']:.4f})"
                for i, row in df_sorted_acc.iterrows()
            )
        )
        f.write("\n\n")

        f.write("### Cohen's Kappa Ranking\n")
        f.write(
            "\n".join(
                f"{i+1}. {row['variant']} ({row['cohen_kappa']:.4f})"
                for i, row in df_sorted_kappa.iterrows()
            )
        )
        f.write("\n\n")

        f.write("### Mean Absolute Error (MAE) Ranking\n")
        f.write(
            "\n".join(
                f"{i+1}. {row['variant']} ({row['mae']:.4f})"
                for i, row in df_sorted_mae.iterrows()
            )
        )
        f.write("\n")


def summarize_token_usage(output_repo: pathlib.Path) -> pd.DataFrame:
    rows = []

    for variant in PROMPT_VARIANTS:
        prompt_name = variant.VARIANT
        usage_summary_file = output_repo / prompt_name / "token_usage_summary.json"

        if usage_summary_file.exists():
            with open(usage_summary_file, "r", encoding="utf-8") as f:
                usage = json.load(f)
            usage["variant"] = prompt_name
            rows.append(usage)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    cols = ["variant"] + [c for c in df.columns if c != "variant"]
    return df[cols]


def main():
    for variant in PROMPT_VARIANTS:
        annotate_for_variant(variant)
        evaluate_annotations(output_repo=OUTPUT_REPO, prompt_variant=variant)

    df = summarize_all_results(OUTPUT_REPO)
    df.to_csv(OUTPUT_REPO / "evaluation_summary.csv", index=False)

    df_tokens = summarize_token_usage(OUTPUT_REPO)
    df_tokens.to_csv(OUTPUT_REPO / "token_usage_summary.csv", index=False)

    write_readme_with_rankings(df, OUTPUT_REPO)


if __name__ == "__main__":
    main()
