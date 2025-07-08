import openai
from openai.types.chat import ParsedChatCompletion

from query_generation.schemas import response_schema


def call_openai(
    client: openai.OpenAI, system_prompt: dict[str, str], user_prompt: dict[str, str]
) -> ParsedChatCompletion[response_schema.QuerySet]:
    result = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[system_prompt, user_prompt],
        n=1,
        response_format=response_schema.QuerySet,
    )
    return result
