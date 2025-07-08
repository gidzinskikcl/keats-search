import json
import tempfile
from schemas import schemas
from benchmarking.models import random_search


def test_random_search_engine_returns_ten_search_results():
    # Create a temporary JSON document file with 15 docs
    test_docs = [
        {
            "documentId": f"doc{i}",
            "content": f"Content {i}",
            "courseName": f"Course {i}",
            "title": f"Lecture {i}",
            "start": "00:00:00",
            "end": "00:01:00",
            "slideNumber": i,
            "keywords": [],
            "type": "SLIDE",
            "speaker": f"Speaker {i}",
        }
        for i in range(15)
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

        # Check that each result is a SearchResult with a DocumentSchema
        assert all(isinstance(res, schemas.SearchResult) for res in results)
        assert all(isinstance(res.document, schemas.DocumentSchema) for res in results)

        # Ensure all returned IDs are from the corpus
        returned_ids = {res.document.doc_id for res in results}
        expected_ids = {doc["documentId"] for doc in test_docs}
        assert returned_ids.issubset(expected_ids)
