import pytest

from documents.ppt import ppt_document_builder, ppt_document
from data_collection.segments import segment


@pytest.fixture
def data():
    result = {
        "doc_id": "7CCSMATAI_w1",
        "doc_title": "Lecture 1",
        "file_name": "lecture1.pptx",
        "file_extension": "pptx",
        "course_ids": ["7CCSMATAI"],
        "course_title": "Advanced Topics in AI",
        "admin_code": "24~25 SEM1 000001",
        "content_type": "TEXT",
        "authors": ["Prof. John Smith"],
        "lecturers": ["Prof. Adam Smith"],
        "created": "2025-04-21T12:01:23",
        "modified": "2025-06-15T06:045:53",
        "last_modified_by": "John Smith",
        "subject": "AI Topics",
        "keywords": "AI, machine learning, data science",
        "page_count": "10",
        "source": "King's College",
        "version": "1.0.0",
        "comments": "",
        "revision": "",
        "category": "",
        "content_status": "",
        "identifier": "",
        "language": "",
        "pages": [
                segment.Segment(
                    nr=2,
                    content="This is a transcript for video segment 2.",
                )
        ]
    }
    return result

@pytest.fixture
def expected(data):
    result = ppt_document.PPTDocument(
        doc_id=data["doc_id"],
        doc_title=data["doc_title"],
        file_name=data["file_name"],
        file_extension=data["file_extension"],
        course_ids=data["course_ids"],
        course_title=data["course_title"],
        admin_code=data["admin_code"],
        content_type=data["content_type"],
        authors=data["lecturers"],
        created=data["created"],
        modified=data["modified"],
        last_modified_by=data["last_modified_by"],
        subject=data["subject"],
        keywords=data["keywords"],
        page_count=data["page_count"],
        source=data["source"],
        version=data["version"],
        pages=data["pages"],
        comments=data["comments"],
        revision=data["revision"],
        category=data["category"],
        content_status=data["content_status"],
        identifier=data["identifier"],
        language=data["language"],

    )
    return result

def test_build(data, expected):
    observed = ppt_document_builder.PPTDocumentBuilder.build(data["doc_id"], data)
    assert observed== expected


