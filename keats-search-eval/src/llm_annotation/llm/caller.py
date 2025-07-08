import openai
from openai.types.chat import ParsedChatCompletion

from llm_annotation.schemas import response_schema


def call_openai(
    client: openai.OpenAI, system_prompt: dict[str, str], user_prompt: dict[str, str]
) -> ParsedChatCompletion[response_schema.AnnotatedPair]:
    result = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[system_prompt, user_prompt],
        n=1,
        response_format=response_schema.AnnotatedPair,
    )
    return result
