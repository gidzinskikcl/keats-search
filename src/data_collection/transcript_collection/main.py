
import json
import pathlib

from data_collection.transcript_collection import yt_transcript_gateway 


def main():
    output_dir = pathlib.Path("/Users/piotrgidzinski/KeatsSearch_workspace/keats-search/data/transcripts")
    urls = {
        "18.404J": [
            "https://www.youtube.com/watch?v=IycOPFmEQk8&t=5s",
            # Add more URLs for this module if needed
        ],
    }
    gateway = yt_transcript_gateway.YouTubeTranscriptGateway(output_dir=output_dir)

    results = []

    for module_id, module_urls in urls.items():
        module_dir = output_dir / module_id
        module_dir.mkdir(parents=True, exist_ok=True)

        gateway = yt_transcript_gateway.YouTubeTranscriptGateway(output_dir=module_dir)

        for url in module_urls:
            print(f"Processing ({module_id}): {url}")
            try:
                result = gateway.get(url)
                results.append(result)

                meta_path = pathlib.Path(result["transcript_file"]).with_suffix(".json") if result["transcript_file"] else module_dir / f"{result['id']}.json"
                with meta_path.open("w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2)

                print(f"Saved metadata to {meta_path}")
                if result.get("transcript_file"):
                    print(f"Saved transcript to {result['transcript_file']}")
                else:
                    print("No transcript found.")
            except Exception as e:
                print(f"Failed to process {url}: {e}")

    print(f"\nProcessed {len(results)} video(s).")


if __name__ == "__main__":
    main()
