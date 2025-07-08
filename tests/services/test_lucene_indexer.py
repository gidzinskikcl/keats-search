from unittest.mock import patch, MagicMock
import pytest

from services import lucene_indexer

def test_index(tmp_path):
    json_path = tmp_path / "docs.json"
    index_dir = tmp_path / "index"
    json_path.write_text("[]")  # simulate a valid JSON file
    index_dir.mkdir()

    indexer = lucene_indexer.LuceneIndexer(index_dir=str(index_dir), json_doc_path=str(json_path))

    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc

        indexer.index()

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "java" in args
        assert str(json_path) in args
        assert str(index_dir) in args


def test_index_file_not_found():
    indexer = lucene_indexer.LuceneIndexer(index_dir="some/index", json_doc_path="nonexistent/file.json")

    with pytest.raises(FileNotFoundError):
        indexer.index()


def test_index_failure(tmp_path):
    json_path = tmp_path / "docs.json"
    index_dir = tmp_path / "index"
    json_path.write_text("[]")
    index_dir.mkdir()

    indexer = lucene_indexer.LuceneIndexer(index_dir=str(index_dir), json_doc_path=str(json_path))

    with patch("subprocess.run") as mock_run:
        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stderr = "Simulated error"
        mock_run.return_value = mock_proc

        with pytest.raises(RuntimeError, match="Indexing failed: Simulated error"):
            indexer.index()
