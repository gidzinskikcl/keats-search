from datetime import datetime, timezone
from pathlib import Path
import json

from data_collection import schemas
from query_generation import main
from query_generation.prompts import templates

# Setup
SAMPLE_ID = "exp2025_lect3_structured"
LECTURE_NAME = "lecture03"
COURSE_NAME = "Data Structures"
MODEL = "gpt-4o-2025-06-12" # change before official run 

# Generate timestamp
now = datetime.now(timezone.utc)
timestamp = now.isoformat()
readable_time = now.strftime("%Y-%m-%d_%H%M")

# File and directory setup
SAMPLE_FILE = f"data/queries/validation/samples/{LECTURE_NAME}_sample.json"
OUTPUT_DIR = Path(f"data/queries/validation/results/{LECTURE_NAME}/{SAMPLE_ID}_{readable_time}")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    # Initialize OpenAI client, prompt version and timestamp
    client = main.load_openai_client()
    prompt_module = templates.V1
    timestamp = datetime.now(timezone.utc).isoformat()
    

    # Load samples
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        sample = json.load(f)

    # Generate questions for each sample
    results = []
    for s in sample:
        print(f"Generating for {s['doc_id']}...")

        material = schemas.LectureMaterial(
            course_name=COURSE_NAME,
            type=schemas.MaterialType(s["type"]),  #TODO 
            title=s["doc_id"],
            content=s["text"],
            length=s["length"]
        )

        try:
            questions = main.generate_questions(
                material=material,
                client=client,
                prompt_module=prompt_module,
            )

        except Exception as e:
            print(f"Error in {s['doc_id']}: {e}")
            questions = []

        result = {
            **s,
            "questions": questions,
            "metadata": {
                "model": MODEL,
                "variant": prompt_module.VARIANT,
                "sample_id": SAMPLE_ID,
                "timestamp": timestamp
            }
        }
        results.append(result)

    # Save results
    output_file = OUTPUT_DIR / f"{SAMPLE_ID}_questions.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Saved structured results to {output_file}")

if __name__ == "__main__":
    main()

