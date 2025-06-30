import datetime
import json
import pathlib

from data_collection.collector import document_collector
from data_collection.extractors import batch_pdf_schema_extractor, batch_transcript_schema_extractor, pdf_schema_extractor, transcript_schema_extractor
from data_collection.parsers import pymupdf_parser, srt_transcript_parser
from data_collection.segmenters import page_segmenter, chapter_segmenter
from data_collection.utils import utils

OUTPUT_REPO = pathlib.Path("data/documents")
COURSES_REPO = pathlib.Path("data")

COURSES = [
    "18.404J",
    "6.006",
    # "6.172",
    # "6.S897",
    "6.0002"
    # add more course folder names here
]


def main():
    """Generates a dataset of segmented documents from lecture materials"""
    start_time = datetime.datetime.now()
    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")

    # Initialize extractors
    pdf_parser = pymupdf_parser.PyMuPdfParser()
    pdf_extractor = pdf_schema_extractor.PdfSchemaExtractor(parser=pdf_parser)
    pdf_batch_extractor = batch_pdf_schema_extractor.BatchPdfSchemaExtractor(extractor=pdf_extractor)

    srt_parser = srt_transcript_parser.SRTTranscriptParser()
    srt_extractor = transcript_schema_extractor.TranscriptSchemaExtractor(parser=srt_parser)
    srt_batch_extractor = batch_transcript_schema_extractor.BatchTranscriptSchemaExtractor(extractor=srt_extractor)

    # Collect all materials
    print("Collecting all materials from files...")
    documents = document_collector.collect(
        pdf_courses_dir=COURSES_REPO / "slides",
        srt_courses_dir=COURSES_REPO / "transcripts" / "lectures",
        courses = COURSES,
        pdf_extractor=pdf_batch_extractor,
        transcript_extractor=srt_batch_extractor,
        pdf_segmenter=page_segmenter.PageSegmenter(),
        srt_segmenter=chapter_segmenter.ChapterSegmenter()
    )
    print("Done")
    # Output directory
    output_dir_base = pathlib.Path(f"{OUTPUT_REPO}/{timestamp}")
    output_dir_base.mkdir(parents=True, exist_ok=True)

    # Save all documents into a single JSON file
    output_file = output_dir_base / "documents.json"
    with open(output_file, "w") as f:
        json.dump([utils.document_to_dict(doc) for doc in documents], f, indent=2)

    print(f"Saved {len(documents)} documents to {output_file}")

if __name__ == "__main__":
    main()
