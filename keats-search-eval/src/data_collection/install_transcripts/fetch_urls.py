import json
import pathlib
from pytube import Playlist


def main():
    input_path = pathlib.Path("keats-search-eval/data/transcripts/urls/playlists.json")
    output_path = pathlib.Path("keats-search-eval/data/transcripts/urls/urls.json")

    with open(input_path) as f:
        playlist_metadata = json.load(f)

    data = {}

    for module_id, entry in playlist_metadata.items():
        url = entry.get("url")
        if not url:
            print(f"Skipping module {module_id}: no URL found.")
            continue

        try:
            playlist = Playlist(url)
            urls = list(playlist.video_urls)
            data[module_id] = urls
            print(f"Found {len(urls)} videos for module {module_id}")
        except Exception as e:
            print(f"Failed to load playlist for module {module_id}: {e}")

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nSaved playlist video URLs to: {output_path}")


if __name__ == "__main__":
    main()
