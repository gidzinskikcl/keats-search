import fitz  # PyMuPDF
from data_collection.educational_content_gateways import content_gateway as gateway
from data_structures import segment, content

class PDFGateway(gateway.EducationalContentGateway):
    """
    A concrete content extractor for PDF files using PyMuPDF.

    Supports extracting text from individual pages (segments) of a PDF file.
    """

    def get(
        self,
        file_path: str,
        metadata: dict[str, str],
    ) -> list[segment.Segment]:
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

        nr_segments = metadata.get("nr_segments", 0)

        for s in range(nr_segments):
            combined_text = self.get_text(file_path, s + 1)
            # In the future, you might also call:
            # images = self.get_images(file_path, s + 1)
            # vector_graphics = self.get_vector_graphics(file_path, s + 1)
            # Then aggregate them as needed.

            sgmnt = segment.Segment(
                id=metadata.get("id", ""),
                segment_nr=s + 1,
                text=combined_text,
                file_metadata=metadata
            )
            results.append(sgmnt)

        return results

    def get_text(self, file_path: str, segment_nr: int) -> str:
        """
        Extract text from a specific page (segment) of a PDF file.

        Args:
            file_path (str): The path to the PDF file.
            segment_nr (int): The 1-based index of the page to extract text from.

        Returns:
            str: The extracted text from the specified page.

        Raises:
            IndexError: If the provided segment number is out of range.
            Exception: If an error occurs while reading the PDF file.
        """
        try:
            with fitz.open(file_path) as pdf_document:
                if segment_nr < 1 or segment_nr > len(pdf_document):
                    raise IndexError(f"Segment number {segment_nr} out of range.")
                page = pdf_document[segment_nr - 1]
                result = page.get_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
            raise e
        return result