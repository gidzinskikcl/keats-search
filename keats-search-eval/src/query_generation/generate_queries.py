import datetime
import json
import pathlib
import random
from collections import defaultdict

from services.collector import materials_collector
from services.gateways import csv_query_gateway
from services.extractors import batch_pdf_schema_extractor, batch_transcript_schema_extractor, pdf_schema_extractor, transcript_schema_extractor
from services.parsers import pymupdf_parser, srt_transcript_parser
from services.segmenters import page_segmenter, chapter_segmenter
from schemas import schemas

from services.llm_based import client as llm_client
from query_generation.llm import question_generator
from query_generation.prompts import templates


# Constants
OUTPUT_REPO = "keats-search-eval/data/queries/results"
COURSES_DIR = pathlib.Path("keats-search-eval/data")
PROMPT = templates.V4

difficulty_levels = {
    "Basic": {
        "explanation": "Assign a basic difficulty level: direct factual question (e.g., definitions, lists)",
        "example": """
            [
                (
                    - question: "Shellcode address"
                    - label: Basic
                    - answer: "The address of the memory region that contains the shellcode."
                )
            ]
        """
    },
    "Intermediate": {
        "explanation": "Assign an intermediate difficulty level: involves understanding or explaining relationships between ideas.",
        "example": """
            [

                (
                    - question: "Why alter a code pointer in code injection?"
                    - label: Intermediate
                    - answer: "Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow."
                )
            ]
        """
    },
    "Advanced": {
        "explanation": "Assign an advanced difficulty level: requires connecting multiple ideas, reasoning through examples, or analyzing concepts.",
        "example": """
            [
                (
                    - question: "What are the steps for code injection?"
                    - label: Advanced
                    - answer: "1. Inject the code to be executed (shellcode) into a writable memory region (stack, data, heap, etc.). 2. Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow. The return address will be the address of the writable memory region that contains the shellcode."
                )
            ]
        """
    }
}

DIFFICULTY_LEVELS = ["Basic", "Intermediate", "Advanced"]
TARGET_PER_LEVEL = None  # Will be set based on total segments
difficulty_counts = defaultdict(int)

COURSES = [
    "18.404J",
    "6.006",
    # "6.172",
    # "6.S897",
    "6.0002"
    # add more course folder names here
]

def choose_balanced_difficulty():
    # Try to balance across difficulties
    remaining = {
        lvl: TARGET_PER_LEVEL - difficulty_counts[lvl]
        for lvl in DIFFICULTY_LEVELS
    }
    # Filter to levels that still need more
    eligible = [lvl for lvl, rem in remaining.items() if rem > 0]

    # If all full, pick randomly
    if not eligible:
        return random.choice(DIFFICULTY_LEVELS)
    
    return random.choice(eligible)


def get_url_for_material(material: schemas.LectureMaterial) -> str | None:
    url_base = pathlib.Path("keats-search-eval/data/transcripts")
    json_path = url_base / material.course_name / material.lecture_title
    if not json_path.exists() or not json_path.is_dir():
        return None

    json_files = list(json_path.glob("*.json"))
    if not json_files:
        return None

    with open(json_files[0], "r") as f:
        data = json.load(f)
        return data.get("webpage_url")


def main():
    """Generates a dataset of questions based on lecture content using a language model."""
    start_time = datetime.datetime.now()
    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")

    # Output directory
    output_dir_base = pathlib.Path(f"{OUTPUT_REPO}/{timestamp}")
    output_dir_base.mkdir(parents=True, exist_ok=True)

    # Initialize OpenAI client and extractors
    client = llm_client.load_openai_client()
    pdf_parser = pymupdf_parser.PyMuPdfParser()
    pdf_extractor = pdf_schema_extractor.PdfSchemaExtractor(parser=pdf_parser)
    pdf_batch_extractor = batch_pdf_schema_extractor.BatchPdfSchemaExtractor(extractor=pdf_extractor)

    srt_parser = srt_transcript_parser.SRTTranscriptParser()
    srt_extractor = transcript_schema_extractor.TranscriptSchemaExtractor(parser=srt_parser)
    srt_batch_extractor = batch_transcript_schema_extractor.BatchTranscriptSchemaExtractor(extractor=srt_extractor)

    # Collect all materials
    print("Collecting all materials from files...")
    materials = materials_collector.collect(
        pdf_courses_dir=COURSES_DIR / "slides",
        srt_courses_dir=COURSES_DIR / "transcripts" / "lectures",
        courses = COURSES,
        pdf_extractor=pdf_batch_extractor,
        transcript_extractor=srt_batch_extractor,
        pdf_segmenter=page_segmenter.PageSegmenter(),
        srt_segmenter=chapter_segmenter.ChapterSegmenter()
    )
    total_queries = []
    questions_by_lecture = defaultdict(list)

    # Group materials by course and type
    by_course = defaultdict(lambda: defaultdict(list))
    for m in materials:
        by_course[m.course_name][m.type].append(m)

    for course in COURSES:
        pdfs = by_course[course][schemas.MaterialType.SLIDES]
        srts = by_course[course][schemas.MaterialType.TRANSCRIPT]

        all_materials = pdfs + srts
        num_samples = min(100, len(all_materials))
        selected_materials = random.sample(all_materials, num_samples)

        random.shuffle(selected_materials) 

        # Update target difficulty counts per course
        global TARGET_PER_LEVEL
        TARGET_PER_LEVEL = max(1, len(selected_materials) // len(DIFFICULTY_LEVELS))

        for material in selected_materials:
            try:
                difficulty_name = choose_balanced_difficulty()
                difficulty_info = difficulty_levels[difficulty_name]

                print(f"Generating for {material.course_name} / {material.doc_id} ({material.type.value})...")
                questions = question_generator.generate_questions(
                    material=material, 
                    client=client,
                    prompt_module=PROMPT,
                    difficulty_lvl=difficulty_name,
                    difficulty_level_instruction=difficulty_info["explanation"],
                    difficulty_level_example=difficulty_info["example"]
                )
                difficulty_counts[difficulty_name] += 1

                url = get_url_for_material(material)
                for q in questions:
                    q["course_name"] = material.course_name
                    q["lecture_title"] = material.lecture_title
                    q["doc_id"] = material.doc_id
                    q["type"] = material.type.value
                    q["url"] = url
                    questions_by_lecture[material.lecture_title].append(q)

                total_queries.extend(questions)

            except Exception as e:
                import traceback
                print(f"Error in {material.course_name}, {material.doc_id}, {material.lecture_title}: {e}")
                traceback.print_exc()

    # Save grouped questions to one JSON per lecture
    for lecture_title, question_list in questions_by_lecture.items():
        course_name = question_list[0]["course_name"]
        output_dir = output_dir_base / "raw_jsons" / course_name
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{lecture_title}.json"
        with open(output_path, "w") as f:
            json.dump(question_list, f, indent=2)

    # Save all to CSV
    csv_output_path = output_dir_base / f"queries-{timestamp}.csv"
    gateway = csv_query_gateway.CSVQueryGateway(filename=csv_output_path)
    gateway.add(data=total_queries)

    # Print summary
    elapsed_seconds = (datetime.datetime.now() - start_time).total_seconds()
    print(f"Generated {len(total_queries)} questions in {elapsed_seconds:.2f} seconds.")
    print(f"All files saved in: {output_dir_base}")


if __name__ == "__main__":
    main()
