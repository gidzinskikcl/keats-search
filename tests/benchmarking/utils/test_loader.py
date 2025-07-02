import io
import json
import unittest
import tempfile
import os
import csv

from benchmarking.utils import loader
from benchmarking.schemas import schemas

from collections import OrderedDict

def test_load_queries(tmp_path):
    data = [
        {"id": "q1", "question": "heap vs stack"},
        {"id": "q2", "question": "process vs thread"}
    ]
    file_path = tmp_path / "queries.json"
    with open(file_path, "w") as f:
        json.dump(data, f)

    observed = loader.load_queries(str(file_path))
    expected = [
        schemas.Query(id="q1", question="heap vs stack"),
        schemas.Query(id="q2", question="process vs thread"),
    ]

    assert observed == expected


def test_load_ground_truth(tmp_path):
    data = {
        "q1": {
            "query": "heap vs stack",
            "query_id": "q1",
            "relevance_scores": {
                "doc1": "HIGHLY_RELEVANT",
                "doc3": "MODERATELY_RELEVANT"
            }
        },
        "q2": {
            "query": "process vs thread",
            "query_id": "q2",
            "relevance_scores": {
                "doc2": "SLIGHTLY_RELEVANT",
                "doc4": "IRRELEVANT"
            }
        }
    }

    file_path = tmp_path / "ground_truth.json"
    with open(file_path, "w") as f:
        json.dump(data, f)

    observed = loader.load_ground_truth(str(file_path))

    expected = schemas.GroundTruth(entries={
        "q1": schemas.GroundTruthEntry(
            query="heap vs stack",
            query_id="q1",
            relevance_scores=OrderedDict({
                "doc1": schemas.RelevanceScore.HIGHLY_RELEVANT,
                "doc3": schemas.RelevanceScore.MODERATELY_RELEVANT
            })
        ),
        "q2": schemas.GroundTruthEntry(
            query="process vs thread",
            query_id="q2",
            relevance_scores=OrderedDict({
                "doc2": schemas.RelevanceScore.SLIGHTLY_RELEVANT,
                "doc4": schemas.RelevanceScore.IRRELEVANT
            })
        )
    })

    assert observed == expected


def test_load_valid_queries_from_csv(monkeypatch):
    csv_content = """index,question,answer,label,difficulty,course_name,lecture_title,doc_id
1,What is Python?,Python is a programming language.,valid,easy,CS101,Intro to Python,D1
2,What is Java?,Java is also a language.,invalid,medium,CS101,Intro to Java,D2
3,What is AI?,AI is the field of study.,valid,hard,CS102,AI Basics,D3
"""


    mock_csv_file = io.StringIO(csv_content)

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: mock_csv_file)

    expected = [
        schemas.Query(id="1", question="What is Python?"),
        schemas.Query(id="3", question="What is AI?"),
    ]

    observed = loader.load_valid_queries_from_csv("dummy_path.csv")
    assert observed == expected



# Function under test
def load_ground_truth_pairs(csv_path: str) -> set[tuple[str, str]]:
    relevant_pairs = set()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["label"].strip().lower() == "valid":
                qid = row["index"].strip()
                doc_id = row["doc_id"].strip()
                relevant_pairs.add((qid, doc_id))
    return relevant_pairs

class TestLoadGroundTruthPairs(unittest.TestCase):

    def setUp(self):
        # Create a temporary CSV file with sample rows
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", newline='', suffix=".csv")
        fieldnames = ["index", "question", "answer", "label", "course_name", "lecture_title", "doc_id"]
        writer = csv.DictWriter(self.temp_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([
            {"index": "Q1", "question": "What is AI?", "answer": "AI is...", "label": "valid", "course_name": "CS", "lecture_title": "Intro", "doc_id": "D1"},
            {"index": "Q1", "question": "What is AI?", "answer": "AI is...", "label": "invalid", "course_name": "CS", "lecture_title": "Intro", "doc_id": "D2"},
            {"index": "Q2", "question": "What is ML?", "answer": "ML is...", "label": "VALID", "course_name": "CS", "lecture_title": "Intro", "doc_id": "D3"},
            {"index": "Q2", "question": "What is ML?", "answer": "ML is...", "label": "not labelled", "course_name": "CS", "lecture_title": "Intro", "doc_id": "D4"},
        ])
        self.temp_file.close()  # Close to flush contents

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_loads_only_valid_labels(self):
        expected = {("Q1", "D1"), ("Q2", "D3")}
        result = load_ground_truth_pairs(self.temp_file.name)
        self.assertEqual(result, expected)

    def test_returns_empty_set_if_no_valid(self):
        # Overwrite with all invalid rows
        with open(self.temp_file.name, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["index", "question", "answer", "label", "course_name", "lecture_title", "doc_id"])
            writer.writeheader()
            writer.writerows([
                {"index": "Q1", "question": "", "answer": "", "label": "not relevant", "course_name": "", "lecture_title": "", "doc_id": "D1"},
                {"index": "Q2", "question": "", "answer": "", "label": "invalid", "course_name": "", "lecture_title": "", "doc_id": "D2"},
            ])
        result = load_ground_truth_pairs(self.temp_file.name)
        self.assertEqual(result, set())

if __name__ == '__main__':
    unittest.main()
