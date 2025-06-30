import pytest
from unittest.mock import patch, MagicMock
from benchmarking.models.lucene.lucene_client import LuceneClient


def test_search_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"documentId": "doc1", "score": 2.5},
        {"documentId": "doc2", "score": 1.8}
    ]

    with patch("requests.post", return_value=mock_response) as mock_post:
        client = LuceneClient("http://localhost:4567")
        results = client.search("what is dna")

        assert results == [
            {"documentId": "doc1", "score": 2.5},
            {"documentId": "doc2", "score": 1.8}
        ]

        mock_post.assert_called_once_with(
            "http://localhost:4567/search",
            json={"query": "what is dna", "topK": 10},
            timeout=5
        )
