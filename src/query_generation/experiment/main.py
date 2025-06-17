from datetime import datetime, timezone
import pathlib
import json

from data_collection import schemas
from query_generation.llm import question_generator
from query_generation.prompts import templates
from query_generation.llm import client as llm_client


# Setup
COURSE_NAME = "Theory of Computation"
MODEL = "gpt-4o-2025-06-17" 
SAMPLE_DIR = "2025-06-13_15-47-47"
SAMPLE = "_3_pdf_7_srt_2025-06-13_15-47-47"
PROMPT_VARIANT = templates.V1

# Generate timestamp
now = datetime.now(timezone.utc)
timestamp = now.isoformat()
readable_time = now.strftime("%Y-%m-%d_%H%M")

# File and directory setup
SAMPLE_FILE = pathlib.Path(f"data/queries/sample/{SAMPLE_DIR}/{SAMPLE}.json")
OUTPUT_DIR = pathlib.Path(f"data/queries/validation/results/{readable_time}/sample_{SAMPLE_DIR}_variant_{PROMPT_VARIANT.__name__}_{readable_time}")


def main():

    # Initialize OpenAI client, prompt version and timestamp
    client = llm_client.load_openai_client()
    timestamp = datetime.now(timezone.utc).isoformat()    

    # Load samples
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        sample = json.load(f)

    # Generate questions for each sample
    results = []
    for s in sample:
        print(f"Generating for {s['doc_id']}...")

        length = 10 if s["type"] == "pdf" else 4439

        material = schemas.LectureMaterial(
            course_name=COURSE_NAME,
            type=schemas.MaterialType(s["type"]),  #TODO 
            title=s["doc_id"],
            content=s["text"],
            length=length
        )

        try:
            questions = question_generator.generate_questions(
                material=material,
                client=client,
                prompt_module=PROMPT_VARIANT,
                num_questions=3 if s["type"] == "pdf" else 6
            )

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
                "timestamp": timestamp
            }
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

