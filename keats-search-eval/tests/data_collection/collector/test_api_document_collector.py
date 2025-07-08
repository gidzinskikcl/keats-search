from datetime import timedelta
from unittest.mock import MagicMock
import pathlib
import pytest

from services.collector import document_api_collector


@pytest.fixture
def expected_api_documents():
    return [
        document_api_collector.ApiDocumentSchema(
            id="Lecture_1.pdf_1_pdf",
            doc_id="Lecture_1.pdf",
            content="This is slide 1 content",
            timestamp=None,
            page_number="1",
            lecture_id="1",
            lecture_title="Lecture 1 - Intro",
            course_id="18.404J",
            course_name="Theory of Computation",
            doc_type=document_api_collector.MaterialType.SLIDES,
        ),
        document_api_collector.ApiDocumentSchema(
            id="video_file_1_1_mp4",
            doc_id="video_file_1",
            content="This is spoken content",
            timestamp=document_api_collector.Timestamp(
                start=timedelta(seconds=0),
                end=timedelta(seconds=10),
            ),
            page_number="1",
            lecture_id="1",
            lecture_title="Lecture 1 - Intro",
            course_id="18.404J",
            course_name="Theory of Computation",
            doc_type=document_api_collector.MaterialType.TRANSCRIPT,
        ),
    ]


def test_collect_api_documents(expected_api_documents):
    # Mock segments
    fake_pdf_segment = MagicMock()
    fake_pdf_segment.parent_file = "Lecture_1.pdf"
    fake_pdf_segment.nr = "1"
    fake_pdf_segment.text = "This is slide 1 content"
    fake_pdf_segment.lecture_id = "1"
    fake_pdf_segment.lecture_name = "Lecture 1 - Intro"
    fake_pdf_segment.course_id = "18.404J"
    fake_pdf_segment.course_name = "Theory of Computation"

    fake_transcript_segment = MagicMock()
    fake_transcript_segment.parent_file = "video_file_1"
    fake_transcript_segment.nr = "1"
    fake_transcript_segment.text = "This is spoken content"
    fake_transcript_segment.lecture_id = "1"
    fake_transcript_segment.lecture_name = "Lecture 1 - Intro"
    fake_transcript_segment.course_id = "18.404J"
    fake_transcript_segment.course_name = "Theory of Computation"
    fake_transcript_segment.timestamp.start = 0
    fake_transcript_segment.timestamp.end = 10

    pdf_extractor = MagicMock()
    transcript_extractor = MagicMock()

    pdf_segmenter = MagicMock()
    srt_segmenter = MagicMock()

    pdf_extractor.get.return_value = MagicMock()
    transcript_extractor.get.return_value = MagicMock()

    pdf_segmenter.segment.return_value = [fake_pdf_segment]
    srt_segmenter.segment.return_value = [fake_transcript_segment]

    courses = ["18.404J"]
    fake_pdf_dir = MagicMock(spec=pathlib.Path)
    fake_srt_dir = MagicMock(spec=pathlib.Path)

    course_dir = MagicMock(spec=pathlib.Path)
    course_dir.name = "18.404J"
    course_dir.is_dir.return_value = True

    lecture_dir = MagicMock(spec=pathlib.Path)
    lecture_dir.name = "Lecture 1 - Intro"
    lecture_dir.is_dir.return_value = True

    pdf_file = MagicMock(spec=pathlib.Path)
    pdf_file.suffix = ".pdf"
    pdf_file.name = "Lecture_1.pdf"

    srt_file = MagicMock(spec=pathlib.Path)
    srt_file.suffix = ".srt"
    srt_file.name = "video_file_1"

    # Patch iterdir/glob for instance methods
    fake_pdf_dir.iterdir.return_value = [course_dir]
    course_dir.iterdir.return_value = [lecture_dir]
    lecture_dir.glob.return_value = [pdf_file]

    fake_srt_dir.iterdir.return_value = [course_dir]
    course_dir.iterdir.return_value = [lecture_dir]
    lecture_dir.glob.return_value = [srt_file]

    observed = document_api_collector.collect_api_documents(
        pdf_courses_dir=fake_pdf_dir,
        srt_courses_dir=fake_srt_dir,
        courses=courses,
        pdf_extractor=pdf_extractor,
        transcript_extractor=transcript_extractor,
        pdf_segmenter=pdf_segmenter,
        srt_segmenter=srt_segmenter,
    )

    assert observed == expected_api_documents
