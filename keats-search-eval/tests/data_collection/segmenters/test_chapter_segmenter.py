from datetime import timedelta
import pytest

from services.segmenters import chapter_segmenter
from schemas import schemas


@pytest.fixture
def expected():
    return [
        schemas.TranscriptSegment(
            nr=1,
            parent_file="lecture1.srt",
            timestamp=schemas.Timestamp(
                start=timedelta(seconds=0), end=timedelta(seconds=15)
            ),
            text="Welcome to the course. In this chapter, we will cover the basics.",
            course_name="Sample Course",
            lecture_name="Lecture 1",
            chapter_title="Introduction",
        ),
        schemas.TranscriptSegment(
            nr=2,
            parent_file="lecture1.srt",
            timestamp=schemas.Timestamp(
                start=timedelta(seconds=20), end=timedelta(seconds=35)
            ),
            text="Chapter 2 begins now. Advanced concepts are covered here.",
            course_name="Sample Course",
            lecture_name="Lecture 1",
            chapter_title="Advanced",
        ),
    ]


@pytest.fixture
def schema():
    return schemas.TranscriptSchema(
        file_name="lecture1.srt",
        duration=timedelta(minutes=1),
        subtitles=[
            schemas.Subtitle(
                nr=1,
                text="Welcome to the course.",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=0), end=timedelta(seconds=5)
                ),
            ),
            schemas.Subtitle(
                nr=2,
                text="In this chapter, we will cover the basics.",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=6), end=timedelta(seconds=10)
                ),
            ),
            schemas.Subtitle(
                nr=3,
                text="Chapter 2 begins now.",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=20), end=timedelta(seconds=25)
                ),
            ),
            schemas.Subtitle(
                nr=4,
                text="Advanced concepts are covered here.",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=26), end=timedelta(seconds=30)
                ),
            ),
        ],
        course_name="Sample Course",
        lecture_name="Lecture 1",
        chapters=[
            schemas.Chapter(
                nr=1,
                title="Introduction",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=0), end=timedelta(seconds=15)
                ),
            ),
            schemas.Chapter(
                nr=2,
                title="Advanced",
                timestamp=schemas.Timestamp(
                    start=timedelta(seconds=20), end=timedelta(seconds=35)
                ),
            ),
        ],
    )


def test_segment_transcript_into_chapters(schema, expected):
    observed = chapter_segmenter.ChapterSegmenter.segment(schema)
    assert observed == expected
