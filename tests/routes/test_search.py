import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)


@pytest.fixture
def expected():
    return [
        {
            "document": {
                "id": "0",
                "doc_id": "doc1",
                "content": "Quick sort is efficient.",
                "course_name": "Introduction to Computer Science",
                "lecture_title": "Lecture 1",
                "course_id": "CS101",
                "lecture_id": "lecture_1",
                "timestamp": {"start": "00:00:00", "end": "00:02:00"},
                "page_number": 1,
                "doc_type": "mp4",
            },
            "score": 0.95,
        }
    ]


@patch("services.bm25_engine.BM25SearchEngine.search")
def test_search_success(mock_search, expected):
    mock_search.return_value = expected

    payload = {
        "query": {"question": "quick sort"},
        "filters": {
            "course_names": ["CS101"],
            "lecture_titles": ["Lecture 1"],
            "doc_ids": ["doc1"],
        },
    }

    response = client.post("/search", json=payload)
    assert response.status_code == 200
    observed = response.json()
    assert observed == expected
