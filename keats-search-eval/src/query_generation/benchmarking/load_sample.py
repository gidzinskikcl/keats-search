import datetime
import pathlib
import json
import random
from typing import Union

from schemas import schemas
from services.extractors import pdf_schema_extractor, transcript_schema_extractor
from services.parsers import pymupdf_parser, srt_transcript_parser
from services.segmenters import page_segmenter, chapter_segmenter


# Constants
OUTPUT_REPO = "keats-search-eval/data/queries/sample"
COURSE = "18.404J"
INPUT_DIR = pathlib.Path("keats-search-eval/data")
TRANSCRIPT_FILE = INPUT_DIR / "transcripts" / COURSE / "IycOPFmEQk8.en-j3PyPqV-e1s"
SLIDES_FILE = (
    INPUT_DIR / "slides" / COURSE / "18c8cd00b14d48dc5865f3bdc41abd76_MIT18_404f20_lec5"
)

slides_to_ignore = [
    1,
]


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


def main():
    start_time = datetime.datetime.now()
    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")

    pdf_parser = pymupdf_parser.PyMuPdfParser()
    pdf_extractor = pdf_schema_extractor.PdfSchemaExtractor(parser=pdf_parser)
    pdf = pdf_extractor.get(file_path=pathlib.Path(f"{SLIDES_FILE}.pdf"))

    srt_parser = srt_transcript_parser.SRTTranscriptParser()
    srt_extractor = transcript_schema_extractor.TranscriptSchemaExtractor(
        parser=srt_parser
    )
    transcript = srt_extractor.get(file_path=pathlib.Path(f"{TRANSCRIPT_FILE}.srt"))

    pdf_segmenter = page_segmenter.PageSegmenter()
    pdf_segments = pdf_segmenter.segment(pdf_schema=pdf)

    srt_segmenter = chapter_segmenter.ChapterSegmenter()
    srt_segments = srt_segmenter.segment(transcript_schema=transcript)

    slides_to_ignore = [1, 12, 13]
    transcripts_to_ignore = [1, 3, 4, 6, 8, 12, 13, 16]

    pdf_segments = [seg for seg in pdf_segments if seg.nr not in slides_to_ignore]
    srt_segments = [seg for seg in srt_segments if seg.nr not in transcripts_to_ignore]

    pdf_count = 3
    srt_count = 7

    sample_data = sample(
        pdf_segments=pdf_segments,
        srt_segments=srt_segments,
        pdf_count=pdf_count,
        srt_count=srt_count,
    )

    # Output directory
    output_dir_base = pathlib.Path(f"{OUTPUT_REPO}/{timestamp}")
    output_dir_base.mkdir(parents=True, exist_ok=True)

    sample_filename = pathlib.Path(f"_{pdf_count}_pdf_{srt_count}_srt_{timestamp}.json")
    sample_path = output_dir_base / sample_filename

    with sample_path.open("w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2)

    print(f"Saved sample to {sample_path}")


if __name__ == "__main__":
    main()
