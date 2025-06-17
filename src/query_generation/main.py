import datetime
import json
import pathlib


from gateways import csv_gateway
from data_collection.extractors import batch_pdf_schema_extractor, batch_transcript_schema_extractor, pdf_schema_extractor, transcript_schema_extractor
from data_collection.parsers import pymupdf_parser, srt_transcript_parser
from data_collection import materials_collector, schemas

from query_generation import utils
from query_generation.llm import client as llm_client


# Constants
OUTPUT_REPO = "data/queries"
COURSES_DIR = "/Users/piotrgidzinski/KeatsSearch_workspace/data/courses/test"


def initialize_pdf_extractors() -> batch_pdf_schema_extractor.BatchPdfSchemaExtractor:
    """Initializes and returns the PDF extractor."""
    parser = pymupdf_parser.PyMuPdfParser()
    extractor = pdf_schema_extractor.PdfSchemaExtractor(parser=parser)
    return batch_pdf_schema_extractor.BatchPdfSchemaExtractor(extractor=extractor)


def initialize_srt_extractors() -> batch_transcript_schema_extractor.BatchTranscriptSchemaExtractor:
    """Initializes and returns the Transcript extractor."""
    parser = srt_transcript_parser.SRTTranscriptParser()
    extractor = transcript_schema_extractor.TranscriptSchemaExtractor(parser=parser)
    return batch_transcript_schema_extractor.BatchTranscriptSchemaExtractor(extractor=extractor)


def determine_num_questions(material: schemas.LectureMaterial) -> int:
    if material.type == schemas.MaterialType.TRANSCRIPT:
        return 5
    elif material.type == schemas.MaterialType.SLIDES:
        if material.length <= 5:
            return 1
        elif material.length <= 9:
            return 2
        else:
            return 5
    else:
        raise ValueError(f"Unknown material type: {material.type}")



    
def save_raw_json(questions_set: list[dict], output_dir_base: pathlib.Path, material: schemas.LectureMaterial) -> None:
    """Saves generated questions to a raw JSON file."""
    course_output_dir = output_dir_base / "raw_jsons" / material.course_name
    course_output_dir.mkdir(parents=True, exist_ok=True)
    output_path = course_output_dir / f"{material.title}.json"
    with open(output_path, "w") as file:
        json.dump(questions_set, file, indent=2)

def main():
    """Generates a dataset of questions based on lecture content using a language model."""
    start_time = datetime.datetime.now()
    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")

    # Output directory
    output_dir_base = pathlib.Path(f"{OUTPUT_REPO}/{timestamp}")
    output_dir_base.mkdir(parents=True, exist_ok=True)

    # Initialize OpenAI client and extractors
    client = llm_client.load_openai_client()
    pdf_extractor = initialize_pdf_extractors()
    transcript_extractor = initialize_srt_extractors()

    # Collect all materials
    courses_dir = pathlib.Path(COURSES_DIR)
    materials = materials_collector.collect(
        courses_dir=courses_dir,
        pdf_extractor=pdf_extractor,
        transcript_extractor=transcript_extractor
    )

    # CSV gateway
    csv_output_path = output_dir_base / f"queries-{timestamp}.csv"
    gateway = csv_gateway.CSVGateway(filename=csv_output_path)

    total_queries = []

    for material in materials:
        num_questions = determine_num_questions(material=material)
        questions = utils.generate_questions(material=material, client=client, num_questions=num_questions)
        save_raw_json(questions, output_dir_base, material)
        total_queries.extend(questions)

    # Save all to CSV
    gateway.add(data=total_queries)

    # Print summary
    elapsed_seconds = (datetime.datetime.now() - start_time).total_seconds()
    print(f"Generated {len(total_queries)} questions in {elapsed_seconds:.2f} seconds.")
    print(f"All files saved in: {output_dir_base}")


if __name__ == "__main__":
    main()
