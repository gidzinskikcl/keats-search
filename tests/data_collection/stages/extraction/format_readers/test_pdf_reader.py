import pytest
from data_collection.stages.extraction.format_readers import pdf_reader
from data_structures import segment


TEST_DATA_DIR = "tests/data/extraction"
TEST_PDF_FILE = TEST_DATA_DIR + "/text_test.pdf"
EMPTY_PDF_FILE = TEST_DATA_DIR + "/empty.pdf"

@pytest.fixture
def reader():
    result = pdf_reader.PDFReader()
    return result


def test_get_text(reader):
    text = reader.get_text(TEST_PDF_FILE, 2)

    expected_text = (
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
    text = reader.get_text(EMPTY_PDF_FILE, 1)
    assert text.strip() == "", f"Expected empty string but got: '{text}'"


def test_get_text_file_not_found(reader):
    fake_path = TEST_DATA_DIR + "/nonexistent_file.pdf"

    with pytest.raises(Exception):
        reader.get_text(fake_path, 1)


def test_load_segments(reader):
    metadata = {"title": "Test Presentation"}
    nr_segments = 2

    segments = reader.load_segments(TEST_PDF_FILE, metadata, nr_segments)

    assert isinstance(segments, list)
    assert len(segments) == nr_segments

    for idx, seg in enumerate(segments, start=1):
        assert isinstance(seg, segment.Segment)
        assert seg.segment_nr == idx
        assert isinstance(seg.text, str)
        assert seg.file_metadata == metadata


        
def test_get_images_raises(reader):
    with pytest.raises(NotImplementedError):
        reader.get_images("dummy.pdf", 1)


def test_get_vector_graphics_raises(reader):
    with pytest.raises(NotImplementedError):
        reader.get_vector_graphics("dummy.pdf", 1)
