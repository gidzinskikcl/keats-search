import pytest
from datetime import timedelta
from schemas import schemas
from services.collector import materials_collector


class MockPdfExtractor:
    def extract_all(self, courses_root, courses):
        return [
            schemas.PdfSchema(
                file_name="slides1",
                pages=[
                    schemas.PdfPage(nr=1, text="Page 1 text"),
                    schemas.PdfPage(nr=2, text="Page 2 text")
                ],
                course_name="TestCourse",
                lecture_name="Lecture 1"
            )
        ]


class MockTranscriptExtractor:
    def extract_all(self, courses_root, courses):
        return [
            schemas.TranscriptSchema(
                file_name="lecture1",
                duration=timedelta(seconds=120),
                subtitles=[
                    schemas.Subtitle(
                        nr=1,
                        text="Hello",
                        timestamp=schemas.Timestamp(start=timedelta(seconds=1), end=timedelta(seconds=2))
                    ),
                    schemas.Subtitle(
                        nr=2,
                        text="World",
                        timestamp=schemas.Timestamp(start=timedelta(seconds=3), end=timedelta(seconds=4))
                    )
                ],
                course_name="TestCourse",
                lecture_name="Lecture 1"
            )
        ]


class MockPdfSegmenter:
    def segment(self, pdf_schema: schemas.PdfSchema):
        return [
            schemas.PdfSegment(
                nr=1,
                parent_file=pdf_schema.file_name,
                text="\n".join(page.text for page in pdf_schema.pages),
                course_name=pdf_schema.course_name,
                lecture_name=pdf_schema.lecture_name
            )
        ]


class MockTranscriptSegmenter:
    def segment(self, transcript_schema: schemas.TranscriptSchema):
        return [
            schemas.TranscriptSegment(
                nr=1,
                parent_file=transcript_schema.file_name,
                timestamp=schemas.Timestamp(start=timedelta(seconds=0), end=timedelta(seconds=120)),
                text="\n".join(sub.text for sub in transcript_schema.subtitles),
                course_name=transcript_schema.course_name,
                lecture_name=transcript_schema.lecture_name
            )
        ]


@pytest.fixture
def expected_pdf_material():
    return [
        schemas.LectureMaterial(
            course_name="TestCourse",
            doc_id="slides1_1_pdf",
            content="Page 1 text\nPage 2 text",
            length=None,
            type=schemas.MaterialType.SLIDES,
            lecture_title="Lecture 1"
        )
    ]


@pytest.fixture
def expected_transcript_material():
    return [
        schemas.LectureMaterial(
            course_name="TestCourse",
            doc_id="lecture1_1_srt",
            content="Hello\nWorld",
            length=None,
            type=schemas.MaterialType.TRANSCRIPT,
            lecture_title="Lecture 1"
        )
    ]


def test_collect_pdfs(tmp_path, expected_pdf_material):
    extractor = MockPdfExtractor()
    segmenter = MockPdfSegmenter()
    observed = materials_collector.collect_pdfs(tmp_path, ["TestCourse"], extractor, segmenter)
    assert observed == expected_pdf_material


def test_collect_transcripts(tmp_path, expected_transcript_material):
    extractor = MockTranscriptExtractor()
    segmenter = MockTranscriptSegmenter()
    observed = materials_collector.collect_transcripts(tmp_path, ["TestCourse"], extractor, segmenter)
    assert observed == expected_transcript_material


def test_collect(tmp_path, expected_pdf_material, expected_transcript_material):
    pdf_path = tmp_path / "slides"
    srt_path = tmp_path / "transcripts"
    pdf_extractor = MockPdfExtractor()
    transcript_extractor = MockTranscriptExtractor()
    pdf_segmenter = MockPdfSegmenter()
    srt_segmenter = MockTranscriptSegmenter()

    observed = materials_collector.collect(
        pdf_path,
        srt_path,
        ["TestCourse"],
        pdf_extractor,
        transcript_extractor,
        pdf_segmenter,
        srt_segmenter
    )

    expected = expected_pdf_material + expected_transcript_material
    assert observed == expected
