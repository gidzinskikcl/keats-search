import pytest
from data_collection.stages.parsing.format_readers import pdf_reader


TEST_DATA_DIR = "tests/data/parsing"
TEST_PDF_FILE = TEST_DATA_DIR + "/text_test.pdf"
EMPTY_PDF_FILE = TEST_DATA_DIR + "/empty.pdf"

@pytest.fixture
def reader():
    result = pdf_reader.PDFReader()
    return result


def test_get_text(reader):
    text = reader.get_text(TEST_PDF_FILE)

    expected_text = (
        "This is a test Presentation for testing the correctness of PDF text reader "
        "Page 2 "
        "• This is bullet point 1 "
        "• This bullet point 2 "
        "• This is bullet point 3 "
        "• This is bullet point 4 "
        "And this is just a pure sentence"
    )

    normalized_result = " ".join(text.split())
    normalized_expected = " ".join(expected_text.split())

    assert normalized_result == normalized_expected, f"Expected:\n{normalized_expected}\n\nGot:\n{normalized_result}"


def test_get_text_empty_pdf(reader):
    text = reader.get_text(EMPTY_PDF_FILE)
    assert text.strip() == "", f"Expected empty string but got: '{text}'"


def test_get_text_file_not_found(reader):
    fake_path = TEST_DATA_DIR + "/nonexistent_file.pdf"

    with pytest.raises(Exception):
        reader.get_text(fake_path)

def test_get_images_raises(reader):
    with pytest.raises(NotImplementedError):
        reader.get_images("dummy.pdf")


def test_get_vector_graphics_raises(reader):
    with pytest.raises(NotImplementedError):
        reader.get_vector_graphics("dummy.pdf")
