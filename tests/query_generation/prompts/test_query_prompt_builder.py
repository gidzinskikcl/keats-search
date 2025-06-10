import textwrap

import pytest

from query_generation.prompts import prompt_schema, query_prompt_builder

@pytest.fixture
def lecture_content():
    result =  "This lecture covers the OSI model, including the application, transport, and network layers."
    return result


@pytest.fixture
def expected(lecture_content):
    result = prompt_schema.PromptHistory(
            prompt_schema.Prompt(
                role=prompt_schema.Role.SYSTEM,
                content=textwrap.dedent(f"""
                    You are a computer science student at a university enrolled in a course on "Introduction to Computer Networks".
                    You have carefully read the lecture content provided below.
                    To check your understanding, you will generate questions that you might ask your lecturer.
                    These questions should be answerable using only the lecture content.
                """).strip()
            ),
            prompt_schema.Prompt(
                role=prompt_schema.Role.USER,
                content=textwrap.dedent(f"""
                    1. Read the lecture content carefully.
                    2. For each question out of 5:
                        a) Write a clear and concise question that can be answered using the lecture content.
                        b) Assign a difficulty level to the question:
                            - Basic — straightforward factual question (e.g. definitions, lists)
                            - Intermediate — requires connecting multiple ideas or explaining examples
                            - Advanced — requires analysis, synthesis, or critical thinking
                        c) Provide an answer to the question based on the lecture content.
                    3. Present your output with the following structure:
                        - question: The question text
                        - label: Difficulty level (Basic/Intermediate/Advanced)
                        - answer: The answer based on the lecture content.

                    Lecture Content:
                    {lecture_content}
                """).strip()
            )
    )
    return result


def test_prompt(expected, lecture_content):
    print(expected)
    observed = query_prompt_builder.QueryPromptBuilder.build(course_name="Introduction to Computer Networks", lecture_content=lecture_content, num_questions=5)
    assert expected == observed