import datetime
import json
import pathlib
from datetime import timedelta

from services.collector import document_collector
from services.extractors import (
    batch_pdf_schema_extractor,
    batch_transcript_schema_extractor,
    pdf_schema_extractor,
    transcript_schema_extractor,
)
from services.parsers import pymupdf_parser, srt_transcript_parser
from services.segmenters import page_segmenter, chapter_segmenter

from schemas import schemas

OUTPUT_REPO = pathlib.Path("keats-search-eval/data/documents")
COURSES_REPO = pathlib.Path("keats-search-eval/data")

COURSES = [
    "18.404J",
    "6.006",
    # "6.172",
    # "6.S897",
    "6.0002",
    # add more course folder names here
]


def document_to_dict(doc: schemas.DocumentSchema) -> dict:
    return {
        "documentId": doc.doc_id,
        "content": doc.content,
        "title": doc.title,
        "start": format_timedelta(doc.timestamp.start) if doc.timestamp else None,
        "end": format_timedelta(doc.timestamp.end) if doc.timestamp else None,
        "slideNumber": doc.pageNumber,
        "keywords": doc.keywords,
        "type": _get_type(doc.doc_type.value),
        "speaker": doc.speaker,
        "courseName": doc.course_name,
    }


def _get_type(type: str) -> str:
    if type == "pdf":
        return "SLIDE"
    elif type == "srt":
        return "VIDEO_TRANSCRIPT"
    else:
        raise ValueError(f"Unsupported document type: '{type}'")


def format_timedelta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def main():
    """Generates a dataset of segmented documents from lecture materials"""
    start_time = datetime.datetime.now()
    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")

    # Initialize extractors
    pdf_parser = pymupdf_parser.PyMuPdfParser()
    pdf_extractor = pdf_schema_extractor.PdfSchemaExtractor(parser=pdf_parser)
    pdf_batch_extractor = batch_pdf_schema_extractor.BatchPdfSchemaExtractor(
        extractor=pdf_extractor
    )

    srt_parser = srt_transcript_parser.SRTTranscriptParser()
    srt_extractor = transcript_schema_extractor.TranscriptSchemaExtractor(
        parser=srt_parser
    )
    srt_batch_extractor = (
        batch_transcript_schema_extractor.BatchTranscriptSchemaExtractor(
            extractor=srt_extractor
        )
    )

    # Collect all materials
    print("Collecting all materials from files...")
    documents = document_collector.collect(
        pdf_courses_dir=COURSES_REPO / "slides",
        srt_courses_dir=COURSES_REPO / "transcripts" / "lectures",
        courses=COURSES,
        pdf_extractor=pdf_batch_extractor,
        transcript_extractor=srt_batch_extractor,
        pdf_segmenter=page_segmenter.PageSegmenter(),
        srt_segmenter=chapter_segmenter.ChapterSegmenter(),
    )
    print("Done")
    # Output directory
    output_dir_base = pathlib.Path(f"{OUTPUT_REPO}/{timestamp}")
    output_dir_base.mkdir(parents=True, exist_ok=True)

    # Save all documents into a single JSON file
    output_file = output_dir_base / "documents.json"
    with open(output_file, "w") as f:
        json.dump([document_to_dict(doc) for doc in documents], f, indent=2)

    print(f"Saved {len(documents)} documents to {output_file}")


if __name__ == "__main__":
    main()
