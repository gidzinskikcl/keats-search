from unittest.mock import MagicMock
import pytest
from benchmarking.models.lucene import lucene_model
from benchmarking.schemas import schemas


@pytest.fixture
def expected():
    result = [
        schemas.Document(doc_id="doc1", content="This is document 1"),
        schemas.Document(doc_id="doc2", content="This is document 2"),
    ]
    return result


def test_search_(expected):
    mock_client = MagicMock()
    mock_client.search.return_value = [
        {"documentId": "doc1", "content": "This is document 1"},
        {"documentId": "doc2", "content": "This is document 2"},
    ]

    model = lucene_model.LuceneModel(client=mock_client)
    query = schemas.Query(id="q1", question="what is dna")

    observed = model.search(query)

    assert observed == expected
