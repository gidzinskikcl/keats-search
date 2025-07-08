import pytest
from unittest.mock import Mock

from llm_annotation.schemas import response_schema
from llm_annotation.llm import caller


@pytest.fixture
def mock_client():
    return Mock()


def test_call_openai(mock_client):
    mock_completion = Mock()
    mock_client.beta.chat.completions.parse.return_value = mock_completion

    system_prompt = {"role": "system", "content": "You are a helpful assistant."}
    user_prompt = {"role": "user", "content": "Tell me a joke."}

    result = caller.call_openai(mock_client, system_prompt, user_prompt)

    mock_client.beta.chat.completions.parse.assert_called_once_with(
        model="gpt-4o",
        messages=[system_prompt, user_prompt],
        n=1,
        response_format=response_schema.AnnotatedPair,
    )
    assert result == mock_completion
