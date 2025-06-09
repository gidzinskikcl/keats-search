import pymupdf

import os

from data_collection.content_gateways import content_gateway as gateway

class PDFGateway(gateway.EducationalContentGateway):
    """
    A concrete content extractor for PDF files using PyMuPDF.

    Supports extracting text from individual pages of a PDF file.
    """

    def __init__(self):
        """
        Initializes the PDFGateway with an optional file path.
        """
        self._file_path = ""

    def get(self) -> dict[str, str]:
        """
        Extracts information from the PDF file, including filename, extension,
        and per-page text, plus metadata like doc_title, authors, date, and more.

        Returns:
            dict: A dictionary with keys:
                - 'file_name'
                - 'file_extension'
                - 'doc_title'
                - 'authors'
                - 'date_created'
                - 'subject'
                - 'keywords'
                - 'page_count'
                - 'pages'
        """
        if not self._file_path:
            raise ValueError("File path is not set. Please set '_file_path' before calling 'get()'.")

        file_name = os.path.basename(self._file_path)
        file_base, file_extension = os.path.splitext(file_name)
        file_extension = file_extension.lstrip(".")

        # Open the PDF file
        doc = pymupdf.open(self._file_path)

        # Extract document metadata
        metadata = doc.metadata or {}
        doc_title = metadata.get("title") or ""
        if not doc_title or doc_title == "Slide 1":
            # Fallback: use the first line of the first page as title
            first_page_text = doc.load_page(0).get_text()
            doc_title = first_page_text.strip().split("\n")[0] if first_page_text else "Untitled Document"

        authors_raw = metadata.get("author", "")
        authors = [author.strip() for author in authors_raw.split(",")] if authors_raw else []

        date_created = metadata.get("creationDate", "")
        subject = metadata.get("subject", "")
        keywords = metadata.get("keywords", "")

        # Extract text from each page
        pages = {}
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            text = page.get_text()
            pages[str(page_number + 1)] = text  # 1-based numbering

        results = {
            "file_name": file_base,
            "file_extension": file_extension,
            "doc_title": doc_title,
            "authors": authors,
            "date_created": date_created,
            "subject": subject,
            "keywords": keywords,
            "page_count": str(doc.page_count),
            "pages": pages
        }

        doc.close()

        return results
    
    def set_file_path(self, file_path: str) -> None:
        """
        Sets the file path for the PDF file to be processed.

        Args:
            file_path (str): The path to the PDF file.
        """
        self._file_path = file_path

    def get_file_path(self) -> str:
        """
        Returns the current file path set for the PDF file.

        Returns:
            str: The path to the PDF file.
        """
        return self._file_path