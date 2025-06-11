import pytest

from unittest.mock import MagicMock

from data_collection import schemas
from data_collection.extractors import batch_pdf_schema_extractor

@pytest.fixture
def mock_extractor():
    extractor = MagicMock()
    def extractor_get(file_path):
        # Return a PdfSchema with file name based on the file's stem
        return schemas.PdfSchema(file_name=file_path.stem, pages=[])
    extractor.get.side_effect = extractor_get
    return extractor

def test_extract_all(tmp_path, mock_extractor):
    # Create a fake directory structure
    course1_dir = tmp_path / "course1"
    course1_dir.mkdir()
    pdf1 = course1_dir / "slide1.pdf"
    pdf2 = course1_dir / "slide2.pdf"
    pdf1.touch()
    pdf2.touch()

    course2_dir = tmp_path / "course2"
    course2_dir.mkdir()
    pdf3 = course2_dir / "lecture1.pdf"
    pdf3.touch()

    # Expected results
    expected_schemas = [
        schemas.PdfSchema(file_name="slide1", pages=[], course_name="course1"),
        schemas.PdfSchema(file_name="slide2", pages=[], course_name="course1"),
        schemas.PdfSchema(file_name="lecture1", pages=[], course_name="course2")
    ]
    batch_extractor = batch_pdf_schema_extractor.BatchPdfSchemaExtractor(mock_extractor)

    observed_schemas = batch_extractor.extract_all(tmp_path)

    assert sorted(observed_schemas, key=lambda x: x.file_name) == sorted(expected_schemas, key=lambda x: x.file_name)

