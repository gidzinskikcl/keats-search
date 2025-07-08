import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def index_request_payload():
    return {
        "document_path": "dummy/path/docs.json",
        "index_dir": "dummy/path/index"
    }


@patch("services.lucene_indexer.LuceneIndexer.index")
def test_index_documents_(mock_index, index_request_payload):
    mock_index.return_value = None  # Simulate success

    response = client.post("/index", json=index_request_payload)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Indexing complete",
        "index_dir": index_request_payload["index_dir"]
    }
    mock_index.assert_called_once()


@patch("services.lucene_indexer.LuceneIndexer.index")
def test_index_documents_failure(mock_index, index_request_payload):
    mock_index.side_effect = RuntimeError("Simulated failure")

    response = client.post("/index", json=index_request_payload)

    assert response.status_code == 500
    assert "Simulated failure" in response.json()["detail"]
