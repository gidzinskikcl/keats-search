import pytest
from unittest.mock import Mock

from query_generation import caller, response_schema


@pytest.fixture
def mock_client():
    return Mock()

def test_call_openai(mock_client):
    # Arrange
    # Mock the API call
    mock_completion = Mock()
    mock_client.beta.chat.completions.parse.return_value = mock_completion

    # Dummy prompts
    system_prompt = {"role": "system", "content": "You are a helpful assistant."}
    user_prompt = {"role": "user", "content": "Tell me a joke."}

    # Act
    result = caller.call_openai(mock_client, system_prompt, user_prompt)

    # Assert
    mock_client.beta.chat.completions.parse.assert_called_once_with(
        model="gpt-4o",
        messages=[system_prompt, user_prompt],
        n=1,
        response_format=response_schema.QuerySet
    )
    assert result == mock_completion
