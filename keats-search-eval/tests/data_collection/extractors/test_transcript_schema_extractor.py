import pathlib
from datetime import timedelta
from unittest.mock import MagicMock

import pytest

from services.extractors.transcript_schema_extractor import TranscriptSchemaExtractor
from schemas import schemas


@pytest.fixture
def mock_parser():
    parser = MagicMock()
    parser.get.return_value = {
        "file_name": "sample.srt",
        "duration": "150",
        "transcript": [
            {"start": "00:00:01,000", "end": "00:00:04,000", "text": "Hello, world!"},
            {
                "start": "00:00:05,000",
                "end": "00:00:07,000",
                "text": "Welcome to the test.",
            },
        ],
        "chapters": [
            {"title": "Introduction", "start_time": "0.0", "end_time": "10.0"},
            {"title": "Summary", "start_time": "10.0", "end_time": "20.0"},
        ],
        "webpage_url": "https://www.this.is.url/test",
        "thumbnail": "https://www.this.is.thumbnail_url/test",
    }
    return parser


@pytest.fixture
def expected():
    result = schemas.TranscriptSchema(
        file_name="sample.srt",
        duration=timedelta(seconds=150),
        subtitles=[
            schemas.Subtitle(
                nr=1,
                text="Hello, world!",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=1), end=timedelta(seconds=4)
                ),
            ),
            schemas.Subtitle(
                nr=2,
                text="Welcome to the test.",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=5), end=timedelta(seconds=7)
                ),
            ),
        ],
        chapters=[
            schemas.Chapter(
                nr=1,
                title="Introduction",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=0), end=timedelta(seconds=10)
                ),
            ),
            schemas.Chapter(
                nr=2,
                title="Summary",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=10), end=timedelta(seconds=20)
                ),
            ),
        ],
        url="https://www.this.is.url/test",
        thumbnail_url="https://www.this.is.thumbnail_url/test",
    )
    return result


def test_transcript_schema_extractor(mock_parser, expected):
    extractor = TranscriptSchemaExtractor(parser=mock_parser)
    dummy_path = pathlib.Path("/fake/path/sample.srt")

    observed = extractor.get(dummy_path)
    assert expected == observed
