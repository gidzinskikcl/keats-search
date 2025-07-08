from datetime import datetime, timezone
import pathlib
import json
import random
from collections import defaultdict


from schemas import schemas
from query_generation.llm import question_generator
from query_generation.prompts import templates
from services.llm_based import client as llm_client


# Setup
COURSE_NAME = "Theory of Computation"
LECTURE_TITLE = "5. CF Pumping Lemma, Turing Machines"
MODEL = "gpt-4o-2025-06-17"
SAMPLE_DIR = "2025-06-13_15-47-47"
SAMPLE = "_3_pdf_7_srt_2025-06-13_15-47-47"
# PROMPT_VARIANT = templates.V3
PROMPT_VARIANT = templates.V4

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
        """,
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
        """,
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
        """,
    },
}

DIFFICULTY_LEVELS = ["Basic", "Intermediate", "Advanced"]
TARGET_PER_LEVEL = None  # Will be set based on total segments
difficulty_counts = defaultdict(int)

# Generate timestamp
now = datetime.now(timezone.utc)
timestamp = now.isoformat()
readable_time = now.strftime("%Y-%m-%d_%H%M")

# File and directory setup
SAMPLE_FILE = pathlib.Path(
    f"keats-search-eval/data/queries/sample/{SAMPLE_DIR}/{SAMPLE}.json"
)
OUTPUT_DIR = pathlib.Path(
    f"keats-search-eval/data/queries/validation/results/{readable_time}/sample_{SAMPLE_DIR}_variant_{PROMPT_VARIANT.__name__}_{readable_time}"
)


def choose_balanced_difficulty():
    # Try to balance across difficulties
    remaining = {
        lvl: TARGET_PER_LEVEL - difficulty_counts[lvl] for lvl in DIFFICULTY_LEVELS
    }
    # Filter to levels that still need more
    eligible = [lvl for lvl, rem in remaining.items() if rem > 0]

    # If all full, pick randomly
    if not eligible:
        return random.choice(DIFFICULTY_LEVELS)

    return random.choice(eligible)


def main():

    # Initialize OpenAI client, prompt version and timestamp
    client = llm_client.load_openai_client()
    timestamp = datetime.now(timezone.utc).isoformat()

    # Load samples
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        sample = json.load(f)

    total_segments = len(sample)
    global TARGET_PER_LEVEL
    TARGET_PER_LEVEL = total_segments // len(DIFFICULTY_LEVELS)

    # Generate questions for each sample
    results = []
    for s in sample:
        print(f"Generating for {s['doc_id']}...")

        length = 10 if s["type"] == "pdf" else 4439

        material = schemas.LectureMaterial(
            course_name=COURSE_NAME,
            type=schemas.MaterialType(s["type"]),
            doc_id=s["doc_id"],
            content=s["text"],
            length=length,
            lecture_title=LECTURE_TITLE,
        )

        try:
            difficulty_name = choose_balanced_difficulty()
            difficulty_info = difficulty_levels[difficulty_name]

            questions = question_generator.generate_questions(
                material=material,
                client=client,
                prompt_module=PROMPT_VARIANT,
                num_questions=1,
                difficulty_lvl=difficulty_name,
                difficulty_level_instruction=difficulty_info["explanation"],
                difficulty_level_example=difficulty_info["example"],
            )

            difficulty_counts[difficulty_name] += 1

        except Exception as e:
            print(f"Error in {s['doc_id']}: {e}")
            questions = []

        result = {
            **s,
            "questions": questions,
            "metadata": {
                "model": MODEL,
                "variant": PROMPT_VARIANT.VARIANT,
                "sample": SAMPLE,
                "timestamp": timestamp,
            },
        }
        results.append(result)

    # Save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"{SAMPLE}_questions.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Saved structured results to {output_file}")


if __name__ == "__main__":
    main()
