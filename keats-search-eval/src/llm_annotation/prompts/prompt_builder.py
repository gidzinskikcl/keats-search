import textwrap

from llm_annotation.prompts import templates
from query_generation.prompts import prompt_schema

class PromptBuilder:

    @staticmethod
    def build(
        course_name: str,
        lecture_name: str,
        question: str,
        answer: str,
        prompt_module: templates.PromptTemplate,
    ) -> prompt_schema.PromptHistory:

        system_content = textwrap.dedent(prompt_module.SYSTEM_PROMPT_TEMPLATE.format(
            course_name=course_name,
            lecture_name=lecture_name
        )).strip()

        user_content = textwrap.dedent(prompt_module.USER_PROMPT_TEMPLATE.format(
            question=question,
            answer=answer
        )).strip()

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
