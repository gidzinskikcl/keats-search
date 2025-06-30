from typing import Union
from datetime import timedelta
import random

from data_collection import schemas

def convert_to_chapters(chapters_dict: list[dict[str, Union[str, float]]]) -> list[schemas.Chapter]:
    result = []
    for nr, c in enumerate(chapters_dict, start=1):
        chapter = schemas.Chapter(
            nr=nr,
            title=c["title"],
            timestamp=schemas.Timestamp(
                start=timedelta(seconds=c["start_time"]),
                end=timedelta(seconds=c["end_time"])
            )
        )
        result.append(chapter)
    return result

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

