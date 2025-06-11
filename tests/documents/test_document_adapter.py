import pytest

# from documents import document_adapter


# from documents.keats import keats_document



# @pytest.fixture
# def sample_segments():
#     return [segment.Segment(nr=1, content="Page 1 text."), segment.Segment(nr=1, content="Page 2 text.")]


# @pytest.fixture
# def pdf_doc(sample_segments):
#     return pdf_document.PDFDocument(
#         doc_id="PDF001",
#         file_name="test.pdf",
#         file_extension="pdf",
#         course_ids=["C101"],
#         course_title="Intro to Testing",
#         admin_code="ADM101",
#         content_type="text",
#         page_count="2",
#         authors=["Author A"],
#         date_created="2025-03-12",
#         source="Library",
#         subject="PDF Subject",
#         keywords="test, pdf",
#         version="1.0",
#         pages=sample_segments
#     )


# @pytest.fixture
# def ppt_doc(sample_segments):
#     return ppt_document.PPTDocument(
#         doc_id="PPT001",
#         doc_title="Test PPT",
#         page_count="3",
#         file_name="test.pptx",
#         file_extension="pptx",
#         course_ids=["C102"],
#         course_title="Advanced Testing",
#         admin_code="ADM102",
#         content_type="text",
#         subject="PPT Subject",
#         authors=["Author B"],
#         keywords="slides, test",
#         comments="Some comments",
#         last_modified_by="Author B",
#         revision="2",
#         created="2025-06-01",
#         modified="2025-06-05",
#         category="Lecture",
#         content_status="final",
#         identifier="PPT123",
#         language="en",
#         version="1.1",
#         source="Course Platform",
#         pages=sample_segments
#     )

@pytest.mark.skip(reason="Needs refinement before integration")
def test_pdf_to_keats(pdf_doc):
    keats_doc = document_adapter.DocumentAdapter.to_keats(pdf_doc)

    for kd in keats_doc:
        assert isinstance(kd, keats_document.KeatsDocument)
        assert kd.parent_file_id == pdf_doc.doc_id
        assert kd.keywords == pdf_doc.keywords
        assert kd.file_type == pdf_doc.file_extension
        assert kd.course_ids == pdf_doc.course_ids
    assert "Page 1 text." in keats_doc[0].text
    assert "Page 2 text." in keats_doc[1].text

@pytest.mark.skip(reason="Needs refinement before integration")
def test_ppt_to_keats(ppt_doc):
    keats_docs = document_adapter.DocumentAdapter.to_keats(ppt_doc)
    for kd in keats_docs:
        assert isinstance(kd,keats_document.KeatsDocument)
        assert kd.parent_file_id == ppt_doc.doc_id
        assert kd.doc_title == ppt_doc.doc_title
        assert kd.keywords == ppt_doc.keywords
        assert kd.content_type == ppt_doc.content_type
        assert kd.course_ids == ppt_doc.course_ids
        assert kd.notes == ppt_doc.comments
    assert "Page 1 text." in keats_docs[0].text
    assert "Page 2 text." in keats_docs[1].text

@pytest.mark.skip(reason="Needs refinement before integration")
def test_invalid_document_type():
    class UnknownDocument:
        pass

    with pytest.raises(ValueError, match="Unsupported document type"):
        document_adapter.DocumentAdapter.to_dict(UnknownDocument())
