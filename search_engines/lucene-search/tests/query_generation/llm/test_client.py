import pytest
from unittest.mock import patch, MagicMock

from query_generation.llm import client as llm_client

def test_load_openai_client_success():
    with patch("os.getenv", return_value="fake-api-key"), \
         patch("query_generation.llm.client.load_dotenv"), \
         patch("query_generation.llm.client.OpenAI") as mock_openai:
        
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        client = llm_client.load_openai_client()
        
        mock_openai.assert_called_once_with(api_key="fake-api-key")
        assert client == mock_client

def test_load_openai_client_missing_key():
    with patch("os.getenv", return_value=None), \
         patch("query_generation.llm.client.load_dotenv"):
        
        with pytest.raises(EnvironmentError, match="Missing PROJ_OPENAI_API_KEY"):
            llm_client.load_openai_client()
