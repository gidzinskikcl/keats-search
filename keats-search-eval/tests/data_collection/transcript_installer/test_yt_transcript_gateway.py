import pytest
from unittest.mock import patch

from services.gateways import yt_transcript_gateway


@pytest.fixture
def mock_info():
    result = {
        "id": "abc123",
        "title": "Sample Video",
        "description": "This is a test video.",
        "uploader": "TestUploader",
        "upload_date": "20240601",
        "duration": 123,
        "view_count": 456,
        "tags": ["test", "video"],
        "webpage_url": "https://youtube.com/watch?v=abc123",
        "thumbnail": "https://thumbnail.url/image.jpg",
        "chapters": [{"start_time": 0, "title": "Intro"}],
    }
    return result


@pytest.fixture
def expected(tmp_path):
    result = {
        "id": "abc123",
        "title": "Sample Video",
        "description": "This is a test video.",
        "uploader": "TestUploader",
        "upload_date": "20240601",
        "duration": 123,
        "view_count": 456,
        "tags": ["test", "video"],
        "webpage_url": "https://youtube.com/watch?v=abc123",
        "thumbnail": "https://thumbnail.url/image.jpg",
        "chapters": [{"start_time": 0, "title": "Intro"}],
        "transcript_file": str(tmp_path / "abc123.en.srt"),
    }
    return result


def test_get_youtube_transcript(tmp_path, mock_info, expected):
    # Simulate that the SRT file exists
    srt_file = tmp_path / "abc123.en.srt"
    srt_file.write_text("1\n00:00:00,000 --> 00:00:01,000\nHello world")

    # Add subtitles for preview (manual)
    mock_preview_info = dict(mock_info)
    mock_preview_info["subtitles"] = {
        "en": [{"url": "https://example.com"}]
    }  # simulate manual presence

    def mock_extract_info(url, download):
        return mock_info if download else mock_preview_info

    with patch("yt_dlp.YoutubeDL.extract_info", side_effect=mock_extract_info):
        gateway = yt_transcript_gateway.YouTubeTranscriptGateway(output_dir=tmp_path)
        observed = gateway.get("https://youtube.com/watch?v=abc123")

    assert expected == observed
    assert srt_file.exists()
