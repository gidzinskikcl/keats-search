import json
import pathlib
import yt_dlp


class YouTubeTranscriptDownloader:
    def __init__(self, output_dir: pathlib.Path):
        self.output_dir = output_dir
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

    def download(self, url: str) -> dict:
        # Step 1: Get metadata without downloading
        preview = yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}).extract_info(url, download=False)
        subtitles = preview.get("subtitles") or {}
        automatic_captions = preview.get("automatic_captions") or {}

        manual_en_available = "en" in subtitles
        auto_en_available = "en" in automatic_captions

        if manual_en_available:
            print("Using manually curated English subtitles...")
            info = self._download_subtitles(url, subtitle_id="en", use_auto=False)
            srt_path = self.output_dir / f"{info['id']}.en.srt"
        elif auto_en_available:
            print("Manual English subtitles not found. Using auto-generated English subtitles...")
            info = self._download_subtitles(url, subtitle_id="en", use_auto=True)
            srt_path = self.output_dir / f"{info['id']}.en-auto.srt"
        else:
            print("No English subtitles available.")
            raise RuntimeError("No English subtitles (manual or auto) found for this video.")

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

        # Save metadata
        meta_path = self.output_dir / f"{metadata['id']}.json"
        with meta_path.open("w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        print(f"Saved metadata to {meta_path}")
        if transcript_file:
            print(f"Saved transcript to {transcript_file}")
        else:
            print("Transcript file not found.")

        return metadata



def main():
    # url = "https://www.youtube.com/watch?v=76dhtgZt38A" # 6.006 6 Binary Trees Part 1
    url = "https://www.youtube.com/watch?v=i9OAOk0CUQE" # 6.006 18 Dynamic Programming Part 4 Rods Subset Sum Pseudopolynomial
    output_dir = pathlib.Path("downloaded_transcript") 
    downloader = YouTubeTranscriptDownloader(output_dir=output_dir)

    try:
        downloader.download(url)
    except Exception as e:
        print(f"Failed to download transcript: {e}")


if __name__ == "__main__":
    main()
