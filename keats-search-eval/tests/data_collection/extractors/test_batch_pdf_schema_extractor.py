import pathlib

import pytest

from unittest.mock import Mock

from schemas import schemas
from services.extractors import batch_pdf_schema_extractor


@pytest.fixture
def pdf_courses(tmp_path: pathlib.Path):
    course1 = tmp_path / "course1"
    course1.mkdir()
    lecture1 = course1 / "Lecture 1"
    lecture1.mkdir()
    (lecture1 / "slide1.1.pdf").touch()
    (lecture1 / "slide1.2.pdf").touch()

    course2 = tmp_path / "course2"
    course2.mkdir()
    lecture2 = course2 / "Lecture 2"
    lecture2.mkdir()
    (lecture2 / "lecture2.1.pdf").touch()

    return tmp_path

@pytest.fixture
def mock_extractor():
    result = Mock()

    def extractor_get(file_path: pathlib.Path) -> schemas.PdfSchema:
        return schemas.PdfSchema(file_name=file_path.stem, pages=[], course_name=None)
    
    result.get.side_effect = extractor_get
    return result


@pytest.fixture
def expected():
    result = [
        schemas.PdfSchema(file_name="slide1.1", pages=[], course_name="course1", lecture_name="Lecture 1"),
        schemas.PdfSchema(file_name="slide1.2", pages=[], course_name="course1", lecture_name="Lecture 1"),
        schemas.PdfSchema(file_name="lecture2.1", pages=[], course_name="course2", lecture_name="Lecture 2")
    ]
    return result

def test_extract_all(pdf_courses, mock_extractor, expected):

    batch_extractor = batch_pdf_schema_extractor.BatchPdfSchemaExtractor(mock_extractor)

    observed = batch_extractor.extract_all(pdf_courses, ["course1", "course2"])


    assert sorted(observed, key=lambda x: (x.course_name, x.file_name)) == expected
    assert mock_extractor.get.call_count == 3


