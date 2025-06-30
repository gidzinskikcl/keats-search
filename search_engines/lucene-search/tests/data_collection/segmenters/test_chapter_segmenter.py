from datetime import timedelta
import pytest

from data_collection.segmenters.chapter_segmenter import ChapterSegmenter
from data_collection.schemas import TranscriptSchema, Subtitle, Timestamp, Chapter, TranscriptSegment

@pytest.fixture
def expected():
    return [
        TranscriptSegment(
            nr=1,
            parent_file="lecture1.srt",
            timestamp=Timestamp(start=timedelta(seconds=0), end=timedelta(seconds=15)),
            text="Welcome to the course. In this chapter, we will cover the basics.",
            course_name="Sample Course",
            lecture_name="Lecture 1"
        ),
        TranscriptSegment(
            nr=2,
            parent_file="lecture1.srt",
            timestamp=Timestamp(start=timedelta(seconds=20), end=timedelta(seconds=35)),
            text="Chapter 2 begins now. Advanced concepts are covered here.",
            course_name="Sample Course",
            lecture_name="Lecture 1"
        )
    ]

@pytest.fixture
def schema():
    return TranscriptSchema(
        file_name="lecture1.srt",
        duration=timedelta(minutes=1),
        subtitles=[
            Subtitle(nr=1, text="Welcome to the course.", timestamp=Timestamp(start=timedelta(seconds=0), end=timedelta(seconds=5))),
            Subtitle(nr=2, text="In this chapter, we will cover the basics.", timestamp=Timestamp(start=timedelta(seconds=6), end=timedelta(seconds=10))),
            Subtitle(nr=3, text="Chapter 2 begins now.", timestamp=Timestamp(start=timedelta(seconds=20), end=timedelta(seconds=25))),
            Subtitle(nr=4, text="Advanced concepts are covered here.", timestamp=Timestamp(start=timedelta(seconds=26), end=timedelta(seconds=30))),
        ],
        course_name="Sample Course",
        lecture_name="Lecture 1",
        chapters=[
            Chapter(nr=1, title="Introduction", timestamp=Timestamp(start=timedelta(seconds=0), end=timedelta(seconds=15))),
            Chapter(nr=2, title="Advanced", timestamp=Timestamp(start=timedelta(seconds=20), end=timedelta(seconds=35))),
        ]
    )

def test_segment_transcript_into_chapters(schema, expected):
    observed = ChapterSegmenter.segment(schema)
    assert observed == expected
