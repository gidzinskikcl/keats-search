
import json
import pathlib

from data_collection.transcript_installer import yt_transcript_gateway 


import json
import pathlib
from data_collection.transcript_installer import yt_transcript_gateway 


def main():
    output_dir = pathlib.Path("/Users/piotrgidzinski/KeatsSearch_workspace/keats-search/data/transcripts")
    urls_path = output_dir / "urls" / "urls.json"

    # Load URLs from JSON
    with urls_path.open("r", encoding="utf-8") as f:
        urls = json.load(f)

    # Define skipped indexes for module '6.006'
    skip_indexes_6006 = {3, 6, 8, 11, 14, 17, 20, 22, 25, 29, 30} 

    results = []

    for module_id, module_urls in urls.items():

        # # Only process '6.006' for now
        # if module_id != "6.006":
        #     continue

        module_dir = output_dir / module_id
        module_dir.mkdir(parents=True, exist_ok=True)

        gateway = yt_transcript_gateway.YouTubeTranscriptGateway(output_dir=module_dir)

        for i, url in enumerate(module_urls):
            one_based_index = i + 1
            if module_id == "6.006" and one_based_index in skip_indexes_6006:
                print(f"Skipping ({module_id}) index {i}: {url}")
                continue

            print(f"Processing ({module_id}) index {i}: {url}")
            try:
                result = gateway.get(url)
                results.append(result)

                meta_path = (
                    pathlib.Path(result["transcript_file"]).with_suffix(".json")
                    if result["transcript_file"]
                    else module_dir / f"{result['id']}.json"
                )
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