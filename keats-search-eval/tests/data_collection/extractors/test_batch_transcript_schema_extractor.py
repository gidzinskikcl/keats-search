import pathlib
from unittest.mock import Mock

import pytest

from services.extractors.batch_transcript_schema_extractor import (
    BatchTranscriptSchemaExtractor,
)
from schemas import schemas


@pytest.fixture
def course_dir(tmp_path: pathlib.Path):
    course1 = tmp_path / "course1"
    course1.mkdir()
    lecture1 = course1 / "Lecture 1"
    lecture1.mkdir()
    (lecture1 / "lecture1.1.srt").touch()
    (lecture1 / "lecture1.2.srt").touch()

    course2 = tmp_path / "course2"
    course2.mkdir()
    lecture2 = course2 / "Lecture 2"
    lecture2.mkdir()
    (lecture2 / "lecture2.1.srt").touch()

    return tmp_path


@pytest.fixture
def mock_extractor():
    result = Mock()

    def extractor_get(file_path: pathlib.Path) -> schemas.PdfSchema:
        return schemas.TranscriptSchema(
            file_name=file_path.stem, duration=None, subtitles=[], course_name=None
        )

    result.get.side_effect = extractor_get
    return result


@pytest.fixture
def expected():
    result = [
        schemas.TranscriptSchema(
            file_name="lecture1.1",
            duration=None,
            subtitles=[],
            course_name="course1",
            lecture_name="Lecture 1",
        ),
        schemas.TranscriptSchema(
            file_name="lecture1.2",
            duration=None,
            subtitles=[],
            course_name="course1",
            lecture_name="Lecture 1",
        ),
        schemas.TranscriptSchema(
            file_name="lecture2.1",
            duration=None,
            subtitles=[],
            course_name="course2",
            lecture_name="Lecture 2",
        ),
    ]
    return result


def test_extract_all(course_dir, mock_extractor, expected):
    batch_extractor = BatchTranscriptSchemaExtractor(extractor=mock_extractor)

    observed = batch_extractor.extract_all(course_dir, ["course1", "course2"])

    print(observed)

    assert sorted(observed, key=lambda x: (x.course_name, x.file_name)) == expected

    assert mock_extractor.get.call_count == 3
