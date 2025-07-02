import textwrap
import pytest

from annotation.prompts import templates, prompt_builder
from query_generation.prompts import prompt_schema


@pytest.fixture
def prompt_inputs():
    return {
        "course_name": "Computer Security",
        "lecture_name": "Code Injection Techniques",
        "question": "Why alter a code pointer in code injection?",
        "answer": "To hijack the control flow and redirect execution to attacker-controlled code."
    }


@pytest.fixture
def expected_prompt_history(prompt_inputs):
    system_content = textwrap.dedent(
        templates.V1.SYSTEM_PROMPT_TEMPLATE.format(
            course_name=prompt_inputs["course_name"],
            lecture_name=prompt_inputs["lecture_name"]
        )
    ).strip()

    user_content = textwrap.dedent(
        templates.V1.USER_PROMPT_TEMPLATE.format(
            question=prompt_inputs["question"],
            answer=prompt_inputs["answer"]
        )
    ).strip()

    return prompt_schema.PromptHistory(
        system_prompt=prompt_schema.Prompt(
            role=prompt_schema.Role.SYSTEM,
            content=system_content
        ),
        user_prompt=prompt_schema.Prompt(
            role=prompt_schema.Role.USER,
            content=user_content
        )
    )


def test_prompt_builder_build(expected_prompt_history, prompt_inputs):
    observed = prompt_builder.PromptBuilder.build(
        course_name=prompt_inputs["course_name"],
        lecture_name=prompt_inputs["lecture_name"],
        question=prompt_inputs["question"],
        answer=prompt_inputs["answer"],
        prompt_module=templates.V1
    )

    assert observed == expected_prompt_history
