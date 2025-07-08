import io
import json

from benchmarking.utils import loader
from schemas import schemas


def test_load_queries(tmp_path):
    data = [
        {"id": "q1", "question": "heap vs stack"},
        {"id": "q2", "question": "process vs thread"},
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
