import json
from datetime import timedelta
from unittest.mock import patch, MagicMock
import pytest

from core import schemas
from services import bm25_engine


@pytest.fixture
def dummy_query():
    return schemas.Query(id="q1", question="quick sort")


@pytest.fixture
def dummy_filters():
    return schemas.Filter(
        courses_ids=["CS101"], lectures_ids=["lecture_1"], doc_ids=["doc1"]
    )


@pytest.fixture
def dummy_java_output():
    return json.dumps(
        [
            {
                "iD": "0",
                "documentId": "doc1",
                "content": "Quick sort is efficient.",
                "courseName": "Introduction to Computer Science",
                "courseId": "CS101",
                "lectureTitle": "Lecture 1",
                "lectureId": "lecture_1",
                "start": "00:00:00",
                "end": "00:02:00",
                "pageNumber": 1,
                "type": "VIDEO_TRANSCRIPT",
                "score": 0.95,
                "url": "https://example.com/doc1",
                "thumbnailUrl": "https://example.com/thumbs/doc1.jpg",
            }
        ]
    )


@pytest.fixture
def expected():
    return [
        schemas.SearchResult(
            document=schemas.DocumentSchema(
                id="0",
                doc_id="doc1",
                content="Quick sort is efficient.",
                doc_type=schemas.MaterialType.TRANSCRIPT,
                course_id="CS101",
                course_name="Introduction to Computer Science",
                lecture_id="lecture_1",
                lecture_title="Lecture 1",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=0), end=timedelta(minutes=2)
                ),
                page_number=1,
                url="https://example.com/doc1",
                thumbnail_url="https://example.com/thumbs/doc1.jpg",
            ),
            score=0.95,
        )
    ]
    return result


@patch("subprocess.run")
def test_search(mock_run, dummy_query, dummy_filters, dummy_java_output, expected):
    mock_proc = MagicMock()
    mock_proc.returncode = 0
    mock_proc.stdout = dummy_java_output
    mock_run.return_value = mock_proc

    engine = bm25_engine.BM25SearchEngine("dummy.json")
    observed = engine.search(dummy_query, 5, dummy_filters)

    assert observed == expected


@patch("subprocess.run")
def test_search_raises_on_error(mock_run, dummy_query, dummy_filters):
    mock_proc = MagicMock()
    mock_proc.returncode = 1
    mock_proc.stderr = "Something went wrong"
    mock_run.return_value = mock_proc

    engine = bm25_engine.BM25SearchEngine("dummy.json")

    with pytest.raises(
        RuntimeError, match="Lucene search failed: Something went wrong"
    ):
        engine.search(dummy_query, 5, dummy_filters)


def test_serialize_filters(dummy_filters):
    engine = bm25_engine.BM25SearchEngine("dummy.json")
    result = engine._serialize_filters(dummy_filters)
    data = json.loads(result)

    assert data["courseId"] == ["CS101"]
    assert data["lectureId"] == ["lecture_1"]
    assert data["documentId"] == ["doc1"]
