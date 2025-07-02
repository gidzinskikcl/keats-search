import json
import pytest
from unittest.mock import patch

from benchmarking.schemas import schemas
from benchmarking.models.lucene import dirichlet


@pytest.fixture
def sample_query():
    return schemas.Query(id="q1", question="search engine")


@pytest.fixture
def sample_java_output():
    return json.dumps([
        {"documentId": "doc1", "content": "Lucene is a full-text search engine.", "courseName": "Information Retrieval", "title": "Lecture 12"},
        {"documentId": "doc2", "content": "It supports ranking, indexing, and search queries.", "courseName": "Information Retrieval", "title": "Lecture 12"}
    ])


def test_search(sample_query, sample_java_output):
    engine = dirichlet.DirichletSearchEngine(jar_path="dummy/path/to/jar", doc_path="dummy/path/to/documents.json")

    # Patch subprocess.run to simulate Java execution
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = sample_java_output
        
        result = engine.search(query=sample_query)

        mock_run.assert_called_with(
            [
                "java",
                "-jar", "dummy/path/to/jar",
                "dummy/path/to/documents.json",
                "search engine",
                "dirichlet"
            ],
            capture_output=True,
            text=True
        )

        assert isinstance(result, list)
        assert all(isinstance(d, schemas.Document) for d in result)
        assert len(result) == 2
        assert result[0].doc_id == "doc1"
        assert "Lucene" in result[0].content

