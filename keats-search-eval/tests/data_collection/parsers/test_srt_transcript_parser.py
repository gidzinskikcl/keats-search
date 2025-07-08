import json
import pathlib
import pytest

from services.parsers import srt_transcript_parser

MAPPING_PATH = pathlib.Path(
    "keats-search-eval/tests/data/file_to_metadata_mapping.json"
)


@pytest.fixture
def parser():
    return srt_transcript_parser.SRTTranscriptParser(mapping_path=MAPPING_PATH)


@pytest.fixture
def file_path():
    return pathlib.Path("keats-search-eval/data/testing/transcripts/sample.en.srt")


@pytest.fixture
def expected():
    return {
        "file_name": "sample.en",
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
            {"title": "Introduction", "start_time": "0.0", "end_time": "5.0"},
            {"title": "Conclusion", "start_time": "5.0", "end_time": "10.0"},
        ],
        "transcript": [
            {
                "index": "1",
                "start": "00:00:00,000",
                "end": "00:00:05,000",
                "text": "Hello, world!",
            },
            {
                "index": "2",
                "start": "00:00:05,000",
                "end": "00:00:10,000",
                "text": "This is a test subtitle.",
            },
        ],
        "course_id": None,
        "course_title": None,
        "lecture_id": None,
        "lecture_title": None,
    }


def test_get(file_path, parser, expected):
    observed = parser.get(file_path, True)
    assert observed == expected


@pytest.fixture
def expected_no_metadata():
    return {
        "file_name": "sample.en",
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
                "text": "Hello, world!",
            },
            {
                "index": "2",
                "start": "00:00:05,000",
                "end": "00:00:10,000",
                "text": "This is a test subtitle.",
            },
        ],
        "course_id": None,
        "course_title": None,
        "lecture_id": None,
        "lecture_title": None,
    }


def test_get_no_metadata(file_path, parser, expected_no_metadata):
    observed = parser.get(file_path, False)
    assert observed == expected_no_metadata


def test_get_nonexistent_file(parser):
    path = pathlib.Path("non/existent/path/to/file.srt")
    with pytest.raises(FileNotFoundError):
        parser.get(path)


def test_get_nonexistent_file_no_metadata(parser):
    path = pathlib.Path("non/existent/path/to/file.srt")
    with pytest.raises(FileNotFoundError):
        parser.get(path, False)


def test_filename_parsing_with_suffix(tmp_path):
    fake_srt = tmp_path / "IiD3YZkkCmE.en-j3PyPqV-e1s.srt"
    fake_json = tmp_path / "IiD3YZkkCmE.en-j3PyPqV-e1s.json"
    fake_mapping = tmp_path / "file_to_metadata_mapping.json"

    # Write test .srt content
    fake_srt.write_text(
        "1\n00:00:00,000 --> 00:00:05,000\nMock line 1\n\n"
        "2\n00:00:05,000 --> 00:00:10,000\nMock line 2"
    )

    # Write test metadata
    fake_json.write_text(
        json.dumps(
            {
                "id": "IiD3YZkkCmE",
                "title": "Mock Lecture",
                "description": "Mock desc",
                "uploader": "MockUploader",
                "upload_date": "20250618",
                "duration": 10,
                "view_count": 100,
                "tags": [""],
                "webpage_url": "",
                "thumbnail": "",
                "chapters": [
                    {"title": "Intro", "start_time": 0.0, "end_time": 5.0},
                    {"title": "End", "start_time": 5.0, "end_time": 10.0},
                ],
            }
        )
    )

    # Write test mapping
    fake_mapping.write_text(
        json.dumps(
            [
                {
                    "doc_id": fake_srt.name,
                    "course_id": "6.006",
                    "course_title": "Intro to Algorithms",
                    "lecture_id": "1",
                    "lecture_title": "Lecture 1",
                }
            ]
        )
    )

    parser = srt_transcript_parser.SRTTranscriptParser(mapping_path=fake_mapping)
    observed = parser.get(fake_srt)

    assert observed["file_name"] == "IiD3YZkkCmE.en-j3PyPqV-e1s"
    assert observed["title"] == "Mock Lecture"
    assert observed["transcript"][0]["text"] == "Mock line 1"
    assert observed["course_id"] == "6.006"
    assert observed["lecture_title"] == "Lecture 1"
