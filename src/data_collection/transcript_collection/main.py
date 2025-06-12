
import json
import pathlib

from data_collection.transcript_collection import yt_transcript_gateway 


def main():
    output_dir = pathlib.Path("/Users/piotrgidzinski/KeatsSearch_workspace/keats-search/data/transcripts")
    urls = [
        "https://youtu.be/tY2gczObpfU?si=gDQM7C3hJoqoqcp2"
    ]
    gateway = yt_transcript_gateway.YouTubeTranscriptGateway(output_dir=output_dir)



    results = []
    for url in urls:
        print(f"Processing: {url}")

        try:
            result = gateway.get(url)
            results.append(result)

            # Save metadata to JSON
            meta_path = pathlib.Path(result["transcript_file"]).with_suffix(".json") if result["transcript_file"] else output_dir / f"{result['id']}.json"
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
