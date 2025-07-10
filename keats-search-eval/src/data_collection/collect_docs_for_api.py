import json
import pathlib
from datetime import timedelta

from services.collector import document_api_collector
from services.extractors import pdf_schema_extractor, transcript_schema_extractor
from services.parsers import pymupdf_parser, srt_transcript_parser
from services.segmenters import page_segmenter, chapter_segmenter

OUTPUT_REPO = pathlib.Path("keats-search-api/data")
COURSES_REPO = pathlib.Path("keats-search-eval/data")
MAPPING_FILE = pathlib.Path(
    "keats-search-eval/data/metadata/file_to_metadata_mapping.json"
)

COURSES = [
    "18.404J",
    "6.006",
    "6.0002",
    # add more course folder names here
]


def format_timedelta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def main():
    """Generates a dataset of segmented documents from lecture materials"""

    # Initialize extractors
    pdf_parser = pymupdf_parser.PyMuPdfParser(mapping_path=MAPPING_FILE)
    pdf_extractor = pdf_schema_extractor.PdfSchemaExtractor(parser=pdf_parser)
    srt_parser = srt_transcript_parser.SRTTranscriptParser(mapping_path=MAPPING_FILE)
    srt_extractor = transcript_schema_extractor.TranscriptSchemaExtractor(
        parser=srt_parser
    )

    # Collect all materials
    print("Collecting all materials from files...")
    documents = document_api_collector.collect_api_documents(
        pdf_courses_dir=COURSES_REPO / "slides" / "lectures",
        srt_courses_dir=COURSES_REPO / "transcripts" / "lectures",
        courses=COURSES,
        pdf_extractor=pdf_extractor,
        transcript_extractor=srt_extractor,
        pdf_segmenter=page_segmenter.PageSegmenter(),
        srt_segmenter=chapter_segmenter.ChapterSegmenter(),
    )
    print("Done")

    # Output directory
    output_dir_base = pathlib.Path(OUTPUT_REPO)
    output_dir_base.mkdir(parents=True, exist_ok=True)

    # Save all documents into a single JSON file
    output_file = output_dir_base / "documents.json"
    with open(output_file, "w") as f:
        json.dump([doc.model_dump_flat() for doc in documents], f, indent=2)

    print(f"Saved {len(documents)} documents to {output_file}")


if __name__ == "__main__":
    main()
