import random
from typing import Optional
from openai import OpenAI

from llm_annotation.prompts import templates, prompt_builder
from llm_annotation.llm import caller
from openai.types.chat import ParsedChatCompletion

from llm_annotation.schemas import response_schema

from dataclasses import dataclass

# For testing purposes
# @dataclass
# class ParsedTest:
#     question: str
#     answer: str
#     relevance: response_schema.BinaryRelevance
#     # reasoning: Optional[str] = None

# @dataclass
# class UsageTest:
#     prompt_tokens: int
#     completion_tokens: int
#     total_tokens: int

# # Mimic the OpenAI response container
# @dataclass
# class AnnotationSetTest:
#     usage: UsageTest
#     parsed: ParsedTest


def annotate(
    client: OpenAI,
    prompt_module: templates.PromptTemplate,
    course_name: str,
    lecture_name: str,
    question: str,
    answer: str,
) -> dict:
    """Generates questions from lecture material using the LLM."""

    prompt = prompt_builder.PromptBuilder.build(
        course_name=course_name,
        lecture_name=lecture_name,
        question=question,
        answer=answer,
        prompt_module=prompt_module,
    )
    try:
        annotations_set = caller.call_openai(
            client=client,
            system_prompt=prompt.system_prompt.to_dict(),
            user_prompt=prompt.user_prompt.to_dict(),
        )

        parsed = annotations_set.choices[0].message.parsed

        # For testing purposes - randomly pick relevance
        # relevance = random.choice([
        #     response_schema.BinaryRelevance.RELEVANT,
        #     response_schema.BinaryRelevance.NOTRELEVANT
        # ])

        # parsed = ParsedTest(
        #     question=question,
        #     answer=answer,
        #     relevance=relevance,
        # )

        # annotations_set = AnnotationSetTest(
        #     usage=UsageTest(
        #         prompt_tokens=random.randint(10, 50),
        #         completion_tokens=random.randint(10, 50),
        #         total_tokens=0  # filled below
        #     ),
        #     parsed=parsed
        # )
        # annotations_set.usage.total_tokens = (
        #     annotations_set.usage.prompt_tokens + annotations_set.usage.completion_tokens
        # )

        #  Access token usage from raw_response
        token_usage = _get_token_usage(annotations_set=annotations_set)

        return {
            "question": parsed.question,
            "answer": parsed.answer,
            "relevance": parsed.relevance.value,
            "tokens": token_usage,
            # "reasoning": parsed.reasoning if parsed.reasoning else None
        }

    except Exception as e:
        print(f"Warning: Could not parse questions for {course_name} - {question}: {e}")
        return []


def _get_token_usage(
    annotations_set: ParsedChatCompletion[response_schema.AnnotatedPair],
) -> dict[str, int]:
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0

    if hasattr(annotations_set, "usage"):
        usage = annotations_set.usage
        prompt_tokens = usage.prompt_tokens if hasattr(usage, "prompt_tokens") else 0
        completion_tokens = (
            usage.completion_tokens if hasattr(usage, "completion_tokens") else 0
        )
        total_tokens = usage.total_tokens if hasattr(usage, "total_tokens") else 0
        # print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total: {total_tokens}")
    else:
        print("Token usage information not available.")

    result = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }
    return result
