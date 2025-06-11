import pathlib
import pytest

from data_collection.parsers import srt_transcript_parser

@pytest.fixture
def file_path():
    result = pathlib.Path("/Users/piotrgidzinski/KeatsSearch_workspace/keats-search/data/testing/transcripts/sample.en.srt")
    return result

@pytest.fixture
def expected():
    result =  {
        "file_name": "sample",
        "file_extension": "srt",
        "id": "sample",
        "title": "Sample Video",
        "description": "A short test video with chapters.",
        "uploader": "TestChannel",
        "upload_date": "20250610",
        "duration": "10",
        "view_count": "123",
        "tags": ["test", "sample"],
        "webpage_url": "https://www.example.com",
        "thumbnail": "https://www.example.com/thumbnail.jpg",
        "chapters": [
            {
                "title": "Introduction",
                "start_time": "0.0",
                "end_time": "5.0"
            },
            {
                "title": "Conclusion",
                "start_time": "5.0",
                "end_time": "10.0"
            }
        ],
        "transcript": [
            {
                "index": "1",
                "start": "00:00:00,000",
                "end": "00:00:05,000",
                "text":"Hello, world!" 
            },
            {
                "index": "2",
                "start": "00:00:05,000",
                "end": "00:00:10,000",
                "text": "This is a test subtitle." 
            }

        ]
    }
    return result

def test_get(file_path, expected):
    parser = srt_transcript_parser.SRTTranscriptParser()
    observed = parser.get(file_path, True)
    assert expected == observed

@pytest.fixture
def expected_no_metadata():
    result =  {
        "file_name": "sample",
        "file_extension": "srt",
        "id": "",
        "title": "",
        "description": "",
        "uploader": "",
        "upload_date": "",
        "duration": "",
        "view_count": "",
        "tags": "",
        "webpage_url": "",
        "thumbnail": "",
        "chapters": [],
        "transcript": [
            {
                "index": "1",
                "start": "00:00:00,000",
                "end": "00:00:05,000",
                "text":"Hello, world!" 
            },
            {
                "index": "2",
                "start": "00:00:05,000",
                "end": "00:00:10,000",
                "text": "This is a test subtitle." 
            }

        ]
         
    }
    return result


def test_get_no_metadata(file_path, expected_no_metadata):
    parser = srt_transcript_parser.SRTTranscriptParser()
    observed = parser.get(file_path, False)
    assert expected_no_metadata == observed

def test_get_nonexistent_file():
    path = pathlib.Path("non/existent/path/to/file.srt")
    parser = srt_transcript_parser.SRTTranscriptParser()
    with pytest.raises(FileNotFoundError):
        parser.get(path)

def test_get_nonexistent_file_no_metadata():
    path = pathlib.Path("non/existent/path/to/file.srt")
    parser = srt_transcript_parser.SRTTranscriptParser()
    with pytest.raises(FileNotFoundError):
        parser.get(path, False)