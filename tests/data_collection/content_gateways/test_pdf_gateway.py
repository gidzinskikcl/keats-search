import pytest

from data_collection.content_gateways import pdf_gateway

TEST_DATA_DIR = "tests/data/extraction"
TEST_PDF_FILE = TEST_DATA_DIR + "/text_test.pdf"
EMPTY_PDF_FILE = TEST_DATA_DIR + "/empty.pdf"

@pytest.fixture
def gateway():
    result = pdf_gateway.PDFGateway()
    result.set_file_path(TEST_PDF_FILE)
    return result

@pytest.fixture
def expected():
    result = {
        'file_name': 'text_test', 
        'file_extension': 'pdf', 
        'doc_title': 'This is a test', 
        'authors': [], 
        'date_created': "D:20250605162709+00'00'", 
        'subject': '', 
        'keywords': '',  
        'page_count': "2", 
        'pages': {
            "1": 'This is a test\nPresentation for testing the correctness of PDF text reader\n', 
            "2": 'Page 2\n\u2022 This is bullet point 1\n\u2022 This bullet point 2\n\u2022 This is bullet point 3\n\u2022 This is bullet point 4\nAnd this is just a pure sentence\n'
        }
    }
    return result

def test_get(gateway, expected):
    observed = gateway.get()
    assert observed == expected

@pytest.fixture
def expected_empty():
    result = {
        'file_name': 'empty', 
        'file_extension': 'pdf', 
        'doc_title': 'Untitled Document', 
        'authors': [], 
        'date_created': "D:20250605163338+00'00'", 
        'subject': '', 
        'keywords': '', 
        'page_count': "1", 
        'pages': {
            "1": '', 
        }
    }
    return result


def test_get_empty_pdf(gateway, expected_empty):
    gateway.set_file_path(EMPTY_PDF_FILE)
    text = gateway.get()
    assert text == expected_empty

def test_get_file_not_found(gateway):
    gateway.set_file_path(TEST_DATA_DIR + "/nonexistent_file.pdf")
    with pytest.raises(Exception):
        gateway.get()


def test_set_get_path(gateway):
    new_path = "new/path/to/file.pdf"
    gateway.set_file_path(new_path)
    assert gateway.get_file_path() == new_path, f"Expected path '{new_path}' but got '{gateway.get_file_path()}'"

