import pytest

from unittest.mock import patch
from datetime import timedelta

from schemas import schemas
from query_generation.benchmarking import load_sample


@pytest.fixture
def pdf_segments():
    return [
        schemas.PdfSegment(
            parent_file="slide_deck.pdf",
            nr=i,
            text=f"PDF Content {i}",
            url="https://testing/url/doc",
            thumbnail_image="1234_thumbnail.jpg",
        )
        for i in range(10)
    ]


@pytest.fixture
def srt_segments():
    return [
        schemas.TranscriptSegment(
            nr=i,
            parent_file="lecture.srt",
            text=f"SRT Content {i}",
            timestamp=schemas.Timestamp(
                start=timedelta(seconds=i * 30), end=timedelta(seconds=(i + 1) * 30)
            ),
            url="https://www.this.is.url/test",
            thumbnail_url="https://www.this.is.thumbnail_url/test",
        )
        for i in range(10)
    ]


@pytest.fixture
def expected_output():
    return [
        {"doc_id": "slide_deck.pdf_0", "text": "PDF Content 0", "type": "pdf"},
        {"doc_id": "lecture.srt_1", "text": "SRT Content 1", "type": "srt"},
        {"doc_id": "lecture.srt_2", "text": "SRT Content 2", "type": "srt"},
    ]


def test_sample(pdf_segments, srt_segments, expected_output):
    with patch(
        "query_generation.benchmarking.load_sample.random.sample",
        side_effect=[[pdf_segments[0]], [srt_segments[1], srt_segments[2]]],
    ):
        observed = load_sample.sample(
            pdf_segments, srt_segments, pdf_count=1, srt_count=2
        )
    assert observed == expected_output


def test_sample_too_few_inputs():
    pdfs = [
        schemas.PdfSegment(
            parent_file="f.pdf",
            nr=0,
            text="only one pdf",
            url="https://testing/url/doc",
            thumbnail_image="1234_thumbnail.jpg",
        )
    ]
    srts = [
        schemas.TranscriptSegment(
            nr=0,
            parent_file="f.srt",
            text="only one srt",
            timestamp=schemas.Timestamp(start=timedelta(0), end=timedelta(seconds=30)),
            url="https://www.this.is.url/test",
            thumbnail_url="https://www.this.is.thumbnail_url/test",
        )
    ]

    with pytest.raises(ValueError, match="Not enough segments"):
        load_sample.sample(pdfs, srts, pdf_count=2, srt_count=1)

    with pytest.raises(ValueError, match="Not enough segments"):
        load_sample.sample(pdfs, srts, pdf_count=1, srt_count=2)
