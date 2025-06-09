from abc import ABC

from data_collection.segments import segment


class Segmenter(ABC):
    """
    Segments the content into meaningful sections
    """

    def segment(self, data: dict[str, str])-> list[segment.Segment]:
        """
        Segments the content from a file into meaningful content segments.
        """
        pass

