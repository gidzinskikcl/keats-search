from pathlib import Path
from unittest.mock import Mock
import pytest

from schemas import schemas
from services.extractors import pdf_schema_extractor
from services.parsers import pdf_parser


class MockPdfParser(pdf_parser.PdfParser):
    def get(self, file_path: Path) -> dict[str, object]:
        return {
            "metadata": {
                "file_name": "sample_test",
                "file_extension": "pdf",
                "format": "PDF 1.7",
                "title": "Test PDF",
                "author": "Author Name",
                "subject": "Testing",
                "keywords": "",
                "creator": "",
                "producer": "",
                "creationDate": "D:20250605162709+00'00'",
                "modDate": "D:20250605162709+00'00'",
                "trapped": "",
                "encryption": "",
                "course_id": "18.404J",
                "lecture_id": "12",
            },
            "text_by_page": ["Page 1 text content.", "Page 2 text content."],
        }


@pytest.fixture
def parser():
    mock_parser = Mock()
    mock_parser.get.return_value = {
        "metadata": {"file_name": "b4d9bf1573dccea21bee82cfba4224d4_MIT18_404f20_lec1"},
        "text_by_page": ["Page 1 text content.", "Page 2 text content."],
        "lecture_id": "1",
        "course_id": "18.404J",
    }
    return mock_parser


@pytest.fixture
def extractor(parser):
    return pdf_schema_extractor.PdfSchemaExtractor(parser)


@pytest.fixture
def test_pdf_path():
    return Path(
        "tests/data/extraction/b4d9bf1573dccea21bee82cfba4224d4_MIT18_404f20_lec1.pdf"
    )


@pytest.fixture
def expected():
    return schemas.PdfSchema(
        file_name="b4d9bf1573dccea21bee82cfba4224d4_MIT18_404f20_lec1",
        course_id="18.404J",
        lecture_id="1",
        pages=[
            schemas.PdfPage(nr=1, text="Page 1 text content."),
            schemas.PdfPage(nr=2, text="Page 2 text content."),
        ],
        url="https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/b4d9bf1573dccea21bee82cfba4224d4_MIT18_404f20_lec1.pdf",
        thumbnail_image="b4d9bf1573dccea21bee82cfba4224d4_MIT18_404f20_lec1_thumbnail.jpg",
    )


def test_extract_returns_correct_schema(extractor, test_pdf_path, expected):
    observed = extractor.get(test_pdf_path)

    assert expected == observed
