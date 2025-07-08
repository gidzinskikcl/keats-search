import json
import re
import pathlib

from typing import Union

from services.parsers import transcript_parser

class SRTTranscriptParser(transcript_parser.TranscriptParser):
    """
    Concrete implementation that parses .srt subtitle files.
    """

    def __init__(self, mapping_path: Union[str, pathlib.Path]):
        self.mapping = self._load_mapping(mapping_path)

    def _load_mapping(self, mapping_path: Union[str, pathlib.Path]) -> dict[str, dict]:
        """Load mapping JSON and index by doc_id (filename)."""
        with open(mapping_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {entry["doc_id"]: entry for entry in data}

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
        result["file_name"] = subtitle_file.stem
        result["file_extension"] = subtitle_file.suffix.lstrip(".")

        # Parse transcript
        result["transcript"] = self._extract_text_from_srt(subtitle_file)

        # Inject course + lecture metadata if found in mapping
        doc_id = subtitle_file.name
        mapping_info = self.mapping.get(doc_id, {})
        result["course_id"] = mapping_info.get("course_id")
        result["course_title"] = mapping_info.get("course_title")
        result["lecture_id"] = mapping_info.get("lecture_id")
        result["lecture_title"] = mapping_info.get("lecture_title")

        return result

    
    def _load_metadata(self, subtitle_file: pathlib.Path) -> dict[str, str]:
        """
        Load the metadata JSON file associated with the subtitle file.
        """
        metadata_file = subtitle_file.with_name(f"{subtitle_file.stem}.json")

        if not metadata_file.exists():
            metadata_file = subtitle_file.with_name(f"{subtitle_file.stem[:-3]}.json")
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

    def _extract_text_from_srt(self, subtitle_file: pathlib.Path) -> list[dict[str, str]]:
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = content.strip().split('\n\n')
        subtitles = []

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                index = lines[0].strip()
                timestamp_line = lines[1].strip()
                text_lines = lines[2:]
                match = re.match(r'(?P<start>\d{2}:\d{2}:\d{2},\d{3}) --> (?P<end>\d{2}:\d{2}:\d{2},\d{3})', timestamp_line)
                if match:
                    subtitles.append({
                        'index': index,
                        'start': match.group('start'),
                        'end': match.group('end'),
                        'text': ' '.join(line.strip() for line in text_lines)
                    })

        return subtitles
