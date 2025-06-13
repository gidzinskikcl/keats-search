import datetime
import pathlib
import json

from query_generation import utils
from data_collection.extractors import pdf_schema_extractor, transcript_schema_extractor
from data_collection.parsers import pymupdf_parser, srt_transcript_parser
from data_collection.segmenters import page_segmenter, chapter_segmenter


# Constants
OUTPUT_REPO = "data/queries/sample"
COURSE = "18.404J"
INPUT_DIR =  pathlib.Path("data")
TRANSCRIPT_FILE = INPUT_DIR / "transcripts" / COURSE / "IycOPFmEQk8.en-j3PyPqV-e1s"
SLIDES_FILE = INPUT_DIR / "slides" / COURSE / "18c8cd00b14d48dc5865f3bdc41abd76_MIT18_404f20_lec5"

slides_to_ignore = [1, ]


def main():
    start_time = datetime.datetime.now()
    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")

    pdf_parser = pymupdf_parser.PyMuPdfParser()
    pdf_extractor = pdf_schema_extractor.PdfSchemaExtractor(parser=pdf_parser)
    pdf = pdf_extractor.get(file_path=pathlib.Path(f"{SLIDES_FILE}.pdf"))

    srt_parser = srt_transcript_parser.SRTTranscriptParser()
    srt_extractor = transcript_schema_extractor.TranscriptSchemaExtractor(parser=srt_parser)
    transcript = srt_extractor.get(file_path=pathlib.Path(f"{TRANSCRIPT_FILE}.srt"))

    pdf_segmenter = page_segmenter.PageSegmenter()
    pdf_segments = pdf_segmenter.segment(pdf_schema=pdf)

    srt_segmenter = chapter_segmenter.ChapterSegmenter()
    with open(f"{TRANSCRIPT_FILE}.json", "r", encoding="utf-8") as f:
        srt_metadata = json.load(f)
    chapters = utils.convert_to_chapters(chapters_dict=srt_metadata["chapters"])
    srt_segments = srt_segmenter.segment(transcript_schema=transcript, chapters=chapters)

    slides_to_ignore = [1, 12, 13]
    transcripts_to_ignore = [1, 3, 4, 6, 8, 12, 13, 16]

    pdf_segments = [seg for seg in pdf_segments if seg.nr not in slides_to_ignore]
    srt_segments = [seg for seg in srt_segments if seg.nr not in transcripts_to_ignore]


    pdf_count = 3
    srt_count = 7 

    sample_data = utils.sample(
        pdf_segments=pdf_segments,
        srt_segments=srt_segments,
        pdf_count=pdf_count,
        srt_count=srt_count
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