import pytest
from unittest.mock import Mock, patch

from llm_annotation.llm import annotator
from llm_annotation.schemas import response_schema

@pytest.fixture
def mock_prompt():
    return Mock(
        system_prompt=Mock(to_dict=Mock(return_value={"role": "system", "content": "system prompt"})),
        user_prompt=Mock(to_dict=Mock(return_value={"role": "user", "content": "user prompt"}))
    )

@pytest.fixture
def mock_parsed_response():
    mock_choice = Mock()
    mock_choice.message.parsed = Mock(
        question="What is photosynthesis?",
        answer="Photosynthesis is the process by which plants make food.",
        relevance=response_schema.BinaryRelevance.RELEVANT
    )

    mock_response = Mock()
    mock_response.choices = [mock_choice]
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    mock_response.usage.total_tokens = 30

    return mock_response

@patch("llm_annotation.llm.annotator.caller.call_openai")
@patch("llm_annotation.llm.annotator.prompt_builder.PromptBuilder.build")
def test_annotate_returns_expected_output(mock_build, mock_call_openai, mock_prompt, mock_parsed_response):
    mock_build.return_value = mock_prompt
    mock_call_openai.return_value = mock_parsed_response

    client = Mock()  # Dummy client

    result = annotator.annotate(
        client=client,
        prompt_module=Mock(),
        course_name="Biology 101",
        lecture_name="Photosynthesis",
        question="What is photosynthesis?",
        answer="Photosynthesis is the process by which plants make food."
    )

    assert isinstance(result, dict)
    assert result["question"] == "What is photosynthesis?"
    assert result["answer"] == "Photosynthesis is the process by which plants make food."
    assert result["relevance"] == "relevant"
    assert result["tokens"] == {
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "total_tokens": 30
    }

    mock_build.assert_called_once()
    mock_call_openai.assert_called_once()
