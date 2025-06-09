import pytest

from data_collection.content_gateways import ppt_gateway

TEST_DATA_DIR = "tests/data/extraction"
TEST_PPT_FILE = TEST_DATA_DIR + "/text_test.pptx"
EMPTY_PPT_FILE = TEST_DATA_DIR + "/empty.pptx"

@pytest.fixture
def reader():
    result = ppt_gateway.PPTGateway()
    result.set_file_path(TEST_PPT_FILE)
    return result


@pytest.fixture
def expected():
    result = {
        "file_name": "text_test",
        "file_extension": "pptx",
        "page_count": "2",
        "doc_title": "This is a test",
        "subject": "",
        "author": "Gidzinski, Piotr P",
        "keywords": "",
        "comments": "",
        "last_modified_by": "Gidzinski, Piotr P",
        "revision": "2",
        "created": "2025-06-05T14:52:17",
        "modified": "2025-06-05T16:26:53",
        "category": "",
        "content_status": "",
        "identifier": "",
        "language": "",
        "version": "",
        "pages": {
            "1": 'This is a test\nPresentation for testing the correctness of PDF text reader', 
            "2": 'Page 2\nThis is bullet point 1\nThis bullet point 2\nThis is bullet point 3\nThis is bullet point 4\nAnd this is just a pure sentence'
        }
    }
    return result

def test_get(reader, expected):
    observed = reader.get()
    assert observed == expected

@pytest.fixture
def expected_empty():
    result = {
        "file_name": "empty",
        "file_extension": "pptx",
        "page_count": "1",
        "doc_title": "PowerPoint Presentation",
        "subject": "",
        "author": "Gidzinski, Piotr P",
        "keywords": "",
        "comments": "",
        "last_modified_by": "Gidzinski, Piotr P",
        "revision": "1",
        "created": "2025-06-05T16:33:25",
        "modified": "2025-06-05T16:33:33",
        "category": "",
        "content_status": "",
        "identifier": "",
        "language": "",
        "version": "",
        "pages": {
            "1": '', 
        }
    }
    return result


def test_get_empty_ppt(reader, expected_empty):
    reader.set_file_path(EMPTY_PPT_FILE)
    text = reader.get()
    assert text == expected_empty


def test_get_file_not_found(reader):
    wrong_path = TEST_DATA_DIR + "/nonexistent_file.pptx"
    reader.set_file_path(wrong_path)

    with pytest.raises(Exception):
        reader.get_text()


def test_set_get_path(reader):
    new_path = "new/path/to/file.pdf"
    reader.set_file_path(new_path)
    assert reader.get_file_path() == new_path, f"Expected path '{new_path}' but got '{reader.get_file_path()}'"