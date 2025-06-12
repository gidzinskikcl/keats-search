import pathlib

import pytest

from unittest.mock import Mock

from data_collection import schemas
from data_collection.extractors import batch_pdf_schema_extractor


@pytest.fixture
def pdf_courses(tmp_path: pathlib.Path):
    course1 = tmp_path / "course1"
    course1.mkdir()
    (course1 / "slide1.pdf").touch()
    (course1 / "slide2.pdf").touch()

    course2 = tmp_path / "course2"
    course2.mkdir()
    (course2 / "lecture1.pdf").touch()

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
        schemas.PdfSchema(file_name="slide1", pages=[], course_name="course1"),
        schemas.PdfSchema(file_name="slide2", pages=[], course_name="course1"),
        schemas.PdfSchema(file_name="lecture1", pages=[], course_name="course2")
    ]
    return result

def test_extract_all(pdf_courses, mock_extractor, expected):

    batch_extractor = batch_pdf_schema_extractor.BatchPdfSchemaExtractor(mock_extractor)

    observed = batch_extractor.extract_all(pdf_courses)


    assert sorted(observed, key=lambda x: (x.course_name, x.file_name)) == expected
    assert mock_extractor.get.call_count == 3


