from datetime import timedelta
import os
import json
import pandas as pd
import tempfile
from textwrap import dedent
import pytest
import csv

from benchmarking.utils import saver
from schemas import schemas


@pytest.mark.skip(reason="Not implemented yet")
def test_save_evaluation_results():
    model_name = "TestModel"
    mean_metrics = {"Precision": 0.8, "MRR": 0.75}
    per_query_metrics = [
        {"query_id": "q1", "Precision": 1.0, "MRR": 1.0},
        {"query_id": "q2", "Precision": 0.6, "MRR": 0.5},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        saver.save_evaluation_results(
            model_name, mean_metrics, per_query_metrics, tmpdir, 1
        )

        # Check if files exist
        json_path = os.path.join(tmpdir, f"{model_name}_mean_metrics.json")
        csv_path = os.path.join(tmpdir, f"{model_name}_per_query_metrics.csv")

        assert os.path.exists(json_path), "JSON file was not created."
        assert os.path.exists(csv_path), "CSV file was not created."

        # Validate JSON content
        with open(json_path, "r") as f:
            loaded_json = json.load(f)
        assert loaded_json == mean_metrics, "JSON content does not match."

        # Validate CSV structure and values
        df = pd.read_csv(csv_path)
        expected_columns = {"metric", "q1", "q2"}
        assert (
            set(df.columns) == expected_columns
        ), f"CSV columns mismatch: {df.columns}"

        # Convert to dict for easier checking
        rows = {row["metric"]: row for _, row in df.iterrows()}

        assert "Precision" in rows
        assert rows["Precision"]["q1"] == 1.0
        assert rows["Precision"]["q2"] == 0.6

        assert "MRR" in rows
        assert rows["MRR"]["q1"] == 1.0
        assert rows["MRR"]["q2"] == 0.5


def test_save_predictions():
    # Create a temporary output file
    with tempfile.NamedTemporaryFile(
        mode="r+", suffix=".csv", delete=False
    ) as tmp_file:
        output_path = tmp_file.name

    # Create a fake DocumentSchema and SearchResult
    doc = schemas.DocumentSchema(
        doc_id="doc123",
        content="Example content with null byte\x00 inside",
        course_name="CourseX",
        title="LectureY",
        timestamp=schemas.Timestamp(
            start=timedelta(minutes=0), end=timedelta(minutes=1)
        ),
        pageNumber=1,
        keywords=["test"],
        doc_type=schemas.MaterialType.SLIDES,
        speaker="Dr. X",
    )
    search_result = schemas.SearchResult(document=doc, score=0.987)

    # Sample predictions dict
    predictions = {"q1": {"question": "What is Lucene?", "results": [search_result]}}

    try:
        # Call the function
        saver.save_predictions(
            output_path=output_path, model_name="test_model", predictions=predictions
        )

        # Read the CSV back
        with open(output_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, quoting=csv.QUOTE_ALL, escapechar="\\")
            rows = list(reader)

        # Check headers and content
        assert rows[0] == [
            "query_id",
            "question",
            "answer",
            "relevance_score",
            "rank",
            "model",
            "doc_id",
            "course",
            "lecture",
        ]
        assert rows[1] == [
            "q1",
            "What is Lucene?",
            "Example content with null byte inside",
            "0.987",
            "1",
            "test_model",
            "doc123",
            "CourseX",
            "LectureY",
        ]
    finally:
        os.remove(output_path)  # Clean up temp file
