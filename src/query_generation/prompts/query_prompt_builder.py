import textwrap

from query_generation.prompts import prompt_builder, prompt_schema
from query_generation.prompts import templates

class QueryPromptBuilder(prompt_builder.PromptBuilder):

    @staticmethod
    def build(
        course_name: str,
        num_questions: int,
        lecture_content: str,
        prompt_module: templates.PromptTemplate,
        lecture_title: str = "N/A",
    ) -> prompt_schema.PromptHistory:

        system_content = textwrap.dedent(prompt_module.SYSTEM_PROMPT_TEMPLATE.format(
            course_name=course_name
        )).strip()

        user_content = textwrap.dedent(prompt_module.USER_PROMPT_TEMPLATE.format(
            lecture_content=lecture_content,
            num_questions=num_questions,
            lecture_title=lecture_title
            
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
