from datetime import timedelta
import json
import pytest
from unittest.mock import patch

from schemas import schemas
from benchmarking.models.lucene import boolean


@pytest.fixture
def sample_query():
    return schemas.Query(id="q1", question="search engine")


@pytest.fixture
def sample_java_output():
    return json.dumps([
        {
            "documentId": "doc1",
            "content": "Lucene is a full-text search engine.",
            "courseName": "Algorithms",
            "title": "Lecture 1",
            "start": "00:00:00",
            "end": "00:01:30",
            "slideNumber": 1,
            "keywords": ["search", "indexing"],
            "type": "SLIDE",
            "speaker": "Prof. A",
            "score": 2.1
        },
        {
            "documentId": "doc2",
            "content": "It supports ranking, indexing, and search queries.",
            "courseName": "Algorithms",
            "title": "Lecture 1",
            "start": None,
            "end": None,
            "slideNumber": 2,
            "keywords": [],
            "type": "SLIDE",
            "speaker": "Prof. B",
            "score": 1.8
        }
    ])

@pytest.fixture
def expected():
    result = [
            schemas.SearchResult(
                document=schemas.DocumentSchema(
                    doc_id="doc1",
                    content="Lucene is a full-text search engine.",
                    course_name="Algorithms",
                    title="Lecture 1",
                    timestamp=schemas.Timestamp(start=timedelta(minutes=0), end=timedelta(minutes=1, seconds=30)),
                    pageNumber=1,
                    keywords=["search", "indexing"],
                    doc_type=schemas.MaterialType.SLIDES,
                    speaker="Prof. A"
                ),
                score=2.1
            ),
            schemas.SearchResult(
                document=schemas.DocumentSchema(
                    doc_id="doc2",
                    content="It supports ranking, indexing, and search queries.",
                    course_name="Algorithms",
                    title="Lecture 1",
                    timestamp=schemas.Timestamp(start=None, end=None),
                    pageNumber=2,
                    keywords=[],
                    doc_type=schemas.MaterialType.SLIDES,
                    speaker="Prof. B"
                ),
                score=1.8
            )
    ]
    return result

def test_search(sample_query, sample_java_output, expected):
    engine = boolean.BooleanSearchEngine(doc_path="dummy/path/to/documents.json", k=5)

    # Patch subprocess.run to simulate Java execution
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = sample_java_output
        
        observed = engine.search(query=sample_query)

        mock_run.assert_called_with(
            [
                "java",
                "-jar", "search_engines/lucene-search/target/boolean-search-jar-with-dependencies.jar",
                "dummy/path/to/documents.json",
                "search engine",
                "5"
            ],
            capture_output=True,
            text=True
        )

        assert observed == expected

