from pathlib import Path

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
                "encryption": ""
            },
            "text_by_page": [
                "Page 1 text content.",
                "Page 2 text content."
            ]
        }

@pytest.fixture
def parser():
    return MockPdfParser()

@pytest.fixture
def extractor(parser):
    return pdf_schema_extractor.PdfSchemaExtractor(parser)

@pytest.fixture
def test_pdf_path():
    return Path("tests/data/extraction/sample_test.pdf")

@pytest.fixture
def expected():
    return schemas.PdfSchema(
        file_name="sample_test",
        pages=[
            schemas.PdfPage(nr=1, text="Page 1 text content."),
            schemas.PdfPage(nr=2, text="Page 2 text content.")
        ]
    )

def test_extract_returns_correct_schema(extractor, test_pdf_path, expected):
    observed = extractor.get(test_pdf_path)

    assert expected == observed
