import pathlib
from typing import Union

import pymupdf

from services.parsers import pdf_parser

class PyMuPdfParser(pdf_parser.PdfParser):
    def get(self, file_path: pathlib.Path) -> dict[str, Union[str, list[str]]]:
        """Extracts metadata and text by page from a PDF file."""
        doc = pymupdf.open(file_path)
        
        # Extract metadata
        metadata = doc.metadata
        cleaned_metadata = {
            "file_name": file_path.stem,     
            "file_extension": file_path.suffix[1:],
            "format": metadata["format"],
            "title": metadata["title"],
            "author": metadata["author"],
            "subject": metadata["subject"],
            "keywords": metadata["keywords"],
            "creator": metadata["creator"],
            "producer": metadata["producer"],
            "creationDate": metadata["creationDate"],
            "modDate": metadata["modDate"],
            "trapped": metadata["trapped"],
            "encryption": "" if metadata["encryption"] == None else metadata["encryption"],
        }
        
        # Extract text by page
        pages_text = []
        for page in doc:
            text = page.get_text()
            pages_text.append(text if text else "")
        
        doc.close()

        result = {
            "metadata": cleaned_metadata,
            "text_by_page": pages_text
        }
        return result