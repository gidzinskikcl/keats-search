import pathlib
from datetime import timedelta
from unittest.mock import MagicMock

import pytest

from data_collection.extractors.transcript_schema_extractor import TranscriptSchemaExtractor
from data_collection import schemas


@pytest.fixture
def mock_parser():
    parser = MagicMock()
    parser.get.return_value = {
        "file_name": "sample.srt",
        "duration": "150",
        "transcript": [
            {
                "start": "00:00:01,000",
                "end": "00:00:04,000",
                "text": "Hello, world!"
            },
            {
                "start": "00:00:05,000",
                "end": "00:00:07,000",
                "text": "Welcome to the test."
            }
        ]
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
                    start=timedelta(seconds=1),
                    end=timedelta(seconds=4)
                )
            ),
            schemas.Subtitle(
                nr=2,
                text="Welcome to the test.",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=5),
                    end=timedelta(seconds=7)
                )
            )
        ]
    )
    return result


def test_transcript_schema_extractor(mock_parser, expected):
    extractor = TranscriptSchemaExtractor(parser=mock_parser)
    dummy_path = pathlib.Path("/fake/path/sample.srt")
    
    observed = extractor.get(dummy_path)
    assert expected == observed

