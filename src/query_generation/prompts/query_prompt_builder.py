import textwrap

from query_generation.prompts import prompt_builder, prompt_schema

class QueryPromptBuilder(prompt_builder.PromptBuilder):

    @staticmethod
    def build(course_name: str, num_questions: int, lecture_content: str) -> prompt_schema.PromptHistory:
        result = prompt_schema.PromptHistory(
            system_prompt=prompt_schema.Prompt(
                role=prompt_schema.Role.SYSTEM,
                content=textwrap.dedent(f"""
                    You are a computer science student at a university enrolled in a course on "{course_name}".
                    You have carefully read the lecture content provided below.
                    To check your understanding, you will generate questions that you might ask your lecturer.
                    These questions should be answerable using only the lecture content.
                """).strip()
            ),
            user_prompt=prompt_schema.Prompt(
                role=prompt_schema.Role.USER,
                content=textwrap.dedent(f"""
                    1. Read the lecture content carefully.
                    2. For each question out of {num_questions}:
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