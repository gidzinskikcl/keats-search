import textwrap
import pytest

from query_generation.prompts import prompt_schema, query_prompt_builder
from query_generation.prompts import templates


@pytest.fixture
def lecture_content():
    return "This lecture covers the OSI model, including the application, transport, and network layers."


@pytest.fixture
def expected_prompt_history(lecture_content):
    course_name = "Introduction to Computer Networks"
    num_questions = 5

    system_content = textwrap.dedent(
        templates.V1.SYSTEM_PROMPT_TEMPLATE.format(course_name=course_name)
    ).strip()

    user_content = textwrap.dedent(
        templates.V1.USER_PROMPT_TEMPLATE.format(
            lecture_content=lecture_content,
            num_questions=num_questions,
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


def test_query_prompt_builder_with_prompt1(expected_prompt_history, lecture_content):
    observed = query_prompt_builder.QueryPromptBuilder.build(
        course_name="Introduction to Computer Networks",
        lecture_content=lecture_content,
        num_questions=5,
        prompt_module=templates.V1
    )

    assert observed == expected_prompt_history


def render_user_prompt(lecture_content: str, num_questions: int) -> str:
    return textwrap.dedent(templates.V1.USER_PROMPT_TEMPLATE.format(
        lecture_content=lecture_content,
        num_questions=num_questions,
        question_word="question" if num_questions == 1 else "questions"
    )).strip()

@pytest.mark.parametrize("num_questions,expected_word", [
    (1, "1 question"),
    (3, "3 questions"),
])
def test_question_word_singular_plural(num_questions, expected_word):
    lecture_content = "Example lecture content."
    result = render_user_prompt(lecture_content, num_questions)
    assert f"Generate {expected_word}" in result