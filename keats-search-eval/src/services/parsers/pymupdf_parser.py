import pathlib
import json
from typing import Union

import pymupdf

from services.parsers import pdf_parser


class PyMuPdfParser(pdf_parser.PdfParser):
    def __init__(self, mapping_path: Union[str, pathlib.Path]):
        self.mapping = self._load_mapping(mapping_path)

    def _load_mapping(self, mapping_path: Union[str, pathlib.Path]) -> dict[str, dict]:
        """Load mapping JSON and index by doc_id for fast lookup."""
        with open(mapping_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {entry["doc_id"]: entry for entry in data}

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
            "encryption": (
                "" if metadata["encryption"] == None else metadata["encryption"]
            ),
        }

        # Extract text by page
        pages_text = []
        for page in doc:
            text = page.get_text()
            pages_text.append(text if text else "")

        doc.close()

        # Look up metadata from mapping
        mapping_info = self.mapping.get(f"{file_path.stem}.pdf", {})
        if mapping_info == {}:
            print("AAAA")
            print(file_path.stem)
        result = {
            "metadata": cleaned_metadata,
            "text_by_page": pages_text,
            "course_id": mapping_info.get("course_id"),
            "course_title": mapping_info.get("course_title"),
            "lecture_id": mapping_info.get("lecture_id"),
            "lecture_title": mapping_info.get("lecture_title"),
        }
        return result
