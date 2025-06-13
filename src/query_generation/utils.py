from typing import Union
from datetime import timedelta
import random
import json

from openai import OpenAI

from data_collection import schemas
from query_generation.prompts import templates, query_prompt_builder
from query_generation import caller


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
    # questions_set = caller.call_openai(
    #     client=client,
    #     system_prompt=prompt.system_prompt.to_dict(),
    #     user_prompt=prompt.user_prompt.to_dict()
    # )

    # For demonstration purposes (mocked)
    questions_set = json.dumps([
        {
            "question": f"What is a key characteristic of NoSQL databases from {material.title}?",
            "label": "Basic",
            "answer": "NoSQL databases allow scaling out by adding more nodes to commodity servers.",
            "explanation": "This question checks understanding of the 'Volume' aspect discussed in the lecture."
        }
    ])

    try:
        return json.loads(questions_set)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON for {material.course_name} - {material.title}")
        return []


def convert_to_chapters(chapters_dict: list[dict[str, Union[str, float]]]) -> list[schemas.Chapter]:
    result = []
    for nr, c in enumerate(chapters_dict, start=1):
        chapter = schemas.Chapter(
            nr=nr,
            title=c["title"],
            timestamp=schemas.Timestamp(
                start=timedelta(seconds=c["start_time"]),
                end=timedelta(seconds=c["end_time"])
            )
        )
        result.append(chapter)
    return result

def sample(
    pdf_segments: list[schemas.PdfSegment],
    srt_segments: list[schemas.TranscriptSegment],
    pdf_count: int,
    srt_count: int,
) -> list[dict[str, Union[str, int]]]:
    if len(pdf_segments) < pdf_count or len(srt_segments) < srt_count:
        raise ValueError("Not enough segments to sample the requested counts.")

    pdf_sample = random.sample(pdf_segments, pdf_count)
    srt_sample = random.sample(srt_segments, srt_count)

    combined = pdf_sample + srt_sample

    result = [
        {
            "doc_id": f"{m.parent_file}_{m.nr}",
            "text": m.text,
            "type": "pdf" if isinstance(m, schemas.PdfSegment) else "srt",
        }
        for m in combined
    ]

    return result

