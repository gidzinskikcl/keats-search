import pytest

from documents.pdf import pdf_document_builder, pdf_document
from data_collection.segments import segment


@pytest.fixture
def data():
    result = {
        "doc_id": "7CCSMATAI_w1",
        "doc_title": "Lecture 1",
        "file_name": "lecture1.pdf",
        "file_extension": "pdf",
        "course_ids": ["7CCSMATAI"],
        "course_title": "Advanced Topics in AI",
        "admin_code": "24~25 SEM1 000001",
        "content_type": "TEXT",
        "page_count": "10",
        "authors": ["Prof. John Smith"],
        "lecturers": ["Prof. Adam Smith"],
        "date_created": "2025-06-06",
        "source": "King's College",
        "subject": "AI Topics",
        "keywords": "AI, machine learning, data science",
        "version": "1.0.0",
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
    result = pdf_document.PDFDocument(
        doc_id=data["doc_id"],
        file_name=data["file_name"],
        file_extension=data["file_extension"],
        course_ids=data["course_ids"],
        course_title=data["course_title"],
        admin_code=data["admin_code"],
        content_type=data["content_type"],
        page_count=data["page_count"],
        authors=data["lecturers"],
        date_created=data["date_created"],
        source=data["source"],
        subject=data["subject"],
        keywords=data["keywords"],
        version=data["version"],
        pages=data["pages"]
    )
    return result

def test_build(data, expected):
    observed = pdf_document_builder.PDFDocumentBuilder.build(data["doc_id"], data)
    assert observed== expected
