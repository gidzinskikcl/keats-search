import json
import pytest
from unittest.mock import MagicMock, patch
from types import SimpleNamespace

from schemas import schemas
from query_generation.llm import question_generator  # Adjust the import path
from query_generation.prompts import templates
from query_generation.schemas import response_schema

@pytest.fixture
def sample_material():
    return schemas.LectureMaterial(
        course_name="Database Systems",
        doc_id="ABCS123",
        lecture_title="Introduction to NoSQL",
        content="NoSQL databases are designed to scale horizontally...",
        type=schemas.MaterialType.TRANSCRIPT,
        length=1200
    )

@pytest.fixture
def mock_prompt_module():
    return MagicMock(spec=templates.PromptTemplate)

@pytest.fixture
def expected():
    return [{
        'question': 'What is a key characteristic of NoSQL databases?',
        'label': 'Basic', 
        'answer': 'NoSQL databases scale horizontally.'
    }]


def test_generate_questions_success(sample_material, mock_prompt_module, expected):
    mock_prompt = MagicMock()
    mock_prompt.system_prompt.to_dict.return_value = {"role": "system", "content": "system prompt"}
    mock_prompt.user_prompt.to_dict.return_value = {"role": "user", "content": "user prompt"}

    # Create a mock parsed QuerySet
    parsed_queryset = response_schema.QuerySet(
        questions=[
            response_schema.Query(
                question="What is a key characteristic of NoSQL databases?",
                label=response_schema.DifficultyLevel.BASIC,
                answer="NoSQL databases scale horizontally."
            )
        ]
    )

    # Construct full mock structure matching OpenAI response
    mock_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    parsed=parsed_queryset
                )
            )
        ]
    )

    with patch("query_generation.prompts.query_prompt_builder.QueryPromptBuilder.build", return_value=mock_prompt) as mock_builder, \
         patch("query_generation.llm.caller.call_openai", return_value=mock_response) as mock_call:

        mock_client = MagicMock()

        observed = question_generator.generate_questions(
            material=sample_material,
            client=mock_client,
            prompt_module=mock_prompt_module,
            num_questions=1
        )

        assert expected == observed
        mock_builder.assert_called_once()
        mock_call.assert_called_once()

def test_generate_questions_json_error(sample_material, mock_prompt_module):
    mock_prompt = MagicMock()
    mock_prompt.system_prompt.to_dict.return_value = {"role": "system", "content": "system prompt"}
    mock_prompt.user_prompt.to_dict.return_value = {"role": "user", "content": "user prompt"}

    with patch("query_generation.prompts.query_prompt_builder.QueryPromptBuilder.build", return_value=mock_prompt), \
         patch("query_generation.llm.caller.call_openai", return_value="not-a-valid-json"):

        mock_client = MagicMock()
        result = question_generator.generate_questions(
            material=sample_material,
            client=mock_client,
            prompt_module=mock_prompt_module,
            num_questions=2
        )

        assert result == []
