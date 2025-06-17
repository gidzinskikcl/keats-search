import json

from openai import OpenAI

from data_collection import schemas
from query_generation.prompts import templates, query_prompt_builder
from query_generation.llm import caller


def generate_questions(
        material: schemas.LectureMaterial, 
        client: OpenAI, 
        prompt_module: templates.PromptTemplate,
        num_questions: int,
) -> list[dict]:
    # TODO write a test for this function
    """Generates questions from lecture material using the LLM."""

    prompt = query_prompt_builder.QueryPromptBuilder.build(
        course_name=material.course_name,
        lecture_content=material.content,
        num_questions=num_questions,
        prompt_module=prompt_module
    )
    # LLM call
    questions_set = caller.call_openai(
        client=client,
        system_prompt=prompt.system_prompt.to_dict(),
        user_prompt=prompt.user_prompt.to_dict()
    )

    # For demonstration purposes (mocked)
    # questions_set = json.dumps([
    #     {
    #         "question": f"What is a key characteristic of NoSQL databases from {material.title}?",
    #         "label": "Basic",
    #         "answer": "NoSQL databases allow scaling out by adding more nodes to commodity servers.",
    #         "explanation": "This question checks understanding of the 'Volume' aspect discussed in the lecture."
    # }
    # ])

    try:
        return json.loads(questions_set)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON for {material.course_name} - {material.title}")
        return []