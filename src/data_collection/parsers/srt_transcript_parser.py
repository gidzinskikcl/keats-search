import json
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
        base_name = subtitle_file.stem
        
        metadata_file = subtitle_file.with_name(f"{base_name}.json")
        
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
