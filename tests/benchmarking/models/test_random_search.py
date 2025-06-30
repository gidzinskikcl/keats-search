import json
import tempfile
from benchmarking.schemas import schemas
from benchmarking.models import random_search


def test_random_search_engine_returns_all_documents():
    # Create a temporary JSON document file
    test_docs = [
        {"documentId": "doc1", "content": "First doc"},
        {"documentId": "doc2", "content": "Second doc"},
        {"documentId": "doc3", "content": "Third doc"},
    ]

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
        json.dump(test_docs, tmp_file)
        tmp_file.flush()

        engine = random_search.RandomSearchEngine(doc_path=tmp_file.name)
        query = schemas.Query(id="q1", question="anything")

        results = engine.search(query)

        # Check type and size
        assert isinstance(results, list)
        assert len(results) == len(test_docs)

        # Check types of elements
        assert all(isinstance(doc, schemas.Document) for doc in results)

        # Check that all doc IDs are returned, just in random order
        returned_ids = set(doc.doc_id for doc in results)
        expected_ids = set(doc["documentId"] for doc in test_docs)
        assert returned_ids == expected_ids
