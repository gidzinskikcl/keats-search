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

    observed = utils.document_to_dict(doc)
    expected = {
        "documentId": "doc123",
        "content": "This is content.",
        "title": "Lecture 1",
        "start": "00:00:10",
        "end": "00:00:20",
        "slideNumber": 1,
        "keywords": ["test", "lecture"],
        "type": "SLIDE",
        "speaker": "Dr. Smith",
        "courseName": "CS101"
    }

    assert observed == expected


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

    observed = utils.document_to_dict(doc)
    expected = {
        "documentId": "doc456",
        "content": "Another document.",
        "title": "Lecture 2",
        "start": None,
        "end": None,
        "slideNumber": 2,
        "keywords": [],
        "type": "VIDEO_TRANSCRIPT",
        "speaker": "N/A",
        "courseName": "ML202"
    }

    assert observed == expected
