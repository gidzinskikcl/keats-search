import pytest
from schemas import schemas
from services.segmenters import page_segmenter


@pytest.fixture
def sample_pdf_schema():
    return schemas.PdfSchema(
        file_name="sample_test",
        pages=[
            schemas.PdfPage(nr=1, text="Page 1 text."),
            schemas.PdfPage(nr=2, text="Page 2 text."),
        ],
        url="https://testing/url/doc",
        thumbnail_image="1234_thumbnail.jpg",
    )


@pytest.fixture
def expected():
    result = [
        schemas.PdfSegment(
            parent_file="sample_test",
            nr=1,
            text="Page 1 text.",
            url="https://testing/url/doc",
            thumbnail_image="1234_thumbnail.jpg",
        ),
        schemas.PdfSegment(
            parent_file="sample_test",
            nr=2,
            text="Page 2 text.",
            url="https://testing/url/doc",
            thumbnail_image="1234_thumbnail.jpg",
        ),
    ]
    return result


def test_page_segmenter(sample_pdf_schema, expected):
    observed_segments = page_segmenter.PageSegmenter.segment(sample_pdf_schema)

    assert observed_segments == expected
