from abc import ABC, abstractmethod
from typing import List
from data_structures import segment

class Reader(ABC):
    """
    Abstract base class for all readers.
    Defines the common interface for extracting content from files.
    """

    def load_segments(
        self,
        file_path: str,
        metadata: dict[str, str],
        nr_segments: int
    ) -> List[segment.Segment]:
        """
        Extracts segments from the file by applying extraction methods.

        Args:
            file_path (str): Path to the file to be processed.
            metadata (dict[str, str]): Metadata associated with the file.
            nr_segments (int): Total number of segments to process.

        Returns:
            list[Segment]: One Segment object per segment, with aggregated text and metadata.
        """
        results = []

        for s in range(nr_segments):
            combined_text = self.get_text(file_path, s + 1)
            # In the future, you might also call:
            # images = self.get_images(file_path, s + 1)
            # vector_graphics = self.get_vector_graphics(file_path, s + 1)
            # Then aggregate them as needed.

            sgmnt = segment.Segment(
                segment_nr=s + 1,
                text=combined_text,
                file_metadata=metadata
            )
            results.append(sgmnt)

        return results

    @abstractmethod
    def get_text(self, file_path: str, segment_nr: int) -> str:
        """
        Extract text from the given file and segment.
        """
        pass

    @abstractmethod
    def get_images(self, file_path: str, segment_nr: int) -> List:
        """
        Extract images from the given file and segment.
        """
        pass

    @abstractmethod
    def get_vector_graphics(self, file_path: str, segment_nr: int) -> List:
        """
        Extract vector graphics from the given file and segment.
        """
        pass
