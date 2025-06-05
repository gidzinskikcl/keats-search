import fitz  # PyMuPDF

from data_collection.stages.parsing.format_parsers import parser


class PDFParser(parser.Parser):
    """
    Concrete parser for PDF files.
    It implements text extraction using PyMuPDF.
    """

    def parse_text(self, file_path: str) -> str:
        """
        Extracts text from a PDF file using PyMuPDF.
        """
        extracted_text = []
        try:
            with fitz.open(file_path) as pdf_document:
                for page_number in range(len(pdf_document)):
                    page = pdf_document[page_number]
                    text = page.get_text()
                    extracted_text.append(text)
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            raise e
        
        result =  "\n".join(extracted_text)
        return result

    def parse_images(self, file_path: str) -> list:
        """
        Image extraction is not implemented yet.
        """
        raise NotImplementedError("Image extraction is not implemented yet.")

    def parse_vector_graphics(self, file_path: str) -> list:
        """
        Vector graphics extraction is not implemented yet.
        """
        raise NotImplementedError("Vector graphics extraction is not implemented yet.")
