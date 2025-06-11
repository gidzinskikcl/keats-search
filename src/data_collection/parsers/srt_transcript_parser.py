import json
import os
import re

import pathlib

from typing import Union

from data_collection.parsers import transcript_parser

class SRTTranscriptParser(transcript_parser.TranscriptParser):
    """
    Concrete implementation that parses .srt subtitle files.
    """

    def get(self, subtitle_file: pathlib.Path, load_metadata: bool = True) -> dict[str, Union[str, list[str], list[dict[str, str]]]]:
        # Step 1: Load metadata
        if load_metadata:
            result = self._load_metadata(subtitle_file)
        else:
            result = {
                "id": "",
                "title": "",
                "description": "",
                "uploader": "",
                "upload_date": "",
                "duration": "",
                "view_count": "",
                "tags": "",
                "webpage_url": "",
                "thumbnail": "",
                "chapters": []
            }

        # Add file name and extension
        result["file_name"] = subtitle_file.stem[:-3]
        result["file_extension"] = subtitle_file.suffix.lstrip(".")

        # Parse transcript
        transcript_text = self._extract_text_from_srt(subtitle_file)

        # Step Combine
        result["transcript"] = transcript_text

        return result
    
    def _load_metadata(self, subtitle_file: pathlib.Path) -> dict[str, str]:
        """
        Load the metadata JSON file associated with the subtitle file.
        """
        base_name = subtitle_file.stem[:-3]  # remove '.en' (3 chars)
        
        metadata_file = subtitle_file.with_name(f"{base_name}.essential_metadata.json")
        
        if not metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found for subtitle file: {subtitle_file}")

        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        chapters = []
        for chapter in metadata["chapters"]:
            chapters.append({
                "title": chapter["title"],
                "start_time": str(chapter["start_time"]),
                "end_time": str(chapter["end_time"])
            })
        
        result = {
            "id": metadata["id"],
            "title": metadata["title"],
            "description": metadata["description"],
            "uploader": metadata["uploader"],
            "upload_date": metadata["upload_date"],
            "duration": str(metadata["duration"]),
            "view_count": str(metadata["view_count"]),
            'tags': metadata['tags'],
            "webpage_url": metadata["webpage_url"],
            "thumbnail": metadata["thumbnail"],
            "chapters": chapters,
        }

        return result

    def _extract_text_from_srt(self, subtitle_file: str) -> str:
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        text_lines = []
        for line in lines:
            line = line.strip()
            # Skip empty lines and lines with sequence numbers or timestamps
            if line.isdigit():
                continue
            if re.match(r'^\d{2}:\d{2}:\d{2},\d{3}', line):
                continue
            text_lines.append(line)

        return ' '.join(text_lines)
