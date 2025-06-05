import fitz  # PyMuPDF
from data_collection.stages.parsing.format_readers import reader

class PDFReader(reader.Reader):
    """
    A concrete content extractor for PDF files using PyMuPDF.

    Supports extracting text from individual pages (segments) of a PDF file.
    """

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

    def get_images(self, file_path: str, segment_nr: int) -> list:
        """
        Extract images from a specific page (segment) of a PDF file.

        Note:
            Currently, this method is not implemented.

        Args:
            file_path (str): The path to the PDF file.
            segment_nr (int): The 1-based index of the page to extract images from.

        Returns:
            list: An empty list (always raises NotImplementedError).

        Raises:
            NotImplementedError: Always, since this method is not yet implemented.
        """
        raise NotImplementedError("Image extraction is not implemented yet.")

    def get_vector_graphics(self, file_path: str, segment_nr: int) -> list:
        """
        Extract vector graphics from a specific page (segment) of a PDF file.

        Note:
            Currently, this method is not implemented.

        Args:
            file_path (str): The path to the PDF file.
            segment_nr (int): The 1-based index of the page to extract vector graphics from.

        Returns:
            list: An empty list (always raises NotImplementedError).

        Raises:
            NotImplementedError: Always, since this method is not yet implemented.
        """
        raise NotImplementedError("Vector graphics extraction is not implemented yet.")
