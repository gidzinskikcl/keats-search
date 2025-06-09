import pathlib
from unittest import mock

from data_collection import document_processor, utils
from documents import document

def test_process_calls_dependencies_correctly():
    # Arrange
    processor = document_processor.DocumentProcessor()

    file_path = pathlib.Path("dummy.pdf")
    metadata_entry = {
        "course_ids": ["6CCS3MDE"],
        "course_title": "Model-driven Engineering",
        "other_key": "some_value"
    }

    # Mock gateway
    mock_gateway = mock.MagicMock()
    mock_gateway.get.return_value = {
        "pages": {"1": "Page 1 content", "2": "Page 2 content"},
        "doc_title": "Test Doc",
        "file_name": "dummy.pdf",
        "file_extension": "pdf",
        "authors": ["Author A"],
        "date": "2025-06-08",
        "subject": "Test Subject",
        "keywords": "Test,PDF",
        "page_count": "2"
    }

    # Mock segmenter
    mock_segmenter = mock.MagicMock()
    mock_segmenter.segment.return_value = {"1": "Segmented Page 1", "2": "Segmented Page 2"}

    # Mock document builder
    mock_doc_builder = mock.MagicMock()
    mock_doc = mock.MagicMock(spec=document.Document)
    mock_doc_builder.build.return_value = mock_doc

    # Mock adapter
    mock_adapter = mock.MagicMock()
    transformed_docs = [mock.MagicMock(spec=document.Document)]
    mock_adapter.to_keats.return_value = transformed_docs

    # Act
    result = processor.process(
        file_path=file_path,
        metadata_entry=metadata_entry,
        gateway=mock_gateway,
        document_builder=mock_doc_builder,
        segmenter=mock_segmenter,
        document_adapter=mock_adapter
    )

    # Assert
    mock_gateway.set_file_path.assert_called_once_with(str(file_path))
    mock_gateway.get.assert_called_once()

    mock_segmenter.segment.assert_called_once_with(data=mock_gateway.get.return_value)
    mock_doc_builder.build.assert_called_once()
    mock_adapter.to_keats.assert_called_once_with(document=mock_doc)

    assert result == transformed_docs


def test_process_slides_multiple_files(monkeypatch, tmp_path):
    """
    - Test that the result is a flattened list of documents.
    - Test that each document was created from a correct file path
    """
    # Arrange
    # Create dummy course folders
    courses_folder = tmp_path
    courseA = courses_folder / "CourseA"
    courseA.mkdir()
    file1 = courseA / "file1.pdf"
    file1.touch()
    file2 = courseA / "file2.pdf"
    file2.touch()

    courseB = courses_folder / "CourseB"
    courseB.mkdir()
    file3 = courseB / "file3.pdf"
    file3.touch()

    # Metadata dictionary
    metadata = {"CourseA": {}, "CourseB": {}}

    # Mock utils functions
    monkeypatch.setattr("data_collection.utils.get_course_info", mock.MagicMock(return_value={"course_ids": ["dummy_id"]}))
    monkeypatch.setattr("data_collection.utils.assign_version", mock.MagicMock(return_value={"course_ids": ["dummy_id"], "version": "1.0.0"}))
    monkeypatch.setattr("data_collection.utils.validate_courses", mock.MagicMock())

    # Mock DocumentProcessor
    mock_processor = mock.MagicMock(spec=document_processor.DocumentProcessor)
    # For simplicity, let's make each call to process() return a single doc wrapped in a list
    mock_processor.process.return_value = ["mock_doc"]

    # Mock content_processors
    fake_content_gateway = mock.MagicMock()
    fake_doc_builder = mock.MagicMock()
    fake_doc_adapter = mock.MagicMock()
    fake_doc_segmenter = mock.MagicMock()
    content_processors = {
        "pdf": (fake_content_gateway, fake_doc_builder, fake_doc_segmenter, fake_doc_adapter)
    }

    # Act
    result, stats = document_processor.process_slides(
        processor=mock_processor,
        courses=courses_folder,
        metadata=metadata,
        content_processors=content_processors
    )   

    # Assert
    assert result == ["mock_doc", "mock_doc", "mock_doc"], "Result should be a flattened list of all documents"
    assert isinstance(stats, utils.SlideProcessingStats), "Stats should be an instance of SlideProcessingStats"

    # Optionally also test stats
    assert stats.total_files == 3
    assert stats.processed_files == 3
    assert stats.file_types["pdf"] == 3
    assert stats.files_per_course_id["dummy_id"] == 3

    # Check that each call to process() used correct arguments
    processed_files = [call.kwargs["file_path"].name for call in mock_processor.process.call_args_list]
    assert set(processed_files) == {"file1.pdf", "file2.pdf", "file3.pdf"}


def test_document_to_dict():
    doc1 = document.Document(doc_id="123")
    doc2 = document.Document(doc_id="456")
    observed = document.to_dict(docs=[doc1, doc2])
    expected = [
        {
            "doc_id": "123"
        },
        {
            "doc_id": "456"
        }
    ]
    assert observed == expected