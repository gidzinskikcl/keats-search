# keats-search-eval/scripts/generate_lucene_index.py

import subprocess
import shutil
from pathlib import Path
import logging

# === CONFIGURATION ===
DOCS_PATH = "fdata/ground_truth/documents.json"
INDEX_DIR = "keats-search-eval/src/benchmarking/models/lucene/index_test"
JAR_PATH = "keats-search-eval/src/benchmarking/models/lucene/bm25-search-api-jar-with-dependencies.jar"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LuceneIndexer")


def main():
    doc_file = Path(DOCS_PATH)
    index_path = Path(INDEX_DIR)
    jar_file = Path(JAR_PATH)

    if not doc_file.exists():
        raise FileNotFoundError(f"Document file not found: {doc_file}")
    if not jar_file.exists():
        raise FileNotFoundError(f"Lucene JAR not found: {jar_file}")

    if index_path.exists():
        logger.info(f"Removing existing index at: {index_path}")
        shutil.rmtree(index_path)

    logger.info(f"Creating Lucene index:\n  Input: {doc_file}\n  Output: {index_path}")

    proc = subprocess.run(
        [
            "java",
            "-jar",
            str(jar_file),
            "--mode",
            "index",
            str(doc_file),
            str(index_path),
        ],
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        logger.error("Indexing failed:")
        logger.error(proc.stderr.strip())
        raise RuntimeError(f"Indexing failed: {proc.stderr.strip()}")

    logger.info("✅ Lucene indexing complete.")


if __name__ == "__main__":
    main()
