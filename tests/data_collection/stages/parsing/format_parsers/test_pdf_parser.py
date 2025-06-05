import pytest
from data_collection.stages.parsing.format_parsers import pdf_parser


TEST_DATA_DIR = "tests/data/parsing"
TEST_PDF_FILE = TEST_DATA_DIR + "/pdf_text_parsing_test.pdf"

@pytest.fixture
def parser():
    result = pdf_parser.PDFParser()
    return result


def test_parse_text_with_real_pdf(parser):
    parsed_text = parser.parse_text(TEST_PDF_FILE)

    expected_text = (
        "This is a test Presentation for testing the correctness of PDF text parser "
        "Page 2 "
        "• This is bullet point 1 "
        "• This bullet point 2 "
        "• This is bullet point 3 "
        "• This is bullet point 4 "
        "And this is just a pure sentence"
    )

    normalized_result = " ".join(parsed_text.split())
    normalized_expected = " ".join(expected_text.split())

    assert normalized_result == normalized_expected, f"Expected:\n{normalized_expected}\n\nGot:\n{normalized_result}"

def test_parse_text_file_not_found(parser):
    fake_path = TEST_DATA_DIR + "/nonexistent_file.pdf"

    with pytest.raises(Exception):
        parser.parse_text(fake_path)

def test_parse_images_raises(parser):
    with pytest.raises(NotImplementedError):
        parser.parse_images("dummy.pdf")


def test_parse_vector_graphics_raises(parser):
    with pytest.raises(NotImplementedError):
        parser.parse_vector_graphics("dummy.pdf")
