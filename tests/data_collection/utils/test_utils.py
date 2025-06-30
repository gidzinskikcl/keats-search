from data_collection import schemas
from datetime import timedelta
from data_collection.utils import utils


def test_document_to_dict_with_timestamp():
    doc = schemas.DocumentSchema(
        doc_id="doc123",
        content="This is content.",
        title="Lecture 1",
        timestamp=schemas.Timestamp(start=timedelta(seconds=10), end=timedelta(seconds=20)),
        pageNumber=1,
        keywords=["test", "lecture"],
        doc_type=schemas.MaterialType.SLIDES,
        speaker="Dr. Smith",
        course_name="CS101"
    )

    result = utils.document_to_dict(doc)
    expected = {
        "doc_id": "doc123",
        "content": "This is content.",
        "title": "Lecture 1",
        "timestamp": {
            "start": 10.0,
            "end": 20.0
        },
        "pageNumber": 1,
        "keywords": ["test", "lecture"],
        "doc_type": "pdf",
        "speaker": "Dr. Smith",
        "course_name": "CS101"
    }

    assert result == expected


def test_document_to_dict_without_timestamp():
    doc = schemas.DocumentSchema(
        doc_id="doc456",
        content="Another document.",
        title="Lecture 2",
        timestamp=None,
        pageNumber=2,
        keywords=[],
        doc_type=schemas.MaterialType.TRANSCRIPT,
        speaker="N/A",
        course_name="ML202"
    )

    result = utils.document_to_dict(doc)
    expected = {
        "doc_id": "doc456",
        "content": "Another document.",
        "title": "Lecture 2",
        "timestamp": None,
        "pageNumber": 2,
        "keywords": [],
        "doc_type": "srt",
        "speaker": "N/A",
        "course_name": "ML202"
    }

    assert result == expected
