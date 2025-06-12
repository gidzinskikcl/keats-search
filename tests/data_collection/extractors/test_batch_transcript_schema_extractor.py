import pathlib
from unittest.mock import Mock

import pytest

from data_collection.extractors.batch_transcript_schema_extractor import BatchTranscriptSchemaExtractor
from data_collection import schemas


@pytest.fixture
def course_dir(tmp_path: pathlib.Path):
    course1 = tmp_path / "course1"
    course1.mkdir()
    (course1 / "lecture1.srt").touch()
    (course1 / "lecture2.srt").touch()

    course2 = tmp_path / "course2"
    course2.mkdir()
    (course2 / "lecture1.srt").touch()

    return tmp_path

@pytest.fixture
def mock_extractor():
    result = Mock()

    def extractor_get(file_path: pathlib.Path) -> schemas.PdfSchema:
        return schemas.TranscriptSchema(file_name=file_path.stem, duration=None, subtitles=[], course_name=None)
    
    result.get.side_effect = extractor_get
    return result

@pytest.fixture
def expected():
    result = [
        schemas.TranscriptSchema(
            file_name="lecture1",
            duration=None,
            subtitles=[],
            course_name="course1"
        ),
        schemas.TranscriptSchema(
            file_name="lecture2",
            duration=None,
            subtitles=[],
            course_name="course1"
        ),
        schemas.TranscriptSchema(
            file_name="lecture1",
            duration=None,
            subtitles=[],
            course_name="course2"
        )
    ]
    return result


def test_extract_all(course_dir, mock_extractor, expected):
    batch_extractor = BatchTranscriptSchemaExtractor(extractor=mock_extractor)

    observed = batch_extractor.extract_all(course_dir)

    print(observed)

    assert sorted(observed, key=lambda x: (x.course_name, x.file_name)) == expected

    assert mock_extractor.get.call_count == 3

