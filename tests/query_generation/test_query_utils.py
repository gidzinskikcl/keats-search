import pytest

from unittest.mock import patch
from datetime import timedelta

from data_collection import schemas
from query_generation import utils



def test_convert_to_chapters():
    sample_input = [
        {"title": "Introduction", "start_time": 0.0, "end_time": 30.0},
        {"title": "Main Topic", "start_time": 30.0, "end_time": 120.0},
    ]

    expected = [
        schemas.Chapter(
            nr=1,
            title="Introduction",
            timestamp=schemas.Timestamp(start=timedelta(seconds=0), end=timedelta(seconds=30))
        ),
        schemas.Chapter(
            nr=2,
            title="Main Topic",
            timestamp=schemas.Timestamp(start=timedelta(seconds=30), end=timedelta(seconds=120))
        ),
    ]

    result = utils.convert_to_chapters(sample_input)
    assert result == expected


@pytest.fixture
def pdf_segments():
    return [
        schemas.PdfSegment(parent_file="slide_deck.pdf", nr=i, text=f"PDF Content {i}")
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
                start=timedelta(seconds=i * 30),
                end=timedelta(seconds=(i + 1) * 30)
            )
        )
        for i in range(10)
    ]


@pytest.fixture
def expected_output():
    return [
        {
            "doc_id": "slide_deck.pdf_0",
            "text": "PDF Content 0",
            "type": "pdf"
        },
        {
            "doc_id": "lecture.srt_1",
            "text": "SRT Content 1",
            "type": "srt"
        },
        {
            "doc_id": "lecture.srt_2",
            "text": "SRT Content 2",
            "type": "srt"
        },
    ]


def test_sample(pdf_segments, srt_segments, expected_output):
    with patch("query_generation.utils.random.sample", side_effect=[[pdf_segments[0]], [srt_segments[1], srt_segments[2]]]):
        observed = utils.sample(pdf_segments, srt_segments, pdf_count=1, srt_count=2)
    assert observed == expected_output


def test_sample_too_few_inputs():
    pdfs = [schemas.PdfSegment(parent_file="f.pdf", nr=0, text="only one pdf")]
    srts = [schemas.TranscriptSegment(
        nr=0,
        parent_file="f.srt",
        text="only one srt",
        timestamp=schemas.Timestamp(start=timedelta(0), end=timedelta(seconds=30))
    )]

    with pytest.raises(ValueError, match="Not enough segments"):
        utils.sample(pdfs, srts, pdf_count=2, srt_count=1)

    with pytest.raises(ValueError, match="Not enough segments"):
        utils.sample(pdfs, srts, pdf_count=1, srt_count=2)
