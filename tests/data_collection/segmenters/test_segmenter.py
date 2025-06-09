import pytest

from data_collection.segments import segment, slides_segmenter

@pytest.fixture
def segmenter():
    result = slides_segmenter.SlidesSegmenter()
    return result

@pytest.fixture
def data():
    result = {
        "id": "1",
        "title": "This is a Title",
        "file_extension": "pdf",
        "pages": {
            "1": "This is a text from page 1",
            "2": "And here is another text but from page 2"
        }
    }
    return result

@pytest.fixture
def expected():
    result = [
        segment.Segment(nr=1, content="This is a text from page 1"),
        segment.Segment(nr=2, content="And here is another text but from page 2")
    ]
    return result

def test_segment(segmenter, data, expected):
    observed = segmenter.segment(data)
    assert observed == expected