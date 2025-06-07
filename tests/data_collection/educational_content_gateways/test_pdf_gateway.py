import pytest
from data_collection.educational_content_gateways import pdf_gateway
from entities import segment


TEST_DATA_DIR = "tests/data/extraction"
TEST_PDF_FILE = TEST_DATA_DIR + "/text_test.pdf"
EMPTY_PDF_FILE = TEST_DATA_DIR + "/empty.pdf"

@pytest.fixture
def metadata():
    return {
        "id": "120004213",
        "title": "Test PDF",
        "nr_segments": 2,
        "file_type": "pdf"
    }

@pytest.fixture
def reader(metadata):
    result = pdf_gateway.PDFGateway()
    result.set_file_path(TEST_PDF_FILE)
    result.set_metadata(metadata)
    return result


def test_get_text():
    text = pdf_gateway.PDFGateway.get_text(TEST_PDF_FILE, 2)

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


def test_get(reader, metadata):
    
    nr_segments = metadata.get("length", 0)

    segments = reader.get()

    assert isinstance(segments, list)
    assert len(segments) == nr_segments

    for idx, seg in enumerate(segments, start=1):
        assert isinstance(seg, segment.Segment)
        assert seg.segment_nr == idx
        assert isinstance(seg.text, str)
        assert seg.file_metadata == metadata

def test_set_get_path(reader):
    new_path = "new/path/to/file.pdf"
    reader.set_file_path(new_path)
    assert reader.get_file_path() == new_path, f"Expected path '{new_path}' but got '{reader.get_file_path()}'"

def test_set_get_metadata(reader, metadata):
    new_metadata = {
        "id": "123456789",
        "title": "Updated PDF",
        "nr_segments": 3,
        "file_type": "pdf"
    }
    reader.set_metadata(new_metadata)
    assert reader.get_metadata() == new_metadata, f"Expected metadata {new_metadata} but got {reader.get_metadata()}"

