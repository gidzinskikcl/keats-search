import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

import config
from main import app  # Adjust if router is in another module

client = TestClient(app)


@pytest.fixture
def sample_docs(tmp_path):
    docs = [
        {
            "course_id": "CS101",
            "lecture_id": "1",
            "doc_id": "doc1",
            "doc_type": "pdf",
            "url": "https://example.com/doc1",
            "thumnail_url": None,
        },
        {
            "course_id": "CS101",
            "lecture_id": "1",
            "doc_id": "doc2",
            "doc_type": "srt",
            "url": "https://example.com/doc2",
            "thumnail_url": "https://example.com/img2",
        },
        {
            "course_id": "CS102",
            "lecture_id": "2",
            "doc_id": "doc3",
            "doc_type": "pdf",
            "url": "https://example.com/doc2",
            "thumnail_url": "https://example.com/img3",
        },
    ]
    doc_path = tmp_path / "documents.json"
    doc_path.write_text(json.dumps(docs))

    config.settings.DOC_PATH = str(doc_path)

    return docs


@pytest.fixture
def expected():
    results = [
        {
            "lecture": "1",
            "files": [
                {
                    "doc_id": "doc1",
                    "doc_type": "pdf",
                    "url": "https://example.com/doc1",
                    "thumbnail_url": None,
                },
                {
                    "doc_id": "doc2",
                    "doc_type": "srt",
                    "url": "https://example.com/doc2",
                    "thumbnail_url": "https://example.com/img2",
                },
            ],
        },
        {
            "lecture": "2",
            "files": [
                {
                    "doc_id": "doc3",
                    "doc_type": "pdf",
                    "url": "https://example.com/doc22",
                    "thumbnail_url": None,
                }
            ],
        },
    ]
    return results


@pytest.fixture
def expected_courses():
    return [
        {"course_id": "1.234", "course_title": "Intro to CS"},
        {"course_id": "2.567", "course_title": "Machine Learning"},
    ]


@patch("routes.metadata.subprocess.run")
def test_list_courses(mock_run, expected_courses):
    mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(expected_courses))

    response = client.get("/courses")
    assert response.status_code == 200
    assert response.json() == expected_courses


@patch("routes.metadata.subprocess.run")
def test_list_files_all(mock_run, sample_docs, expected):
    mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(expected))

    response = client.get("/files")
    assert response.status_code == 200
    assert response.json() == expected


@patch("routes.metadata.subprocess.run")
def test_list_files_filtered(mock_run, sample_docs):
    expected = [
        {
            "lecture": "1",
            "files": [
                {
                    "doc_id": "doc1",
                    "doc_type": "pdf",
                    "url": "https://example.com/doc1",
                    "thumbnail_url": None,
                },
                {
                    "doc_id": "doc2",
                    "doc_type": "srt",
                    "url": "https://example.com/doc2",
                    "thumbnail_url": "https://example.com/img2",
                },
            ],
        }
    ]

    mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(expected))

    response = client.get("/files", params={"course": "CS101", "lecture": 1})
    assert response.status_code == 200
    assert response.json() == expected


@pytest.fixture
def expected_lectures():
    return [
        {"lecture_id": "1", "lecture_title": "lecture 1"},
        {"lecture_id": "2", "lecture_title": "lecture 2"},
    ]


@patch("routes.metadata.subprocess.run")
def test_list_lectures_all(mock_run, expected_lectures):
    mock_run.return_value = MagicMock(
        returncode=0, stdout=json.dumps(expected_lectures)
    )

    response = client.get("/lectures")
    assert response.status_code == 200
    assert response.json() == expected_lectures
