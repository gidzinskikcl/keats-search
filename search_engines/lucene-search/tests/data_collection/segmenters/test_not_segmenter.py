import pytest

from data_collection import schemas
from data_collection.segmenters import not_segmenter

@pytest.fixture
def sample_pdf_schema():
    return schemas.PdfSchema(
        file_name="sample_test",
        pages=[
            schemas.PdfPage(nr=1, text="Page 1 text."),
            schemas.PdfPage(nr=2, text="Page 2 text.")
        ]
    )

@pytest.fixture
def expected():
    result = [
        schemas.PdfSegment(parent_file="sample_test", nr=1, text="Page 1 text.\nPage 2 text.")
    ]
    return result

def test_not_segmenter(sample_pdf_schema, expected):
    observed_segments = not_segmenter.NotSegmenter.segment(sample_pdf_schema)

    assert observed_segments == expected