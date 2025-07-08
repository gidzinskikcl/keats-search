import pytest
from unittest.mock import patch, MagicMock

from services.llm_based import client as llm_client

def test_load_openai_client_success():
    with patch("os.getenv", return_value="fake-api-key"), \
         patch("services.llm_based.client.load_dotenv"), \
         patch("services.llm_based.client.OpenAI") as mock_openai:
        
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        client = llm_client.load_openai_client()
        
        mock_openai.assert_called_once_with(api_key="fake-api-key")
        assert client == mock_client

def test_load_openai_client_missing_key():
    with patch("os.getenv", return_value=None), \
         patch("services.llm_based.client.load_dotenv"):
        
        with pytest.raises(EnvironmentError, match="Missing PROJ_OPENAI_API_KEY"):
            llm_client.load_openai_client()
