import pytest
from data_collection.transformers import segment2doc
from entities import segment, document

@pytest.fixture
def transformer():
    return segment2doc.Segment2DocumentTransformer()

@pytest.mark.parametrize(
    "text, file_metadata, expected_doc_id, expected_file_type, expected_content_type, expected_keywords, expected_length, expected_start_time, expected_end_time",
    [
        (
            "This is some sample text for slide 1.",
            {
                "doc_id": "7CCSMATAI_w1_seg_1",
                "course_id": "7CCSMATAI",
                "segment_id": "2599942",
                "segment_nr": 1,
                "file_extension": "pdf",
                "doc_title": "Lecture 1",
                "course_title": "Advanced Topics in AI",
                "speakers": ["Prof. John Smith"],
                "date": "2025-06-06",
                "length": "15",
                "url": "https://example.com/slides/1.pdf",
                "description": "Introductory lecture on AI topics",
                "notes": "Important for final exam",
                "source": "King's College",
                "version": "1.0.0",
                "is_segmented": "True",
                "keywords": "AI, machine learning, data science"
            },
            "7CCSMATAI_w1_seg_1",
            document.FileType.PDF,
            document.ContentType.TEXT,
            ["AI", "machine learning", "data science"],
            15,
            "",
            ""
        ),
        (
            "This is a transcript for video segment 2.",
            {
                "doc_id": "7CCSMATAI_v1_seg_2",
                "course_id": "7CCSMATAI",
                "segment_id": "2599943",
                "segment_nr": 2,
                "file_extension": "mp4",
                "doc_title": "Lecture 2",
                "course_title": "Advanced Topics in AI",
                "speakers": ["Prof. Jane Doe"],
                "date": "2025-06-07",
                "length": "300",  # duration in seconds
                "url": "https://example.com/videos/2.mp4",
                "description": "Advanced lecture on deep learning",
                "notes": "Focus on CNNs",
                "source": "King's College",
                "version": "1.0.0",
                "is_segmented": "True",
                "keywords": "deep learning, CNN, video",
                "start_time": "00:05:16",
                "end_time": "00:10:23"
            },
            "7CCSMATAI_v1_seg_2",
            document.FileType.MP4,
            document.ContentType.TEXT,
            ["deep learning", "CNN", "video"],
            300,
            "00:05:16",
            "00:10:23"
        )
    ]
)
def test_transform_segment_to_document(
    transformer,
    text,
    file_metadata,
    expected_doc_id,
    expected_file_type,
    expected_content_type,
    expected_keywords,
    expected_length,
    expected_start_time,
    expected_end_time
):
    sgmnt = segment.Segment(
        id=file_metadata["segment_id"],
        segment_nr=file_metadata["segment_nr"],
        text=text,
        file_metadata=file_metadata
    )
    transformer.set_content(sgmnt)
    document = transformer.transform()

    # Assertions
    assert document.doc_id == expected_doc_id
    assert document.doc_title == file_metadata["doc_title"]
    assert document.segment_nr == file_metadata["segment_nr"]
    assert document.text == text
    assert document.url == file_metadata["url"]
    assert document.start_time == expected_start_time
    assert document.end_time == expected_end_time
    assert document.course_id == file_metadata["course_id"]
    assert document.course_title == file_metadata["course_title"]
    assert document.speakers == file_metadata["speakers"]
    assert document.date == file_metadata["date"]
    assert document.file_type == expected_file_type
    assert document.content_type == expected_content_type
    assert document.length == expected_length
    assert document.description == file_metadata["description"]
    assert document.notes == file_metadata["notes"]
    assert document.is_segmented is True
    assert document.source == file_metadata["source"]
    assert document.version == file_metadata["version"]
    assert document.keywords == expected_keywords


def test_set_test_content(transformer):
    """
    Test setting segments in the transformer.
    """
    sgmnt = segment.Segment(id="seg_1", segment_nr=1, text="Text for segment 1", file_metadata={"doc_id": "seg_1"})
    
    transformer.set_content(sgmnt)

    assert transformer.get_content() == sgmnt
