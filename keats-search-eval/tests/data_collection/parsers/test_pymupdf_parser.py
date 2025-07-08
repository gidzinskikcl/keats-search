import pytest
from pathlib import Path
import pymupdf
import json

from services.parsers import pymupdf_parser

TEST_DATA_DIR = Path("keats-search-eval/tests/data/extraction")
TEST_PDF_FILE = TEST_DATA_DIR / "text_test.pdf"
EMPTY_PDF_FILE = TEST_DATA_DIR / "empty.pdf"
MAPPING_FILE = Path("keats-search-eval/tests/data/file_to_metadata_mapping.json")  # <- dummy mapping for test

@pytest.fixture
def pdf_file():
    return TEST_PDF_FILE

@pytest.fixture
def empty_pdf_file():
    return EMPTY_PDF_FILE

@pytest.fixture
def nonexistent_file():
    return TEST_DATA_DIR / "nonexistent_file.pdf"

@pytest.fixture
def parser():
    return pymupdf_parser.PyMuPdfParser(mapping_path=MAPPING_FILE)

@pytest.fixture
def expected():
    return {
        "metadata": {
            "file_name": "text_test",
            "file_extension": "pdf",
            "format": "PDF 1.7",
            "title": "",
            "author": "",
            "subject": "",
            "keywords": "",
            "creator": "",
            "producer": "",
            "creationDate": "D:20250605162709+00'00'",
            "modDate": "D:20250605162709+00'00'",
            "trapped": "",
            "encryption": ""
        },
        "text_by_page": [
            "This is a test\nPresentation for testing the correctness of PDF text reader\n",
            "Page 2\n• This is bullet point 1\n• This bullet point 2\n• This is bullet point 3\n• This is bullet point 4\nAnd this is just a pure sentence\n"
        ],
        "course_id": None,
        "course_title": None,
        "lecture_id": None,
        "lecture_title": None
    }

@pytest.fixture
def expected_empty():
    return {
        "metadata": {
            "file_name": "empty",
            "file_extension": "pdf",
            "format": "PDF 1.7",
            "title": "",
            "author": "",
            "subject": "",
            "keywords": "",
            "creator": "",
            "producer": "",
            "creationDate": "D:20250605163338+00'00'",
            "modDate": "D:20250605163338+00'00'",
            "trapped": "",
            "encryption": ""
        },
        "text_by_page": [""],
        "course_id": None,
        "course_title": None,
        "lecture_id": None,
        "lecture_title": None
    }

def test_get(pdf_file, parser, expected):
    observed = parser.get(pdf_file)
    assert observed == expected

def test_get_empty_pdf(empty_pdf_file, parser, expected_empty):
    observed = parser.get(empty_pdf_file)
    assert observed == expected_empty

def test_get_file_not_found(parser, nonexistent_file):
    with pytest.raises(pymupdf.FileNotFoundError):
        parser.get(nonexistent_file)
