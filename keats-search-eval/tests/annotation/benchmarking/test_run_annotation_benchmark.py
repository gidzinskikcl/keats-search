import json
import pathlib
import tempfile
import statistics
from unittest import mock

from llm_annotation.benchmarking import run_annotation_benchmark


# We'll patch OUTPUT_REPO to point to a temp dir
@mock.patch(
    "llm_annotation.benchmarking.run_annotation_benchmark.OUTPUT_REPO",
    new_callable=lambda: tempfile.mkdtemp(),
)
def test_record_token_usage(mock_output_repo):

    test_data = [
        {"prompt_tokens": 1000, "completion_tokens": 500, "total_tokens": 1500},
        {"prompt_tokens": 2000, "completion_tokens": 1000, "total_tokens": 3000},
        {"prompt_tokens": 1500, "completion_tokens": 750, "total_tokens": 2250},
    ]

    run_annotation_benchmark.record_token_usage(test_data, mock_output_repo)

    usage_path = pathlib.Path(mock_output_repo) / "token_usage.json"
    summary_path = pathlib.Path(mock_output_repo) / "token_usage_summary.json"

    # Check that both files exist
    assert usage_path.exists(), "Token usage file not created."
    assert summary_path.exists(), "Token usage summary file not created."

    # Check usage file contents
    with open(usage_path, "r", encoding="utf-8") as f:
        saved_usage = json.load(f)
    assert saved_usage == test_data, "Saved token usage does not match input."

    # Compute expected summary
    prompt = [1000, 2000, 1500]
    completion = [500, 1000, 750]
    total = [1500, 3000, 2250]
    costs = [
        round((p / 1000) * 0.005 + (c / 1000) * 0.02, 6)
        for p, c in zip(prompt, completion)
    ]

    expected_summary = {
        "total_prompt_tokens": sum(prompt),
        "total_completion_tokens": sum(completion),
        "total_tokens": sum(total),
        "total_cost_usd": round(sum(costs), 6),
        "average_prompt_tokens": round(statistics.mean(prompt), 2),
        "average_completion_tokens": round(statistics.mean(completion), 2),
        "average_total_tokens": round(statistics.mean(total), 2),
        "average_cost_usd": round(statistics.mean(costs), 6),
        "median_prompt_tokens": round(statistics.median(prompt), 2),
        "median_completion_tokens": round(statistics.median(completion), 2),
        "median_total_tokens": round(statistics.median(total), 2),
        "median_cost_usd": round(statistics.median(costs), 6),
    }

    # Check summary contents
    with open(summary_path, "r", encoding="utf-8") as f:
        saved_summary = json.load(f)
    assert saved_summary == expected_summary, "Summary file contents incorrect."
