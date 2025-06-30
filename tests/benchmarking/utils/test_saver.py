import os
import json
import pandas as pd
import tempfile
from benchmarking.utils import saver

def test_save_evaluation_results():
    model_name = "TestModel"
    mean_metrics = {"Precision": 0.8, "MRR": 0.75}
    per_query_metrics = [
        {"query_id": "q1", "Precision": 1.0, "MRR": 1.0},
        {"query_id": "q2", "Precision": 0.6, "MRR": 0.5},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        saver.save_evaluation_results(model_name, mean_metrics, per_query_metrics, tmpdir)

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
        assert set(df.columns) == expected_columns, f"CSV columns mismatch: {df.columns}"

        # Convert to dict for easier checking
        rows = {row["metric"]: row for _, row in df.iterrows()}

        assert "Precision" in rows
        assert rows["Precision"]["q1"] == 1.0
        assert rows["Precision"]["q2"] == 0.6

        assert "MRR" in rows
        assert rows["MRR"]["q1"] == 1.0
        assert rows["MRR"]["q2"] == 0.5
