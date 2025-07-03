from openai import OpenAI

from llm_annotation.prompts import templates, prompt_builder
from llm_annotation.llm import caller


def annotate(
        client: OpenAI, 
        prompt_module: templates.PromptTemplate,
        course_name: str,
        lecture_name: str,
        question: str,
        answer: str
) -> list[dict]:
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
            user_prompt=prompt.user_prompt.to_dict()
        )

        parsed = annotations_set.choices[0].message.parsed
    
        return {
            "question": parsed.question,
            "answer": parsed.answer,
            "relevance": parsed.relevance.name.lower(), 
        }

    except Exception as e:
        print(f"Warning: Could not parse questions for {course_name} - {question}: {e}")
        return []