import pytest

from datetime import timedelta


from data_collection import schemas
from data_collection import materials_collector


class MockPdfSchema:
    def __init__(self, course_name, file_name, page_texts):
        self.course_name = course_name
        self.file_name = file_name
        self.pages = [schemas.PdfPage(nr=idx, text=text) for idx, text in enumerate(page_texts, start=1)]


class MockTranscriptSchema:
    def __init__(self, course_name, file_name, subtitles, duration):
        self.course_name = course_name
        self.file_name = file_name
        self.subtitles = [
            schemas.Subtitle(nr=i, text=text, timestamp=schemas.Timestamp(start=timedelta(seconds=i), end=timedelta(seconds=i+1)))
            for i, text in enumerate(subtitles, start=1)
        ]
        self.duration = duration


class MockPdfExtractor:
    def extract_all(self, courses_dir):
        return [
            MockPdfSchema("TestCourse", "slides1", ["Page 1 text", "Page 2 text"])
        ]


class MockTranscriptExtractor:
    def extract_all(self, courses_dir):
        return [
            MockTranscriptSchema("TestCourse", "lecture1", ["Hello", "World"], 120)
        ]

@pytest.fixture
def expected_pdf_material():
    result = [
        schemas.LectureMaterial(
            course_name="TestCourse",
            title="slides1",
            content="Page 1 text\nPage 2 text",
            length=2,
            type=schemas.MaterialType.SLIDES
        )
    ] 
    return result


@pytest.fixture
def expected_transcript_material():
    result = [
        schemas.LectureMaterial(
            course_name="TestCourse",
            title="lecture1",
            content="Hello\nWorld",
            length=120,
            type=schemas.MaterialType.TRANSCRIPT
        )
    ] 
    return result


def test_collect_pdfs(tmp_path, expected_pdf_material):
    extractor = MockPdfExtractor()
    observed = materials_collector.collect_pdfs(tmp_path, extractor)

    assert expected_pdf_material == observed


def test_collect_transcripts(tmp_path, expected_transcript_material):
    extractor = MockTranscriptExtractor()
    observed = materials_collector.collect_transcripts(tmp_path, extractor)

    assert expected_transcript_material == observed


def test_collect(tmp_path, expected_pdf_material, expected_transcript_material):
    pdf_extractor = MockPdfExtractor()
    transcript_extractor = MockTranscriptExtractor()

    observed = materials_collector.collect(tmp_path, pdf_extractor, transcript_extractor)

    expected = expected_pdf_material + expected_transcript_material
    assert observed == expected