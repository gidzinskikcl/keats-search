import pathlib

import yt_dlp

from data_collection.transcript_installer import transcript_gateway

class YouTubeTranscriptGateway(transcript_gateway.TranscriptGateway):
    def __init__(self, output_dir):
        
        self.output_dir = pathlib.Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _download_subtitles(self, url: str, subtitle_id: str, use_auto: bool = False):
        options = {
            "quiet": True,
            "skip_download": True,
            "subtitleslangs": [subtitle_id],
            "subtitlesformat": "srt",
            "outtmpl": str(self.output_dir / '%(id)s.%(ext)s'),
            "writesubtitles": not use_auto,
            "writeautomaticsub": use_auto,
        }

        ytdl = yt_dlp.YoutubeDL(options)
        return ytdl.extract_info(url, download=True)

    def get(self, url: str) -> dict:
        """Extract transcript and metadata from a YouTube video URL."""

        # Step 1: Preview metadata to detect available manual subtitles
        preview = yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}).extract_info(url, download=False)
        subtitles = preview.get("subtitles") or {}
        subtitle_id = next(iter(subtitles.keys()), None)  # Pick first available if exists

        # Step 2: Download manual if available, else fallback to auto
        if subtitle_id:
            info = self._download_subtitles(url, subtitle_id=subtitle_id, use_auto=False)
            srt_path = self.output_dir / f"{info['id']}.{subtitle_id}.srt"
        else:
            print("Manual subtitle not found, installing automatic...")
            info = self._download_subtitles(url, subtitle_id="en", use_auto=True)
            srt_path = self.output_dir / f"{info['id']}.en-auto.srt"

        transcript_file = str(srt_path) if srt_path.exists() else None

        metadata = {
            "id": info.get("id"),
            "title": info.get("title"),
            "description": info.get("description"),
            "uploader": info.get("uploader"),
            "upload_date": info.get("upload_date"),
            "duration": info.get("duration"),
            "view_count": info.get("view_count"),
            "tags": info.get("tags", []),
            "webpage_url": info.get("webpage_url"),
            "thumbnail": info.get("thumbnail"),
            "chapters": info.get("chapters", []),
            "transcript_file": transcript_file
        }

        return metadata
