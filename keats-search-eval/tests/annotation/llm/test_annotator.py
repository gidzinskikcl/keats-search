import pytest
from unittest.mock import MagicMock, patch
from types import SimpleNamespace

from llm_annotation.prompts import templates
from llm_annotation.llm import annotator

# === Fixtures ===

@pytest.fixture
def sample_annotate_input():
    return {
        "course_name": "Computer Security",
        "lecture_name": "Code Injection",
        "question": "Why alter a code pointer in code injection?",
        "answer": "To hijack the execution flow and run attacker code."
    }

@pytest.fixture
def mock_prompt_module():
    return MagicMock(spec=templates.PromptTemplate)

@pytest.fixture
def expected():
    return {
        "question": "Why alter a code pointer in code injection?",
        "answer": "To hijack the execution flow and run attacker code.",
        "relevance": "relevant"
    }

@pytest.mark.skip(reason="Not implemented yet")
def test_annotate_success(sample_annotate_input, mock_prompt_module, expected):
    mock_prompt = MagicMock()
    mock_prompt.system_prompt.to_dict.return_value = {"role": "system", "content": "system prompt"}
    mock_prompt.user_prompt.to_dict.return_value = {"role": "user", "content": "user prompt"}

    # Mock parsed structure with relevance enum
    parsed_result = SimpleNamespace(
        question=sample_annotate_input["question"],
        answer=sample_annotate_input["answer"],
        relevance=SimpleNamespace(name="RELEVANT")
    )


    mock_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(parsed=parsed_result)
            )
        ]
    )

    with patch("annotation.prompts.prompt_builder.PromptBuilder.build", return_value=mock_prompt) as mock_builder, \
         patch("annotation.llm.caller.call_openai", return_value=mock_response) as mock_call:

        mock_client = MagicMock()
        observed = annotator.annotate(
            client=mock_client,
            prompt_module=mock_prompt_module,
            **sample_annotate_input
        )

        assert observed == expected
        mock_builder.assert_called_once()
        mock_call.assert_called_once()

@pytest.mark.skip(reason="Not implemented yet")
def test_annotate_fallback_on_error(sample_annotate_input, mock_prompt_module):
    mock_prompt = MagicMock()
    mock_prompt.system_prompt.to_dict.return_value = {"role": "system", "content": "system prompt"}
    mock_prompt.user_prompt.to_dict.return_value = {"role": "user", "content": "user prompt"}

    with patch("annotation.prompts.prompt_builder.PromptBuilder.build", return_value=mock_prompt), \
         patch("annotation.llm.caller.call_openai", side_effect=Exception("mock error")):

        mock_client = MagicMock()
        result = annotator.annotate(
            client=mock_client,
            prompt_module=mock_prompt_module,
            **sample_annotate_input
        )

        assert result == []
