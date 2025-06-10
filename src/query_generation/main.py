import datetime
import json
import os
import pathlib

from dotenv import load_dotenv
from openai import OpenAI

import caller
from gateways import csv_gateway
from prompts import query_prompt_builder


# Load environment variables from .env
load_dotenv()
# Set your API key
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

OUTPUT_REPO = "data/queries"


def main():
    """
    Generates a dataset of questions based on lecture content using a language model.

    This script iterates over predefined courses and materials, generates question prompts, 
    calls an LLM to generate questions. The output includes:
    - Raw JSON files organised by course.
    - A CSV summary file with all generated questions and answers.

    This approach was inspired by the work on generating test suites using LLMs 
    by Herdel et al. (2024) [https://doi.org/10.48550/arXiv.2407.12454]
    """
    start_time = datetime.datetime.now()
    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")

    # Define base output directory for this run
    output_dir_base = pathlib.Path(f"{OUTPUT_REPO}/{timestamp}")
    output_dir_base.mkdir(parents=True, exist_ok=True)

    courses = ...

    csv_output_path = output_dir_base / f"queries-{timestamp}.csv"
    gateway = csv_gateway.CSVGateway(filename=csv_output_path)

    total_queries = []

    for course, materials in courses.items():
        for m in materials:

            # Generate a prompt
            prompt = query_prompt_builder.QueryPromptBuilder.build(
                course_name=course, 
                lecture_content=m["content"], 
                num_questions=m["page_count"]
            )

            # Call LLM and generate questions
            questions_set = caller.call_openai(
                client=client,
                system_prompt=prompt.system_prompt.to_dict(),
                user_prompt=prompt.user_prompt.to_dict()
            )

            questions_set = json.dumps([
                {
                    "question": f"What is a key characteristic of NoSQL databases from {m['title']}?",
                    "label": "Basic",
                    "answer": "NoSQL databases allow scaling out by adding more nodes to commodity servers.",
                    "explanation": "This question checks understanding of the 'Volume' aspect discussed in the lecture."
                }
            ])


            # Write raw JSON output
            course_output_dir = output_dir_base / "raw_jsons" / course
            course_output_dir.mkdir(parents=True, exist_ok=True)

            output_path = course_output_dir / f"{m['title']}.json"

            with open(output_path, "w") as file:
                file.write(questions_set)

            # Load JSON from string
            try:
                loaded_questions = json.loads(questions_set)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON for {course} - {m['title']}")
                loaded_questions = []

            # Accumulate total questions
            total_queries.extend(loaded_questions)

    # Add all questions to the CSV
    gateway.add(data=total_queries)

    # Print summary
    time_difference = datetime.datetime.now() - start_time
    elapsed_seconds = time_difference.total_seconds()
    print(f"Generated {len(total_queries)} questions in {elapsed_seconds:.2f} seconds.")
    print(f"All files saved in: {output_dir_base}")


if __name__ == "__main__":
    main()
