import pathlib
from unittest.mock import Mock
from datetime import timedelta

from schemas import schemas
from services.collector import document_collector


def test_collect():
    pdf_schema = Mock()
    pdf_segment = schemas.PdfSegment(
        parent_file="slide_deck",
        nr=1,
        text="PDF slide content",
        course_name="IR",
        lecture_name="Intro to IR"
    )

    transcript_schema = Mock()
    transcript_segment = schemas.TranscriptSegment(
        nr=2,
        parent_file="lecture_vid",
        timestamp=schemas.Timestamp(start=timedelta(seconds=0), end=timedelta(seconds=30)),
        text="Transcript content",
        course_name="IR",
        lecture_name="Intro to IR"
    )
    transcript_segment.chapter_title = "Introduction"

    pdf_extractor = Mock()
    pdf_extractor.extract_all.return_value = [pdf_schema]

    pdf_segmenter = Mock()
    pdf_segmenter.segment.return_value = [pdf_segment]

    transcript_extractor = Mock()
    transcript_extractor.extract_all.return_value = [transcript_schema]

    transcript_segmenter = Mock()
    transcript_segmenter.segment.return_value = [transcript_segment]

    observed = document_collector.collect(
        pdf_courses_dir=pathlib.Path("/path/to/pdfs"),
        srt_courses_dir=pathlib.Path("/path/to/srts"),
        courses=["IR"],
        pdf_extractor=pdf_extractor,
        transcript_extractor=transcript_extractor,
        pdf_segmenter=pdf_segmenter,
        srt_segmenter=transcript_segmenter,
    )

    expected = [
        schemas.DocumentSchema(
            doc_id="slide_deck_1_pdf",
            content="PDF slide content",
            title="Intro to IR",
            timestamp=None,
            pageNumber=1,
            keywords=[],
            doc_type=schemas.MaterialType.SLIDES,
            speaker=None,
            course_name="IR"
        ),
        schemas.DocumentSchema(
            doc_id="lecture_vid_2_srt",
            content="Transcript content",
            title="Intro to IR",
            timestamp=schemas.Timestamp(start=timedelta(seconds=0), end=timedelta(seconds=30)),
            pageNumber=2,
            keywords=["Introduction"],
            doc_type=schemas.MaterialType.TRANSCRIPT,
            speaker="Unknown",
            course_name="IR"
        )
    ]

    assert observed == expected



def test_collect_pdf_documents():
    pdf_schema = Mock()
    pdf_segment = schemas.PdfSegment(
        parent_file="slides",
        nr=5,
        text="Content from PDF",
        course_name="ML",
        lecture_name="Neural Nets"
    )

    extractor = Mock()
    extractor.extract_all.return_value = [pdf_schema]

    segmenter = Mock()
    segmenter.segment.return_value = [pdf_segment]

    observed = document_collector.collect_pdf_documents(
        courses_dir=pathlib.Path("/fake/dir"),
        courses=["ML"],
        extractor=extractor,
        segmenter=segmenter
    )

    expected = [
        schemas.DocumentSchema(
            doc_id="slides_5_pdf",
            content="Content from PDF",
            title="Neural Nets",
            timestamp=None,
            pageNumber=5,
            keywords=[],
            doc_type=schemas.MaterialType.SLIDES,
            speaker=None,
            course_name="ML"
        )
    ]

    assert observed == expected



def test_collect_transcript_documents():
    transcript_schema = Mock()
    transcript_segment = schemas.TranscriptSegment(
        nr=1,
        parent_file="video1",
        timestamp=schemas.Timestamp(start=timedelta(seconds=0), end=timedelta(seconds=60)),
        text="Lecture segment content",
        course_name="AI",
        lecture_name="Search Algorithms"
    )
    transcript_segment.chapter_title = "Search Overview"

    extractor = Mock()
    extractor.extract_all.return_value = [transcript_schema]

    segmenter = Mock()
    segmenter.segment.return_value = [transcript_segment]

    observed = document_collector.collect_transcript_documents(
        courses_dir=pathlib.Path("/fake/dir"),
        courses=["AI"],
        extractor=extractor,
        segmenter=segmenter
    )

    expected = [
        schemas.DocumentSchema(
            doc_id="video1_1_srt",
            content="Lecture segment content",
            title="Search Algorithms",
            timestamp=schemas.Timestamp(start=timedelta(seconds=0), end=timedelta(seconds=60)),
            pageNumber=1,
            keywords=["Search Overview"],
            doc_type=schemas.MaterialType.TRANSCRIPT,
            speaker="Unknown",
            course_name="AI"
        )
    ]

    assert observed == expected

