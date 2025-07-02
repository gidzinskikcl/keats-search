import json
import tempfile
from benchmarking.schemas import schemas
from benchmarking.models import random_search


def test_random_search_engine_returns_ten_documents():
    # Create a temporary JSON document file with 15 docs
    test_docs = [
        {"documentId": f"doc{i}", "content": f"Content {i}", "courseName": f"Course {i}", "title": f"Lecture {i}"} for i in range(15)
    ]

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
        json.dump(test_docs, tmp_file)
        tmp_file.flush()

        engine = random_search.RandomSearchEngine(doc_path=tmp_file.name)
        query = schemas.Query(id="q1", question="anything")

        results = engine.search(query)

        # Check that exactly 10 results are returned
        assert isinstance(results, list)
        assert len(results) == 10

        # Check types of elements
        assert all(isinstance(doc, schemas.Document) for doc in results)

        # Ensure all returned IDs are from the corpus
        returned_ids = set(doc.doc_id for doc in results)
        expected_ids = set(doc["documentId"] for doc in test_docs)
        assert returned_ids.issubset(expected_ids)
