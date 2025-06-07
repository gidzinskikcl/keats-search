from dataclasses import dataclass
from unittest.mock import Mock
import pytest

from data_collection.transformers import transformer
from gateways import doc_gateway
from data_collection.educational_content_gateways import content_gateway

from data_collection.data_processors import doc_processor

class DummySegment:
    def __init__(self, id, segment_nr):
        self.id = id
        self.segment_nr = segment_nr

@dataclass
class DummyDocument:
    id: str

    def to_dict(self):
        return {"id": self.id}


@pytest.fixture
def mock_data():
    return [
        {"file_path": "dummy_path_1", "metadata": {"id": "123", "title": "Dummy 1"}},
        {"file_path": "dummy_path_2", "metadata": {"id": "456", "title": "Dummy 2"}}
    ]

def test_document_processor_process(mock_data):
    mock_import_gateway = Mock(spec=content_gateway.EducationalContentGateway)
    mock_transformer = Mock(spec=transformer.Transformer)
    mock_export_gateway = Mock(spec=doc_gateway.DocumentGateway)


    # Mock content from import_gateway
    dummy_segments = [DummySegment(id=f"seg_{i}", segment_nr=i) for i in range(1, 6)]
    mock_import_gateway.get.return_value = dummy_segments
    mock_import_gateway.set_file_path = Mock()
    mock_import_gateway.set_metadata = Mock()


    # Mock transformer's output
    dummy_document = DummyDocument(id="doc_id")
    mock_transformer.transform.return_value = dummy_document

    mock_logger = Mock()

    processor = doc_processor.DocumentProcessor(mock_data, mock_import_gateway, mock_transformer, mock_export_gateway, mock_logger)

    # Act
    processor.process()

    # Assert
    mock_import_gateway.get.call_count == 2 
    assert mock_transformer.set_content.call_count == 10
    assert mock_transformer.transform.call_count == 10

    # Check that each call passed the segment
    for idx, seg in enumerate(dummy_segments * 2):
        assert mock_transformer.set_content.call_args_list[idx].kwargs['content'] == seg

    # Check export_gateway was called once with a list of documents
    mock_export_gateway.add.assert_called_once()
    docs_passed = mock_export_gateway.add.call_args[1]['documents']
    assert len(docs_passed) == 10
    assert all(isinstance(doc, dict) for doc in docs_passed)
