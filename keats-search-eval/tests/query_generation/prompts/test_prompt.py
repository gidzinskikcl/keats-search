import pytest

from query_generation.prompts import prompt_schema


@pytest.fixture
def system_prompt():
    result = prompt_schema.Prompt(
        prompt_schema.Role.SYSTEM, "You are a student that needs to work on assignment"
    )
    return result


def test_to_dict(system_prompt):
    expected = {
        "role": "system",
        "content": "You are a student that needs to work on assignment",
    }
    observed = system_prompt.to_dict()
    assert expected == observed
