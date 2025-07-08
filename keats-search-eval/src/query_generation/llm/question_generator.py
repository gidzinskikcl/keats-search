from openai import OpenAI

from schemas import schemas
from query_generation.prompts import templates, query_prompt_builder
from query_generation.llm import caller


def generate_questions(
        material: schemas.LectureMaterial, 
        client: OpenAI, 
        prompt_module: templates.PromptTemplate,
        num_questions: int = None,
        difficulty_lvl: str = "",
        difficulty_level_instruction: str = "",
        difficulty_level_example: str = ""
) -> list[dict]:
    """Generates questions from lecture material using the LLM."""

    prompt = query_prompt_builder.QueryPromptBuilder.build(
        course_name=material.course_name,
        lecture_content=material.content,
        num_questions=num_questions,
        prompt_module=prompt_module,
        lecture_title=material.lecture_title,
        difficulty_lvl=difficulty_lvl,
        difficulty_level_instruction=difficulty_level_instruction,
        difficulty_level_example=difficulty_level_example
    )
    try:
        questions_set = caller.call_openai(
            client=client,
            system_prompt=prompt.system_prompt.to_dict(),
            user_prompt=prompt.user_prompt.to_dict()
        )

        parsed = questions_set.choices[0].message.parsed
    
        return [
            {
                "question": q.question,
                "label": q.label.name.title(), 
                "answer": q.answer
            }
            for q in parsed.questions
        ]

    except Exception as e:
        print(f"Warning: Could not parse questions for {material.course_name} - {material.doc_id}: {e}")
        return []